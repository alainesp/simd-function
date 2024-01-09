##################################################################################
# This file is part of 'SIMD-Function'
# 
# Copyright (c) 2024 by Alain Espinosa.
##################################################################################

from dataclasses import dataclass
from inspect import stack
# from atexit import register as register_at_exit
from enum import Enum
import operator

##################################################################################
# Scalar types
##################################################################################
void = None
from ctypes import _SimpleCData as ctype

from ctypes import c_int8  as int8_t
from ctypes import c_int16 as int16_t
from ctypes import c_int32 as int32_t
from ctypes import c_int64 as int64_t

from ctypes import c_uint8  as uint8_t
from ctypes import c_uint16 as uint16_t
from ctypes import c_uint32 as uint32_t
from ctypes import c_uint64 as uint64_t

from ctypes import c_float as float
from ctypes import c_double as double

##################################################################################
# Utils
##################################################################################
def get_function_definition_filename() -> str:
    """Get the name of the Python file"""
    return [s.filename for s in stack() if s.filename != __file__][0]

@dataclass
class Comment:
    line: int
    comment: str

def get_comments() -> list[Comment]:
    """Get the comments from the Python file"""
    comments: list[Comment] = []
    
    with open(get_function_definition_filename(), 'r') as f:
        line_number = 1
        while 1:
            line: str = f.readline()
            if not line: break
            
            comment_begin = line.find('#')
            if comment_begin >= 0:
                comments.append(Comment(line_number, line[comment_begin:].replace('#', '//')))
            line_number += 1
       
    comments.append(Comment(1_000_000_000, '// end of file'))     
    return comments
    
def get_line_number() -> int:
    """Get the line number on the function definition"""
    return [s for s in stack() if s.filename != __file__][0].lineno

def retrieve_name(var) -> str:
    """
    Gets the name of var. Does it from the out most frame inner-wards.
    :param var: variable to get name from.
    :return: string
    """
    for fi in reversed(stack()):
        if fi.filename == __file__:
            return ''
        
        names = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is var]
        if len(names) > 0:
            return names[0]
        
##################################################################################
# Targets
##################################################################################
class Target(Enum):
    PLAIN_C           = 1
    # SSE2_INTRINSICS   = 2
    # AVX_INTRINSICS    = 3
    # AVX2_INTRINSICS   = 4
    # AVX512_INTRINSICS = 5

default_targets: list[Target] = [Target.PLAIN_C]

##################################################################################
# Instructions
##################################################################################
@dataclass
class Instruction:
    result: any
    line_number: int
    
    def generate_code(self, target: Target, instruction_by_tmp: dict[any, any]):
        raise NotImplementedError

def get_expresion(tmp: any, target: Target, instruction_by_tmp: dict[any, Instruction]) -> str:
    if isinstance(tmp, int):
        return f'{hex(tmp) if tmp >= 255 else tmp}'
    if tmp.is_constant:
        return f'{hex(tmp.constant_value) if tmp >= 255 else tmp}'
    if not tmp.is_tmp():
        return tmp.name
    
    return instruction_by_tmp[tmp].generate_code(target, instruction_by_tmp)

class LoadInstruction(Instruction):
    memory: any
    index: any # Should support any index (constant, scalar, ...)
    
    def __init__(self, result, memory, index) -> None:
        super().__init__(result, get_line_number())
        self.memory = memory
        self.index = index
    
    def generate_code(self, target: Target, instruction_by_tmp: dict[any, Instruction]):
        memory_expression = f'{self.memory.name}[{self.index}]'
        match target:
            case Target.PLAIN_C:
                if self.result.is_tmp():
                    return memory_expression
                else:
                    return f'{self.result.name} = {memory_expression};'
            case _: raise NotImplementedError
        
class StoreInstruction(Instruction):
    memory: any
    index: any # Should support any index (constant, scalar, ...)
    operand: any
    
    def __init__(self, operand, memory, index) -> None:
        super().__init__(None, get_line_number())
        self.memory = memory
        self.index = index
        self.operand = operand
    
    def generate_code(self, target: Target, instruction_by_tmp: dict[any, Instruction]):
        memory_expression = f'{self.memory.name}[{self.index}]'
        match target:
            case Target.PLAIN_C:
                return f'{memory_expression} = {get_expresion(self.operand, target, instruction_by_tmp)};'
            case _: raise NotImplementedError
 
