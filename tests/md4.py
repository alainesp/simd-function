#######################################################
# MD4 Message-Digest Algorithm
#######################################################

# Note: above comment is added to the C file but this one do not
import sys
sys.path.append('src/')
from simd_function import *

state = VectorMemoryArray(uint32_t, 4)  # the state
block = VectorMemoryArray(uint32_t, 16) # The message
SQRT_2 = 0x5a827999
SQRT_3 = 0x6ed9eba1

# Note: Below comment is added to C file before the function definition
    
## <summary>
## MD4 compress block
## </summary>
## <param name="state">The md4 state</param>
## <param name="block">The message to compress</param>
with Function(void)(state, block) as md4_block:
    # Load state
    a = state[0]
    b = state[1]
    c = state[2]
    d = state[3]

    # Round 1
    with Repeat(4):
        a += block[0]; t = c ^ d; t &= b; a += d ^ t; a = rotl(a,  3);
        d += block[1]; t = b ^ c; t &= a; d += c ^ t; d = rotl(d,  7);
        c += block[2]; t = a ^ b; t &= d; c += b ^ t; c = rotl(c, 11);
        b += block[3]; t = d ^ a; t &= c; b += a ^ t; b = rotl(b, 19);
        block += 4
    block -= 4 * 4

     # Round 2
    with Repeat(4):
        a += block[ 0]; t = d | c; tt = c & d; a += SQRT_2; t &= b; a += t | tt; a = rotl(a,  3);
        d += block[ 4]; t = c | b; tt = b & c; d += SQRT_2; t &= a; d += t | tt; d = rotl(d,  5);
        c += block[ 8]; t = b | a; tt = a & b; c += SQRT_2; t &= d; c += t | tt; c = rotl(c,  9);
        b += block[12]; t = a | d; tt = d & a; b += SQRT_2; t &= c; b += t | tt; b = rotl(b, 13);
        block += 1
    block -= 4

    # Round 3
    for i in [0, 2, 1, 3]:
        a += block[i +  0]; t = b ^ c; a += SQRT_3; a += t ^ d; a = rotl(a,  3);
        d += block[i +  8];            d += SQRT_3; d += t ^ a; d = rotl(d,  9);
        c += block[i +  4]; t = a ^ d; c += SQRT_3; c += t ^ b; c = rotl(c, 11);
        b += block[i + 12];            b += SQRT_3; b += t ^ c; b = rotl(b, 15);
        
    # Save state
    state[0] += a;
    state[1] += b;
    state[2] += c;
    state[3] += d;
    
# Define targets
md4_block.targets = [Target.PLAIN_C, Target.SSE2, Target.AVX, Target.AVX2, Target.AVX512]
md4_block.parallelization_factor[Target.SSE2  ] = [1, 2, 3, 4]
md4_block.parallelization_factor[Target.AVX   ] = [1, 2, 3, 4]
md4_block.parallelization_factor[Target.AVX2  ] = [1, 2, 3, 4]
md4_block.parallelization_factor[Target.AVX512] = [1, 2, 3, 4]
generate_code()
