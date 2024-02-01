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
        a += block[0]; t = c ^ d; t &= b; t ^= d; a += t;     t = a <<  3; a >>= (32 -  3); a |= t; 
        d += block[1]; t = b ^ c; t &= a; t ^= c; d += t;     t = d <<  7; d >>= (32 -  7); d |= t;
        c += block[2]; t = a ^ b; t &= d; t ^= b; c += t;     t = c << 11; c >>= (32 - 11); c |= t;
        b += block[3]; t = d ^ a; t &= c; t ^= a; b += t;     t = b << 19; b >>= (32 - 19); b |= t;
        block += 4
    block -= 4 * 4

     # Round 2
    with Repeat(4):
        a += block[ 0]; t = d | c; tt = c & d; a += SQRT_2; t &= b; a += t | tt;     t = a <<  3; a >>= (32 -  3); a |= t;
        d += block[ 4]; t = c | b; tt = b & c; d += SQRT_2; t &= a; d += t | tt;     t = d <<  5; d >>= (32 -  5); d |= t;
        c += block[ 8]; t = b | a; tt = a & b; c += SQRT_2; t &= d; c += t | tt;     t = c <<  9; c >>= (32 -  9); c |= t;
        b += block[12]; t = a | d; tt = d & a; b += SQRT_2; t &= c; b += t | tt;     t = b << 13; b >>= (32 - 13); b |= t;
        block += 1
    block -= 4

    # Round 3
    for i in [0, 2, 1, 3]:
        a += block[i +  0]; t = b ^ c; a += SQRT_3; a += t ^ d;     t = a <<  3; a >>= (32 -  3); a |= t;
        d += block[i +  8];            d += SQRT_3; d += t ^ a;     t = d <<  9; d >>= (32 -  9); d |= t;
        c += block[i +  4]; t = a ^ d; c += SQRT_3; c += t ^ b;     t = c << 11; c >>= (32 - 11); c |= t;
        b += block[i + 12];            b += SQRT_3; b += t ^ c;     t = b << 15; b >>= (32 - 15); b |= t;
        
    # Save state
    state[0] += a;
    state[1] += b;
    state[2] += c;
    state[3] += d;

with Function(void)(state, block) as md4_block_:
    # Load state
    a = state[0]
    b = state[1]
    c = state[2]
    d = state[3]

    # Round 1
    with Repeat(4):
        a += block[0]; t = ternary_logic(d, c, b, 0xd8); a += t; a = rotl(a,  3);
        d += block[1]; t = ternary_logic(c, b, a, 0xd8); d += t; d = rotl(d,  7);
        c += block[2]; t = ternary_logic(b, a, d, 0xd8); c += t; c = rotl(c, 11);
        b += block[3]; t = ternary_logic(a, d, c, 0xd8); b += t; b = rotl(b, 19);
        block += 4
    block -= 4 * 4

     # Round 2
    with Repeat(4):
        a += block[ 0]; t = ternary_logic(d, c, b, 0xE8); a += SQRT_2; a += t; a = rotl(a,  3);
        d += block[ 4]; t = ternary_logic(c, b, a, 0xE8); d += SQRT_2; d += t; d = rotl(d,  5);
        c += block[ 8]; t = ternary_logic(b, a, d, 0xE8); c += SQRT_2; c += t; c = rotl(c,  9);
        b += block[12]; t = ternary_logic(a, d, c, 0xE8); b += SQRT_2; b += t; b = rotl(b, 13);
        block += 1
    block -= 4

    # Round 3
    for i in [0, 2, 1, 3]:
        a += block[i +  0]; t = ternary_logic(d, c, b, 0x96); a += SQRT_3; a += t; a = rotl(a,  3);
        d += block[i +  8]; t = ternary_logic(c, b, a, 0x96); d += SQRT_3; d += t; d = rotl(d,  9);
        c += block[i +  4]; t = ternary_logic(b, a, d, 0x96); c += SQRT_3; c += t; c = rotl(c, 11);
        b += block[i + 12]; t = ternary_logic(a, d, c, 0x96); b += SQRT_3; b += t; b = rotl(b, 15);
        
    # Save state
    state[0] += a;
    state[1] += b;
    state[2] += c;
    state[3] += d;
    
# Define targets
md4_block.targets  = [Target.PLAIN_C, Target.SSE2, Target.AVX, Target.AVX2]
md4_block_.targets = [Target.AVX512]
md4_block.parallelization_factor [Target.SSE2  ] = [2, 3, 4]
md4_block.parallelization_factor [Target.AVX   ] = [2, 3, 4]
md4_block.parallelization_factor [Target.AVX2  ] = [2, 3, 4]
md4_block_.parallelization_factor[Target.AVX512] = [2, 3, 4]
generate_code()