class UnaryInstruction(Instruction):
    operand: any
    c_operator: str
    
    def __init__(self, result, operand, c_operator: str) -> None:
        super().__init__(result, get_line_number())
        self.operand = operand
        self.c_operator = c_operator
        
    def generate_code(self, target: Target, instruction_by_tmp: dict[any, Instruction]):
        operand_expression = f'{self.c_operator}({get_expresion(self.operand, target, instruction_by_tmp)})'
        match target:
            case Target.PLAIN_C:
                if self.result.is_tmp():
                    return operand_expression
                else:
                    return f'{self.result.name} = {operand_expression};'
            case _: raise NotImplementedError
            
class ReturnInstruction(UnaryInstruction):
    def __init__(self, operand) -> None:
        super().__init__(None, operand, '')
    def generate_code(self, target: Target, instruction_by_tmp: dict[any, Instruction]):
        return f'return {get_expresion(self.operand, target, instruction_by_tmp)};'
    
class BinaryInstruction(Instruction):
    operand1: any
    operand2: any
    c_operator: str
    
    def __init__(self, result, operand1, operand2, c_operator: str = '') -> None:
        super().__init__(result, get_line_number())
        self.operand1 = operand1
        self.operand2 = operand2
        self.c_operator = c_operator
        
    def get_expresions(self, target: Target, instruction_by_tmp: dict[any, Instruction]) -> (str, str):
        return (get_expresion(self.operand1, target, instruction_by_tmp), get_expresion(self.operand2, target, instruction_by_tmp))
    
    def generate_code(self, target: Target, instruction_by_tmp: dict[any, Instruction]):
        operand1_expression, operand2_expression = self.get_expresions(target, instruction_by_tmp)
        match target:
            case Target.PLAIN_C:
                if self.result.is_tmp():
                    return f'({operand1_expression} {self.c_operator} {operand2_expression})'
                else:
                    if self.result.name == operand1_expression:
                        return f'{self.result.name} {self.c_operator}= {operand2_expression};'
                    elif self.result.name == operand2_expression:
                        return f'{self.result.name} {self.c_operator}= {operand1_expression};'
                    else:
                        return f'{self.result.name} = {operand1_expression} {self.c_operator} {operand2_expression};'
            case _: raise NotImplementedError

class CallInstruction(BinaryInstruction):
    def generate_code(self, target: Target, instruction_by_tmp: dict[any, Instruction]):
        operand1_expression, operand2_expression = self.get_expresions(target, instruction_by_tmp)
        call_result = f'{self.c_operator}({operand1_expression}, {operand2_expression})'
        match target:
            case Target.PLAIN_C:
                if self.result.is_tmp():
                    return call_result
                else:
                    return f'{self.result.name} = {call_result};'
            case _: raise NotImplementedError
            
# Aritmetic      
class AddInstruction(BinaryInstruction):
    def __init__(self, result, operand1, operand2) -> None:
        super().__init__(result, operand1, operand2, '+')
class SubInstruction(BinaryInstruction):
    def __init__(self, result, operand1, operand2) -> None:
        super().__init__(result, operand1, operand2, '-')
        
class ProductInstruction(BinaryInstruction):
    def __init__(self, result, operand1, operand2) -> None:
        super().__init__(result, operand1, operand2, '*')
class DivisionInstruction(BinaryInstruction):
    def __init__(self, result, operand1, operand2) -> None:
        super().__init__(result, operand1, operand2, '/')
class ModuloInstruction(BinaryInstruction):
    def __init__(self, result, operand1, operand2) -> None:
        super().__init__(result, operand1, operand2, '%')
# class PowerInstruction(BinaryInstruction):
#     def __init__(self, result, operand1, operand2) -> None:
#         super().__init__(result, operand1, operand2, '*')
        
# Logical
class AndInstruction(BinaryInstruction):
    def __init__(self, result, operand1, operand2) -> None:
        super().__init__(result, operand1, operand2, '&')
