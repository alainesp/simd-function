##################################################################################
# This file is part of 'SIMD-Function'
# 
# Copyright (c) 2024 by Alain Espinosa.
##################################################################################

from dataclasses import dataclass
from inspect import stack
# from atexit import register as register_at_exit
from enum import IntEnum
import operator
from os import path
from pathlib import Path
from termcolor import colored
from copy import deepcopy

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
class Target(IntEnum):
    PLAIN_C     = 1
    SSE2        = 2
    AVX         = 3
    AVX2        = 4
    AVX512      = 5
    
    MASM64_AVX  = 6
    MASM64_AVX2 = 7

default_targets: list[Target] = [Target.PLAIN_C]
def target_simd_size(target: Target) -> int:
    match target:
        case Target.PLAIN_C: return 1
        case Target.SSE2 | Target.AVX | Target.MASM64_AVX: return 4 # TODO: Consider AVX for floats
        case Target.AVX2 | Target.MASM64_AVX2: return 8
        case Target.AVX512: return 16
        case _: raise NotImplementedError

##################################################################################
# Instructions
##################################################################################
from _ctypes import sizeof

@dataclass
class Instruction:
    result: 'Variable'
    line_number: int
    is_nope: bool = False
    
    def generate_code(self, target: Target, instruction_by_tmp: dict['Variable', 'Instruction']):
        raise NotImplementedError
    def register_constant(self, constants: set[int | float]):
        pass
    def use_value(self, value) -> bool:
        return False

def get_expresion(tmp: 'int | float | Variable', target: Target, instruction_by_tmp: dict['Variable', Instruction]) -> str:
    if isinstance(tmp, int) or isinstance(tmp, float):
        return f'{tmp}'
    if target == Target.PLAIN_C and isinstance(tmp, Variable) and tmp.is_constant:
        return f'{hex(tmp.constant_value)}'
    if not tmp.is_tmp():
        return tmp.name
    if tmp.is_constant:
        return f'{hex(tmp.constant_value)}'
    
    return instruction_by_tmp[tmp].generate_code(target, instruction_by_tmp)

def is_float_type(c_type: ctype) -> bool:
    return c_type == float or c_type == double

class LoadInstruction(Instruction):
    memory: 'MemoryArray'
    index: any # Should support any index (constant, scalar, ...)
    
    def __init__(self, result, memory, index) -> None:
        super().__init__(result, get_line_number())
        self.memory = memory
        self.index = index
    
    def generate_code(self, target: Target, instruction_by_tmp: dict[any, Instruction]):
        if target == Target.PLAIN_C or isinstance(self.memory, ScalarMemoryArray):
            memory_expression = f'{self.memory.name}[{self.index}]'
            if self.result.is_tmp():
                return memory_expression
            else:
                return f'{self.result.name} = {memory_expression};'
            
        # Load data instruction
        if target == Target.MASM64_AVX or target == Target.MASM64_AVX2:
            memory_expression = f'[{self.memory.name} + {self.index}*REG_BYTE_SIZE]'
            if self.result.is_tmp():
                return memory_expression
            else:
                return f'vmovdq{'a' if self.memory.alignment >= 16 else 'u'} {self.result.name}, {get_reg_simd_name(target)}word ptr {memory_expression}\n'
        else:
            aligment_str = ''
            if (target == Target.SSE2 and self.memory.alignment < 16) or \
               (target == Target.AVX and is_float_type(self.memory.c_type) and self.memory.alignment < 32) or \
               (target == Target.AVX and not is_float_type(self.memory.c_type) and self.memory.alignment < 16) or \
               (target == Target.AVX2 and self.memory.alignment < 32) or \
               (target == Target.AVX512 and self.memory.alignment < 64):
                aligment_str = 'u'
            # Expresion
            memory_expression = f'load{aligment_str}({self.memory.name} + {self.index})'
            if self.result.is_tmp():
                return memory_expression
            else:
                return f'{self.result.name} = {memory_expression};'
        
class StoreInstruction(Instruction):
    memory: 'MemoryArray'
    index: any # Should support any index (constant, scalar, ...)
    operand: 'Scalar | Vector | int | float'
    
    def __init__(self, operand, memory, index) -> None:
        super().__init__(None, get_line_number())
        self.memory = memory
        self.index = index
        self.operand = operand
        
    def register_constant(self, constants: set[int | float]):
        if isinstance(self.operand, int) or isinstance(self.operand, float):
            constants.add(self.operand)
            self.operand = Vector(self.memory.c_type, True, self.operand, is_uninitialize=False)
            self.operand.name = f'const_{hex(self.operand.constant_value)}'
        elif self.operand.is_constant:
            constants.add(self.operand.constant_value)
            self.operand.name = f'const_{hex(self.operand.constant_value)}'
            
    def use_value(self, value) -> bool:
        return self.operand == value
    
    def generate_code(self, target: Target, instruction_by_tmp: dict[any, Instruction]):
        if target == Target.PLAIN_C or isinstance(self.memory, ScalarMemoryArray):
            memory_expression = f'{self.memory.name}[{self.index}]'
            return f'{memory_expression} = {get_expresion(self.operand, target, instruction_by_tmp)};'
        
        if target == Target.MASM64_AVX or target == Target.MASM64_AVX2:
            memory_expression = f'[{self.memory.name} + {self.index}*REG_BYTE_SIZE]'
            return f'vmovdq{'a' if self.memory.alignment >= 16 else 'u'} {get_reg_simd_name(target)}word ptr {memory_expression}, {self.operand.name}\n'
        else:
            # Load data instruction
            aligment_str = ''
            if (target == Target.SSE2 and self.memory.alignment < 16) or \
               (target == Target.AVX and self.memory.alignment < 32 and (self.memory.c_type == float or self.memory.c_type == double)) or \
               (target == Target.AVX and self.memory.alignment < 16 and (self.memory.c_type != float and self.memory.c_type != double)) or \
               (target == Target.AVX2 and self.memory.alignment < 32) or \
               (target == Target.AVX512 and self.memory.alignment < 64):
                aligment_str = 'u'
            # Expresion
            return f'store{aligment_str}({self.memory.name} + {self.index}, {get_expresion(self.operand, target, instruction_by_tmp)});'
 
