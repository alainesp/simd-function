#######################################################
# SHA512 - Secure Hash Algorithm 2
#######################################################

import sys
sys.path.append('src/')
from simd_function import *

state = VectorMemoryArray(uint64_t, 8)  # The state
W     = VectorMemoryArray(uint64_t, 16) # The message
sha512_consts = [
    0x428A2F98D728AE22, 0x7137449123EF65CD, 0xB5C0FBCFEC4D3B2F, 0xE9B5DBA58189DBBC, 0x3956C25BF348B538, 0x59F111F1B605D019, 0x923F82A4AF194F9B, 0xAB1C5ED5DA6D8118,
    0xD807AA98A3030242, 0x12835B0145706FBE, 0x243185BE4EE4B28C, 0x550C7DC3D5FFB4E2, 0x72BE5D74F27B896F, 0x80DEB1FE3B1696B1, 0x9BDC06A725C71235, 0xC19BF174CF692694,

    0xE49B69C19EF14AD2, 0xEFBE4786384F25E3, 0x0FC19DC68B8CD5B5, 0x240CA1CC77AC9C65, 0x2DE92C6F592B0275, 0x4A7484AA6EA6E483, 0x5CB0A9DCBD41FBD4, 0x76F988DA831153B5,
    0x983E5152EE66DFAB, 0xA831C66D2DB43210, 0xB00327C898FB213F, 0xBF597FC7BEEF0EE4, 0xC6E00BF33DA88FC2, 0xD5A79147930AA725, 0x06CA6351E003826F, 0x142929670A0E6E70,

    0x27B70A8546D22FFC, 0x2E1B21385C26C926, 0x4D2C6DFC5AC42AED, 0x53380D139D95B3DF, 0x650A73548BAF63DE, 0x766A0ABB3C77B2A8, 0x81C2C92E47EDAEE6, 0x92722C851482353B,
    0xA2BFE8A14CF10364, 0xA81A664BBC423001, 0xC24B8B70D0F89791, 0xC76C51A30654BE30, 0xD192E819D6EF5218, 0xD69906245565A910, 0xF40E35855771202A, 0x106AA07032BBD1B8,
    
    0x19A4C116B8D2D0C8, 0x1E376C085141AB53, 0x2748774CDF8EEB99, 0x34B0BCB5E19B48A8, 0x391C0CB3C5C95A63, 0x4ED8AA4AE3418ACB, 0x5B9CCA4F7763E373, 0x682E6FF3D6B2B8A3,
    0x748F82EE5DEFB2FC, 0x78A5636F43172F60, 0x84C87814A1F0AB72, 0x8CC702081A6439EC, 0x90BEFFFA23631E28, 0xA4506CEBDE82BDE9, 0xBEF9A3F7B2C67915, 0xC67178F2E372532B,

    0xCA273ECEEA26619C, 0xD186B8C721C0C207, 0xEADA7DD6CDE0EB1E, 0xF57D4F7FEE6ED178, 0x06F067AA72176FBA, 0x0A637DC5A2C898A6, 0x113F9804BEF90DAE, 0x1B710B35131C471B,
    0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc, 0x431d67c49c100d4c, 0x4cc5d4becb3e42b6, 0x597f299cfc657e2a, 0x5fcb6fab3ad6faec, 0x6c44198c4a475817,
]