class OrInstruction(BinaryInstruction):
    def __init__(self, result, operand1, operand2) -> None:
        super().__init__(result, operand1, operand2, '|')
class XorInstruction(BinaryInstruction):
    def __init__(self, result, operand1, operand2) -> None:
        super().__init__(result, operand1, operand2, '^')
        
# Shift/Rotations
class ShiftLInstruction(BinaryInstruction):
    def __init__(self, result, operand1, operand2) -> None:
        super().__init__(result, operand1, operand2, '<<')
class ShiftRInstruction(BinaryInstruction):
    def __init__(self, result, operand1, operand2) -> None:
        super().__init__(result, operand1, operand2, '>>')
class RotlInstruction(CallInstruction):
    def generate_code(self, target: Target, instruction_by_tmp: dict[any, Instruction]):
        if self.operand1.c_type == uint32_t:
            self.c_operator = '_rotl'
        elif self.operand1.c_type == uint64_t:
            self.c_operator = '_rotl64'
        else:
            raise NotImplementedError
        return super().generate_code(target, instruction_by_tmp)

##################################################################################
# SIMD function
##################################################################################
def get_type(var: any, target: Target) -> str:
    
    if isinstance(var, Vector) or isinstance(var, VectorMemoryArray): 
        match target:
            case Target.PLAIN_C: return retrieve_name(var.c_type)
            case _: raise NotImplementedError
            
    if isinstance(var, Scalar):
        return retrieve_name(var.c_type)
    
    if var is None:
        return 'void'
    
    return retrieve_name(var) 

class Param:
    name: str
    obj: any
    
    def __init__(self, obj) -> None:
        self.obj = obj
        self.name = retrieve_name(obj)

class Function:
    result_type: ctype
    name: str
    params: list[Param]
    instructions: list[Instruction]
    targets: list[Target]
    exited: bool = False
    
    def __init__(self, result_type: ctype = void, targets: list[Target] = default_targets):
        self.result_type = result_type
        self.params = []
        self.instructions = []
        self.targets = targets
    
    def __call__(self, *args):
        for arg in args:
            self.params.append(Param(arg))
        return self
            
    # with managment
    def __enter__(self):
        self.line_function_definition = get_line_number()
        self.instructions = []
        defined_functions.append(self)
        return self
    
    def __exit__(self, exception_type, exception_value, traceback):
        self.exited = True
        if exception_type is not None:
            raise exception_type
        
        self.name = retrieve_name(self)
        if not self.name or self.name == 'self':
            raise NameError('Please provide a name for the function')
    
    def get_includes(self, includes: set):
        for target in self.targets:
            match target:
                case Target.PLAIN_C: includes.add('stdint.h')
                case _: raise NotImplementedError
    
    def generate_code(self, output, comments: list[Comment]):
        # Generate code for all targets
        for target in self.targets:
            # Function signature
            output.write(f'{get_type(self.result_type, target)} {self.name}(')
            param_separator: str = ''
            for arg in self.params:
                param_suffix = f'[{arg.obj.num_elems}]' if isinstance(arg.obj, VectorMemoryArray) and arg.obj.num_elems > 0 else ''
                output.write(f'{param_separator}{get_type(arg.obj, target)} {arg.name}{param_suffix}')
                param_separator = ', '
            output.write(') {\n')
            
            variable_names = set()
            for arg in self.params:
                variable_names.add(arg.name)
            
            # Function body
            current_line = self.line_function_definition + 1
            comment_index = 0
            while comments[comment_index].line <= current_line:
                comment_index += 1
            
            instruction_by_tmp = {}
            for instruction in self.instructions:
                if not isinstance(instruction, StoreInstruction) and not isinstance(instruction, ReturnInstruction):
                    instruction_by_tmp[instruction.result] = instruction
                if isinstance(instruction, StoreInstruction) or isinstance(instruction, ReturnInstruction) or not instruction.result.is_tmp():
                    # Write comments
                    if instruction.line_number > comments[comment_index].line:
                        output.write('\n'*(comments[comment_index].line - current_line))
                        output.write(f'\t{comments[comment_index].comment}')
                        current_line = comments[comment_index].line + 1
                        comment_index += 1
                        
                    # Write line spaces
                    if current_line > instruction.line_number: # Support cycles in Python
                        current_line = instruction.line_number - 1
                    output.write('\n'*(instruction.line_number - current_line))
                    current_line = instruction.line_number
                    # Instruction
                    output.write('\t')
                    if instruction.result and instruction.result.name not in variable_names:
                        output.write(f'{get_type(instruction.result, target)} ')
                        variable_names.add(instruction.result.name)
                    output.write(instruction.generate_code(target, instruction_by_tmp))
                      
            output.write('\n}\n\n')
    
    def Return(self, value):
        if self.exited:
            raise TypeError('Function return outside definition')
        
        if isinstance(value, Vector):
            if self.result_type.c_type != value.c_type:
                raise TypeError
            self.instructions.append(ReturnInstruction(value))          
        elif isinstance(value, Scalar):
            if self.result_type != value.c_type:
                raise TypeError
            self.instructions.append(ReturnInstruction(value))
        else:
            raise TypeError