class UnaryInstruction(Instruction):
    operand: 'Scalar | Vector | int | float'
    c_operator: str
    
    def __init__(self, result, operand, c_operator: str) -> None:
        super().__init__(result, get_line_number())
        self.operand = operand
        self.c_operator = c_operator
        
    def register_constant(self, constants: set[int | float]):
        if isinstance(self.operand, int) or isinstance(self.operand, float):
            constants.add(self.operand)
            self.operand = Vector(self.memory.c_type, True, self.operand, is_uninitialize=False)
            self.operand.name = f'const_{hex(self.operand.constant_value)}'
        elif self.operand.is_constant:
            constants.add(self.operand.constant_value)
            self.operand.name = f'const_{hex(self.operand.constant_value)}'
            
    def use_value(self, value) -> bool:
        return self.operand == value
        
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
    need_vector_operands: bool = False
    
    def __init__(self, result, operand1, operand2, c_operator: str = '') -> None:
        super().__init__(result, get_line_number())
        self.operand1 = operand1
        self.operand2 = operand2
        self.c_operator = c_operator
        
    def register_constant(self, constants: set[int | float]):
        if isinstance(self.operand1, int) or isinstance(self.operand1, float):
            constants.add(self.operand1)
            self.operand1 = Vector(self.operand1.c_type, True, self.operand1, is_uninitialize=False)
            self.operand1.name = f'const_{hex(self.operand1.constant_value)}'
        elif isinstance(self.operand1, Variable) and self.operand1.is_constant:
            constants.add(self.operand1.constant_value)
            self.operand1.name = f'const_{hex(self.operand1.constant_value)}'
            
        if isinstance(self.operand1, MemoryArray):
            return
        
        if isinstance(self.operand2, int) or isinstance(self.operand2, float):
            constants.add(self.operand2)
            self.operand2 = Vector(self.operand1.c_type, True, self.operand2, is_uninitialize=False)
            self.operand2.name = f'const_{hex(self.operand2.constant_value)}'
        elif self.operand2.is_constant:
            constants.add(self.operand2.constant_value)
            self.operand2.name = f'const_{hex(self.operand2.constant_value)}'
            
    def use_value(self, value) -> bool:
        return self.operand1 == value or self.operand2 == value
        
    def get_expresions(self, target: Target, instruction_by_tmp: dict[any, Instruction]) -> (str, str):
        return (get_expresion(self.operand1, target, instruction_by_tmp), get_expresion(self.operand2, target, instruction_by_tmp))
    
    def generate_code(self, target: Target, instruction_by_tmp: dict[any, Instruction]):
        if self.is_nope: return ''
        operand1_expression, operand2_expression = self.get_expresions(target, instruction_by_tmp)
        
        if target == Target.MASM64_AVX or target == Target.MASM64_AVX2:
            # Check memory access
            if self.operand1.is_tmp() and isinstance(instruction_by_tmp[self.operand1], LoadInstruction) and \
               self.operand2.is_tmp() and isinstance(instruction_by_tmp[self.operand2], LoadInstruction):
                raise TypeError
            # Move memory access to last operand
            if self.operand1.is_tmp() and isinstance(instruction_by_tmp[self.operand1], LoadInstruction):
                operand1_expression, operand2_expression = operand2_expression, operand1_expression
            elif self.result.name and self.result.name == operand2_expression:
                operand1_expression, operand2_expression = operand2_expression, operand1_expression
            
            return f'{self.get_call(target)}    {self.result.name}, {operand1_expression}, {operand2_expression}\n'
        else:
            if self.c_operator:
            # if self.c_operator and (target == Target.PLAIN_C or (isinstance(self.operand1, Scalar) and (isinstance(self.operand2, Scalar) or isinstance(self.operand2, int))) \
            #     or isinstance(self.operand1, MemoryArray)):
                if self.result.is_tmp():
                    return f'({operand1_expression} {self.c_operator} {operand2_expression})'
                else:
                    if self.result.name == operand1_expression:
                        return f'{self.result.name} {self.c_operator}= {operand2_expression};'
                    elif self.result.name == operand2_expression:
                        return f'{self.result.name} {self.c_operator}= {operand1_expression};'
                    else:
                        return f'{self.result.name} = {operand1_expression} {self.c_operator} {operand2_expression};'
                    
            # Vectorization
            # if self.need_vector_operands and not isinstance(self.operand2, Vector):
            #     operand2_expression = f'_mm{'' if target == Target.SSE2 else '256'}_set1_{get_vector_ins_sizeof('', self.operand1.c_type)}({operand2_expression})'
            # if self.need_vector_operands and isinstance(self.operand2, Vector) and self.operand2.is_constant:
            #     operand2_expression = f'_mm{'' if target == Target.SSE2 else '256'}_set1_{get_vector_ins_sizeof('', self.operand1.c_type)}({hex(self.operand2.constant_value)})'
                
            call_result = f'{self.get_call(target)}({operand1_expression}, {operand2_expression})'
            if self.result.is_tmp():
                return call_result
            else:
                return f'{self.result.name} = {call_result};'
            
