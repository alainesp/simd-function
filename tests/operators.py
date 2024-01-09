#######################################################
# Simple operator tests
#######################################################

import sys
sys.path.append('src/')
from simd_function import *

op1 = Vector(uint32_t, is_uninitialize=False) # first operand
op2 = Vector(uint32_t, is_uninitialize=False) # second operand
op2_scalar = Scalar(uint32_t, is_uninitialize=False)

# Addition operator
with Function(Vector(uint32_t))(op1, op2) as add:
    add.Return(op1 + op2)
    
# Substraction operator
with Function(Vector(uint32_t))(op1, op2) as sub:
    sub.Return(op1 - op2)
    
# Product operator
with Function(Vector(uint32_t))(op1, op2) as prod:
    prod.Return(op1 * op2)
    
# Division operator
# with Function(Vector(uint32_t))(op1, op2) as div:
#     div.Return(op1 / op2)
# with Function(Vector(uint32_t))(op1, op2) as div1:
#     div1.Return(op1 // op2)
# with Function(Vector(uint32_t))(op1, op2) as mod:
#     mod.Return(op1 % op2)
   
# Power operator 
with Function(Vector(uint32_t))(op1) as pow:
    pow.Return(op1 ** 2)
    
# Shift left operator 
with Function(Vector(uint32_t))(op1, op2_scalar) as shiftl:
    shiftl.Return(op1 << op2_scalar)
# Shift right operator 
with Function(Vector(uint32_t))(op1, op2_scalar) as shiftr:
    shiftr.Return(op1 >> op2_scalar)
    
generate_code()