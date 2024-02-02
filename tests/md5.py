#######################################################
# MD4 Message-Digest Algorithm
#######################################################

import sys
sys.path.append('src/')
from simd_function import *

state = VectorMemoryArray(uint32_t, 4)  # the state
block = VectorMemoryArray(uint32_t, 16) # The message
md5_consts = VectorMemoryArray(uint32_t, is_global = True, is_parallelizable = False, initial_values = [
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,

    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,

    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05, 0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,

    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391
])
    
## <summary>
## MD5 compress block
## </summary>
## <param name="state">The md5 state</param>
## <param name="block">The message to compress</param>
with Function(void)(state, block) as md5_block:
    # Load state
    a = state[0]
    b = state[1]
    c = state[2]
    d = state[3]

    # Round 1
    for i in range(0, 16, 4):
        a += block[i+0]; t = c ^ d; t &= b; a += md5_consts[i+0]; t ^= d; a += t; a = rotl(a,  7); a += b;
        d += block[i+1]; t = b ^ c; t &= a; d += md5_consts[i+1]; t ^= c; d += t; d = rotl(d, 12); d += a;
        c += block[i+2]; t = a ^ b; t &= d; c += md5_consts[i+2]; t ^= b; c += t; c = rotl(c, 17); c += d;
        b += block[i+3]; t = d ^ a; t &= c; b += md5_consts[i+3]; t ^= a; b += t; b = rotl(b, 22); b += c;

	# Round 2
    for i in range(0, 16, 4):
        a += block[(i+1 ) & 15]; t = b ^ c; t &= d; a += md5_consts[i+0+16]; t ^= c; a += t; a = rotl(a,  5); a += b;
        d += block[(i+6 ) & 15]; t = a ^ b; t &= c; d += md5_consts[i+1+16]; t ^= b; d += t; d = rotl(d,  9); d += a;
        c += block[(i+11) & 15]; t = d ^ a; t &= b; c += md5_consts[i+2+16]; t ^= a; c += t; c = rotl(c, 14); c += d;
        b += block[(i+0 ) & 15]; t = c ^ d; t &= a; b += md5_consts[i+3+16]; t ^= d; b += t; b = rotl(b, 20); b += c;

	# Round 3
    for i,const_i in zip([0, -4, -8, -12], [0, 4, 8, 12]):
        a += block[(i+5 +16) & 15]; t = c ^ d; a += md5_consts[const_i+0+32]; t ^= b; a += t; a = rotl(a,  4); a += b;
        d += block[(i+8 +16) & 15]; t = b ^ c; d += md5_consts[const_i+1+32]; t ^= a; d += t; d = rotl(d, 11); d += a;
        c += block[(i+11+16) & 15]; t = a ^ b; c += md5_consts[const_i+2+32]; t ^= d; c += t; c = rotl(c, 16); c += d;
        b += block[(i+14+16) & 15]; t = d ^ a; b += md5_consts[const_i+3+32]; t ^= c; b += t; b = rotl(b, 23); b += c;

	# Round 4
    for i,const_i in zip([0, 12, 24, 36], [0, 4, 8, 12]):
        a += block[(i+0 ) & 15]; t = ~d; a += md5_consts[const_i+0+48]; t |= b; t ^= c; a += t; a = rotl(a,  6); a += b;
        d += block[(i+7 ) & 15]; t = ~c; d += md5_consts[const_i+1+48]; t |= a; t ^= b; d += t; d = rotl(d, 10); d += a;
        c += block[(i+14) & 15]; t = ~b; c += md5_consts[const_i+2+48]; t |= d; t ^= a; c += t; c = rotl(c, 15); c += d;
        b += block[(i+5 ) & 15]; t = ~a; b += md5_consts[const_i+3+48]; t |= c; t ^= d; b += t; b = rotl(b, 21); b += c;
        
    # Save state
    state[0] += a;
    state[1] += b;
    state[2] += c;
    state[3] += d;

with Function(void)(state, block) as md5_block_:
    # Load state
    a = state[0]
    b = state[1]
    c = state[2]
    d = state[3]

    # Round 1
    for i in range(0, 16, 4):
        a += block[i+0]; a += (d ^ (b & (c ^ d))); a += md5_consts[i+0]; a = rotl(a,  7); a += b;
        d += block[i+1]; d += (c ^ (a & (b ^ c))); d += md5_consts[i+1]; d = rotl(d, 12); d += a;
        c += block[i+2]; c += (b ^ (d & (a ^ b))); c += md5_consts[i+2]; c = rotl(c, 17); c += d;
        b += block[i+3]; b += (a ^ (c & (d ^ a))); b += md5_consts[i+3]; b = rotl(b, 22); b += c;

	# Round 2
    for i in range(0, 16, 4):
        a += block[(i+1 ) & 15]; a += (c ^ (d & (b ^ c))); a += md5_consts[i+0+16]; a = rotl(a,  5); a += b;
        d += block[(i+6 ) & 15]; d += (b ^ (c & (a ^ b))); d += md5_consts[i+1+16]; d = rotl(d,  9); d += a;
        c += block[(i+11) & 15]; c += (a ^ (b & (d ^ a))); c += md5_consts[i+2+16]; c = rotl(c, 14); c += d;
        b += block[(i+0 ) & 15]; b += (d ^ (a & (c ^ d))); b += md5_consts[i+3+16]; b = rotl(b, 20); b += c;

	# Round 3
    for i,const_i in zip([0, -4, -8, -12], [0, 4, 8, 12]):
        a += block[(i+5 +16) & 15]; a += (b ^ c ^ d); a += md5_consts[const_i+0+32]; a = rotl(a,  4); a += b;
        d += block[(i+8 +16) & 15]; d += (a ^ b ^ c); d += md5_consts[const_i+1+32]; d = rotl(d, 11); d += a;
        c += block[(i+11+16) & 15]; c += (d ^ a ^ b); c += md5_consts[const_i+2+32]; c = rotl(c, 16); c += d;
        b += block[(i+14+16) & 15]; b += (c ^ d ^ a); b += md5_consts[const_i+3+32]; b = rotl(b, 23); b += c;

	# Round 4
    for i,const_i in zip([0, 12, 24, 36], [0, 4, 8, 12]):
        a += block[(i+0 ) & 15]; a += (c ^ (b | ~d)); a += md5_consts[const_i+0+48]; a = rotl(a,  6); a += b;
        d += block[(i+7 ) & 15]; d += (b ^ (a | ~c)); d += md5_consts[const_i+1+48]; d = rotl(d, 10); d += a;
        c += block[(i+14) & 15]; c += (a ^ (d | ~b)); c += md5_consts[const_i+2+48]; c = rotl(c, 15); c += d;
        b += block[(i+5 ) & 15]; b += (d ^ (c | ~a)); b += md5_consts[const_i+3+48]; b = rotl(b, 21); b += c;
        
    # Save state
    state[0] += a;
    state[1] += b;
    state[2] += c;
    state[3] += d;
    
# Define targets
md5_block.targets  = [Target.PLAIN_C, Target.SSE2, Target.AVX, Target.AVX2]
md5_block_.targets = [Target.AVX512]
md5_block.parallelization_factor [Target.SSE2  ] = [2, 3, 4]
md5_block.parallelization_factor [Target.AVX   ] = [2, 3, 4]
md5_block.parallelization_factor [Target.AVX2  ] = [2, 3, 4]
md5_block_.parallelization_factor[Target.AVX512] = [2, 3, 4]
generate_code()