# Aritmetic      
class AddInstruction(BinaryInstruction):
    def __init__(self, result, operand1, operand2) -> None:
        super().__init__(result, operand1, operand2, '+')
        self.need_vector_operands = True
    def get_call(self, target: Target) -> str:
        match target:
            case Target.MASM64_AVX | Target.MASM64_AVX2: return f'vpaddd' # TODO: handle floats, and other ints
            case _: raise NotImplementedError
        
class SubInstruction(BinaryInstruction):
    def __init__(self, result, operand1, operand2) -> None:
        super().__init__(result, operand1, operand2, '-')
        self.need_vector_operands = True
    def get_call(self, target: Target) -> str:
        raise NotImplementedError
        
class ProductInstruction(BinaryInstruction):
    def __init__(self, result, operand1, operand2) -> None:
        super().__init__(result, operand1, operand2, '*')
    def get_call(self, target: Target) -> str:
        raise NotImplementedError
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
class LogicalInstruction(BinaryInstruction):
    op_name: str
    def __init__(self, result, operand1, operand2, c_operator: str, op_name: str) -> None:
        super().__init__(result, operand1, operand2, c_operator)
        self.need_vector_operands = True
        self.op_name = op_name
    def get_call(self, target: Target):
        match target:
            case Target.MASM64_AVX | Target.MASM64_AVX2: return f'vp{self.op_name}' # TODO: handle floats
            case _: raise NotImplementedError
class AndInstruction(LogicalInstruction):
    def __init__(self, result, operand1, operand2) -> None:
        super().__init__(result, operand1, operand2, '&', 'and')
class OrInstruction(LogicalInstruction):
    def __init__(self, result, operand1, operand2) -> None:
        super().__init__(result, operand1, operand2, '|', 'or')
class XorInstruction(LogicalInstruction):
    def __init__(self, result, operand1, operand2) -> None:
        super().__init__(result, operand1, operand2, '^', 'xor')
        
# Shift/Rotations
class ShiftLInstruction(BinaryInstruction):
    def __init__(self, result, operand1, operand2) -> None:
        super().__init__(result, operand1, operand2, '<<')

    def register_constant(self, constants: set[int | float]):
        pass
        
    def get_call(self, target: Target) -> str:
        if isinstance(self.operand2, int) or isinstance(self.operand2, Scalar):
            match target:
                case Target.MASM64_AVX | Target.MASM64_AVX2: return f'vpslld' # TODO: handle floats
                case _: raise NotImplementedError
        
        raise TypeError
class ShiftRInstruction(BinaryInstruction):
    def __init__(self, result, operand1, operand2) -> None:
        super().__init__(result, operand1, operand2, '>>')
        
    def register_constant(self, constants: set[int | float]):
        pass
       
    def get_call(self, target: Target) -> str:
        if isinstance(self.operand2, int) or isinstance(self.operand2, Scalar):
            match target:
                case Target.MASM64_AVX | Target.MASM64_AVX2: return f'vpsrld' # TODO: handle floats
                case _: raise NotImplementedError
        
        raise TypeError
class RotlInstruction(BinaryInstruction):
    def register_constant(self, constants: set[int | float]):
        pass
       
    def get_call(self, target: Target) -> str:
        if target == Target.PLAIN_C or isinstance(self.operand1, Scalar):
            return 'std::rotl'
            
        raise NotImplementedError
           
class RepeatInstruction(Instruction):
    count: int
    is_close: bool
    
    def __init__(self, count: int, is_close: bool) -> None:
        super().__init__(None, get_line_number())
        self.count = count
        self.is_close = is_close
        if is_close:
            self.line_number = defined_functions[-1].instructions[-1].line_number + 1
    
    def generate_code(self, target: Target, instruction_by_tmp: dict['Variable', 'Instruction']) -> str:
        if self.is_nope: return ''
        
        match target:
            case Target.PLAIN_C | Target.SSE2 | Target.AVX | Target.AVX2 | Target.AVX512:
                if self.is_close:
                    return '}\n'
                else:
                    return f'for (int i = 0; i < {self.count}; i++) ' + '{'
            case _: raise NotImplementedError

@dataclass
class Repeat:
    count: int
    
    def __enter__(self):
        defined_functions[-1].instructions.append(RepeatInstruction(self.count, False))
    
    def __exit__(self, exception_type, exception_value, traceback):
        defined_functions[-1].instructions.append(RepeatInstruction(self.count, True))
    
