#######################################################
# SHA1 - Secure Hash Algorithm 1
#######################################################

import sys
sys.path.append('src/')
from simd_function import *

state = VectorMemoryArray(uint32_t, 5)  # The state
W     = VectorMemoryArray(uint32_t, 16) # The message

## <summary>
## SHA1 compress block
## </summary>
## <param name="state">The SHA1 state</param>
## <param name="block">The message to compress</param>
with Function(void)(state, W) as sha1_block:
    # Load state
    A = state[0]
    B = state[1]
    C = state[2]
    D = state[3]
    E = state[4]

    # Round 1
    E += rotl(A, 5) + (D ^ (B & (C ^ D))) + 0x5a827999 + W[0 ]; B = rotl(B, 30);
    D += rotl(E, 5) + (C ^ (A & (B ^ C))) + 0x5a827999 + W[1 ]; A = rotl(A, 30);
    C += rotl(D, 5) + (B ^ (E & (A ^ B))) + 0x5a827999 + W[2 ]; E = rotl(E, 30);
    B += rotl(C, 5) + (A ^ (D & (E ^ A))) + 0x5a827999 + W[3 ]; D = rotl(D, 30);
    A += rotl(B, 5) + (E ^ (C & (D ^ E))) + 0x5a827999 + W[4 ]; C = rotl(C, 30);
    E += rotl(A, 5) + (D ^ (B & (C ^ D))) + 0x5a827999 + W[5 ]; B = rotl(B, 30);
    D += rotl(E, 5) + (C ^ (A & (B ^ C))) + 0x5a827999 + W[6 ]; A = rotl(A, 30);
    C += rotl(D, 5) + (B ^ (E & (A ^ B))) + 0x5a827999 + W[7 ]; E = rotl(E, 30);
    B += rotl(C, 5) + (A ^ (D & (E ^ A))) + 0x5a827999 + W[8 ]; D = rotl(D, 30);
    A += rotl(B, 5) + (E ^ (C & (D ^ E))) + 0x5a827999 + W[9 ]; C = rotl(C, 30);
    E += rotl(A, 5) + (D ^ (B & (C ^ D))) + 0x5a827999 + W[10]; B = rotl(B, 30);
    D += rotl(E, 5) + (C ^ (A & (B ^ C))) + 0x5a827999 + W[11]; A = rotl(A, 30);
    C += rotl(D, 5) + (B ^ (E & (A ^ B))) + 0x5a827999 + W[12]; E = rotl(E, 30);
    B += rotl(C, 5) + (A ^ (D & (E ^ A))) + 0x5a827999 + W[13]; D = rotl(D, 30);
    A += rotl(B, 5) + (E ^ (C & (D ^ E))) + 0x5a827999 + W[14]; C = rotl(C, 30);
    E += rotl(A, 5) + (D ^ (B & (C ^ D))) + 0x5a827999 + W[15]; B = rotl(B, 30);
    for i in range(16):
        t = W[i] ^ W[(i-3+16) & 15] ^ W[(i-8+16) & 15] ^ W[(i-14+16) & 15 ]
        W[i] = rotl(t, 1)
    D += rotl(E, 5) + (C ^ (A & (B ^ C))) + 0x5a827999 + W[0]; A = rotl(A, 30);
    C += rotl(D, 5) + (B ^ (E & (A ^ B))) + 0x5a827999 + W[1]; E = rotl(E, 30);
    B += rotl(C, 5) + (A ^ (D & (E ^ A))) + 0x5a827999 + W[2]; D = rotl(D, 30);
    A += rotl(B, 5) + (E ^ (C & (D ^ E))) + 0x5a827999 + W[3]; C = rotl(C, 30);

    # Round 2
    E += rotl(A, 5) + (B ^ C ^ D) + 0x6ed9eba1 + W[4 ]; B = rotl(B, 30);
    D += rotl(E, 5) + (A ^ B ^ C) + 0x6ed9eba1 + W[5 ]; A = rotl(A, 30);
    C += rotl(D, 5) + (E ^ A ^ B) + 0x6ed9eba1 + W[6 ]; E = rotl(E, 30);
    B += rotl(C, 5) + (D ^ E ^ A) + 0x6ed9eba1 + W[7 ]; D = rotl(D, 30);
    A += rotl(B, 5) + (C ^ D ^ E) + 0x6ed9eba1 + W[8 ]; C = rotl(C, 30);
    E += rotl(A, 5) + (B ^ C ^ D) + 0x6ed9eba1 + W[9 ]; B = rotl(B, 30);
    D += rotl(E, 5) + (A ^ B ^ C) + 0x6ed9eba1 + W[10]; A = rotl(A, 30);
    C += rotl(D, 5) + (E ^ A ^ B) + 0x6ed9eba1 + W[11]; E = rotl(E, 30);
    B += rotl(C, 5) + (D ^ E ^ A) + 0x6ed9eba1 + W[12]; D = rotl(D, 30);
    A += rotl(B, 5) + (C ^ D ^ E) + 0x6ed9eba1 + W[13]; C = rotl(C, 30);
    E += rotl(A, 5) + (B ^ C ^ D) + 0x6ed9eba1 + W[14]; B = rotl(B, 30);
    D += rotl(E, 5) + (A ^ B ^ C) + 0x6ed9eba1 + W[15]; A = rotl(A, 30);
    for i in range(16):
        t = W[i] ^ W[(i-3+16) & 15] ^ W[(i-8+16) & 15] ^ W[(i-14+16) & 15 ]
        W[i] = rotl(t, 1)
    C += rotl(D, 5) + (E ^ A ^ B) + 0x6ed9eba1 + W[0 ]; E = rotl(E, 30);
    B += rotl(C, 5) + (D ^ E ^ A) + 0x6ed9eba1 + W[1 ]; D = rotl(D, 30);
    A += rotl(B, 5) + (C ^ D ^ E) + 0x6ed9eba1 + W[2 ]; C = rotl(C, 30);
    E += rotl(A, 5) + (B ^ C ^ D) + 0x6ed9eba1 + W[3 ]; B = rotl(B, 30);
    D += rotl(E, 5) + (A ^ B ^ C) + 0x6ed9eba1 + W[4 ]; A = rotl(A, 30);
    C += rotl(D, 5) + (E ^ A ^ B) + 0x6ed9eba1 + W[5 ]; E = rotl(E, 30);
    B += rotl(C, 5) + (D ^ E ^ A) + 0x6ed9eba1 + W[6 ]; D = rotl(D, 30);
    A += rotl(B, 5) + (C ^ D ^ E) + 0x6ed9eba1 + W[7 ]; C = rotl(C, 30);
    
    # Round 3
    E += rotl(A, 5) + ((B & C) | (D & (B | C))) + 0x8F1BBCDC + W[ 8]; B = rotl(B, 30);
    D += rotl(E, 5) + ((A & B) | (C & (A | B))) + 0x8F1BBCDC + W[ 9]; A = rotl(A, 30);
    C += rotl(D, 5) + ((E & A) | (B & (E | A))) + 0x8F1BBCDC + W[10]; E = rotl(E, 30);
    B += rotl(C, 5) + ((D & E) | (A & (D | E))) + 0x8F1BBCDC + W[11]; D = rotl(D, 30);
    A += rotl(B, 5) + ((C & D) | (E & (C | D))) + 0x8F1BBCDC + W[12]; C = rotl(C, 30);
    E += rotl(A, 5) + ((B & C) | (D & (B | C))) + 0x8F1BBCDC + W[13]; B = rotl(B, 30);
    D += rotl(E, 5) + ((A & B) | (C & (A | B))) + 0x8F1BBCDC + W[14]; A = rotl(A, 30);
    C += rotl(D, 5) + ((E & A) | (B & (E | A))) + 0x8F1BBCDC + W[15]; E = rotl(E, 30);
    for i in range(16):
        t = W[i] ^ W[(i-3+16) & 15] ^ W[(i-8+16) & 15] ^ W[(i-14+16) & 15 ]
        W[i] = rotl(t, 1)
    B += rotl(C, 5) + ((D & E) | (A & (D | E))) + 0x8F1BBCDC + W[ 0]; D = rotl(D, 30);
    A += rotl(B, 5) + ((C & D) | (E & (C | D))) + 0x8F1BBCDC + W[ 1]; C = rotl(C, 30);
    E += rotl(A, 5) + ((B & C) | (D & (B | C))) + 0x8F1BBCDC + W[ 2]; B = rotl(B, 30);
    D += rotl(E, 5) + ((A & B) | (C & (A | B))) + 0x8F1BBCDC + W[ 3]; A = rotl(A, 30);
    C += rotl(D, 5) + ((E & A) | (B & (E | A))) + 0x8F1BBCDC + W[ 4]; E = rotl(E, 30);
    B += rotl(C, 5) + ((D & E) | (A & (D | E))) + 0x8F1BBCDC + W[ 5]; D = rotl(D, 30);
    A += rotl(B, 5) + ((C & D) | (E & (C | D))) + 0x8F1BBCDC + W[ 6]; C = rotl(C, 30);
    E += rotl(A, 5) + ((B & C) | (D & (B | C))) + 0x8F1BBCDC + W[ 7]; B = rotl(B, 30);
    D += rotl(E, 5) + ((A & B) | (C & (A | B))) + 0x8F1BBCDC + W[ 8]; A = rotl(A, 30);
    C += rotl(D, 5) + ((E & A) | (B & (E | A))) + 0x8F1BBCDC + W[ 9]; E = rotl(E, 30);
    B += rotl(C, 5) + ((D & E) | (A & (D | E))) + 0x8F1BBCDC + W[10]; D = rotl(D, 30);
    A += rotl(B, 5) + ((C & D) | (E & (C | D))) + 0x8F1BBCDC + W[11]; C = rotl(C, 30);

    # Round 4
    E += rotl(A, 5) + (B ^ C ^ D) + 0xCA62C1D6 + W[12]; B = rotl(B, 30);
    D += rotl(E, 5) + (A ^ B ^ C) + 0xCA62C1D6 + W[13]; A = rotl(A, 30);
    C += rotl(D, 5) + (E ^ A ^ B) + 0xCA62C1D6 + W[14]; E = rotl(E, 30);
    B += rotl(C, 5) + (D ^ E ^ A) + 0xCA62C1D6 + W[15]; D = rotl(D, 30);
    for i in range(16):
        t = W[i] ^ W[(i-3+16) & 15] ^ W[(i-8+16) & 15] ^ W[(i-14+16) & 15 ]
        W[i] = rotl(t, 1)
    A += rotl(B, 5) + (C ^ D ^ E) + 0xCA62C1D6 + W[ 0]; C = rotl(C, 30);
    E += rotl(A, 5) + (B ^ C ^ D) + 0xCA62C1D6 + W[ 1]; B = rotl(B, 30);
    D += rotl(E, 5) + (A ^ B ^ C) + 0xCA62C1D6 + W[ 2]; A = rotl(A, 30);
    C += rotl(D, 5) + (E ^ A ^ B) + 0xCA62C1D6 + W[ 3]; E = rotl(E, 30);
    B += rotl(C, 5) + (D ^ E ^ A) + 0xCA62C1D6 + W[ 4]; D = rotl(D, 30);
    A += rotl(B, 5) + (C ^ D ^ E) + 0xCA62C1D6 + W[ 5]; C = rotl(C, 30);
    E += rotl(A, 5) + (B ^ C ^ D) + 0xCA62C1D6 + W[ 6]; B = rotl(B, 30);
    D += rotl(E, 5) + (A ^ B ^ C) + 0xCA62C1D6 + W[ 7]; A = rotl(A, 30);
    C += rotl(D, 5) + (E ^ A ^ B) + 0xCA62C1D6 + W[ 8]; E = rotl(E, 30);
    B += rotl(C, 5) + (D ^ E ^ A) + 0xCA62C1D6 + W[ 9]; D = rotl(D, 30);
    A += rotl(B, 5) + (C ^ D ^ E) + 0xCA62C1D6 + W[10]; C = rotl(C, 30);
    E += rotl(A, 5) + (B ^ C ^ D) + 0xCA62C1D6 + W[11]; B = rotl(B, 30);
    D += rotl(E, 5) + (A ^ B ^ C) + 0xCA62C1D6 + W[12]; A = rotl(A, 30);
    C += rotl(D, 5) + (E ^ A ^ B) + 0xCA62C1D6 + W[13]; E = rotl(E, 30);
    B += rotl(C, 5) + (D ^ E ^ A) + 0xCA62C1D6 + W[14]; D = rotl(D, 30);
    A += rotl(B, 5) + (C ^ D ^ E) + 0xCA62C1D6 + W[15]; C = rotl(C, 30);

    # Save state
    state[0] += A
    state[1] += B
    state[2] += C
    state[3] += D
    state[4] += E

