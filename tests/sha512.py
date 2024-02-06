#######################################################
# SHA512 - Secure Hash Algorithm 2
#######################################################

import sys
sys.path.append('src/')
from simd_function import *

state = VectorMemoryArray(uint64_t, 8)  # The state
W     = VectorMemoryArray(uint64_t, 16) # The message
consts_raw = [
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
consts_simd   = VectorMemoryArray(uint64_t, is_global=True, is_parallelizable=False, initial_values=consts_raw)
consts_scalar = ScalarMemoryArray(uint64_t, is_global=True, is_parallelizable=False, initial_values=consts_raw)

# Generator
def sha512_block_generator(state, W, consts):
    # Load state
    H, E, F, G, D, A, B, C = state[7], state[4], state[5], state[6], state[3], state[0], state[1], state[2]
    W0 , W1 , W2 , W3  = W[ 0], W[ 1], W[ 2], W[ 3]
    W4 , W5 , W6 , W7  = W[ 4], W[ 5], W[ 6], W[ 7]
    W8 , W9 , W10, W11 = W[ 8], W[ 9], W[10], W[11]
    W12, W13, W14, W15 = W[12], W[13], W[14], W[15]

    # Round 1
    H += ternary_logic(rotl(E, 50), rotl(E, 46), rotl(E, 23), 0x96)  +  ternary_logic(G, F, E, 0xd8)  +  consts[ 0] + W0 ;   D += H;   H += ternary_logic(rotl(A, 36), rotl(A, 30), rotl(A, 25), 0x96)  +  ternary_logic(A, B, C, 0xE8)
    G += ternary_logic(rotl(D, 50), rotl(D, 46), rotl(D, 23), 0x96)  +  ternary_logic(F, E, D, 0xd8)  +  consts[ 1] + W1 ;   C += G;   G += ternary_logic(rotl(H, 36), rotl(H, 30), rotl(H, 25), 0x96)  +  ternary_logic(H, A, B, 0xE8)
    F += ternary_logic(rotl(C, 50), rotl(C, 46), rotl(C, 23), 0x96)  +  ternary_logic(E, D, C, 0xd8)  +  consts[ 2] + W2 ;   B += F;   F += ternary_logic(rotl(G, 36), rotl(G, 30), rotl(G, 25), 0x96)  +  ternary_logic(G, H, A, 0xE8)
    E += ternary_logic(rotl(B, 50), rotl(B, 46), rotl(B, 23), 0x96)  +  ternary_logic(D, C, B, 0xd8)  +  consts[ 3] + W3 ;   A += E;   E += ternary_logic(rotl(F, 36), rotl(F, 30), rotl(F, 25), 0x96)  +  ternary_logic(F, G, H, 0xE8)
    D += ternary_logic(rotl(A, 50), rotl(A, 46), rotl(A, 23), 0x96)  +  ternary_logic(C, B, A, 0xd8)  +  consts[ 4] + W4 ;   H += D;   D += ternary_logic(rotl(E, 36), rotl(E, 30), rotl(E, 25), 0x96)  +  ternary_logic(E, F, G, 0xE8)
    C += ternary_logic(rotl(H, 50), rotl(H, 46), rotl(H, 23), 0x96)  +  ternary_logic(B, A, H, 0xd8)  +  consts[ 5] + W5 ;   G += C;   C += ternary_logic(rotl(D, 36), rotl(D, 30), rotl(D, 25), 0x96)  +  ternary_logic(D, E, F, 0xE8)
    B += ternary_logic(rotl(G, 50), rotl(G, 46), rotl(G, 23), 0x96)  +  ternary_logic(A, H, G, 0xd8)  +  consts[ 6] + W6 ;   F += B;   B += ternary_logic(rotl(C, 36), rotl(C, 30), rotl(C, 25), 0x96)  +  ternary_logic(C, D, E, 0xE8)
    A += ternary_logic(rotl(F, 50), rotl(F, 46), rotl(F, 23), 0x96)  +  ternary_logic(H, G, F, 0xd8)  +  consts[ 7] + W7 ;   E += A;   A += ternary_logic(rotl(B, 36), rotl(B, 30), rotl(B, 25), 0x96)  +  ternary_logic(B, C, D, 0xE8)
    H += ternary_logic(rotl(E, 50), rotl(E, 46), rotl(E, 23), 0x96)  +  ternary_logic(G, F, E, 0xd8)  +  consts[ 8] + W8 ;   D += H;   H += ternary_logic(rotl(A, 36), rotl(A, 30), rotl(A, 25), 0x96)  +  ternary_logic(A, B, C, 0xE8)
    G += ternary_logic(rotl(D, 50), rotl(D, 46), rotl(D, 23), 0x96)  +  ternary_logic(F, E, D, 0xd8)  +  consts[ 9] + W9 ;   C += G;   G += ternary_logic(rotl(H, 36), rotl(H, 30), rotl(H, 25), 0x96)  +  ternary_logic(H, A, B, 0xE8)
    F += ternary_logic(rotl(C, 50), rotl(C, 46), rotl(C, 23), 0x96)  +  ternary_logic(E, D, C, 0xd8)  +  consts[10] + W10;   B += F;   F += ternary_logic(rotl(G, 36), rotl(G, 30), rotl(G, 25), 0x96)  +  ternary_logic(G, H, A, 0xE8)
    E += ternary_logic(rotl(B, 50), rotl(B, 46), rotl(B, 23), 0x96)  +  ternary_logic(D, C, B, 0xd8)  +  consts[11] + W11;   A += E;   E += ternary_logic(rotl(F, 36), rotl(F, 30), rotl(F, 25), 0x96)  +  ternary_logic(F, G, H, 0xE8)
    D += ternary_logic(rotl(A, 50), rotl(A, 46), rotl(A, 23), 0x96)  +  ternary_logic(C, B, A, 0xd8)  +  consts[12] + W12;   H += D;   D += ternary_logic(rotl(E, 36), rotl(E, 30), rotl(E, 25), 0x96)  +  ternary_logic(E, F, G, 0xE8)
    C += ternary_logic(rotl(H, 50), rotl(H, 46), rotl(H, 23), 0x96)  +  ternary_logic(B, A, H, 0xd8)  +  consts[13] + W13;   G += C;   C += ternary_logic(rotl(D, 36), rotl(D, 30), rotl(D, 25), 0x96)  +  ternary_logic(D, E, F, 0xE8)
    B += ternary_logic(rotl(G, 50), rotl(G, 46), rotl(G, 23), 0x96)  +  ternary_logic(A, H, G, 0xd8)  +  consts[14] + W14;   F += B;   B += ternary_logic(rotl(C, 36), rotl(C, 30), rotl(C, 25), 0x96)  +  ternary_logic(C, D, E, 0xE8)
    A += ternary_logic(rotl(F, 50), rotl(F, 46), rotl(F, 23), 0x96)  +  ternary_logic(H, G, F, 0xd8)  +  consts[15] + W15;   E += A;   A += ternary_logic(rotl(B, 36), rotl(B, 30), rotl(B, 25), 0x96)  +  ternary_logic(B, C, D, 0xE8)
    consts += 16
    
    # Round 2-5
    with Repeat(4):
        W0  += ternary_logic(rotl(W14, 45), rotl(W14, 3), (W14 >> 6), 0x96)  +  W9   +  ternary_logic(rotl(W1 , 63), rotl(W1 , 56), (W1  >> 7), 0x96);   H += ternary_logic(rotl(E, 50), rotl(E, 46), rotl(E, 23), 0x96)  +  ternary_logic(G, F, E, 0xd8)  +  consts[ 0] + W0 ; D += H; H +=  ternary_logic(rotl(A, 36), rotl(A, 30), rotl(A, 25), 0x96) + ternary_logic(A, B, C, 0xE8)
        W1  += ternary_logic(rotl(W15, 45), rotl(W15, 3), (W15 >> 6), 0x96)  +  W10  +  ternary_logic(rotl(W2 , 63), rotl(W2 , 56), (W2  >> 7), 0x96);   G += ternary_logic(rotl(D, 50), rotl(D, 46), rotl(D, 23), 0x96)  +  ternary_logic(F, E, D, 0xd8)  +  consts[ 1] + W1 ; C += G; G +=  ternary_logic(rotl(H, 36), rotl(H, 30), rotl(H, 25), 0x96) + ternary_logic(H, A, B, 0xE8)
        W2  += ternary_logic(rotl(W0 , 45), rotl(W0 , 3), (W0  >> 6), 0x96)  +  W11  +  ternary_logic(rotl(W3 , 63), rotl(W3 , 56), (W3  >> 7), 0x96);   F += ternary_logic(rotl(C, 50), rotl(C, 46), rotl(C, 23), 0x96)  +  ternary_logic(E, D, C, 0xd8)  +  consts[ 2] + W2 ; B += F; F +=  ternary_logic(rotl(G, 36), rotl(G, 30), rotl(G, 25), 0x96) + ternary_logic(G, H, A, 0xE8)
        W3  += ternary_logic(rotl(W1 , 45), rotl(W1 , 3), (W1  >> 6), 0x96)  +  W12  +  ternary_logic(rotl(W4 , 63), rotl(W4 , 56), (W4  >> 7), 0x96);   E += ternary_logic(rotl(B, 50), rotl(B, 46), rotl(B, 23), 0x96)  +  ternary_logic(D, C, B, 0xd8)  +  consts[ 3] + W3 ; A += E; E +=  ternary_logic(rotl(F, 36), rotl(F, 30), rotl(F, 25), 0x96) + ternary_logic(F, G, H, 0xE8)
        W4  += ternary_logic(rotl(W2 , 45), rotl(W2 , 3), (W2  >> 6), 0x96)  +  W13  +  ternary_logic(rotl(W5 , 63), rotl(W5 , 56), (W5  >> 7), 0x96);   D += ternary_logic(rotl(A, 50), rotl(A, 46), rotl(A, 23), 0x96)  +  ternary_logic(C, B, A, 0xd8)  +  consts[ 4] + W4 ; H += D; D +=  ternary_logic(rotl(E, 36), rotl(E, 30), rotl(E, 25), 0x96) + ternary_logic(E, F, G, 0xE8)
        W5  += ternary_logic(rotl(W3 , 45), rotl(W3 , 3), (W3  >> 6), 0x96)  +  W14  +  ternary_logic(rotl(W6 , 63), rotl(W6 , 56), (W6  >> 7), 0x96);   C += ternary_logic(rotl(H, 50), rotl(H, 46), rotl(H, 23), 0x96)  +  ternary_logic(B, A, H, 0xd8)  +  consts[ 5] + W5 ; G += C; C +=  ternary_logic(rotl(D, 36), rotl(D, 30), rotl(D, 25), 0x96) + ternary_logic(D, E, F, 0xE8)
        W6  += ternary_logic(rotl(W4 , 45), rotl(W4 , 3), (W4  >> 6), 0x96)  +  W15  +  ternary_logic(rotl(W7 , 63), rotl(W7 , 56), (W7  >> 7), 0x96);   B += ternary_logic(rotl(G, 50), rotl(G, 46), rotl(G, 23), 0x96)  +  ternary_logic(A, H, G, 0xd8)  +  consts[ 6] + W6 ; F += B; B +=  ternary_logic(rotl(C, 36), rotl(C, 30), rotl(C, 25), 0x96) + ternary_logic(C, D, E, 0xE8)
        W7  += ternary_logic(rotl(W5 , 45), rotl(W5 , 3), (W5  >> 6), 0x96)  +  W0   +  ternary_logic(rotl(W8 , 63), rotl(W8 , 56), (W8  >> 7), 0x96);   A += ternary_logic(rotl(F, 50), rotl(F, 46), rotl(F, 23), 0x96)  +  ternary_logic(H, G, F, 0xd8)  +  consts[ 7] + W7 ; E += A; A +=  ternary_logic(rotl(B, 36), rotl(B, 30), rotl(B, 25), 0x96) + ternary_logic(B, C, D, 0xE8)
        W8  += ternary_logic(rotl(W6 , 45), rotl(W6 , 3), (W6  >> 6), 0x96)  +  W1   +  ternary_logic(rotl(W9 , 63), rotl(W9 , 56), (W9  >> 7), 0x96);   H += ternary_logic(rotl(E, 50), rotl(E, 46), rotl(E, 23), 0x96)  +  ternary_logic(G, F, E, 0xd8)  +  consts[ 8] + W8 ; D += H; H +=  ternary_logic(rotl(A, 36), rotl(A, 30), rotl(A, 25), 0x96) + ternary_logic(A, B, C, 0xE8)
        W9  += ternary_logic(rotl(W7 , 45), rotl(W7 , 3), (W7  >> 6), 0x96)  +  W2   +  ternary_logic(rotl(W10, 63), rotl(W10, 56), (W10 >> 7), 0x96);   G += ternary_logic(rotl(D, 50), rotl(D, 46), rotl(D, 23), 0x96)  +  ternary_logic(F, E, D, 0xd8)  +  consts[ 9] + W9 ; C += G; G +=  ternary_logic(rotl(H, 36), rotl(H, 30), rotl(H, 25), 0x96) + ternary_logic(H, A, B, 0xE8)
        W10 += ternary_logic(rotl(W8 , 45), rotl(W8 , 3), (W8  >> 6), 0x96)  +  W3   +  ternary_logic(rotl(W11, 63), rotl(W11, 56), (W11 >> 7), 0x96);   F += ternary_logic(rotl(C, 50), rotl(C, 46), rotl(C, 23), 0x96)  +  ternary_logic(E, D, C, 0xd8)  +  consts[10] + W10; B += F; F +=  ternary_logic(rotl(G, 36), rotl(G, 30), rotl(G, 25), 0x96) + ternary_logic(G, H, A, 0xE8)
        W11 += ternary_logic(rotl(W9 , 45), rotl(W9 , 3), (W9  >> 6), 0x96)  +  W4   +  ternary_logic(rotl(W12, 63), rotl(W12, 56), (W12 >> 7), 0x96);   E += ternary_logic(rotl(B, 50), rotl(B, 46), rotl(B, 23), 0x96)  +  ternary_logic(D, C, B, 0xd8)  +  consts[11] + W11; A += E; E +=  ternary_logic(rotl(F, 36), rotl(F, 30), rotl(F, 25), 0x96) + ternary_logic(F, G, H, 0xE8)
        W12 += ternary_logic(rotl(W10, 45), rotl(W10, 3), (W10 >> 6), 0x96)  +  W5   +  ternary_logic(rotl(W13, 63), rotl(W13, 56), (W13 >> 7), 0x96);   D += ternary_logic(rotl(A, 50), rotl(A, 46), rotl(A, 23), 0x96)  +  ternary_logic(C, B, A, 0xd8)  +  consts[12] + W12; H += D; D +=  ternary_logic(rotl(E, 36), rotl(E, 30), rotl(E, 25), 0x96) + ternary_logic(E, F, G, 0xE8)
        W13 += ternary_logic(rotl(W11, 45), rotl(W11, 3), (W11 >> 6), 0x96)  +  W6   +  ternary_logic(rotl(W14, 63), rotl(W14, 56), (W14 >> 7), 0x96);   C += ternary_logic(rotl(H, 50), rotl(H, 46), rotl(H, 23), 0x96)  +  ternary_logic(B, A, H, 0xd8)  +  consts[13] + W13; G += C; C +=  ternary_logic(rotl(D, 36), rotl(D, 30), rotl(D, 25), 0x96) + ternary_logic(D, E, F, 0xE8)
        W14 += ternary_logic(rotl(W12, 45), rotl(W12, 3), (W12 >> 6), 0x96)  +  W7   +  ternary_logic(rotl(W15, 63), rotl(W15, 56), (W15 >> 7), 0x96);   B += ternary_logic(rotl(G, 50), rotl(G, 46), rotl(G, 23), 0x96)  +  ternary_logic(A, H, G, 0xd8)  +  consts[14] + W14; F += B; B +=  ternary_logic(rotl(C, 36), rotl(C, 30), rotl(C, 25), 0x96) + ternary_logic(C, D, E, 0xE8)
        W15 += ternary_logic(rotl(W13, 45), rotl(W13, 3), (W13 >> 6), 0x96)  +  W8   +  ternary_logic(rotl(W0 , 63), rotl(W0 , 56), (W0  >> 7), 0x96);   A += ternary_logic(rotl(F, 50), rotl(F, 46), rotl(F, 23), 0x96)  +  ternary_logic(H, G, F, 0xd8)  +  consts[15] + W15; E += A; A +=  ternary_logic(rotl(B, 36), rotl(B, 30), rotl(B, 25), 0x96) + ternary_logic(B, C, D, 0xE8)
        consts += 16

    # Save state
    state[7] += H
    state[3] += D
    state[6] += G
    state[2] += C
    state[5] += F
    state[1] += B
    state[4] += E
    state[0] += A

## <summary>
## SHA512 compress block
## </summary>
## <param name="state">The SHA512 state</param>
## <param name="block">The message to compress</param>
with Function(void)(state, W) as sha512_block:
    sha512_block_generator(state, W, consts_simd)

with Function(void)(state, W) as sha512_block_avx512:
    sha512_block_generator(state, W, consts_scalar)
    
# Define targets
sha512_block.targets  = [Target.PLAIN_C, Target.SSE2, Target.AVX]
sha512_block_avx512.targets = [Target.AVX2, Target.AVX512]
sha512_block_avx512.name = 'sha512_block'
# Build and run
generate_code()
build_and_run('C:/Program Files/CMake/bin/cmake.exe', run_benchmark=True, run_tests=True, 
              sde_test_cpus=['-knm'], 
              sde_exe='C:/Users/Alain/Downloads/sde-external-9.33.0-2024-01-07-win/sde.exe')