##################################################################################
# SIMD function
##################################################################################
def get_type(var: any, target: Target) -> str:
    
    if isinstance(var, Vector) or isinstance(var, VectorMemoryArray): 
        match target:
            case Target.PLAIN_C: return retrieve_name(var.c_type)
            case Target.SSE2:
                if var.c_type == float: return 'simd::Vec128Float'
                if var.c_type == double: return 'simd::Vec128Double'
                return f'simd::Vec128{retrieve_name(var.c_type)[0]}{sizeof(var.c_type) * 8}'
            case Target.AVX:
                if var.c_type == float: return 'simd::Vec256Float'
                if var.c_type == double: return 'simd::Vec256Double'
                return f'simd::Vec128{retrieve_name(var.c_type)[0]}{sizeof(var.c_type) * 8}'
            case Target.AVX2:
                if var.c_type == float: return 'simd::Vec256Float'
                if var.c_type == double: return 'simd::Vec256Double'
                return f'simd::Vec256{retrieve_name(var.c_type)[0]}{sizeof(var.c_type) * 8}'
            case Target.AVX512:
                if var.c_type == float: return 'simd::Vec512Float'
                if var.c_type == double: return 'simd::Vec512Double'
                return f'simd::Vec512{retrieve_name(var.c_type)[0]}{sizeof(var.c_type) * 8}'
            
            case Target.MASM64_AVX : return '__m128' if var.c_type == float else ('__m128d' if var.c_type == double else '__m128i')
            case Target.MASM64_AVX2: return '__m256' if var.c_type == float else ('__m256d' if var.c_type == double else '__m256i')
            case _: raise NotImplementedError
            
    if isinstance(var, Scalar) or isinstance(var, ScalarMemoryArray):
        return retrieve_name(var.c_type)
    
    if var is None:
        return 'void'
    
    return retrieve_name(var) 

def get_reg_simd_name(target: Target) -> str:
    match target:
        case Target.MASM64_AVX: return 'xmm'
        case Target.MASM64_AVX2: return 'ymm'
        #case Target.MASM64_AVX512: return 'zmm'
        case _: raise NotImplementedError