## <summary>
## SHA512 compress block
## </summary>
## <param name="state">The SHA512 state</param>
## <param name="block">The message to compress</param>
with Function(void)(state, W) as sha512_block:
    # Load state
    A, B, C, D, E, F, G, H = state[0], state[1], state[2], state[3], state[4], state[5], state[6], state[7]
    W0 , W1 , W2 , W3  = W[ 0], W[ 1], W[ 2], W[ 3]
    W4 , W5 , W6 , W7  = W[ 4], W[ 5], W[ 6], W[ 7]
    W8 , W9 , W10, W11 = W[ 8], W[ 9], W[10], W[11]
    W12, W13, W14, W15 = W[12], W[13], W[14], W[15]

    # Round 1
    H += (rotl(E, 26) ^ rotl(E, 21) ^ rotl(E, 7))  +  (G ^ (E & (F ^ G)))  +  sha512_consts[ 0] + W0 ;   D += H;   H += (rotl(A, 30) ^ rotl(A, 19) ^ rotl(A, 10))  +  ((A & B) | (C & (A | B)));
    G += (rotl(D, 26) ^ rotl(D, 21) ^ rotl(D, 7))  +  (F ^ (D & (E ^ F)))  +  sha512_consts[ 1] + W1 ;   C += G;   G += (rotl(H, 30) ^ rotl(H, 19) ^ rotl(H, 10))  +  ((H & A) | (B & (H | A)));
    F += (rotl(C, 26) ^ rotl(C, 21) ^ rotl(C, 7))  +  (E ^ (C & (D ^ E)))  +  sha512_consts[ 2] + W2 ;   B += F;   F += (rotl(G, 30) ^ rotl(G, 19) ^ rotl(G, 10))  +  ((G & H) | (A & (G | H)));
    E += (rotl(B, 26) ^ rotl(B, 21) ^ rotl(B, 7))  +  (D ^ (B & (C ^ D)))  +  sha512_consts[ 3] + W3 ;   A += E;   E += (rotl(F, 30) ^ rotl(F, 19) ^ rotl(F, 10))  +  ((F & G) | (H & (F | G)));
    D += (rotl(A, 26) ^ rotl(A, 21) ^ rotl(A, 7))  +  (C ^ (A & (B ^ C)))  +  sha512_consts[ 4] + W4 ;   H += D;   D += (rotl(E, 30) ^ rotl(E, 19) ^ rotl(E, 10))  +  ((E & F) | (G & (E | F)));
    C += (rotl(H, 26) ^ rotl(H, 21) ^ rotl(H, 7))  +  (B ^ (H & (A ^ B)))  +  sha512_consts[ 5] + W5 ;   G += C;   C += (rotl(D, 30) ^ rotl(D, 19) ^ rotl(D, 10))  +  ((D & E) | (F & (D | E)));
    B += (rotl(G, 26) ^ rotl(G, 21) ^ rotl(G, 7))  +  (A ^ (G & (H ^ A)))  +  sha512_consts[ 6] + W6 ;   F += B;   B += (rotl(C, 30) ^ rotl(C, 19) ^ rotl(C, 10))  +  ((C & D) | (E & (C | D)));
    A += (rotl(F, 26) ^ rotl(F, 21) ^ rotl(F, 7))  +  (H ^ (F & (G ^ H)))  +  sha512_consts[ 7] + W7 ;   E += A;   A += (rotl(B, 30) ^ rotl(B, 19) ^ rotl(B, 10))  +  ((B & C) | (D & (B | C)));
    H += (rotl(E, 26) ^ rotl(E, 21) ^ rotl(E, 7))  +  (G ^ (E & (F ^ G)))  +  sha512_consts[ 8] + W8 ;   D += H;   H += (rotl(A, 30) ^ rotl(A, 19) ^ rotl(A, 10))  +  ((A & B) | (C & (A | B)));
    G += (rotl(D, 26) ^ rotl(D, 21) ^ rotl(D, 7))  +  (F ^ (D & (E ^ F)))  +  sha512_consts[ 9] + W9 ;   C += G;   G += (rotl(H, 30) ^ rotl(H, 19) ^ rotl(H, 10))  +  ((H & A) | (B & (H | A)));
    F += (rotl(C, 26) ^ rotl(C, 21) ^ rotl(C, 7))  +  (E ^ (C & (D ^ E)))  +  sha512_consts[10] + W10;   B += F;   F += (rotl(G, 30) ^ rotl(G, 19) ^ rotl(G, 10))  +  ((G & H) | (A & (G | H)));
    E += (rotl(B, 26) ^ rotl(B, 21) ^ rotl(B, 7))  +  (D ^ (B & (C ^ D)))  +  sha512_consts[11] + W11;   A += E;   E += (rotl(F, 30) ^ rotl(F, 19) ^ rotl(F, 10))  +  ((F & G) | (H & (F | G)));
    D += (rotl(A, 26) ^ rotl(A, 21) ^ rotl(A, 7))  +  (C ^ (A & (B ^ C)))  +  sha512_consts[12] + W12;   H += D;   D += (rotl(E, 30) ^ rotl(E, 19) ^ rotl(E, 10))  +  ((E & F) | (G & (E | F)));
    C += (rotl(H, 26) ^ rotl(H, 21) ^ rotl(H, 7))  +  (B ^ (H & (A ^ B)))  +  sha512_consts[13] + W13;   G += C;   C += (rotl(D, 30) ^ rotl(D, 19) ^ rotl(D, 10))  +  ((D & E) | (F & (D | E)));
    B += (rotl(G, 26) ^ rotl(G, 21) ^ rotl(G, 7))  +  (A ^ (G & (H ^ A)))  +  sha512_consts[14] + W14;   F += B;   B += (rotl(C, 30) ^ rotl(C, 19) ^ rotl(C, 10))  +  ((C & D) | (E & (C | D)));
    A += (rotl(F, 26) ^ rotl(F, 21) ^ rotl(F, 7))  +  (H ^ (F & (G ^ H)))  +  sha512_consts[15] + W15;   E += A;   A += (rotl(B, 30) ^ rotl(B, 19) ^ rotl(B, 10))  +  ((B & C) | (D & (B | C)));

    # Round 2-5
    for i in range(16, 80, 16):
        W0  += (rotl(W14, 15) ^ rotl(W14, 13) ^ (W14 >> 10))  +  W9   +  (rotl(W1 , 25) ^ rotl(W1 , 14) ^ (W1  >> 3));   H += (rotl(E, 26) ^ rotl(E, 21) ^ rotl(E, 7))  +  (G ^ (E & (F ^ G)))  +  sha512_consts[i +  0] + W0 ; D += H; H += (rotl(A, 30) ^ rotl(A, 19) ^ rotl(A, 10)) + ((A & B) | (C & (A | B)));
        W1  += (rotl(W15, 15) ^ rotl(W15, 13) ^ (W15 >> 10))  +  W10  +  (rotl(W2 , 25) ^ rotl(W2 , 14) ^ (W2  >> 3));   G += (rotl(D, 26) ^ rotl(D, 21) ^ rotl(D, 7))  +  (F ^ (D & (E ^ F)))  +  sha512_consts[i +  1] + W1 ; C += G; G += (rotl(H, 30) ^ rotl(H, 19) ^ rotl(H, 10)) + ((H & A) | (B & (H | A)));
        W2  += (rotl(W0 , 15) ^ rotl(W0 , 13) ^ (W0  >> 10))  +  W11  +  (rotl(W3 , 25) ^ rotl(W3 , 14) ^ (W3  >> 3));   F += (rotl(C, 26) ^ rotl(C, 21) ^ rotl(C, 7))  +  (E ^ (C & (D ^ E)))  +  sha512_consts[i +  2] + W2 ; B += F; F += (rotl(G, 30) ^ rotl(G, 19) ^ rotl(G, 10)) + ((G & H) | (A & (G | H)));
        W3  += (rotl(W1 , 15) ^ rotl(W1 , 13) ^ (W1  >> 10))  +  W12  +  (rotl(W4 , 25) ^ rotl(W4 , 14) ^ (W4  >> 3));   E += (rotl(B, 26) ^ rotl(B, 21) ^ rotl(B, 7))  +  (D ^ (B & (C ^ D)))  +  sha512_consts[i +  3] + W3 ; A += E; E += (rotl(F, 30) ^ rotl(F, 19) ^ rotl(F, 10)) + ((F & G) | (H & (F | G)));
        W4  += (rotl(W2 , 15) ^ rotl(W2 , 13) ^ (W2  >> 10))  +  W13  +  (rotl(W5 , 25) ^ rotl(W5 , 14) ^ (W5  >> 3));   D += (rotl(A, 26) ^ rotl(A, 21) ^ rotl(A, 7))  +  (C ^ (A & (B ^ C)))  +  sha512_consts[i +  4] + W4 ; H += D; D += (rotl(E, 30) ^ rotl(E, 19) ^ rotl(E, 10)) + ((E & F) | (G & (E | F)));
        W5  += (rotl(W3 , 15) ^ rotl(W3 , 13) ^ (W3  >> 10))  +  W14  +  (rotl(W6 , 25) ^ rotl(W6 , 14) ^ (W6  >> 3));   C += (rotl(H, 26) ^ rotl(H, 21) ^ rotl(H, 7))  +  (B ^ (H & (A ^ B)))  +  sha512_consts[i +  5] + W5 ; G += C; C += (rotl(D, 30) ^ rotl(D, 19) ^ rotl(D, 10)) + ((D & E) | (F & (D | E)));
        W6  += (rotl(W4 , 15) ^ rotl(W4 , 13) ^ (W4  >> 10))  +  W15  +  (rotl(W7 , 25) ^ rotl(W7 , 14) ^ (W7  >> 3));   B += (rotl(G, 26) ^ rotl(G, 21) ^ rotl(G, 7))  +  (A ^ (G & (H ^ A)))  +  sha512_consts[i +  6] + W6 ; F += B; B += (rotl(C, 30) ^ rotl(C, 19) ^ rotl(C, 10)) + ((C & D) | (E & (C | D)));
        W7  += (rotl(W5 , 15) ^ rotl(W5 , 13) ^ (W5  >> 10))  +  W0   +  (rotl(W8 , 25) ^ rotl(W8 , 14) ^ (W8  >> 3));   A += (rotl(F, 26) ^ rotl(F, 21) ^ rotl(F, 7))  +  (H ^ (F & (G ^ H)))  +  sha512_consts[i +  7] + W7 ; E += A; A += (rotl(B, 30) ^ rotl(B, 19) ^ rotl(B, 10)) + ((B & C) | (D & (B | C)));
        W8  += (rotl(W6 , 15) ^ rotl(W6 , 13) ^ (W6  >> 10))  +  W1   +  (rotl(W9 , 25) ^ rotl(W9 , 14) ^ (W9  >> 3));   H += (rotl(E, 26) ^ rotl(E, 21) ^ rotl(E, 7))  +  (G ^ (E & (F ^ G)))  +  sha512_consts[i +  8] + W8 ; D += H; H += (rotl(A, 30) ^ rotl(A, 19) ^ rotl(A, 10)) + ((A & B) | (C & (A | B)));
        W9  += (rotl(W7 , 15) ^ rotl(W7 , 13) ^ (W7  >> 10))  +  W2   +  (rotl(W10, 25) ^ rotl(W10, 14) ^ (W10 >> 3));   G += (rotl(D, 26) ^ rotl(D, 21) ^ rotl(D, 7))  +  (F ^ (D & (E ^ F)))  +  sha512_consts[i +  9] + W9 ; C += G; G += (rotl(H, 30) ^ rotl(H, 19) ^ rotl(H, 10)) + ((H & A) | (B & (H | A)));
        W10 += (rotl(W8 , 15) ^ rotl(W8 , 13) ^ (W8  >> 10))  +  W3   +  (rotl(W11, 25) ^ rotl(W11, 14) ^ (W11 >> 3));   F += (rotl(C, 26) ^ rotl(C, 21) ^ rotl(C, 7))  +  (E ^ (C & (D ^ E)))  +  sha512_consts[i + 10] + W10; B += F; F += (rotl(G, 30) ^ rotl(G, 19) ^ rotl(G, 10)) + ((G & H) | (A & (G | H)));
        W11 += (rotl(W9 , 15) ^ rotl(W9 , 13) ^ (W9  >> 10))  +  W4   +  (rotl(W12, 25) ^ rotl(W12, 14) ^ (W12 >> 3));   E += (rotl(B, 26) ^ rotl(B, 21) ^ rotl(B, 7))  +  (D ^ (B & (C ^ D)))  +  sha512_consts[i + 11] + W11; A += E; E += (rotl(F, 30) ^ rotl(F, 19) ^ rotl(F, 10)) + ((F & G) | (H & (F | G)));
        W12 += (rotl(W10, 15) ^ rotl(W10, 13) ^ (W10 >> 10))  +  W5   +  (rotl(W13, 25) ^ rotl(W13, 14) ^ (W13 >> 3));   D += (rotl(A, 26) ^ rotl(A, 21) ^ rotl(A, 7))  +  (C ^ (A & (B ^ C)))  +  sha512_consts[i + 12] + W12; H += D; D += (rotl(E, 30) ^ rotl(E, 19) ^ rotl(E, 10)) + ((E & F) | (G & (E | F)));
        W13 += (rotl(W11, 15) ^ rotl(W11, 13) ^ (W11 >> 10))  +  W6   +  (rotl(W14, 25) ^ rotl(W14, 14) ^ (W14 >> 3));   C += (rotl(H, 26) ^ rotl(H, 21) ^ rotl(H, 7))  +  (B ^ (H & (A ^ B)))  +  sha512_consts[i + 13] + W13; G += C; C += (rotl(D, 30) ^ rotl(D, 19) ^ rotl(D, 10)) + ((D & E) | (F & (D | E)));
        W14 += (rotl(W12, 15) ^ rotl(W12, 13) ^ (W12 >> 10))  +  W7   +  (rotl(W15, 25) ^ rotl(W15, 14) ^ (W15 >> 3));   B += (rotl(G, 26) ^ rotl(G, 21) ^ rotl(G, 7))  +  (A ^ (G & (H ^ A)))  +  sha512_consts[i + 14] + W14; F += B; B += (rotl(C, 30) ^ rotl(C, 19) ^ rotl(C, 10)) + ((C & D) | (E & (C | D)));
        W15 += (rotl(W13, 15) ^ rotl(W13, 13) ^ (W13 >> 10))  +  W8   +  (rotl(W0 , 25) ^ rotl(W0 , 14) ^ (W0  >> 3));   A += (rotl(F, 26) ^ rotl(F, 21) ^ rotl(F, 7))  +  (H ^ (F & (G ^ H)))  +  sha512_consts[i + 15] + W15; E += A; A += (rotl(B, 30) ^ rotl(B, 19) ^ rotl(B, 10)) + ((B & C) | (D & (B | C)));

    # Save state
    state[0] += A
    state[1] += B
    state[2] += C
    state[3] += D
    state[4] += E
    state[5] += F
    state[6] += G
    state[7] += H