with Function(void)(state, W) as sha1_block_:
    pass
    # # Load state
    # a = state[0]
    # b = state[1]
    # c = state[2]
    # d = state[3]

    # # Round 1
    # for i in range(0, 16, 4):
    #     a += block[i + 0]; t = ternary_logic(d, c, b, 0xd8); a += md5_consts[const_i + 0]; a += t; a = rotl(a,  7); a += b;
    #     d += block[i + 1]; t = ternary_logic(c, b, a, 0xd8); d += md5_consts[const_i + 1]; d += t; d = rotl(d, 12); d += a;
    #     c += block[i + 2]; t = ternary_logic(b, a, d, 0xd8); c += md5_consts[const_i + 2]; c += t; c = rotl(c, 17); c += d;
    #     b += block[i + 3]; t = ternary_logic(a, d, c, 0xd8); b += md5_consts[const_i + 3]; b += t; b = rotl(b, 22); b += c;
    #     const_i += 4

	# # Round 2
    # for i in range(0, 16, 4):
    #     a += block[(i +  1) & 15]; t = ternary_logic(c, b, d, 0xd8); a += md5_consts[const_i + 0]; a += t; a = rotl(a,  5); a += b;
    #     d += block[(i +  6) & 15]; t = ternary_logic(b, a, c, 0xd8); d += md5_consts[const_i + 1]; d += t; d = rotl(d,  9); d += a;
    #     c += block[(i + 11) & 15]; t = ternary_logic(a, d, b, 0xd8); c += md5_consts[const_i + 2]; c += t; c = rotl(c, 14); c += d;
    #     b += block[(i +  0) & 15]; t = ternary_logic(d, c, a, 0xd8); b += md5_consts[const_i + 3]; b += t; b = rotl(b, 20); b += c;
    #     const_i += 4

	# # Round 3
    # for i in [0, -4, -8, -12]:
    #     a += block[(i +  5 + 16) & 15]; t = ternary_logic(d, c, b, 0x96); a += md5_consts[const_i + 0]; a += t; a = rotl(a,  4); a += b;
    #     d += block[(i +  8 + 16) & 15]; t = ternary_logic(c, b, a, 0x96); d += md5_consts[const_i + 1]; d += t; d = rotl(d, 11); d += a;
    #     c += block[(i + 11 + 16) & 15]; t = ternary_logic(b, a, d, 0x96); c += md5_consts[const_i + 2]; c += t; c = rotl(c, 16); c += d;
    #     b += block[(i + 14 + 16) & 15]; t = ternary_logic(a, d, c, 0x96); b += md5_consts[const_i + 3]; b += t; b = rotl(b, 23); b += c;
    #     const_i += 4

	# # Round 4
    # for i in [0, 12, 24, 36]:
    #     a += block[(i +  0) & 15]; t = ternary_logic(b, c, d, 0x39); a += md5_consts[const_i + 0]; a += t; a = rotl(a,  6); a += b;
    #     d += block[(i +  7) & 15]; t = ternary_logic(a, b, c, 0x39); d += md5_consts[const_i + 1]; d += t; d = rotl(d, 10); d += a;
    #     c += block[(i + 14) & 15]; t = ternary_logic(d, a, b, 0x39); c += md5_consts[const_i + 2]; c += t; c = rotl(c, 15); c += d;
    #     b += block[(i +  5) & 15]; t = ternary_logic(c, d, a, 0x39); b += md5_consts[const_i + 3]; b += t; b = rotl(b, 21); b += c;
    #     const_i += 4
        
    # # Save state
    # state[0] += a
    # state[1] += b
    # state[2] += c
    # state[3] += d
    
# Define targets
sha1_block.targets  = [Target.AVX2]#Target.PLAIN_C, Target.SSE2, Target.AVX, Target.AVX2]
sha1_block_.targets = [Target.AVX512]
sha1_block.parallelization_factor [Target.SSE2  ] = [1, 2, 3, 4]
sha1_block.parallelization_factor [Target.AVX   ] = [1, 2, 3, 4]
sha1_block.parallelization_factor [Target.AVX2  ] = [1, 2, 3, 4]
sha1_block_.parallelization_factor[Target.AVX512] = [1, 2, 3, 4]
generate_code()