class Function:
    result_type: ctype
    name: str
    params: list['Variable | MemoryArray']
    instructions: list[Instruction]
    targets: list[Target]
    parallelization_factor: dict[Target, int]
    exited: bool = False
    
    def __init__(self, result_type: ctype = void, targets: list[Target] = default_targets):
        self.result_type = result_type
        self.params = []
        self.instructions = []
        self.targets = targets
        self.parallelization_factor = {}
        for target in Target:
            self.parallelization_factor[target] = 1
    
    def __call__(self, *args):
        for arg in args:
            self.params.append(arg)
            arg.find_name()
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
    
    def get_includes(self, includes: set[str]):
        for target in self.targets:
            match target:
                case Target.PLAIN_C | Target.SSE2 | Target.AVX | Target.AVX2 | Target.AVX512:
                    pass
                case Target.MASM64_AVX | Target.MASM64_AVX2: pass
                case _: raise NotImplementedError
    
    def __get_params_definition(self, target: Target) -> str:
        result = '('
        
        param_separator: str = ''
        for arg in self.params:
            param_suffix = f'[{arg.num_elems}]' if isinstance(arg, MemoryArray) else ''
            result += f'{param_separator}{get_type(arg, target)} {arg.name}{param_suffix}'
            param_separator = ', '
            
        return result + ')'
    
    def __convert_rotations_to_shifts(self):
        for ins in self.instructions:
            if isinstance(ins, RotlInstruction):
                i = self.instructions.index(ins)
                self.instructions.remove(ins)
                
                t0 = Vector(ins.result.c_type, is_uninitialize=False)
                t1 = Vector(ins.result.c_type, is_uninitialize=False)
                self.instructions.insert(i, ShiftRInstruction(t0, ins.operand1, sizeof(t0.c_type)*8-ins.operand2))
                self.instructions.insert(i+1, ShiftLInstruction(t1, ins.operand1, ins.operand2))
                self.instructions.insert(i+2, OrInstruction(ins.result, t1, t0))
                self.instructions[i].line_number = ins.line_number
                self.instructions[i+1].line_number = ins.line_number
                self.instructions[i+2].line_number = ins.line_number
                
    def generate_code(self, output, comments: list[Comment], is_header: bool):
        if is_header:
            for target in self.targets:
                # Parallelization
                for arg in self.params:
                    if isinstance(arg, VectorMemoryArray):       
                        arg.num_elems *= self.parallelization_factor[target]
                output.write(f'{get_type(self.result_type, target)} {self.name}_{target.name.lower()}{self.__get_params_definition(target)};\n')
                # Revert Parallelization
                for arg in self.params:
                    if isinstance(arg, VectorMemoryArray):       
                        arg.num_elems //= self.parallelization_factor[target]            
            return
        
        if not hasattr(self, 'instructions_with_rot'):
            self.instructions_with_rot = deepcopy(self.instructions)
        self.__convert_rotations_to_shifts()
        old_instructions = self.instructions
        old_params = self.params
                    
        if Target.MASM64_AVX in self.targets or Target.MASM64_AVX2 in self.targets:
            # Last time we use the register
            last_use: dict[Vector, int] = {}
            for i, instruction in enumerate(self.instructions):
                for j in range(i+1, len(self.instructions)):
                    if self.instructions[j].use_value(instruction.result):
                        last_use[instruction.result] = j

            tmp_in_use: list[bool] = [False] * 64
            tmp_reset: list[list[int]] =[ [] for _ in range(len(self.instructions)) ]
            x64_registers: set[str] = set()
            num_mem_loads, num_mem_stores, num_logical_arithmetic, num_shifts = 0, 0, 0, 0
            tmps_vector = set()
            for i, instruction in enumerate(self.instructions):
                # Reset elements
                for index in tmp_reset[i]:
                    tmp_in_use[index] = False
                
                if instruction.result and instruction.result.is_tmp() and not isinstance(instruction, LoadInstruction):
                    # Reuse variables
                    if hasattr(instruction, 'operand1') and isinstance(instruction.operand1, Vector) and instruction.operand1.name and \
                        instruction.operand1 not in tmps_vector and instruction.operand1 in last_use and last_use[instruction.operand1] <= i:
                        instruction.result.name = instruction.operand1.name
                    elif hasattr(instruction, 'operand2') and isinstance(instruction.operand2, Vector) and instruction.operand2.name and \
                        instruction.operand2 not in tmps_vector and instruction.operand2 in last_use and last_use[instruction.operand2] <= i:
                        instruction.result.name = instruction.operand2.name
                    else:
                        tmp_index = tmp_in_use.index(False)
                        instruction.result.name = f't{tmp_index}'
                        tmp_in_use[tmp_index] = True
                        tmp_reset[last_use[instruction.result]].append(tmp_index)
                        tmps_vector.add(instruction.result)
                    
                # Count registers
                if instruction.result and instruction.result.name:
                    x64_registers.add(instruction.result.name)
                # Count instructions
                if isinstance(instruction, LoadInstruction): num_mem_loads += 1
                if isinstance(instruction, StoreInstruction): num_mem_stores += 1
                if isinstance(instruction, LogicalInstruction) or isinstance(instruction, AddInstruction): num_logical_arithmetic += 1
                if isinstance(instruction, RotlInstruction): num_shifts += 2; num_logical_arithmetic += 1
                if isinstance(instruction, ShiftLInstruction) or isinstance(instruction, ShiftRInstruction): num_shifts += 1
            
            # Show data
            print(f'Function: {colored(self.name, 'green')}')
            print(f'\tSIMD Register: {len(x64_registers)} / 16')
            print(f'\tInstructions: {len(self.instructions)}')
            print(f'\tMemLoads: {num_mem_loads}')
            print(f'\tMemStores: {num_mem_stores}')
            print(f'\tLogicalArithmetics: {num_logical_arithmetic}')
            print(f'\tShifts: {num_shifts}')
        
        # Generate code for all targets
        for target in self.targets:
            ########################################################################################
            # Parallelization
            ########################################################################################
            parallel_factor = self.parallelization_factor[target]
            # Params
            self.params = deepcopy(old_params)
            for arg in self.params:
                if isinstance(arg, VectorMemoryArray):       
                    arg.num_elems *= parallel_factor
                    
            self.instructions = [] 
            if parallel_factor <= 1:
                self.instructions = deepcopy(old_instructions) if target != Target.PLAIN_C else self.instructions_with_rot
            elif parallel_factor == 2:
                for ins0, ins1 in zip(deepcopy(old_instructions), deepcopy(old_instructions)):
                    if isinstance(ins0, RepeatInstruction): ins1.is_nope = True
                    self.instructions += [ins0, ins1]
            elif parallel_factor == 3:
                for ins0, ins1, ins2 in zip(deepcopy(old_instructions), deepcopy(old_instructions), deepcopy(old_instructions)):
                    if isinstance(ins0, RepeatInstruction): ins1.is_nope = True; ins2.is_nope = True
                    self.instructions += [ins0, ins1, ins2]
            elif parallel_factor == 4:
                for ins0, ins1, ins2, ins3 in zip(deepcopy(old_instructions), deepcopy(old_instructions), deepcopy(old_instructions), deepcopy(old_instructions)):
                    if isinstance(ins0, RepeatInstruction): ins1.is_nope = True; ins2.is_nope = True; ins3.is_nope = True
                    self.instructions += [ins0, ins1, ins2, ins3]
            else:
                raise NotImplementedError
            
            if parallel_factor > 1:
                for i in range(0, len(self.instructions), parallel_factor):
                    # Variables
                    if self.instructions[i].result and self.instructions[i].result.name:
                        if isinstance(self.instructions[i].result, MemoryArray):
                            self.instructions[i].operand2 *= parallel_factor
                            for p in range(1, parallel_factor):
                                self.instructions[i + p].is_nope = True
                        else:
                            for p in range(parallel_factor):
                                self.instructions[i + p].result.name += f'{p}'
                    # Memory access
                    if isinstance(self.instructions[i], LoadInstruction) or isinstance(self.instructions[i], StoreInstruction):
                        for p in range(parallel_factor):
                            self.instructions[i + p].index = self.instructions[i + p].index * parallel_factor + p
            ########################################################################################
                
            # Find the instruction by the result
            instruction_by_tmp = {}
            for instruction in self.instructions:
                if not isinstance(instruction, StoreInstruction) and not isinstance(instruction, ReturnInstruction):
                    instruction_by_tmp[instruction.result] = instruction
                
            # Function signature
            match target:
                case Target.PLAIN_C | Target.SSE2 | Target.AVX | Target.AVX2 | Target.AVX512:
                    output.write(f'extern "C" {get_type(self.result_type, target)} {self.name}_{target.name.lower()}{self.__get_params_definition(target)}')
                    output.write('\n{\n')
                    
                    last_type: str = ''
                    variable_names = set()
                    param_names = set([arg.name for arg in self.params])
                    for instruction in self.instructions:
                        if instruction.result and instruction.result.name and instruction.result.name not in variable_names and instruction.result.name not in param_names:
                            variable_names.add(instruction.result.name)
                            new_type: str = get_type(instruction.result, target)
                            if new_type == last_type:
                                output.write(f', {instruction.result.name}')
                            else:
                                output.write(f'{";\n" if last_type else ""}\t{new_type} {instruction.result.name}')
                                last_type = new_type
                    output.write(';\n\n')
                    
                case Target.MASM64_AVX | Target.MASM64_AVX2:
                    x64_abi_params = ['rcx', 'rdx', 'r8', 'r9']
                    
                    output.write(f'REG_BYTE_SIZE = {16 if target == Target.MASM64_AVX else 32}\n')
                    # TODO Support this well
                    for index,arg in enumerate(self.params):
                        output.write(f'{arg.name} EQU {x64_abi_params[index]}\n')
                        
                    x64_registers: list[str] = []
                    for instruction in self.instructions:
                        if instruction.result and instruction.result.name and instruction.result.name not in [reg_name for reg_name in x64_registers]:
                            x64_registers.append(instruction.result.name)
                    
                    # TODO: Use registers depending on var type
                    for index,var_name in enumerate(x64_registers):
                        output.write(f'{var_name} EQU {get_reg_simd_name(target)}{index}\n')
                        
                    # Function signature
                    output.write(f'{self.name}_{target.name} PROC ;{self.__get_params_definition(target)} -> {get_type(self.result_type, target)}\n')
                case _: raise NotImplementedError
            
            variable_names = set()
            for arg in self.params:
                variable_names.add(arg.name)
            # Define params and variables
            for instruction in self.instructions:
                if instruction.result and instruction.result.name not in variable_names:
                    variable_names.add(instruction.result.name)
            
            # Function body
            current_line = self.line_function_definition + 1
            comment_index = 0
            while comments[comment_index].line < current_line:
                comment_index += 1
            
            tabulation = '\t'
            for instruction in self.instructions:
                if instruction.is_nope: continue
                
                if isinstance(instruction, RepeatInstruction) and instruction.is_close:
                    tabulation = tabulation.removesuffix('\t')
                    
                if isinstance(instruction, StoreInstruction) or isinstance(instruction, ReturnInstruction) or isinstance(instruction, RepeatInstruction) or not instruction.result.is_tmp():
                    # Write comments
                    if instruction.line_number > comments[comment_index].line:
                        output.write('\n'*(comments[comment_index].line - current_line))
                        output.write(f'{tabulation}{comments[comment_index].comment}')
                        current_line = comments[comment_index].line + 1
                        comment_index += 1
                        
                    # Write line spaces
                    if current_line > instruction.line_number: # Support cycles in Python
                        current_line = instruction.line_number - 1
                    output.write('\n'*(instruction.line_number - current_line))
                    current_line = instruction.line_number
                    # Instruction
                    output.write(tabulation)
                    if instruction.result and instruction.result.name not in variable_names:
                        output.write(f'{get_type(instruction.result, target)} ')
                        variable_names.add(instruction.result.name)
                    output.write(instruction.generate_code(target, instruction_by_tmp))
                    
                if isinstance(instruction, RepeatInstruction) and not instruction.is_close:
                    tabulation += '\t'
            
            # Close function definition
            match target:
                case Target.PLAIN_C | Target.SSE2 | Target.AVX | Target.AVX2 | Target.AVX512:          
                    output.write('\n}\n\n')
                case Target.MASM64_AVX | Target.MASM64_AVX2:
                    output.write(f'\n\n\tvzeroupper\n\tRET\n{self.name}_{target.name} ENDP\n\n')
                case _: raise NotImplementedError
                
        self.instructions = old_instructions
        self.params = old_params
    
    def Return(self, value):
        if self.exited:
            raise TypeError('Function return outside definition')
        
        if isinstance(value, Variable):
            if self.result_type.c_type != value.c_type:
                raise TypeError
            self.instructions.append(ReturnInstruction(value))
        else:
            raise TypeError

