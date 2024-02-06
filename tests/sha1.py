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
    E, A, C, D, B = state[4], state[0], state[2], state[3], state[1]
    W0 , W1 , W2 , W3  = W[ 0], W[ 1], W[ 2], W[ 3]
    W4 , W5 , W6 , W7  = W[ 4], W[ 5], W[ 6], W[ 7]
    W8 , W9 , W10, W11 = W[ 8], W[ 9], W[10], W[11]
    W12, W13, W14, W15 = W[12], W[13], W[14], W[15]

    # Round 1
    E += rotl(A, 5); E += ternary_logic(D, C, B, 0xd8); E += 0x5a827999; E += W0 ; B = rotl(B, 30)
    D += rotl(E, 5); D += ternary_logic(C, B, A, 0xd8); D += 0x5a827999; D += W1 ; A = rotl(A, 30)
    C += rotl(D, 5); C += ternary_logic(B, A, E, 0xd8); C += 0x5a827999; C += W2 ; E = rotl(E, 30)
    B += rotl(C, 5); B += ternary_logic(A, E, D, 0xd8); B += 0x5a827999; B += W3 ; D = rotl(D, 30)
    A += rotl(B, 5); A += ternary_logic(E, D, C, 0xd8); A += 0x5a827999; A += W4 ; C = rotl(C, 30)
    E += rotl(A, 5); E += ternary_logic(D, C, B, 0xd8); E += 0x5a827999; E += W5 ; B = rotl(B, 30)
    D += rotl(E, 5); D += ternary_logic(C, B, A, 0xd8); D += 0x5a827999; D += W6 ; A = rotl(A, 30)
    C += rotl(D, 5); C += ternary_logic(B, A, E, 0xd8); C += 0x5a827999; C += W7 ; E = rotl(E, 30)
    B += rotl(C, 5); B += ternary_logic(A, E, D, 0xd8); B += 0x5a827999; B += W8 ; D = rotl(D, 30)
    A += rotl(B, 5); A += ternary_logic(E, D, C, 0xd8); A += 0x5a827999; A += W9 ; C = rotl(C, 30)
    E += rotl(A, 5); E += ternary_logic(D, C, B, 0xd8); E += 0x5a827999; E += W10; B = rotl(B, 30)
    D += rotl(E, 5); D += ternary_logic(C, B, A, 0xd8); D += 0x5a827999; D += W11; A = rotl(A, 30)
    C += rotl(D, 5); C += ternary_logic(B, A, E, 0xd8); C += 0x5a827999; C += W12; E = rotl(E, 30)
    B += rotl(C, 5); B += ternary_logic(A, E, D, 0xd8); B += 0x5a827999; B += W13; D = rotl(D, 30)
    A += rotl(B, 5); A += ternary_logic(E, D, C, 0xd8); A += 0x5a827999; A += W14; C = rotl(C, 30)
    E += rotl(A, 5); E += ternary_logic(D, C, B, 0xd8); E += 0x5a827999; E += W15; B = rotl(B, 30)
    t = ternary_logic(W2 , W13, W8 , 0x96); D += 0x5a827999; W0  ^= t; W0  = rotl(W0 , 1);    D += rotl(E, 5); D += ternary_logic(C, B, A, 0xd8); D += W0; A = rotl(A, 30)
    t = ternary_logic(W3 , W14, W9 , 0x96); C += 0x5a827999; W1  ^= t; W1  = rotl(W1 , 1);    C += rotl(D, 5); C += ternary_logic(B, A, E, 0xd8); C += W1; E = rotl(E, 30)   
    t = ternary_logic(W4 , W15, W10, 0x96); B += 0x5a827999; W2  ^= t; W2  = rotl(W2 , 1);    B += rotl(C, 5); B += ternary_logic(A, E, D, 0xd8); B += W2; D = rotl(D, 30)
    t = ternary_logic(W5 , W0 , W11, 0x96); A += 0x5a827999; W3  ^= t; W3  = rotl(W3 , 1);    A += rotl(B, 5); A += ternary_logic(E, D, C, 0xd8); A += W3; C = rotl(C, 30)
                                                             
    # Round 2                                                
    t = ternary_logic(W6 , W1 , W12, 0x96); E += 0x6ed9eba1; W4  ^= t; W4  = rotl(W4 , 1);    E += rotl(A, 5); E += ternary_logic(B, C, D, 0x96); E += W4 ; B = rotl(B, 30)
    t = ternary_logic(W7 , W2 , W13, 0x96); D += 0x6ed9eba1; W5  ^= t; W5  = rotl(W5 , 1);    D += rotl(E, 5); D += ternary_logic(A, B, C, 0x96); D += W5 ; A = rotl(A, 30)
    t = ternary_logic(W8 , W3 , W14, 0x96); C += 0x6ed9eba1; W6  ^= t; W6  = rotl(W6 , 1);    C += rotl(D, 5); C += ternary_logic(E, A, B, 0x96); C += W6 ; E = rotl(E, 30)
    t = ternary_logic(W9 , W4 , W15, 0x96); B += 0x6ed9eba1; W7  ^= t; W7  = rotl(W7 , 1);    B += rotl(C, 5); B += ternary_logic(D, E, A, 0x96); B += W7 ; D = rotl(D, 30)
    t = ternary_logic(W10, W5 , W0 , 0x96); A += 0x6ed9eba1; W8  ^= t; W8  = rotl(W8 , 1);    A += rotl(B, 5); A += ternary_logic(C, D, E, 0x96); A += W8 ; C = rotl(C, 30)
    t = ternary_logic(W11, W6 , W1 , 0x96); E += 0x6ed9eba1; W9  ^= t; W9  = rotl(W9 , 1);    E += rotl(A, 5); E += ternary_logic(B, C, D, 0x96); E += W9 ; B = rotl(B, 30)
    t = ternary_logic(W12, W7 , W2 , 0x96); D += 0x6ed9eba1; W10 ^= t; W10 = rotl(W10, 1);    D += rotl(E, 5); D += ternary_logic(A, B, C, 0x96); D += W10; A = rotl(A, 30)
    t = ternary_logic(W13, W8 , W3 , 0x96); C += 0x6ed9eba1; W11 ^= t; W11 = rotl(W11, 1);    C += rotl(D, 5); C += ternary_logic(E, A, B, 0x96); C += W11; E = rotl(E, 30)
    t = ternary_logic(W14, W9 , W4 , 0x96); B += 0x6ed9eba1; W12 ^= t; W12 = rotl(W12, 1);    B += rotl(C, 5); B += ternary_logic(D, E, A, 0x96); B += W12; D = rotl(D, 30)
    t = ternary_logic(W15, W10, W5 , 0x96); A += 0x6ed9eba1; W13 ^= t; W13 = rotl(W13, 1);    A += rotl(B, 5); A += ternary_logic(C, D, E, 0x96); A += W13; C = rotl(C, 30)
    t = ternary_logic(W0 , W11, W6 , 0x96); E += 0x6ed9eba1; W14 ^= t; W14 = rotl(W14, 1);    E += rotl(A, 5); E += ternary_logic(B, C, D, 0x96); E += W14; B = rotl(B, 30)
    t = ternary_logic(W1 , W12, W7 , 0x96); D += 0x6ed9eba1; W15 ^= t; W15 = rotl(W15, 1);    D += rotl(E, 5); D += ternary_logic(A, B, C, 0x96); D += W15; A = rotl(A, 30)
    t = ternary_logic(W2 , W13, W8 , 0x96); C += 0x6ed9eba1; W0  ^= t; W0  = rotl(W0 , 1);    C += rotl(D, 5); C += ternary_logic(E, A, B, 0x96); C += W0 ; E = rotl(E, 30)
    t = ternary_logic(W3 , W14, W9 , 0x96); B += 0x6ed9eba1; W1  ^= t; W1  = rotl(W1 , 1);    B += rotl(C, 5); B += ternary_logic(D, E, A, 0x96); B += W1 ; D = rotl(D, 30)
    t = ternary_logic(W4 , W15, W10, 0x96); A += 0x6ed9eba1; W2  ^= t; W2  = rotl(W2 , 1);    A += rotl(B, 5); A += ternary_logic(C, D, E, 0x96); A += W2 ; C = rotl(C, 30)
    t = ternary_logic(W5 , W0 , W11, 0x96); E += 0x6ed9eba1; W3  ^= t; W3  = rotl(W3 , 1);    E += rotl(A, 5); E += ternary_logic(B, C, D, 0x96); E += W3 ; B = rotl(B, 30)
    t = ternary_logic(W6 , W1 , W12, 0x96); D += 0x6ed9eba1; W4  ^= t; W4  = rotl(W4 , 1);    D += rotl(E, 5); D += ternary_logic(A, B, C, 0x96); D += W4 ; A = rotl(A, 30)
    t = ternary_logic(W7 , W2 , W13, 0x96); C += 0x6ed9eba1; W5  ^= t; W5  = rotl(W5 , 1);    C += rotl(D, 5); C += ternary_logic(E, A, B, 0x96); C += W5 ; E = rotl(E, 30)
    t = ternary_logic(W8 , W3 , W14, 0x96); B += 0x6ed9eba1; W6  ^= t; W6  = rotl(W6 , 1);    B += rotl(C, 5); B += ternary_logic(D, E, A, 0x96); B += W6 ; D = rotl(D, 30)
    t = ternary_logic(W9 , W4 , W15, 0x96); A += 0x6ed9eba1; W7  ^= t; W7  = rotl(W7 , 1);    A += rotl(B, 5); A += ternary_logic(C, D, E, 0x96); A += W7 ; C = rotl(C, 30)
                                                             
    # Round 3                                                
    t = ternary_logic(W10, W5 , W0 , 0x96); E += 0x8F1BBCDC; W8  ^= t; W8  = rotl(W8 , 1);    E += rotl(A, 5); E += ternary_logic(B, C, D, 0xE8); E += W8 ; B = rotl(B, 30)
    t = ternary_logic(W11, W6 , W1 , 0x96); D += 0x8F1BBCDC; W9  ^= t; W9  = rotl(W9 , 1);    D += rotl(E, 5); D += ternary_logic(A, B, C, 0xE8); D += W9 ; A = rotl(A, 30)
    t = ternary_logic(W12, W7 , W2 , 0x96); C += 0x8F1BBCDC; W10 ^= t; W10 = rotl(W10, 1);    C += rotl(D, 5); C += ternary_logic(E, A, B, 0xE8); C += W10; E = rotl(E, 30)
    t = ternary_logic(W13, W8 , W3 , 0x96); B += 0x8F1BBCDC; W11 ^= t; W11 = rotl(W11, 1);    B += rotl(C, 5); B += ternary_logic(D, E, A, 0xE8); B += W11; D = rotl(D, 30)
    t = ternary_logic(W14, W9 , W4 , 0x96); A += 0x8F1BBCDC; W12 ^= t; W12 = rotl(W12, 1);    A += rotl(B, 5); A += ternary_logic(C, D, E, 0xE8); A += W12; C = rotl(C, 30)
    t = ternary_logic(W15, W10, W5 , 0x96); E += 0x8F1BBCDC; W13 ^= t; W13 = rotl(W13, 1);    E += rotl(A, 5); E += ternary_logic(B, C, D, 0xE8); E += W13; B = rotl(B, 30)
    t = ternary_logic(W0 , W11, W6 , 0x96); D += 0x8F1BBCDC; W14 ^= t; W14 = rotl(W14, 1);    D += rotl(E, 5); D += ternary_logic(A, B, C, 0xE8); D += W14; A = rotl(A, 30)
    t = ternary_logic(W1 , W12, W7 , 0x96); C += 0x8F1BBCDC; W15 ^= t; W15 = rotl(W15, 1);    C += rotl(D, 5); C += ternary_logic(E, A, B, 0xE8); C += W15; E = rotl(E, 30)
    t = ternary_logic(W2 , W13, W8 , 0x96); B += 0x8F1BBCDC; W0  ^= t; W0  = rotl(W0 , 1);    B += rotl(C, 5); B += ternary_logic(D, E, A, 0xE8); B += W0 ; D = rotl(D, 30)
    t = ternary_logic(W3 , W14, W9 , 0x96); A += 0x8F1BBCDC; W1  ^= t; W1  = rotl(W1 , 1);    A += rotl(B, 5); A += ternary_logic(C, D, E, 0xE8); A += W1 ; C = rotl(C, 30)
    t = ternary_logic(W4 , W15, W10, 0x96); E += 0x8F1BBCDC; W2  ^= t; W2  = rotl(W2 , 1);    E += rotl(A, 5); E += ternary_logic(B, C, D, 0xE8); E += W2 ; B = rotl(B, 30)
    t = ternary_logic(W5 , W0 , W11, 0x96); D += 0x8F1BBCDC; W3  ^= t; W3  = rotl(W3 , 1);    D += rotl(E, 5); D += ternary_logic(A, B, C, 0xE8); D += W3 ; A = rotl(A, 30)
    t = ternary_logic(W6 , W1 , W12, 0x96); C += 0x8F1BBCDC; W4  ^= t; W4  = rotl(W4 , 1);    C += rotl(D, 5); C += ternary_logic(E, A, B, 0xE8); C += W4 ; E = rotl(E, 30)
    t = ternary_logic(W7 , W2 , W13, 0x96); B += 0x8F1BBCDC; W5  ^= t; W5  = rotl(W5 , 1);    B += rotl(C, 5); B += ternary_logic(D, E, A, 0xE8); B += W5 ; D = rotl(D, 30)
    t = ternary_logic(W8 , W3 , W14, 0x96); A += 0x8F1BBCDC; W6  ^= t; W6  = rotl(W6 , 1);    A += rotl(B, 5); A += ternary_logic(C, D, E, 0xE8); A += W6 ; C = rotl(C, 30)
    t = ternary_logic(W9 , W4 , W15, 0x96); E += 0x8F1BBCDC; W7  ^= t; W7  = rotl(W7 , 1);    E += rotl(A, 5); E += ternary_logic(B, C, D, 0xE8); E += W7 ; B = rotl(B, 30)
    t = ternary_logic(W10, W5 , W0 , 0x96); D += 0x8F1BBCDC; W8  ^= t; W8  = rotl(W8 , 1);    D += rotl(E, 5); D += ternary_logic(A, B, C, 0xE8); D += W8 ; A = rotl(A, 30)
    t = ternary_logic(W11, W6 , W1 , 0x96); C += 0x8F1BBCDC; W9  ^= t; W9  = rotl(W9 , 1);    C += rotl(D, 5); C += ternary_logic(E, A, B, 0xE8); C += W9 ; E = rotl(E, 30)
    t = ternary_logic(W12, W7 , W2 , 0x96); B += 0x8F1BBCDC; W10 ^= t; W10 = rotl(W10, 1);    B += rotl(C, 5); B += ternary_logic(D, E, A, 0xE8); B += W10; D = rotl(D, 30)
    t = ternary_logic(W13, W8 , W3 , 0x96); A += 0x8F1BBCDC; W11 ^= t; W11 = rotl(W11, 1);    A += rotl(B, 5); A += ternary_logic(C, D, E, 0xE8); A += W11; C = rotl(C, 30)
                                                             
    # Round 4                                                
    t = ternary_logic(W14, W9 , W4 , 0x96); E += 0xCA62C1D6; W12 ^= t; W12 = rotl(W12, 1);    E += rotl(A, 5); E += ternary_logic(B, C, D, 0x96); E += W12; B = rotl(B, 30)
    t = ternary_logic(W15, W10, W5 , 0x96); D += 0xCA62C1D6; W13 ^= t; W13 = rotl(W13, 1);    D += rotl(E, 5); D += ternary_logic(A, B, C, 0x96); D += W13; A = rotl(A, 30)
    t = ternary_logic(W0 , W11, W6 , 0x96); C += 0xCA62C1D6; W14 ^= t; W14 = rotl(W14, 1);    C += rotl(D, 5); C += ternary_logic(E, A, B, 0x96); C += W14; E = rotl(E, 30)
    t = ternary_logic(W1 , W12, W7 , 0x96); B += 0xCA62C1D6; W15 ^= t; W15 = rotl(W15, 1);    B += rotl(C, 5); B += ternary_logic(D, E, A, 0x96); B += W15; D = rotl(D, 30)
    t = ternary_logic(W2 , W13, W8 , 0x96); A += 0xCA62C1D6; W0  ^= t; W0  = rotl(W0 , 1);    A += rotl(B, 5); A += ternary_logic(C, D, E, 0x96); A += W0 ; C = rotl(C, 30)
    t = ternary_logic(W3 , W14, W9 , 0x96); E += 0xCA62C1D6; W1  ^= t; W1  = rotl(W1 , 1);    E += rotl(A, 5); E += ternary_logic(B, C, D, 0x96); E += W1 ; B = rotl(B, 30)
    t = ternary_logic(W4 , W15, W10, 0x96); D += 0xCA62C1D6; W2  ^= t; W2  = rotl(W2 , 1);    D += rotl(E, 5); D += ternary_logic(A, B, C, 0x96); D += W2 ; A = rotl(A, 30)
    t = ternary_logic(W5 , W0 , W11, 0x96); C += 0xCA62C1D6; W3  ^= t; W3  = rotl(W3 , 1);    C += rotl(D, 5); C += ternary_logic(E, A, B, 0x96); C += W3 ; E = rotl(E, 30)
    t = ternary_logic(W6 , W1 , W12, 0x96); B += 0xCA62C1D6; W4  ^= t; W4  = rotl(W4 , 1);    B += rotl(C, 5); B += ternary_logic(D, E, A, 0x96); B += W4 ; D = rotl(D, 30)
    t = ternary_logic(W7 , W2 , W13, 0x96); A += 0xCA62C1D6; W5  ^= t; W5  = rotl(W5 , 1);    A += rotl(B, 5); A += ternary_logic(C, D, E, 0x96); A += W5 ; C = rotl(C, 30)
    t = ternary_logic(W8 , W3 , W14, 0x96); E += 0xCA62C1D6; W6  ^= t; W6  = rotl(W6 , 1);    E += rotl(A, 5); E += ternary_logic(B, C, D, 0x96); E += W6 ; B = rotl(B, 30)
    t = ternary_logic(W9 , W4 , W15, 0x96); D += 0xCA62C1D6; W7  ^= t; W7  = rotl(W7 , 1);    D += rotl(E, 5); D += ternary_logic(A, B, C, 0x96); D += W7 ; A = rotl(A, 30)
    t = ternary_logic(W10, W5 , W0 , 0x96); C += 0xCA62C1D6; W8  ^= t; W8  = rotl(W8 , 1);    C += rotl(D, 5); C += ternary_logic(E, A, B, 0x96); C += W8 ; E = rotl(E, 30)
    t = ternary_logic(W11, W6 , W1 , 0x96); B += 0xCA62C1D6; W9  ^= t; W9  = rotl(W9 , 1);    B += rotl(C, 5); B += ternary_logic(D, E, A, 0x96); B += W9 ; D = rotl(D, 30)
    t = ternary_logic(W12, W7 , W2 , 0x96); A += 0xCA62C1D6; W10 ^= t; W10 = rotl(W10, 1);    A += rotl(B, 5); A += ternary_logic(C, D, E, 0x96); A += W10; C = rotl(C, 30)
    t = ternary_logic(W13, W8 , W3 , 0x96); E += 0xCA62C1D6; W11 ^= t; W11 = rotl(W11, 1);    E += rotl(A, 5); E += ternary_logic(B, C, D, 0x96); E += W11; B = rotl(B, 30)
    t = ternary_logic(W14, W9 , W4 , 0x96); D += 0xCA62C1D6; W12 ^= t; W12 = rotl(W12, 1);    D += rotl(E, 5); D += ternary_logic(A, B, C, 0x96); D += W12; A = rotl(A, 30)
    t = ternary_logic(W15, W10, W5 , 0x96); C += 0xCA62C1D6; W13 ^= t; W13 = rotl(W13, 1);    C += rotl(D, 5); C += ternary_logic(E, A, B, 0x96); C += W13; E = rotl(E, 30)
    t = ternary_logic(W0 , W11, W6 , 0x96); B += 0xCA62C1D6; W14 ^= t; W14 = rotl(W14, 1);    B += rotl(C, 5); B += ternary_logic(D, E, A, 0x96); B += W14; D = rotl(D, 30)
    t = ternary_logic(W1 , W12, W7 , 0x96); A += 0xCA62C1D6; W15 ^= t; W15 = rotl(W15, 1);    A += rotl(B, 5); A += ternary_logic(C, D, E, 0x96); A += W15; C = rotl(C, 30)

    # Save state
    state[4] += E
    state[3] += D
    state[2] += C
    state[1] += B
    state[0] += A
    
# Define targets
sha1_block.targets  = [Target.PLAIN_C, Target.SSE2, Target.AVX, Target.AVX2, Target.AVX512]
# Build and run
generate_code()
build_and_run('C:/Program Files/CMake/bin/cmake.exe', run_benchmark=True, run_tests=True, 
              sde_test_cpus=['-knm'], 
              sde_exe='C:/Users/Alain/Downloads/sde-external-9.33.0-2024-01-07-win/sde.exe')