defined_functions: list[Function] = []
def generate_code(filename: str):
    includes: set = {'stdint.h', 'assert.h'}
    for func in defined_functions:
        func.get_includes(includes)
    
    comments: list[Comment] = get_comments()
    
    with open(filename, 'w') as output:
        # Save comments
        line = 1
        for comment in comments:
            if comment.line == line:
                output.write(comment.comment)
                line += 1
            else:
                break
        comments = [c for c in comments if c.line >= line]
        output.write('// Automatically generated code by SIMD-function library\n\n')
        
        output.writelines([f'#include <{include}>\n' for include in includes])
        output.write('\n')
        
        for func in defined_functions:
            # Functions comments
            comments_before = []
            line = func.line_function_definition - 1
            while 1:
                comments_at_line = [c.comment for c in comments if c.line == line]
                if len(comments_at_line) == 0:
                    break
                else:
                    comments_before += comments_at_line
                    line -= 1
                    
            output.writelines(reversed(comments_before))
            func.generate_code(output, comments)
        
#register_at_exit(generate_code)
   
##################################################################################
# SIMD data types
##################################################################################
class Variable:
    c_type: ctype
    is_uninitialize: bool = True
    is_constant: bool = False
    line_vector_definition: int = 0
    name: str = ''
    constant_value: int = 0
    
    def __init__(self, c_type: ctype, is_constant: bool = False, constant_value: int = 0, is_uninitialize: bool = True):
        self.line_function_definition = get_line_number()
        self.c_type = c_type
        self.is_constant = is_constant
        self.is_uninitialize = is_uninitialize
        if is_constant:
            self.is_uninitialize = False
            self.constant_value = constant_value
        
    # Checks
    def check_uninitialize(self):
        if self.is_uninitialize:
            raise ValueError('The variable is uninitialize')
    def check_same_type(self, other):
        if self.c_type != other.c_type:
            raise ValueError('The two vectors need to be of the same type')     
    def perform_checks(self, other):
        self.check_uninitialize()
        
        if isinstance(other, Vector) or isinstance(other, Scalar):
            other.check_uninitialize()
            self.check_same_type(other)
        elif not isinstance(other, int):
            raise TypeError('Operation only support Vectors or integer constants')
    
    def find_name(self) -> None:
        if not self.name and not self.is_constant:
            self.name = retrieve_name(self)
            
    def is_tmp(self) -> bool:
        return not self.name
    ########################################################################
    # Binary Operators
    ########################################################################
    def _binary_op(self: "Scalar | Vector", other: "int | float | Scalar | Vector", op, instruction: Instruction):
        self.perform_checks(other)
        
        # Constant folding
        if self.is_constant and isinstance(other, int):
            self.constant_value = op(self.constant_value, other)
            return self
        if self.is_constant and other.is_constant:
            self.constant_value = op(self.constant_value, other.constant_value)
            return self
        
        self.find_name()
        if isinstance(other, Vector) or isinstance(other, Scalar):
            other.find_name()
        
        if isinstance(self, Vector) or isinstance(other, Vector):
            result = Vector(self.c_type, is_uninitialize=False)
        elif isinstance(self, Scalar) or isinstance(other, Scalar):
            result = Scalar(self.c_type, is_uninitialize=False)
        else:
            raise TypeError
        defined_functions[-1].instructions.append(instruction(result, self, other))
        return result
        
    def __add__(self, other):
        return self._binary_op(other, operator.__add__, AddInstruction)
    def __sub__(self, other):
        return self._binary_op(other, operator.__sub__, SubInstruction)
    def __mul__(self, other):	
        return self._binary_op(other, operator.__mul__, ProductInstruction)
    def __truediv__(self, other):
        return self._binary_op(other, operator.__floordiv__, DivisionInstruction)	
    def __floordiv__(self, other):
        return self._binary_op(other, operator.__floordiv__, DivisionInstruction)	
    def __mod__(self, other):
        return self._binary_op(other, operator.__mod__, ModuloInstruction)
    def __pow__(self, other):
        if other == 2:
            return self._binary_op(self, operator.__mul__, ProductInstruction)
        else:
            raise NotImplementedError
    
    # Shift/Rotations
    def __rshift__(self, other):
         return self._binary_op(other, operator.__rshift__, ShiftRInstruction)
    def __lshift__(self, other):
         return self._binary_op(other, operator.__lshift__, ShiftLInstruction)
    def rotate_left(self, other):
        global ror_width
        ror_width = sizeof(self.c_type) * 8
        return self._binary_op(other, rotl, RotlInstruction)
    
    # Logical
    def __and__(self, other):
        return self._binary_op(other, operator.__and__, AndInstruction)
    def __or__(self, other):
        return self._binary_op(other, operator.__or__, OrInstruction)
    def __xor__(self, other):
        return self._binary_op(other, operator.__xor__, XorInstruction)
    
    ########################################################################
    # Comparison Operators
    ########################################################################
    # Operator	Magic Method
    # <	__lt__(self, other)
    # >	__gt__(self, other)
    # <=	__le__(self, other)
    # >=	__ge__(self, other)
    # ==	__eq__(self, other)
    # !=	__ne__(self, other)
    
    ########################################################################
    # Assignment Operators
    ########################################################################
    # Operator	Magic Method
    # -=	__isub__(self, other)
    # +=	__iadd__(self, other)
    # *=	__imul__(self, other)
    # /=	__idiv__(self, other)
    # //=	__ifloordiv__(self, other)
    # %=	__imod__(self, other)
    # **=	__ipow__(self, other)
    # >>=	__irshift__(self, other)
    # <<=	__ilshift__(self, other)
    # &=	__iand__(self, other)
    # |=	__ior__(self, other)
    # ^=	__ixor__(self, other)
    
    ########################################################################
    # Unary Operators
    ########################################################################
    # Operator	Magic Method
    # –	__neg__(self)
    # +	__pos__(self)
    # ~	__invert__(self)
    