defined_functions: list[Function] = []
def generate_code_one_file(filename: str, targets: set[Target], comments: list[Comment]) -> None:
    
    functions: list[Function] = [func for func in defined_functions if len(targets.intersection(func.targets)) > 0]
    # Set targets
    original_targets = [func.targets for func in functions]
    for func in functions:
        func.targets = list(targets)
        func.targets.sort()
          
    is_header = filename.endswith('.h')  
    is_masm_file: bool = not is_header and (Target.MASM64_AVX in targets or Target.MASM64_AVX2 in targets) 
    # Constants
    constants: set[int | float] = set()
    if is_masm_file: 
        for func in functions:
            for instruction in func.instructions:
                instruction.register_constant(constants)
    
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
        output.write(f'{';' if is_masm_file else '//'} Automatically generated code by SIMD-function library\n\n')
        
        # Includes
        # includes: set = set()
        # for func in functions:
        #     func.get_includes(includes)
        # output.writelines([f'#include "{include}"\n' for include in includes])
        output.write(
'''#define SimdScalarType uint32_t
#include "../src/simd.hpp"
#include <bit>
using namespace simd;
''')
        # Constants
        if len(constants) > 0:
            if is_masm_file:
                output.write(
'''CONST SEGMENT READONLY ALIGN(64) 'DATA' ALIAS('.const')
ALIGN 64

''')
                for constant in constants:
                    if isinstance(constant, int):
                        # TODO Support more int types
                        output.write(f'const_{hex(constant)} DD ')
                        for i in range(8 if Target.MASM64_AVX2 in targets else 4):
                            output.write(f'{"" if i == 0 else ","}{hex(constant).replace('0x', '0')}H')
                        output.write('\n')
                    else:
                        raise NotImplementedError
                    
                output.write('\nCONST	ENDS\n\n')
            else:
                pass # TODO-------------------------
                # for constant in constants:
                #     if isinstance(constant, int):
                #         # TODO Support more int types
                #         operand2_expression = f'_mm{'' if target == Target.SSE2 else '256'}_set1_{get_vector_ins_sizeof('', self.operand1.c_type)}({operand2_expression})'
                #         output.write(f'static const const_{hex(constant)} = ;\n')
            
        # begin of code
        if is_masm_file:
            output.write('.code\n')
        
        # Get macros needed
        if not is_header:
            macros = set()
            for func in functions:
                for instruction in func.instructions:
                    if hasattr(instruction, 'used_macros'):
                        for t in func.targets:
                            macro = instruction.used_macros(t)
                            if macro:
                                macros.add(macro)
            # Write the macros
            output.writelines(macros)
            output.write('\n')
        
        if is_header:
            output.write(
'''#ifdef __cplusplus
extern "C"
{
#endif

''')
        for func in functions:
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
            func.generate_code(output, comments, is_header)
            
        if is_header:
            output.write('''
#ifdef __cplusplus
}
#endif
''')
            
        # End of file
        if is_masm_file:
            output.write('end\n')
    
    # Restore original targets
    for (func, t) in zip(functions, original_targets):
        func.targets = t
    
def generate_code(filename_root: str = None, include_tests: bool = True):
    # Group targets on the same file
    c_code_targets: set[Target] = set()
    masm64_targets: set[Target] = set()
    for func in defined_functions:
        for target in func.targets:
            match target:
                case Target.PLAIN_C | Target.SSE2 | Target.AVX | Target.AVX2 | Target.AVX512:
                    c_code_targets.add(target)
                case Target.MASM64_AVX | Target.MASM64_AVX2:
                    masm64_targets.add(target)
                case _: raise NotImplementedError   
    
    comments: list[Comment] = get_comments()
    
    if filename_root is None:
        filename_root = get_function_definition_filename().removesuffix('.py')
    
    # Generate code
    generate_code_one_file(filename_root + ".h", c_code_targets | masm64_targets, comments)
    if len(c_code_targets) > 0:
        generate_code_one_file(filename_root + ".cpp", c_code_targets, comments)
    for comment in comments:
        comment.comment = comment.comment.replace('//', ';')
    if len(masm64_targets) > 0:
        generate_code_one_file(filename_root + ".asm", masm64_targets, comments)
    
    # Generate Google Tests
    if include_tests:
        with open(path.dirname(filename_root) + '/CMakeLists.txt', 'w') as cmakelist:
            cmakelist.write(
'''
###############################################################################################################
# This file is part of 'Fast-Small-Crypto'
###############################################################################################################
cmake_minimum_required (VERSION 3.12)

project (fast-small-crypto VERSION 1.0.0.0 DESCRIPTION "Fast crypto implementations for small data" LANGUAGES C CXX ASM_MASM)

# Enable Hot Reload for MSVC compilers if supported.
if (POLICY CMP0141)
  cmake_policy(SET CMP0141 NEW)
  set(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT "$<IF:$<AND:$<C_COMPILER_ID:MSVC>,$<CXX_COMPILER_ID:MSVC>>,$<$<CONFIG:Debug,RelWithDebInfo>:EditAndContinue>,$<$<CONFIG:Debug,RelWithDebInfo>:ProgramDatabase>>")
endif()

###############################################################################################################
# Testing
###############################################################################################################
include(FetchContent)
SET(BUILD_GMOCK OFF)
FetchContent_Declare(googletest URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip)            
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

enable_testing()

add_executable(runUnitTests tests.cpp)
set_property(TARGET runUnitTests PROPERTY CXX_STANDARD 20) # C++ language to use
target_link_libraries(runUnitTests PRIVATE gtest_main)

include(GoogleTest)
gtest_discover_tests(runUnitTests)

###############################################################################################################
# Benchmark
###############################################################################################################
add_executable(runBenchmark benchmark.cpp md4.cpp md4.asm arch_x64.asm)
set_property(TARGET runBenchmark PROPERTY CXX_STANDARD 20)	 # C++ language to use

FetchContent_Declare(benchmark URL https://github.com/google/benchmark/archive/refs/tags/v1.8.3.zip)
set(BENCHMARK_ENABLE_TESTING OFF CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(benchmark)
target_link_libraries(runBenchmark PRIVATE benchmark::benchmark benchmark::benchmark_main)
''')
        
        with open(path.dirname(filename_root) + '/tests.cpp', 'w') as tests:
            tests.write(f'#include <gtest/gtest.h>\n#include "{Path(filename_root).name}.h"\n\n')
            
        with open(path.dirname(filename_root) + '/benchmark.cpp', 'w') as benchmark:
            benchmark.write(f'#include <benchmark/benchmark.h>\n#include "{Path(filename_root).name}.h"\n\n')
            
            for func in defined_functions:
                for target in func.targets:
                    benchmark.write(f'static void BM_{func.name}_{target.name}(benchmark::State& _benchmark_state) ')
                    benchmark.write('{\n')
                    # Function params declaration
                    for arg in func.params:
                        param_suffix = f'[{arg.num_elems * (func.parallelization_factor[target] if isinstance(arg, VectorMemoryArray) else 1)}]' if isinstance(arg, MemoryArray) else ''
                        benchmark.write(f'\t{get_type(arg, target)} {arg.name}{param_suffix};\n')
                    
                    benchmark.write('\tuint32_t num_calls = 0;\n')
                    benchmark.write('\tfor (auto _ : _benchmark_state) {\n')
                    benchmark.write(f'\t\t{func.name}_{target.name.lower()}(')
                    param_separator: str = ''
                    for arg in func.params:
                        benchmark.write(f'{param_separator}{arg.name}')
                        param_separator = ', '
                    benchmark.write(');\n\t\tnum_calls++;\n\t}\n')
                    benchmark.write(f'\t_benchmark_state.counters["CallRate"] = benchmark::Counter(num_calls * {
                        target_simd_size(target) * func.parallelization_factor[target]}, benchmark::Counter::kIsRate);\n')
                    benchmark.write('}\n')
                    # Register the function as a benchmark
                    benchmark.write(f'BENCHMARK(BM_{func.name}_{target.name});\n\n')
                    
            benchmark.write('''
// My code
extern "C" void dcc_ntlm_part_avx2(__m256i state[12], __m256i block[48]);
static void BM_md4_block_avx2_asm(benchmark::State& _benchmark_state) {
	__m256i state[12];
	__m256i block[48];
	uint32_t num_calls = 0;

	for (auto _ : _benchmark_state) {
		dcc_ntlm_part_avx2(state, block);
		num_calls++;
	}
	_benchmark_state.counters["CallRate"] = benchmark::Counter(num_calls * 24, benchmark::Counter::kIsRate);
}
BENCHMARK(BM_md4_block_avx2_asm);
''')
            
        
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
    constant_value: int | float = 0
    
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
    def rotl(self, other):
        return self._binary_op(other, raise_exception, RotlInstruction)
    
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
def raise_exception(op1, op2):
    raise NotImplementedError
    
