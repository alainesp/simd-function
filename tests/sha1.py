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
    A, B, C, D, E = state[0], state[1], state[2], state[3], state[4]
    W0 , W1 , W2 , W3  = W[ 0], W[ 1], W[ 2], W[ 3]
    W4 , W5 , W6 , W7  = W[ 4], W[ 5], W[ 6], W[ 7]
    W8 , W9 , W10, W11 = W[ 8], W[ 9], W[10], W[11]
    W12, W13, W14, W15 = W[12], W[13], W[14], W[15]

    # Round 1
    E += rotl(A, 5) + (D ^ (B & (C ^ D))) + 0x5a827999 + W0 ; B = rotl(B, 30);
    D += rotl(E, 5) + (C ^ (A & (B ^ C))) + 0x5a827999 + W1 ; A = rotl(A, 30);
    C += rotl(D, 5) + (B ^ (E & (A ^ B))) + 0x5a827999 + W2 ; E = rotl(E, 30);
    B += rotl(C, 5) + (A ^ (D & (E ^ A))) + 0x5a827999 + W3 ; D = rotl(D, 30);
    A += rotl(B, 5) + (E ^ (C & (D ^ E))) + 0x5a827999 + W4 ; C = rotl(C, 30);
    E += rotl(A, 5) + (D ^ (B & (C ^ D))) + 0x5a827999 + W5 ; B = rotl(B, 30);
    D += rotl(E, 5) + (C ^ (A & (B ^ C))) + 0x5a827999 + W6 ; A = rotl(A, 30);
    C += rotl(D, 5) + (B ^ (E & (A ^ B))) + 0x5a827999 + W7 ; E = rotl(E, 30);
    B += rotl(C, 5) + (A ^ (D & (E ^ A))) + 0x5a827999 + W8 ; D = rotl(D, 30);
    A += rotl(B, 5) + (E ^ (C & (D ^ E))) + 0x5a827999 + W9 ; C = rotl(C, 30);
    E += rotl(A, 5) + (D ^ (B & (C ^ D))) + 0x5a827999 + W10; B = rotl(B, 30);
    D += rotl(E, 5) + (C ^ (A & (B ^ C))) + 0x5a827999 + W11; A = rotl(A, 30);
    C += rotl(D, 5) + (B ^ (E & (A ^ B))) + 0x5a827999 + W12; E = rotl(E, 30);
    B += rotl(C, 5) + (A ^ (D & (E ^ A))) + 0x5a827999 + W13; D = rotl(D, 30);
    A += rotl(B, 5) + (E ^ (C & (D ^ E))) + 0x5a827999 + W14; C = rotl(C, 30);
    E += rotl(A, 5) + (D ^ (B & (C ^ D))) + 0x5a827999 + W15; B = rotl(B, 30);
    W0  ^= W13 ^ W8  ^ W2 ; W0  = rotl(W0 , 1);    D += rotl(E, 5) + (C ^ (A & (B ^ C))) + 0x5a827999 + W0; A = rotl(A, 30);
    W1  ^= W14 ^ W9  ^ W3 ; W1  = rotl(W1 , 1);    C += rotl(D, 5) + (B ^ (E & (A ^ B))) + 0x5a827999 + W1; E = rotl(E, 30);
    W2  ^= W15 ^ W10 ^ W4 ; W2  = rotl(W2 , 1);    B += rotl(C, 5) + (A ^ (D & (E ^ A))) + 0x5a827999 + W2; D = rotl(D, 30);
    W3  ^= W0  ^ W11 ^ W5 ; W3  = rotl(W3 , 1);    A += rotl(B, 5) + (E ^ (C & (D ^ E))) + 0x5a827999 + W3; C = rotl(C, 30);
    
    # Round 2
    W4  ^= W1  ^ W12 ^ W6 ; W4  = rotl(W4 , 1);    E += rotl(A, 5) + (B ^ C ^ D) + 0x6ed9eba1 + W4 ; B = rotl(B, 30);
    W5  ^= W2  ^ W13 ^ W7 ; W5  = rotl(W5 , 1);    D += rotl(E, 5) + (A ^ B ^ C) + 0x6ed9eba1 + W5 ; A = rotl(A, 30);
    W6  ^= W3  ^ W14 ^ W8 ; W6  = rotl(W6 , 1);    C += rotl(D, 5) + (E ^ A ^ B) + 0x6ed9eba1 + W6 ; E = rotl(E, 30);
    W7  ^= W4  ^ W15 ^ W9 ; W7  = rotl(W7 , 1);    B += rotl(C, 5) + (D ^ E ^ A) + 0x6ed9eba1 + W7 ; D = rotl(D, 30);
    W8  ^= W5  ^ W0  ^ W10; W8  = rotl(W8 , 1);    A += rotl(B, 5) + (C ^ D ^ E) + 0x6ed9eba1 + W8 ; C = rotl(C, 30);
    W9  ^= W6  ^ W1  ^ W11; W9  = rotl(W9 , 1);    E += rotl(A, 5) + (B ^ C ^ D) + 0x6ed9eba1 + W9 ; B = rotl(B, 30);
    W10 ^= W7  ^ W2  ^ W12; W10 = rotl(W10, 1);    D += rotl(E, 5) + (A ^ B ^ C) + 0x6ed9eba1 + W10; A = rotl(A, 30);
    W11 ^= W8  ^ W3  ^ W13; W11 = rotl(W11, 1);    C += rotl(D, 5) + (E ^ A ^ B) + 0x6ed9eba1 + W11; E = rotl(E, 30);
    W12 ^= W9  ^ W4  ^ W14; W12 = rotl(W12, 1);    B += rotl(C, 5) + (D ^ E ^ A) + 0x6ed9eba1 + W12; D = rotl(D, 30);
    W13 ^= W10 ^ W5  ^ W15; W13 = rotl(W13, 1);    A += rotl(B, 5) + (C ^ D ^ E) + 0x6ed9eba1 + W13; C = rotl(C, 30);
    W14 ^= W11 ^ W6  ^ W0 ; W14 = rotl(W14, 1);    E += rotl(A, 5) + (B ^ C ^ D) + 0x6ed9eba1 + W14; B = rotl(B, 30);
    W15 ^= W12 ^ W7  ^ W1 ; W15 = rotl(W15, 1);    D += rotl(E, 5) + (A ^ B ^ C) + 0x6ed9eba1 + W15; A = rotl(A, 30);
    W0  ^= W13 ^ W8  ^ W2 ; W0  = rotl(W0 , 1);    C += rotl(D, 5) + (E ^ A ^ B) + 0x6ed9eba1 + W0 ; E = rotl(E, 30);
    W1  ^= W14 ^ W9  ^ W3 ; W1  = rotl(W1 , 1);    B += rotl(C, 5) + (D ^ E ^ A) + 0x6ed9eba1 + W1 ; D = rotl(D, 30);
    W2  ^= W15 ^ W10 ^ W4 ; W2  = rotl(W2 , 1);    A += rotl(B, 5) + (C ^ D ^ E) + 0x6ed9eba1 + W2 ; C = rotl(C, 30);
    W3  ^= W0  ^ W11 ^ W5 ; W3  = rotl(W3 , 1);    E += rotl(A, 5) + (B ^ C ^ D) + 0x6ed9eba1 + W3 ; B = rotl(B, 30);
    W4  ^= W1  ^ W12 ^ W6 ; W4  = rotl(W4 , 1);    D += rotl(E, 5) + (A ^ B ^ C) + 0x6ed9eba1 + W4 ; A = rotl(A, 30);
    W5  ^= W2  ^ W13 ^ W7 ; W5  = rotl(W5 , 1);    C += rotl(D, 5) + (E ^ A ^ B) + 0x6ed9eba1 + W5 ; E = rotl(E, 30);
    W6  ^= W3  ^ W14 ^ W8 ; W6  = rotl(W6 , 1);    B += rotl(C, 5) + (D ^ E ^ A) + 0x6ed9eba1 + W6 ; D = rotl(D, 30);
    W7  ^= W4  ^ W15 ^ W9 ; W7  = rotl(W7 , 1);    A += rotl(B, 5) + (C ^ D ^ E) + 0x6ed9eba1 + W7 ; C = rotl(C, 30);
    
    # Round 3
    W8  ^= W5  ^ W0  ^ W10; W8  = rotl(W8 , 1);    E += rotl(A, 5) + ((B & C) | (D & (B | C))) + 0x8F1BBCDC + W8 ; B = rotl(B, 30);
    W9  ^= W6  ^ W1  ^ W11; W9  = rotl(W9 , 1);    D += rotl(E, 5) + ((A & B) | (C & (A | B))) + 0x8F1BBCDC + W9 ; A = rotl(A, 30);
    W10 ^= W7  ^ W2  ^ W12; W10 = rotl(W10, 1);    C += rotl(D, 5) + ((E & A) | (B & (E | A))) + 0x8F1BBCDC + W10; E = rotl(E, 30);
    W11 ^= W8  ^ W3  ^ W13; W11 = rotl(W11, 1);    B += rotl(C, 5) + ((D & E) | (A & (D | E))) + 0x8F1BBCDC + W11; D = rotl(D, 30);
    W12 ^= W9  ^ W4  ^ W14; W12 = rotl(W12, 1);    A += rotl(B, 5) + ((C & D) | (E & (C | D))) + 0x8F1BBCDC + W12; C = rotl(C, 30);
    W13 ^= W10 ^ W5  ^ W15; W13 = rotl(W13, 1);    E += rotl(A, 5) + ((B & C) | (D & (B | C))) + 0x8F1BBCDC + W13; B = rotl(B, 30);
    W14 ^= W11 ^ W6  ^ W0 ; W14 = rotl(W14, 1);    D += rotl(E, 5) + ((A & B) | (C & (A | B))) + 0x8F1BBCDC + W14; A = rotl(A, 30);
    W15 ^= W12 ^ W7  ^ W1 ; W15 = rotl(W15, 1);    C += rotl(D, 5) + ((E & A) | (B & (E | A))) + 0x8F1BBCDC + W15; E = rotl(E, 30);
    W0  ^= W13 ^ W8  ^ W2 ; W0  = rotl(W0 , 1);    B += rotl(C, 5) + ((D & E) | (A & (D | E))) + 0x8F1BBCDC + W0 ; D = rotl(D, 30);
    W1  ^= W14 ^ W9  ^ W3 ; W1  = rotl(W1 , 1);    A += rotl(B, 5) + ((C & D) | (E & (C | D))) + 0x8F1BBCDC + W1 ; C = rotl(C, 30);
    W2  ^= W15 ^ W10 ^ W4 ; W2  = rotl(W2 , 1);    E += rotl(A, 5) + ((B & C) | (D & (B | C))) + 0x8F1BBCDC + W2 ; B = rotl(B, 30);
    W3  ^= W0  ^ W11 ^ W5 ; W3  = rotl(W3 , 1);    D += rotl(E, 5) + ((A & B) | (C & (A | B))) + 0x8F1BBCDC + W3 ; A = rotl(A, 30);
    W4  ^= W1  ^ W12 ^ W6 ; W4  = rotl(W4 , 1);    C += rotl(D, 5) + ((E & A) | (B & (E | A))) + 0x8F1BBCDC + W4 ; E = rotl(E, 30);
    W5  ^= W2  ^ W13 ^ W7 ; W5  = rotl(W5 , 1);    B += rotl(C, 5) + ((D & E) | (A & (D | E))) + 0x8F1BBCDC + W5 ; D = rotl(D, 30);
    W6  ^= W3  ^ W14 ^ W8 ; W6  = rotl(W6 , 1);    A += rotl(B, 5) + ((C & D) | (E & (C | D))) + 0x8F1BBCDC + W6 ; C = rotl(C, 30);
    W7  ^= W4  ^ W15 ^ W9 ; W7  = rotl(W7 , 1);    E += rotl(A, 5) + ((B & C) | (D & (B | C))) + 0x8F1BBCDC + W7 ; B = rotl(B, 30);
    W8  ^= W5  ^ W0  ^ W10; W8  = rotl(W8 , 1);    D += rotl(E, 5) + ((A & B) | (C & (A | B))) + 0x8F1BBCDC + W8 ; A = rotl(A, 30);
    W9  ^= W6  ^ W1  ^ W11; W9  = rotl(W9 , 1);    C += rotl(D, 5) + ((E & A) | (B & (E | A))) + 0x8F1BBCDC + W9 ; E = rotl(E, 30);
    W10 ^= W7  ^ W2  ^ W12; W10 = rotl(W10, 1);    B += rotl(C, 5) + ((D & E) | (A & (D | E))) + 0x8F1BBCDC + W10; D = rotl(D, 30);
    W11 ^= W8  ^ W3  ^ W13; W11 = rotl(W11, 1);    A += rotl(B, 5) + ((C & D) | (E & (C | D))) + 0x8F1BBCDC + W11; C = rotl(C, 30);
    
    # Round 4
    W12 ^= W9  ^ W4  ^ W14; W12 = rotl(W12, 1);    E += rotl(A, 5) + (B ^ C ^ D) + 0xCA62C1D6 + W12; B = rotl(B, 30);
    W13 ^= W10 ^ W5  ^ W15; W13 = rotl(W13, 1);    D += rotl(E, 5) + (A ^ B ^ C) + 0xCA62C1D6 + W13; A = rotl(A, 30);
    W14 ^= W11 ^ W6  ^ W0 ; W14 = rotl(W14, 1);    C += rotl(D, 5) + (E ^ A ^ B) + 0xCA62C1D6 + W14; E = rotl(E, 30);
    W15 ^= W12 ^ W7  ^ W1 ; W15 = rotl(W15, 1);    B += rotl(C, 5) + (D ^ E ^ A) + 0xCA62C1D6 + W15; D = rotl(D, 30);
    W0  ^= W13 ^ W8  ^ W2 ; W0  = rotl(W0 , 1);    A += rotl(B, 5) + (C ^ D ^ E) + 0xCA62C1D6 + W0 ; C = rotl(C, 30);
    W1  ^= W14 ^ W9  ^ W3 ; W1  = rotl(W1 , 1);    E += rotl(A, 5) + (B ^ C ^ D) + 0xCA62C1D6 + W1 ; B = rotl(B, 30);
    W2  ^= W15 ^ W10 ^ W4 ; W2  = rotl(W2 , 1);    D += rotl(E, 5) + (A ^ B ^ C) + 0xCA62C1D6 + W2 ; A = rotl(A, 30);
    W3  ^= W0  ^ W11 ^ W5 ; W3  = rotl(W3 , 1);    C += rotl(D, 5) + (E ^ A ^ B) + 0xCA62C1D6 + W3 ; E = rotl(E, 30);
    W4  ^= W1  ^ W12 ^ W6 ; W4  = rotl(W4 , 1);    B += rotl(C, 5) + (D ^ E ^ A) + 0xCA62C1D6 + W4 ; D = rotl(D, 30);
    W5  ^= W2  ^ W13 ^ W7 ; W5  = rotl(W5 , 1);    A += rotl(B, 5) + (C ^ D ^ E) + 0xCA62C1D6 + W5 ; C = rotl(C, 30);
    W6  ^= W3  ^ W14 ^ W8 ; W6  = rotl(W6 , 1);    E += rotl(A, 5) + (B ^ C ^ D) + 0xCA62C1D6 + W6 ; B = rotl(B, 30);
    W7  ^= W4  ^ W15 ^ W9 ; W7  = rotl(W7 , 1);    D += rotl(E, 5) + (A ^ B ^ C) + 0xCA62C1D6 + W7 ; A = rotl(A, 30);
    W8  ^= W5  ^ W0  ^ W10; W8  = rotl(W8 , 1);    C += rotl(D, 5) + (E ^ A ^ B) + 0xCA62C1D6 + W8 ; E = rotl(E, 30);
    W9  ^= W6  ^ W1  ^ W11; W9  = rotl(W9 , 1);    B += rotl(C, 5) + (D ^ E ^ A) + 0xCA62C1D6 + W9 ; D = rotl(D, 30);
    W10 ^= W7  ^ W2  ^ W12; W10 = rotl(W10, 1);    A += rotl(B, 5) + (C ^ D ^ E) + 0xCA62C1D6 + W10; C = rotl(C, 30);
    W11 ^= W8  ^ W3  ^ W13; W11 = rotl(W11, 1);    E += rotl(A, 5) + (B ^ C ^ D) + 0xCA62C1D6 + W11; B = rotl(B, 30);
    W12 ^= W9  ^ W4  ^ W14; W12 = rotl(W12, 1);    D += rotl(E, 5) + (A ^ B ^ C) + 0xCA62C1D6 + W12; A = rotl(A, 30);
    W13 ^= W10 ^ W5  ^ W15; W13 = rotl(W13, 1);    C += rotl(D, 5) + (E ^ A ^ B) + 0xCA62C1D6 + W13; E = rotl(E, 30);
    W14 ^= W11 ^ W6  ^ W0 ; W14 = rotl(W14, 1);    B += rotl(C, 5) + (D ^ E ^ A) + 0xCA62C1D6 + W14; D = rotl(D, 30);
    W15 ^= W12 ^ W7  ^ W1 ; W15 = rotl(W15, 1);    A += rotl(B, 5) + (C ^ D ^ E) + 0xCA62C1D6 + W15; C = rotl(C, 30);

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
sha1_block.parallelization_factor [Target.SSE2  ] = [1, 2, 3]
sha1_block.parallelization_factor [Target.AVX   ] = [1, 2, 3]
sha1_block.parallelization_factor [Target.AVX2  ] = [1, 2, 3]
sha1_block_.parallelization_factor[Target.AVX512] = [1, 2, 3, 4]
generate_code()