class Vector(Variable):
    pass
class Scalar(Variable):
    pass
        
# TODO: 
from _ctypes import sizeof
ror_width = 32
def rotl(n, shift):
    mask: int = 2**ror_width-1
    return (mask & (n << shift)) | (mask & (n >> (ror_width-shift)))
def ROTATE(op1: Vector, op2):
    # TODO: Handle constants here
    return op1.rotate_left(op2)
    
@dataclass
class VectorMemoryArray:
    c_type: ctype
    num_elems: int
    alignment: int = 0
    name: str = ''
    
    def checks(self, index):
        if not isinstance(index, int):
            raise TypeError('Memory index should be constant')
        
        if index < 0 or index >= self.num_elems:
            raise IndexError
        
        assert len(defined_functions) > 0
        
    def find_name(self) -> None:
        if not self.name:# and not self.is_constant:
            self.name = retrieve_name(self)
            
    def __getitem__(self, index):
        self.checks(index)      
        self.find_name()
        
        result = Vector(self.c_type, is_uninitialize=False)
        defined_functions[-1].instructions.append(LoadInstruction(result, memory=self, index=index))
        return result
    
    def __setitem__(self, index, value):
        self.checks(index)
        self.find_name()
        if isinstance(value, Vector):
            value.find_name()
        
        assert value.c_type == self.c_type
        defined_functions[-1].instructions.append(StoreInstruction(operand=value, memory=self, index=index))