def rotl_constant(n, shift, ror_width: int):
    mask: int = 2**ror_width-1
    return (mask & (n << shift)) | (mask & (n >> (ror_width-shift)))
def rotl(op1: int | Scalar | Vector, op2: int | Scalar | Vector) -> int | Scalar | Vector:
    if isinstance(op1, int) and isinstance(op2, int):
        return rotl_constant(op1, op2, 32)
    if (isinstance(op1, Scalar) or isinstance(op1, Vector)) and op1.is_constant and isinstance(op2, int):
        return rotl_constant(op1.constant_value, op2, sizeof(op1.c_type)*8)
    if isinstance(op1, int) and (isinstance(op2, Scalar) or isinstance(op2, Vector)) and op2.is_constant:
        return rotl_constant(op1, op2.constant_value, sizeof(op2.c_type)*8)
    if (isinstance(op1, Scalar) or isinstance(op1, Vector)) and op1.is_constant and (isinstance(op2, Scalar) or isinstance(op2, Vector)) and op2.is_constant:
        return rotl_constant(op1.constant_value, op2.constant_value, sizeof(op1.c_type)*8)
    
    return op1.rotl(op2)
    
class MemoryArray:
    c_type: ctype
    num_elems: int
    name: str = ''
    
    def __init__(self, c_type: ctype, num_elems: int):
        self.c_type = c_type
        self.num_elems = num_elems
        
    def is_tmp(self) -> bool:
        return not self.name
    
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
        
        if isinstance(self, VectorMemoryArray):
            result = Vector(self.c_type, is_uninitialize=False)
        elif isinstance(self, ScalarMemoryArray):
            result = Scalar(self.c_type, is_uninitialize=False)
        else:
            raise TypeError
        defined_functions[-1].instructions.append(LoadInstruction(result, memory=self, index=index))
        return result
    
    def __setitem__(self, index, value):
        self.checks(index)
        self.find_name()
        if isinstance(value, Vector) or isinstance(value, Scalar):
            value.find_name()
        
        assert value.c_type == self.c_type
        defined_functions[-1].instructions.append(StoreInstruction(operand=value, memory=self, index=index))
        
    def __add__(self, other):
        self.find_name()
        if not isinstance(other, int) and not isinstance(other, Scalar):
            raise TypeError    
        defined_functions[-1].instructions.append(AddInstruction(self, self, other))
        return self
        
    def __sub__(self, other):
        self.find_name()
        if not isinstance(other, int) and not isinstance(other, Scalar):
            raise TypeError    
        defined_functions[-1].instructions.append(SubInstruction(self, self, other))
        return self
        
class VectorMemoryArray(MemoryArray):
    alignment: int = 64
class ScalarMemoryArray(MemoryArray):
    pass