with Function(void)(state, W) as sha512_block_:
    # Load state
    A, B, C, D, E, F, G, H = state[0], state[1], state[2], state[3], state[4], state[5], state[6], state[7]
    W0 , W1 , W2 , W3  = W[ 0], W[ 1], W[ 2], W[ 3]
    W4 , W5 , W6 , W7  = W[ 4], W[ 5], W[ 6], W[ 7]
    W8 , W9 , W10, W11 = W[ 8], W[ 9], W[10], W[11]
    W12, W13, W14, W15 = W[12], W[13], W[14], W[15]

    # Round 1
    H += ternary_logic(rotl(E, 26), rotl(E, 21), rotl(E, 7), 0x96)  +  ternary_logic(G, F, E, 0xd8)  +  sha512_consts[ 0] + W0 ;   D += H;   H += ternary_logic(rotl(A, 30), rotl(A, 19), rotl(A, 10), 0x96)  +  ternary_logic(A, B, C, 0xE8);
    G += ternary_logic(rotl(D, 26), rotl(D, 21), rotl(D, 7), 0x96)  +  ternary_logic(F, E, D, 0xd8)  +  sha512_consts[ 1] + W1 ;   C += G;   G += ternary_logic(rotl(H, 30), rotl(H, 19), rotl(H, 10), 0x96)  +  ternary_logic(H, A, B, 0xE8);
    F += ternary_logic(rotl(C, 26), rotl(C, 21), rotl(C, 7), 0x96)  +  ternary_logic(E, D, C, 0xd8)  +  sha512_consts[ 2] + W2 ;   B += F;   F += ternary_logic(rotl(G, 30), rotl(G, 19), rotl(G, 10), 0x96)  +  ternary_logic(G, H, A, 0xE8);
    E += ternary_logic(rotl(B, 26), rotl(B, 21), rotl(B, 7), 0x96)  +  ternary_logic(D, C, B, 0xd8)  +  sha512_consts[ 3] + W3 ;   A += E;   E += ternary_logic(rotl(F, 30), rotl(F, 19), rotl(F, 10), 0x96)  +  ternary_logic(F, G, H, 0xE8);
    D += ternary_logic(rotl(A, 26), rotl(A, 21), rotl(A, 7), 0x96)  +  ternary_logic(C, B, A, 0xd8)  +  sha512_consts[ 4] + W4 ;   H += D;   D += ternary_logic(rotl(E, 30), rotl(E, 19), rotl(E, 10), 0x96)  +  ternary_logic(E, F, G, 0xE8);
    C += ternary_logic(rotl(H, 26), rotl(H, 21), rotl(H, 7), 0x96)  +  ternary_logic(B, A, H, 0xd8)  +  sha512_consts[ 5] + W5 ;   G += C;   C += ternary_logic(rotl(D, 30), rotl(D, 19), rotl(D, 10), 0x96)  +  ternary_logic(D, E, F, 0xE8);
    B += ternary_logic(rotl(G, 26), rotl(G, 21), rotl(G, 7), 0x96)  +  ternary_logic(A, H, G, 0xd8)  +  sha512_consts[ 6] + W6 ;   F += B;   B += ternary_logic(rotl(C, 30), rotl(C, 19), rotl(C, 10), 0x96)  +  ternary_logic(C, D, E, 0xE8);
    A += ternary_logic(rotl(F, 26), rotl(F, 21), rotl(F, 7), 0x96)  +  ternary_logic(H, G, F, 0xd8)  +  sha512_consts[ 7] + W7 ;   E += A;   A += ternary_logic(rotl(B, 30), rotl(B, 19), rotl(B, 10), 0x96)  +  ternary_logic(B, C, D, 0xE8);
    H += ternary_logic(rotl(E, 26), rotl(E, 21), rotl(E, 7), 0x96)  +  ternary_logic(G, F, E, 0xd8)  +  sha512_consts[ 8] + W8 ;   D += H;   H += ternary_logic(rotl(A, 30), rotl(A, 19), rotl(A, 10), 0x96)  +  ternary_logic(A, B, C, 0xE8);
    G += ternary_logic(rotl(D, 26), rotl(D, 21), rotl(D, 7), 0x96)  +  ternary_logic(F, E, D, 0xd8)  +  sha512_consts[ 9] + W9 ;   C += G;   G += ternary_logic(rotl(H, 30), rotl(H, 19), rotl(H, 10), 0x96)  +  ternary_logic(H, A, B, 0xE8);
    F += ternary_logic(rotl(C, 26), rotl(C, 21), rotl(C, 7), 0x96)  +  ternary_logic(E, D, C, 0xd8)  +  sha512_consts[10] + W10;   B += F;   F += ternary_logic(rotl(G, 30), rotl(G, 19), rotl(G, 10), 0x96)  +  ternary_logic(G, H, A, 0xE8);
    E += ternary_logic(rotl(B, 26), rotl(B, 21), rotl(B, 7), 0x96)  +  ternary_logic(D, C, B, 0xd8)  +  sha512_consts[11] + W11;   A += E;   E += ternary_logic(rotl(F, 30), rotl(F, 19), rotl(F, 10), 0x96)  +  ternary_logic(F, G, H, 0xE8);
    D += ternary_logic(rotl(A, 26), rotl(A, 21), rotl(A, 7), 0x96)  +  ternary_logic(C, B, A, 0xd8)  +  sha512_consts[12] + W12;   H += D;   D += ternary_logic(rotl(E, 30), rotl(E, 19), rotl(E, 10), 0x96)  +  ternary_logic(E, F, G, 0xE8);
    C += ternary_logic(rotl(H, 26), rotl(H, 21), rotl(H, 7), 0x96)  +  ternary_logic(B, A, H, 0xd8)  +  sha512_consts[13] + W13;   G += C;   C += ternary_logic(rotl(D, 30), rotl(D, 19), rotl(D, 10), 0x96)  +  ternary_logic(D, E, F, 0xE8);
    B += ternary_logic(rotl(G, 26), rotl(G, 21), rotl(G, 7), 0x96)  +  ternary_logic(A, H, G, 0xd8)  +  sha512_consts[14] + W14;   F += B;   B += ternary_logic(rotl(C, 30), rotl(C, 19), rotl(C, 10), 0x96)  +  ternary_logic(C, D, E, 0xE8);
    A += ternary_logic(rotl(F, 26), rotl(F, 21), rotl(F, 7), 0x96)  +  ternary_logic(H, G, F, 0xd8)  +  sha512_consts[15] + W15;   E += A;   A += ternary_logic(rotl(B, 30), rotl(B, 19), rotl(B, 10), 0x96)  +  ternary_logic(B, C, D, 0xE8);

    # Round 2-5
    for i in range(16, 80, 16):
        W0  += ternary_logic(rotl(W14, 15), rotl(W14, 13), (W14 >> 10), 0x96)  +  W9   +  ternary_logic(rotl(W1 , 25), rotl(W1 , 14), (W1  >> 3), 0x96);   H += ternary_logic(rotl(E, 26), rotl(E, 21), rotl(E, 7), 0x96)  +  ternary_logic(G, F, E, 0xd8)  +  sha512_consts[i +  0] + W0 ; D += H; H +=  ternary_logic(rotl(A, 30), rotl(A, 19), rotl(A, 10), 0x96) + ternary_logic(A, B, C, 0xE8);
        W1  += ternary_logic(rotl(W15, 15), rotl(W15, 13), (W15 >> 10), 0x96)  +  W10  +  ternary_logic(rotl(W2 , 25), rotl(W2 , 14), (W2  >> 3), 0x96);   G += ternary_logic(rotl(D, 26), rotl(D, 21), rotl(D, 7), 0x96)  +  ternary_logic(F, E, D, 0xd8)  +  sha512_consts[i +  1] + W1 ; C += G; G +=  ternary_logic(rotl(H, 30), rotl(H, 19), rotl(H, 10), 0x96) + ternary_logic(H, A, B, 0xE8);
        W2  += ternary_logic(rotl(W0 , 15), rotl(W0 , 13), (W0  >> 10), 0x96)  +  W11  +  ternary_logic(rotl(W3 , 25), rotl(W3 , 14), (W3  >> 3), 0x96);   F += ternary_logic(rotl(C, 26), rotl(C, 21), rotl(C, 7), 0x96)  +  ternary_logic(E, D, C, 0xd8)  +  sha512_consts[i +  2] + W2 ; B += F; F +=  ternary_logic(rotl(G, 30), rotl(G, 19), rotl(G, 10), 0x96) + ternary_logic(G, H, A, 0xE8);
        W3  += ternary_logic(rotl(W1 , 15), rotl(W1 , 13), (W1  >> 10), 0x96)  +  W12  +  ternary_logic(rotl(W4 , 25), rotl(W4 , 14), (W4  >> 3), 0x96);   E += ternary_logic(rotl(B, 26), rotl(B, 21), rotl(B, 7), 0x96)  +  ternary_logic(D, C, B, 0xd8)  +  sha512_consts[i +  3] + W3 ; A += E; E +=  ternary_logic(rotl(F, 30), rotl(F, 19), rotl(F, 10), 0x96) + ternary_logic(F, G, H, 0xE8);
        W4  += ternary_logic(rotl(W2 , 15), rotl(W2 , 13), (W2  >> 10), 0x96)  +  W13  +  ternary_logic(rotl(W5 , 25), rotl(W5 , 14), (W5  >> 3), 0x96);   D += ternary_logic(rotl(A, 26), rotl(A, 21), rotl(A, 7), 0x96)  +  ternary_logic(C, B, A, 0xd8)  +  sha512_consts[i +  4] + W4 ; H += D; D +=  ternary_logic(rotl(E, 30), rotl(E, 19), rotl(E, 10), 0x96) + ternary_logic(E, F, G, 0xE8);
        W5  += ternary_logic(rotl(W3 , 15), rotl(W3 , 13), (W3  >> 10), 0x96)  +  W14  +  ternary_logic(rotl(W6 , 25), rotl(W6 , 14), (W6  >> 3), 0x96);   C += ternary_logic(rotl(H, 26), rotl(H, 21), rotl(H, 7), 0x96)  +  ternary_logic(B, A, H, 0xd8)  +  sha512_consts[i +  5] + W5 ; G += C; C +=  ternary_logic(rotl(D, 30), rotl(D, 19), rotl(D, 10), 0x96) + ternary_logic(D, E, F, 0xE8);
        W6  += ternary_logic(rotl(W4 , 15), rotl(W4 , 13), (W4  >> 10), 0x96)  +  W15  +  ternary_logic(rotl(W7 , 25), rotl(W7 , 14), (W7  >> 3), 0x96);   B += ternary_logic(rotl(G, 26), rotl(G, 21), rotl(G, 7), 0x96)  +  ternary_logic(A, H, G, 0xd8)  +  sha512_consts[i +  6] + W6 ; F += B; B +=  ternary_logic(rotl(C, 30), rotl(C, 19), rotl(C, 10), 0x96) + ternary_logic(C, D, E, 0xE8);
        W7  += ternary_logic(rotl(W5 , 15), rotl(W5 , 13), (W5  >> 10), 0x96)  +  W0   +  ternary_logic(rotl(W8 , 25), rotl(W8 , 14), (W8  >> 3), 0x96);   A += ternary_logic(rotl(F, 26), rotl(F, 21), rotl(F, 7), 0x96)  +  ternary_logic(H, G, F, 0xd8)  +  sha512_consts[i +  7] + W7 ; E += A; A +=  ternary_logic(rotl(B, 30), rotl(B, 19), rotl(B, 10), 0x96) + ternary_logic(B, C, D, 0xE8);
        W8  += ternary_logic(rotl(W6 , 15), rotl(W6 , 13), (W6  >> 10), 0x96)  +  W1   +  ternary_logic(rotl(W9 , 25), rotl(W9 , 14), (W9  >> 3), 0x96);   H += ternary_logic(rotl(E, 26), rotl(E, 21), rotl(E, 7), 0x96)  +  ternary_logic(G, F, E, 0xd8)  +  sha512_consts[i +  8] + W8 ; D += H; H +=  ternary_logic(rotl(A, 30), rotl(A, 19), rotl(A, 10), 0x96) + ternary_logic(A, B, C, 0xE8);
        W9  += ternary_logic(rotl(W7 , 15), rotl(W7 , 13), (W7  >> 10), 0x96)  +  W2   +  ternary_logic(rotl(W10, 25), rotl(W10, 14), (W10 >> 3), 0x96);   G += ternary_logic(rotl(D, 26), rotl(D, 21), rotl(D, 7), 0x96)  +  ternary_logic(F, E, D, 0xd8)  +  sha512_consts[i +  9] + W9 ; C += G; G +=  ternary_logic(rotl(H, 30), rotl(H, 19), rotl(H, 10), 0x96) + ternary_logic(H, A, B, 0xE8);
        W10 += ternary_logic(rotl(W8 , 15), rotl(W8 , 13), (W8  >> 10), 0x96)  +  W3   +  ternary_logic(rotl(W11, 25), rotl(W11, 14), (W11 >> 3), 0x96);   F += ternary_logic(rotl(C, 26), rotl(C, 21), rotl(C, 7), 0x96)  +  ternary_logic(E, D, C, 0xd8)  +  sha512_consts[i + 10] + W10; B += F; F +=  ternary_logic(rotl(G, 30), rotl(G, 19), rotl(G, 10), 0x96) + ternary_logic(G, H, A, 0xE8);
        W11 += ternary_logic(rotl(W9 , 15), rotl(W9 , 13), (W9  >> 10), 0x96)  +  W4   +  ternary_logic(rotl(W12, 25), rotl(W12, 14), (W12 >> 3), 0x96);   E += ternary_logic(rotl(B, 26), rotl(B, 21), rotl(B, 7), 0x96)  +  ternary_logic(D, C, B, 0xd8)  +  sha512_consts[i + 11] + W11; A += E; E +=  ternary_logic(rotl(F, 30), rotl(F, 19), rotl(F, 10), 0x96) + ternary_logic(F, G, H, 0xE8);
        W12 += ternary_logic(rotl(W10, 15), rotl(W10, 13), (W10 >> 10), 0x96)  +  W5   +  ternary_logic(rotl(W13, 25), rotl(W13, 14), (W13 >> 3), 0x96);   D += ternary_logic(rotl(A, 26), rotl(A, 21), rotl(A, 7), 0x96)  +  ternary_logic(C, B, A, 0xd8)  +  sha512_consts[i + 12] + W12; H += D; D +=  ternary_logic(rotl(E, 30), rotl(E, 19), rotl(E, 10), 0x96) + ternary_logic(E, F, G, 0xE8);
        W13 += ternary_logic(rotl(W11, 15), rotl(W11, 13), (W11 >> 10), 0x96)  +  W6   +  ternary_logic(rotl(W14, 25), rotl(W14, 14), (W14 >> 3), 0x96);   C += ternary_logic(rotl(H, 26), rotl(H, 21), rotl(H, 7), 0x96)  +  ternary_logic(B, A, H, 0xd8)  +  sha512_consts[i + 13] + W13; G += C; C +=  ternary_logic(rotl(D, 30), rotl(D, 19), rotl(D, 10), 0x96) + ternary_logic(D, E, F, 0xE8);
        W14 += ternary_logic(rotl(W12, 15), rotl(W12, 13), (W12 >> 10), 0x96)  +  W7   +  ternary_logic(rotl(W15, 25), rotl(W15, 14), (W15 >> 3), 0x96);   B += ternary_logic(rotl(G, 26), rotl(G, 21), rotl(G, 7), 0x96)  +  ternary_logic(A, H, G, 0xd8)  +  sha512_consts[i + 14] + W14; F += B; B +=  ternary_logic(rotl(C, 30), rotl(C, 19), rotl(C, 10), 0x96) + ternary_logic(C, D, E, 0xE8);
        W15 += ternary_logic(rotl(W13, 15), rotl(W13, 13), (W13 >> 10), 0x96)  +  W8   +  ternary_logic(rotl(W0 , 25), rotl(W0 , 14), (W0  >> 3), 0x96);   A += ternary_logic(rotl(F, 26), rotl(F, 21), rotl(F, 7), 0x96)  +  ternary_logic(H, G, F, 0xd8)  +  sha512_consts[i + 15] + W15; E += A; A +=  ternary_logic(rotl(B, 30), rotl(B, 19), rotl(B, 10), 0x96) + ternary_logic(B, C, D, 0xE8);

    # Save state
    state[0] += A
    state[1] += B
    state[2] += C
    state[3] += D
    state[4] += E
    state[5] += F
    state[6] += G
    state[7] += H
    
# Define targets
sha512_block.targets  = [Target.PLAIN_C, Target.SSE2, Target.AVX, Target.AVX2]
sha512_block_.targets = [Target.AVX512]
sha512_block.parallelization_factor [Target.SSE2  ] = [1, 2]
sha512_block.parallelization_factor [Target.AVX   ] = [1, 2]
sha512_block.parallelization_factor [Target.AVX2  ] = [1, 2]
sha512_block_.parallelization_factor[Target.AVX512] = [1, 2]
# Build and run
generate_code()
build_and_run('C:/Program Files/CMake/bin/cmake.exe', run_benchmark=False, run_tests=True, 
              sde_test_cpus=['-knm'], 
              sde_exe='C:/Users/Alain/Downloads/sde-external-9.33.0-2024-01-07-win/sde.exe')
