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
    E += rotl(A, 5); E += D ^ (B & (C ^ D)); E += 0x5a827999; E += W0 ; B = rotl(B, 30);
    D += rotl(E, 5); D += C ^ (A & (B ^ C)); D += 0x5a827999; D += W1 ; A = rotl(A, 30);
    C += rotl(D, 5); C += B ^ (E & (A ^ B)); C += 0x5a827999; C += W2 ; E = rotl(E, 30);
    B += rotl(C, 5); B += A ^ (D & (E ^ A)); B += 0x5a827999; B += W3 ; D = rotl(D, 30);
    A += rotl(B, 5); A += E ^ (C & (D ^ E)); A += 0x5a827999; A += W4 ; C = rotl(C, 30);
    E += rotl(A, 5); E += D ^ (B & (C ^ D)); E += 0x5a827999; E += W5 ; B = rotl(B, 30);
    D += rotl(E, 5); D += C ^ (A & (B ^ C)); D += 0x5a827999; D += W6 ; A = rotl(A, 30);
    C += rotl(D, 5); C += B ^ (E & (A ^ B)); C += 0x5a827999; C += W7 ; E = rotl(E, 30);
    B += rotl(C, 5); B += A ^ (D & (E ^ A)); B += 0x5a827999; B += W8 ; D = rotl(D, 30);
    A += rotl(B, 5); A += E ^ (C & (D ^ E)); A += 0x5a827999; A += W9 ; C = rotl(C, 30);
    E += rotl(A, 5); E += D ^ (B & (C ^ D)); E += 0x5a827999; E += W10; B = rotl(B, 30);
    D += rotl(E, 5); D += C ^ (A & (B ^ C)); D += 0x5a827999; D += W11; A = rotl(A, 30);
    C += rotl(D, 5); C += B ^ (E & (A ^ B)); C += 0x5a827999; C += W12; E = rotl(E, 30);
    B += rotl(C, 5); B += A ^ (D & (E ^ A)); B += 0x5a827999; B += W13; D = rotl(D, 30);
    A += rotl(B, 5); A += E ^ (C & (D ^ E)); A += 0x5a827999; A += W14; C = rotl(C, 30);
    E += rotl(A, 5); E += D ^ (B & (C ^ D)); E += 0x5a827999; E += W15; B = rotl(B, 30);
    W0  ^= W13; W0  ^= W8 ; W0  ^= W2 ; W0  = rotl(W0 , 1);    D += rotl(E, 5); D += C ^ (A & (B ^ C)); D += 0x5a827999; D += W0; A = rotl(A, 30);
    W1  ^= W14; W1  ^= W9 ; W1  ^= W3 ; W1  = rotl(W1 , 1);    C += rotl(D, 5); C += B ^ (E & (A ^ B)); C += 0x5a827999; C += W1; E = rotl(E, 30);
    W2  ^= W15; W2  ^= W10; W2  ^= W4 ; W2  = rotl(W2 , 1);    B += rotl(C, 5); B += A ^ (D & (E ^ A)); B += 0x5a827999; B += W2; D = rotl(D, 30);
    W3  ^= W0 ; W3  ^= W11; W3  ^= W5 ; W3  = rotl(W3 , 1);    A += rotl(B, 5); A += E ^ (C & (D ^ E)); A += 0x5a827999; A += W3; C = rotl(C, 30);
    
    # Round 2
    W4  ^= W1 ; W4  ^= W12; W4  ^= W6 ; W4  = rotl(W4 , 1);    E += rotl(A, 5); E += (B ^ C ^ D); E += 0x6ed9eba1; E += W4 ; B = rotl(B, 30);
    W5  ^= W2 ; W5  ^= W13; W5  ^= W7 ; W5  = rotl(W5 , 1);    D += rotl(E, 5); D += (A ^ B ^ C); D += 0x6ed9eba1; D += W5 ; A = rotl(A, 30);
    W6  ^= W3 ; W6  ^= W14; W6  ^= W8 ; W6  = rotl(W6 , 1);    C += rotl(D, 5); C += (E ^ A ^ B); C += 0x6ed9eba1; C += W6 ; E = rotl(E, 30);
    W7  ^= W4 ; W7  ^= W15; W7  ^= W9 ; W7  = rotl(W7 , 1);    B += rotl(C, 5); B += (D ^ E ^ A); B += 0x6ed9eba1; B += W7 ; D = rotl(D, 30);
    W8  ^= W5 ; W8  ^= W0 ; W8  ^= W10; W8  = rotl(W8 , 1);    A += rotl(B, 5); A += (C ^ D ^ E); A += 0x6ed9eba1; A += W8 ; C = rotl(C, 30);
    W9  ^= W6 ; W9  ^= W1 ; W9  ^= W11; W9  = rotl(W9 , 1);    E += rotl(A, 5); E += (B ^ C ^ D); E += 0x6ed9eba1; E += W9 ; B = rotl(B, 30);
    W10 ^= W7 ; W10 ^= W2 ; W10 ^= W12; W10 = rotl(W10, 1);    D += rotl(E, 5); D += (A ^ B ^ C); D += 0x6ed9eba1; D += W10; A = rotl(A, 30);
    W11 ^= W8 ; W11 ^= W3 ; W11 ^= W13; W11 = rotl(W11, 1);    C += rotl(D, 5); C += (E ^ A ^ B); C += 0x6ed9eba1; C += W11; E = rotl(E, 30);
    W12 ^= W9 ; W12 ^= W4 ; W12 ^= W14; W12 = rotl(W12, 1);    B += rotl(C, 5); B += (D ^ E ^ A); B += 0x6ed9eba1; B += W12; D = rotl(D, 30);
    W13 ^= W10; W13 ^= W5 ; W13 ^= W15; W13 = rotl(W13, 1);    A += rotl(B, 5); A += (C ^ D ^ E); A += 0x6ed9eba1; A += W13; C = rotl(C, 30);
    W14 ^= W11; W14 ^= W6 ; W14 ^= W0 ; W14 = rotl(W14, 1);    E += rotl(A, 5); E += (B ^ C ^ D); E += 0x6ed9eba1; E += W14; B = rotl(B, 30);
    W15 ^= W12; W15 ^= W7 ; W15 ^= W1 ; W15 = rotl(W15, 1);    D += rotl(E, 5); D += (A ^ B ^ C); D += 0x6ed9eba1; D += W15; A = rotl(A, 30);
    W0  ^= W13; W0  ^= W8 ; W0  ^= W2 ; W0  = rotl(W0 , 1);    C += rotl(D, 5); C += (E ^ A ^ B); C += 0x6ed9eba1; C += W0 ; E = rotl(E, 30);
    W1  ^= W14; W1  ^= W9 ; W1  ^= W3 ; W1  = rotl(W1 , 1);    B += rotl(C, 5); B += (D ^ E ^ A); B += 0x6ed9eba1; B += W1 ; D = rotl(D, 30);
    W2  ^= W15; W2  ^= W10; W2  ^= W4 ; W2  = rotl(W2 , 1);    A += rotl(B, 5); A += (C ^ D ^ E); A += 0x6ed9eba1; A += W2 ; C = rotl(C, 30);
    W3  ^= W0 ; W3  ^= W11; W3  ^= W5 ; W3  = rotl(W3 , 1);    E += rotl(A, 5); E += (B ^ C ^ D); E += 0x6ed9eba1; E += W3 ; B = rotl(B, 30);
    W4  ^= W1 ; W4  ^= W12; W4  ^= W6 ; W4  = rotl(W4 , 1);    D += rotl(E, 5); D += (A ^ B ^ C); D += 0x6ed9eba1; D += W4 ; A = rotl(A, 30);
    W5  ^= W2 ; W5  ^= W13; W5  ^= W7 ; W5  = rotl(W5 , 1);    C += rotl(D, 5); C += (E ^ A ^ B); C += 0x6ed9eba1; C += W5 ; E = rotl(E, 30);
    W6  ^= W3 ; W6  ^= W14; W6  ^= W8 ; W6  = rotl(W6 , 1);    B += rotl(C, 5); B += (D ^ E ^ A); B += 0x6ed9eba1; B += W6 ; D = rotl(D, 30);
    W7  ^= W4 ; W7  ^= W15; W7  ^= W9 ; W7  = rotl(W7 , 1);    A += rotl(B, 5); A += (C ^ D ^ E); A += 0x6ed9eba1; A += W7 ; C = rotl(C, 30);
    
    # Round 3
    W8  ^= W5 ; W8  ^= W0 ; W8  ^= W10; W8  = rotl(W8 , 1);    E += rotl(A, 5); E += ((B & C) | (D & (B | C))); E += 0x8F1BBCDC; E += W8 ; B = rotl(B, 30);
    W9  ^= W6 ; W9  ^= W1 ; W9  ^= W11; W9  = rotl(W9 , 1);    D += rotl(E, 5); D += ((A & B) | (C & (A | B))); D += 0x8F1BBCDC; D += W9 ; A = rotl(A, 30);
    W10 ^= W7 ; W10 ^= W2 ; W10 ^= W12; W10 = rotl(W10, 1);    C += rotl(D, 5); C += ((E & A) | (B & (E | A))); C += 0x8F1BBCDC; C += W10; E = rotl(E, 30);
    W11 ^= W8 ; W11 ^= W3 ; W11 ^= W13; W11 = rotl(W11, 1);    B += rotl(C, 5); B += ((D & E) | (A & (D | E))); B += 0x8F1BBCDC; B += W11; D = rotl(D, 30);
    W12 ^= W9 ; W12 ^= W4 ; W12 ^= W14; W12 = rotl(W12, 1);    A += rotl(B, 5); A += ((C & D) | (E & (C | D))); A += 0x8F1BBCDC; A += W12; C = rotl(C, 30);
    W13 ^= W10; W13 ^= W5 ; W13 ^= W15; W13 = rotl(W13, 1);    E += rotl(A, 5); E += ((B & C) | (D & (B | C))); E += 0x8F1BBCDC; E += W13; B = rotl(B, 30);
    W14 ^= W11; W14 ^= W6 ; W14 ^= W0 ; W14 = rotl(W14, 1);    D += rotl(E, 5); D += ((A & B) | (C & (A | B))); D += 0x8F1BBCDC; D += W14; A = rotl(A, 30);
    W15 ^= W12; W15 ^= W7 ; W15 ^= W1 ; W15 = rotl(W15, 1);    C += rotl(D, 5); C += ((E & A) | (B & (E | A))); C += 0x8F1BBCDC; C += W15; E = rotl(E, 30);
    W0  ^= W13; W0  ^= W8 ; W0  ^= W2 ; W0  = rotl(W0 , 1);    B += rotl(C, 5); B += ((D & E) | (A & (D | E))); B += 0x8F1BBCDC; B += W0 ; D = rotl(D, 30);
    W1  ^= W14; W1  ^= W9 ; W1  ^= W3 ; W1  = rotl(W1 , 1);    A += rotl(B, 5); A += ((C & D) | (E & (C | D))); A += 0x8F1BBCDC; A += W1 ; C = rotl(C, 30);
    W2  ^= W15; W2  ^= W10; W2  ^= W4 ; W2  = rotl(W2 , 1);    E += rotl(A, 5); E += ((B & C) | (D & (B | C))); E += 0x8F1BBCDC; E += W2 ; B = rotl(B, 30);
    W3  ^= W0 ; W3  ^= W11; W3  ^= W5 ; W3  = rotl(W3 , 1);    D += rotl(E, 5); D += ((A & B) | (C & (A | B))); D += 0x8F1BBCDC; D += W3 ; A = rotl(A, 30);
    W4  ^= W1 ; W4  ^= W12; W4  ^= W6 ; W4  = rotl(W4 , 1);    C += rotl(D, 5); C += ((E & A) | (B & (E | A))); C += 0x8F1BBCDC; C += W4 ; E = rotl(E, 30);
    W5  ^= W2 ; W5  ^= W13; W5  ^= W7 ; W5  = rotl(W5 , 1);    B += rotl(C, 5); B += ((D & E) | (A & (D | E))); B += 0x8F1BBCDC; B += W5 ; D = rotl(D, 30);
    W6  ^= W3 ; W6  ^= W14; W6  ^= W8 ; W6  = rotl(W6 , 1);    A += rotl(B, 5); A += ((C & D) | (E & (C | D))); A += 0x8F1BBCDC; A += W6 ; C = rotl(C, 30);
    W7  ^= W4 ; W7  ^= W15; W7  ^= W9 ; W7  = rotl(W7 , 1);    E += rotl(A, 5); E += ((B & C) | (D & (B | C))); E += 0x8F1BBCDC; E += W7 ; B = rotl(B, 30);
    W8  ^= W5 ; W8  ^= W0 ; W8  ^= W10; W8  = rotl(W8 , 1);    D += rotl(E, 5); D += ((A & B) | (C & (A | B))); D += 0x8F1BBCDC; D += W8 ; A = rotl(A, 30);
    W9  ^= W6 ; W9  ^= W1 ; W9  ^= W11; W9  = rotl(W9 , 1);    C += rotl(D, 5); C += ((E & A) | (B & (E | A))); C += 0x8F1BBCDC; C += W9 ; E = rotl(E, 30);
    W10 ^= W7 ; W10 ^= W2 ; W10 ^= W12; W10 = rotl(W10, 1);    B += rotl(C, 5); B += ((D & E) | (A & (D | E))); B += 0x8F1BBCDC; B += W10; D = rotl(D, 30);
    W11 ^= W8 ; W11 ^= W3 ; W11 ^= W13; W11 = rotl(W11, 1);    A += rotl(B, 5); A += ((C & D) | (E & (C | D))); A += 0x8F1BBCDC; A += W11; C = rotl(C, 30);
    
    # Round 4
    W12 ^= W9 ; W12 ^= W4 ; W12 ^= W14; W12 = rotl(W12, 1);    E += rotl(A, 5); E += (B ^ C ^ D); E += 0xCA62C1D6; E += W12; B = rotl(B, 30);
    W13 ^= W10; W13 ^= W5 ; W13 ^= W15; W13 = rotl(W13, 1);    D += rotl(E, 5); D += (A ^ B ^ C); D += 0xCA62C1D6; D += W13; A = rotl(A, 30);
    W14 ^= W11; W14 ^= W6 ; W14 ^= W0 ; W14 = rotl(W14, 1);    C += rotl(D, 5); C += (E ^ A ^ B); C += 0xCA62C1D6; C += W14; E = rotl(E, 30);
    W15 ^= W12; W15 ^= W7 ; W15 ^= W1 ; W15 = rotl(W15, 1);    B += rotl(C, 5); B += (D ^ E ^ A); B += 0xCA62C1D6; B += W15; D = rotl(D, 30);
    W0  ^= W13; W0  ^= W8 ; W0  ^= W2 ; W0  = rotl(W0 , 1);    A += rotl(B, 5); A += (C ^ D ^ E); A += 0xCA62C1D6; A += W0 ; C = rotl(C, 30);
    W1  ^= W14; W1  ^= W9 ; W1  ^= W3 ; W1  = rotl(W1 , 1);    E += rotl(A, 5); E += (B ^ C ^ D); E += 0xCA62C1D6; E += W1 ; B = rotl(B, 30);
    W2  ^= W15; W2  ^= W10; W2  ^= W4 ; W2  = rotl(W2 , 1);    D += rotl(E, 5); D += (A ^ B ^ C); D += 0xCA62C1D6; D += W2 ; A = rotl(A, 30);
    W3  ^= W0 ; W3  ^= W11; W3  ^= W5 ; W3  = rotl(W3 , 1);    C += rotl(D, 5); C += (E ^ A ^ B); C += 0xCA62C1D6; C += W3 ; E = rotl(E, 30);
    W4  ^= W1 ; W4  ^= W12; W4  ^= W6 ; W4  = rotl(W4 , 1);    B += rotl(C, 5); B += (D ^ E ^ A); B += 0xCA62C1D6; B += W4 ; D = rotl(D, 30);
    W5  ^= W2 ; W5  ^= W13; W5  ^= W7 ; W5  = rotl(W5 , 1);    A += rotl(B, 5); A += (C ^ D ^ E); A += 0xCA62C1D6; A += W5 ; C = rotl(C, 30);
    W6  ^= W3 ; W6  ^= W14; W6  ^= W8 ; W6  = rotl(W6 , 1);    E += rotl(A, 5); E += (B ^ C ^ D); E += 0xCA62C1D6; E += W6 ; B = rotl(B, 30);
    W7  ^= W4 ; W7  ^= W15; W7  ^= W9 ; W7  = rotl(W7 , 1);    D += rotl(E, 5); D += (A ^ B ^ C); D += 0xCA62C1D6; D += W7 ; A = rotl(A, 30);
    W8  ^= W5 ; W8  ^= W0 ; W8  ^= W10; W8  = rotl(W8 , 1);    C += rotl(D, 5); C += (E ^ A ^ B); C += 0xCA62C1D6; C += W8 ; E = rotl(E, 30);
    W9  ^= W6 ; W9  ^= W1 ; W9  ^= W11; W9  = rotl(W9 , 1);    B += rotl(C, 5); B += (D ^ E ^ A); B += 0xCA62C1D6; B += W9 ; D = rotl(D, 30);
    W10 ^= W7 ; W10 ^= W2 ; W10 ^= W12; W10 = rotl(W10, 1);    A += rotl(B, 5); A += (C ^ D ^ E); A += 0xCA62C1D6; A += W10; C = rotl(C, 30);
    W11 ^= W8 ; W11 ^= W3 ; W11 ^= W13; W11 = rotl(W11, 1);    E += rotl(A, 5); E += (B ^ C ^ D); E += 0xCA62C1D6; E += W11; B = rotl(B, 30);
    W12 ^= W9 ; W12 ^= W4 ; W12 ^= W14; W12 = rotl(W12, 1);    D += rotl(E, 5); D += (A ^ B ^ C); D += 0xCA62C1D6; D += W12; A = rotl(A, 30);
    W13 ^= W10; W13 ^= W5 ; W13 ^= W15; W13 = rotl(W13, 1);    C += rotl(D, 5); C += (E ^ A ^ B); C += 0xCA62C1D6; C += W13; E = rotl(E, 30);
    W14 ^= W11; W14 ^= W6 ; W14 ^= W0 ; W14 = rotl(W14, 1);    B += rotl(C, 5); B += (D ^ E ^ A); B += 0xCA62C1D6; B += W14; D = rotl(D, 30);
    W15 ^= W12; W15 ^= W7 ; W15 ^= W1 ; W15 = rotl(W15, 1);    A += rotl(B, 5); A += (C ^ D ^ E); A += 0xCA62C1D6; A += W15; C = rotl(C, 30);

    # Save state
    state[0] += A
    state[1] += B
    state[2] += C
    state[3] += D
    state[4] += E

with Function(void)(state, W) as sha1_block_:
    # Load state
    A, B, C, D, E = state[0], state[1], state[2], state[3], state[4]
    W0 , W1 , W2 , W3  = W[ 0], W[ 1], W[ 2], W[ 3]
    W4 , W5 , W6 , W7  = W[ 4], W[ 5], W[ 6], W[ 7]
    W8 , W9 , W10, W11 = W[ 8], W[ 9], W[10], W[11]
    W12, W13, W14, W15 = W[12], W[13], W[14], W[15]

    # Round 1
    E += rotl(A, 5); E += ternary_logic(D, C, B, 0xd8); E += 0x5a827999; E += W0 ; B = rotl(B, 30);
    D += rotl(E, 5); D += ternary_logic(C, B, A, 0xd8); D += 0x5a827999; D += W1 ; A = rotl(A, 30);
    C += rotl(D, 5); C += ternary_logic(B, A, E, 0xd8); C += 0x5a827999; C += W2 ; E = rotl(E, 30);
    B += rotl(C, 5); B += ternary_logic(A, E, D, 0xd8); B += 0x5a827999; B += W3 ; D = rotl(D, 30);
    A += rotl(B, 5); A += ternary_logic(E, D, C, 0xd8); A += 0x5a827999; A += W4 ; C = rotl(C, 30);
    E += rotl(A, 5); E += ternary_logic(D, C, B, 0xd8); E += 0x5a827999; E += W5 ; B = rotl(B, 30);
    D += rotl(E, 5); D += ternary_logic(C, B, A, 0xd8); D += 0x5a827999; D += W6 ; A = rotl(A, 30);
    C += rotl(D, 5); C += ternary_logic(B, A, E, 0xd8); C += 0x5a827999; C += W7 ; E = rotl(E, 30);
    B += rotl(C, 5); B += ternary_logic(A, E, D, 0xd8); B += 0x5a827999; B += W8 ; D = rotl(D, 30);
    A += rotl(B, 5); A += ternary_logic(E, D, C, 0xd8); A += 0x5a827999; A += W9 ; C = rotl(C, 30);
    E += rotl(A, 5); E += ternary_logic(D, C, B, 0xd8); E += 0x5a827999; E += W10; B = rotl(B, 30);
    D += rotl(E, 5); D += ternary_logic(C, B, A, 0xd8); D += 0x5a827999; D += W11; A = rotl(A, 30);
    C += rotl(D, 5); C += ternary_logic(B, A, E, 0xd8); C += 0x5a827999; C += W12; E = rotl(E, 30);
    B += rotl(C, 5); B += ternary_logic(A, E, D, 0xd8); B += 0x5a827999; B += W13; D = rotl(D, 30);
    A += rotl(B, 5); A += ternary_logic(E, D, C, 0xd8); A += 0x5a827999; A += W14; C = rotl(C, 30);
    E += rotl(A, 5); E += ternary_logic(D, C, B, 0xd8); E += 0x5a827999; E += W15; B = rotl(B, 30);
    W0  = ternary_logic(W0 , W13, W8 , 0x96); W0  ^= W2 ; W0  = rotl(W0 , 1);    D += rotl(E, 5); D += ternary_logic(C, B, A, 0xd8); D += 0x5a827999; D += W0; A = rotl(A, 30);
    W1  = ternary_logic(W1 , W14, W9 , 0x96); W1  ^= W3 ; W1  = rotl(W1 , 1);    C += rotl(D, 5); C += ternary_logic(B, A, E, 0xd8); C += 0x5a827999; C += W1; E = rotl(E, 30);
    W2  = ternary_logic(W2 , W15, W10, 0x96); W2  ^= W4 ; W2  = rotl(W2 , 1);    B += rotl(C, 5); B += ternary_logic(A, E, D, 0xd8); B += 0x5a827999; B += W2; D = rotl(D, 30);
    W3  = ternary_logic(W3 , W0 , W11, 0x96); W3  ^= W5 ; W3  = rotl(W3 , 1);    A += rotl(B, 5); A += ternary_logic(E, D, C, 0xd8); A += 0x5a827999; A += W3; C = rotl(C, 30);
    
    # Round 2
    W4  = ternary_logic(W4 , W1 , W12, 0x96); W4  ^= W6 ; W4  = rotl(W4 , 1);    E += rotl(A, 5); E += ternary_logic(B, C, D, 0x96); E += 0x6ed9eba1; E += W4 ; B = rotl(B, 30);
    W5  = ternary_logic(W5 , W2 , W13, 0x96); W5  ^= W7 ; W5  = rotl(W5 , 1);    D += rotl(E, 5); D += ternary_logic(A, B, C, 0x96); D += 0x6ed9eba1; D += W5 ; A = rotl(A, 30);
    W6  = ternary_logic(W6 , W3 , W14, 0x96); W6  ^= W8 ; W6  = rotl(W6 , 1);    C += rotl(D, 5); C += ternary_logic(E, A, B, 0x96); C += 0x6ed9eba1; C += W6 ; E = rotl(E, 30);
    W7  = ternary_logic(W7 , W4 , W15, 0x96); W7  ^= W9 ; W7  = rotl(W7 , 1);    B += rotl(C, 5); B += ternary_logic(D, E, A, 0x96); B += 0x6ed9eba1; B += W7 ; D = rotl(D, 30);
    W8  = ternary_logic(W8 , W5 , W0 , 0x96); W8  ^= W10; W8  = rotl(W8 , 1);    A += rotl(B, 5); A += ternary_logic(C, D, E, 0x96); A += 0x6ed9eba1; A += W8 ; C = rotl(C, 30);
    W9  = ternary_logic(W9 , W6 , W1 , 0x96); W9  ^= W11; W9  = rotl(W9 , 1);    E += rotl(A, 5); E += ternary_logic(B, C, D, 0x96); E += 0x6ed9eba1; E += W9 ; B = rotl(B, 30);
    W10 = ternary_logic(W10, W7 , W2 , 0x96); W10 ^= W12; W10 = rotl(W10, 1);    D += rotl(E, 5); D += ternary_logic(A, B, C, 0x96); D += 0x6ed9eba1; D += W10; A = rotl(A, 30);
    W11 = ternary_logic(W11, W8 , W3 , 0x96); W11 ^= W13; W11 = rotl(W11, 1);    C += rotl(D, 5); C += ternary_logic(E, A, B, 0x96); C += 0x6ed9eba1; C += W11; E = rotl(E, 30);
    W12 = ternary_logic(W12, W9 , W4 , 0x96); W12 ^= W14; W12 = rotl(W12, 1);    B += rotl(C, 5); B += ternary_logic(D, E, A, 0x96); B += 0x6ed9eba1; B += W12; D = rotl(D, 30);
    W13 = ternary_logic(W13, W10, W5 , 0x96); W13 ^= W15; W13 = rotl(W13, 1);    A += rotl(B, 5); A += ternary_logic(C, D, E, 0x96); A += 0x6ed9eba1; A += W13; C = rotl(C, 30);
    W14 = ternary_logic(W14, W11, W6 , 0x96); W14 ^= W0 ; W14 = rotl(W14, 1);    E += rotl(A, 5); E += ternary_logic(B, C, D, 0x96); E += 0x6ed9eba1; E += W14; B = rotl(B, 30);
    W15 = ternary_logic(W15, W12, W7 , 0x96); W15 ^= W1 ; W15 = rotl(W15, 1);    D += rotl(E, 5); D += ternary_logic(A, B, C, 0x96); D += 0x6ed9eba1; D += W15; A = rotl(A, 30);
    W0  = ternary_logic(W0 , W13, W8 , 0x96); W0  ^= W2 ; W0  = rotl(W0 , 1);    C += rotl(D, 5); C += ternary_logic(E, A, B, 0x96); C += 0x6ed9eba1; C += W0 ; E = rotl(E, 30);
    W1  = ternary_logic(W1 , W14, W9 , 0x96); W1  ^= W3 ; W1  = rotl(W1 , 1);    B += rotl(C, 5); B += ternary_logic(D, E, A, 0x96); B += 0x6ed9eba1; B += W1 ; D = rotl(D, 30);
    W2  = ternary_logic(W2 , W15, W10, 0x96); W2  ^= W4 ; W2  = rotl(W2 , 1);    A += rotl(B, 5); A += ternary_logic(C, D, E, 0x96); A += 0x6ed9eba1; A += W2 ; C = rotl(C, 30);
    W3  = ternary_logic(W3 , W0 , W11, 0x96); W3  ^= W5 ; W3  = rotl(W3 , 1);    E += rotl(A, 5); E += ternary_logic(B, C, D, 0x96); E += 0x6ed9eba1; E += W3 ; B = rotl(B, 30);
    W4  = ternary_logic(W4 , W1 , W12, 0x96); W4  ^= W6 ; W4  = rotl(W4 , 1);    D += rotl(E, 5); D += ternary_logic(A, B, C, 0x96); D += 0x6ed9eba1; D += W4 ; A = rotl(A, 30);
    W5  = ternary_logic(W5 , W2 , W13, 0x96); W5  ^= W7 ; W5  = rotl(W5 , 1);    C += rotl(D, 5); C += ternary_logic(E, A, B, 0x96); C += 0x6ed9eba1; C += W5 ; E = rotl(E, 30);
    W6  = ternary_logic(W6 , W3 , W14, 0x96); W6  ^= W8 ; W6  = rotl(W6 , 1);    B += rotl(C, 5); B += ternary_logic(D, E, A, 0x96); B += 0x6ed9eba1; B += W6 ; D = rotl(D, 30);
    W7  = ternary_logic(W7 , W4 , W15, 0x96); W7  ^= W9 ; W7  = rotl(W7 , 1);    A += rotl(B, 5); A += ternary_logic(C, D, E, 0x96); A += 0x6ed9eba1; A += W7 ; C = rotl(C, 30);
    
    # Round 3
    W8  = ternary_logic(W8 , W5 , W0 , 0x96); W8  ^= W10; W8  = rotl(W8 , 1);    E += rotl(A, 5); E += ternary_logic(B, C, D, 0xE8); E += 0x8F1BBCDC; E += W8 ; B = rotl(B, 30);
    W9  = ternary_logic(W9 , W6 , W1 , 0x96); W9  ^= W11; W9  = rotl(W9 , 1);    D += rotl(E, 5); D += ternary_logic(A, B, C, 0xE8); D += 0x8F1BBCDC; D += W9 ; A = rotl(A, 30);
    W10 = ternary_logic(W10, W7 , W2 , 0x96); W10 ^= W12; W10 = rotl(W10, 1);    C += rotl(D, 5); C += ternary_logic(E, A, B, 0xE8); C += 0x8F1BBCDC; C += W10; E = rotl(E, 30);
    W11 = ternary_logic(W11, W8 , W3 , 0x96); W11 ^= W13; W11 = rotl(W11, 1);    B += rotl(C, 5); B += ternary_logic(D, E, A, 0xE8); B += 0x8F1BBCDC; B += W11; D = rotl(D, 30);
    W12 = ternary_logic(W12, W9 , W4 , 0x96); W12 ^= W14; W12 = rotl(W12, 1);    A += rotl(B, 5); A += ternary_logic(C, D, E, 0xE8); A += 0x8F1BBCDC; A += W12; C = rotl(C, 30);
    W13 = ternary_logic(W13, W10, W5 , 0x96); W13 ^= W15; W13 = rotl(W13, 1);    E += rotl(A, 5); E += ternary_logic(B, C, D, 0xE8); E += 0x8F1BBCDC; E += W13; B = rotl(B, 30);
    W14 = ternary_logic(W14, W11, W6 , 0x96); W14 ^= W0 ; W14 = rotl(W14, 1);    D += rotl(E, 5); D += ternary_logic(A, B, C, 0xE8); D += 0x8F1BBCDC; D += W14; A = rotl(A, 30);
    W15 = ternary_logic(W15, W12, W7 , 0x96); W15 ^= W1 ; W15 = rotl(W15, 1);    C += rotl(D, 5); C += ternary_logic(E, A, B, 0xE8); C += 0x8F1BBCDC; C += W15; E = rotl(E, 30);
    W0  = ternary_logic(W0 , W13, W8 , 0x96); W0  ^= W2 ; W0  = rotl(W0 , 1);    B += rotl(C, 5); B += ternary_logic(D, E, A, 0xE8); B += 0x8F1BBCDC; B += W0 ; D = rotl(D, 30);
    W1  = ternary_logic(W1 , W14, W9 , 0x96); W1  ^= W3 ; W1  = rotl(W1 , 1);    A += rotl(B, 5); A += ternary_logic(C, D, E, 0xE8); A += 0x8F1BBCDC; A += W1 ; C = rotl(C, 30);
    W2  = ternary_logic(W2 , W15, W10, 0x96); W2  ^= W4 ; W2  = rotl(W2 , 1);    E += rotl(A, 5); E += ternary_logic(B, C, D, 0xE8); E += 0x8F1BBCDC; E += W2 ; B = rotl(B, 30);
    W3  = ternary_logic(W3 , W0 , W11, 0x96); W3  ^= W5 ; W3  = rotl(W3 , 1);    D += rotl(E, 5); D += ternary_logic(A, B, C, 0xE8); D += 0x8F1BBCDC; D += W3 ; A = rotl(A, 30);
    W4  = ternary_logic(W4 , W1 , W12, 0x96); W4  ^= W6 ; W4  = rotl(W4 , 1);    C += rotl(D, 5); C += ternary_logic(E, A, B, 0xE8); C += 0x8F1BBCDC; C += W4 ; E = rotl(E, 30);
    W5  = ternary_logic(W5 , W2 , W13, 0x96); W5  ^= W7 ; W5  = rotl(W5 , 1);    B += rotl(C, 5); B += ternary_logic(D, E, A, 0xE8); B += 0x8F1BBCDC; B += W5 ; D = rotl(D, 30);
    W6  = ternary_logic(W6 , W3 , W14, 0x96); W6  ^= W8 ; W6  = rotl(W6 , 1);    A += rotl(B, 5); A += ternary_logic(C, D, E, 0xE8); A += 0x8F1BBCDC; A += W6 ; C = rotl(C, 30);
    W7  = ternary_logic(W7 , W4 , W15, 0x96); W7  ^= W9 ; W7  = rotl(W7 , 1);    E += rotl(A, 5); E += ternary_logic(B, C, D, 0xE8); E += 0x8F1BBCDC; E += W7 ; B = rotl(B, 30);
    W8  = ternary_logic(W8 , W5 , W0 , 0x96); W8  ^= W10; W8  = rotl(W8 , 1);    D += rotl(E, 5); D += ternary_logic(A, B, C, 0xE8); D += 0x8F1BBCDC; D += W8 ; A = rotl(A, 30);
    W9  = ternary_logic(W9 , W6 , W1 , 0x96); W9  ^= W11; W9  = rotl(W9 , 1);    C += rotl(D, 5); C += ternary_logic(E, A, B, 0xE8); C += 0x8F1BBCDC; C += W9 ; E = rotl(E, 30);
    W10 = ternary_logic(W10, W7 , W2 , 0x96); W10 ^= W12; W10 = rotl(W10, 1);    B += rotl(C, 5); B += ternary_logic(D, E, A, 0xE8); B += 0x8F1BBCDC; B += W10; D = rotl(D, 30);
    W11 = ternary_logic(W11, W8 , W3 , 0x96); W11 ^= W13; W11 = rotl(W11, 1);    A += rotl(B, 5); A += ternary_logic(C, D, E, 0xE8); A += 0x8F1BBCDC; A += W11; C = rotl(C, 30);
    
    # Round 4
    W12 = ternary_logic(W12, W9 , W4 , 0x96); W12 ^= W14; W12 = rotl(W12, 1);    E += rotl(A, 5); E += ternary_logic(B, C, D, 0x96); E += 0xCA62C1D6; E += W12; B = rotl(B, 30);
    W13 = ternary_logic(W13, W10, W5 , 0x96); W13 ^= W15; W13 = rotl(W13, 1);    D += rotl(E, 5); D += ternary_logic(A, B, C, 0x96); D += 0xCA62C1D6; D += W13; A = rotl(A, 30);
    W14 = ternary_logic(W14, W11, W6 , 0x96); W14 ^= W0 ; W14 = rotl(W14, 1);    C += rotl(D, 5); C += ternary_logic(E, A, B, 0x96); C += 0xCA62C1D6; C += W14; E = rotl(E, 30);
    W15 = ternary_logic(W15, W12, W7 , 0x96); W15 ^= W1 ; W15 = rotl(W15, 1);    B += rotl(C, 5); B += ternary_logic(D, E, A, 0x96); B += 0xCA62C1D6; B += W15; D = rotl(D, 30);
    W0  = ternary_logic(W0 , W13, W8 , 0x96); W0  ^= W2 ; W0  = rotl(W0 , 1);    A += rotl(B, 5); A += ternary_logic(C, D, E, 0x96); A += 0xCA62C1D6; A += W0 ; C = rotl(C, 30);
    W1  = ternary_logic(W1 , W14, W9 , 0x96); W1  ^= W3 ; W1  = rotl(W1 , 1);    E += rotl(A, 5); E += ternary_logic(B, C, D, 0x96); E += 0xCA62C1D6; E += W1 ; B = rotl(B, 30);
    W2  = ternary_logic(W2 , W15, W10, 0x96); W2  ^= W4 ; W2  = rotl(W2 , 1);    D += rotl(E, 5); D += ternary_logic(A, B, C, 0x96); D += 0xCA62C1D6; D += W2 ; A = rotl(A, 30);
    W3  = ternary_logic(W3 , W0 , W11, 0x96); W3  ^= W5 ; W3  = rotl(W3 , 1);    C += rotl(D, 5); C += ternary_logic(E, A, B, 0x96); C += 0xCA62C1D6; C += W3 ; E = rotl(E, 30);
    W4  = ternary_logic(W4 , W1 , W12, 0x96); W4  ^= W6 ; W4  = rotl(W4 , 1);    B += rotl(C, 5); B += ternary_logic(D, E, A, 0x96); B += 0xCA62C1D6; B += W4 ; D = rotl(D, 30);
    W5  = ternary_logic(W5 , W2 , W13, 0x96); W5  ^= W7 ; W5  = rotl(W5 , 1);    A += rotl(B, 5); A += ternary_logic(C, D, E, 0x96); A += 0xCA62C1D6; A += W5 ; C = rotl(C, 30);
    W6  = ternary_logic(W6 , W3 , W14, 0x96); W6  ^= W8 ; W6  = rotl(W6 , 1);    E += rotl(A, 5); E += ternary_logic(B, C, D, 0x96); E += 0xCA62C1D6; E += W6 ; B = rotl(B, 30);
    W7  = ternary_logic(W7 , W4 , W15, 0x96); W7  ^= W9 ; W7  = rotl(W7 , 1);    D += rotl(E, 5); D += ternary_logic(A, B, C, 0x96); D += 0xCA62C1D6; D += W7 ; A = rotl(A, 30);
    W8  = ternary_logic(W8 , W5 , W0 , 0x96); W8  ^= W10; W8  = rotl(W8 , 1);    C += rotl(D, 5); C += ternary_logic(E, A, B, 0x96); C += 0xCA62C1D6; C += W8 ; E = rotl(E, 30);
    W9  = ternary_logic(W9 , W6 , W1 , 0x96); W9  ^= W11; W9  = rotl(W9 , 1);    B += rotl(C, 5); B += ternary_logic(D, E, A, 0x96); B += 0xCA62C1D6; B += W9 ; D = rotl(D, 30);
    W10 = ternary_logic(W10, W7 , W2 , 0x96); W10 ^= W12; W10 = rotl(W10, 1);    A += rotl(B, 5); A += ternary_logic(C, D, E, 0x96); A += 0xCA62C1D6; A += W10; C = rotl(C, 30);
    W11 = ternary_logic(W11, W8 , W3 , 0x96); W11 ^= W13; W11 = rotl(W11, 1);    E += rotl(A, 5); E += ternary_logic(B, C, D, 0x96); E += 0xCA62C1D6; E += W11; B = rotl(B, 30);
    W12 = ternary_logic(W12, W9 , W4 , 0x96); W12 ^= W14; W12 = rotl(W12, 1);    D += rotl(E, 5); D += ternary_logic(A, B, C, 0x96); D += 0xCA62C1D6; D += W12; A = rotl(A, 30);
    W13 = ternary_logic(W13, W10, W5 , 0x96); W13 ^= W15; W13 = rotl(W13, 1);    C += rotl(D, 5); C += ternary_logic(E, A, B, 0x96); C += 0xCA62C1D6; C += W13; E = rotl(E, 30);
    W14 = ternary_logic(W14, W11, W6 , 0x96); W14 ^= W0 ; W14 = rotl(W14, 1);    B += rotl(C, 5); B += ternary_logic(D, E, A, 0x96); B += 0xCA62C1D6; B += W14; D = rotl(D, 30);
    W15 = ternary_logic(W15, W12, W7 , 0x96); W15 ^= W1 ; W15 = rotl(W15, 1);    A += rotl(B, 5); A += ternary_logic(C, D, E, 0x96); A += 0xCA62C1D6; A += W15; C = rotl(C, 30);

    # Save state
    state[0] += A
    state[1] += B
    state[2] += C
    state[3] += D
    state[4] += E
    
# Define targets
sha1_block.targets  = [Target.PLAIN_C, Target.SSE2, Target.AVX, Target.AVX2]
sha1_block_.targets = [Target.AVX512]
sha1_block.parallelization_factor [Target.SSE2  ] = [1, 2]
sha1_block.parallelization_factor [Target.AVX   ] = [1, 2]
sha1_block.parallelization_factor [Target.AVX2  ] = [1, 2]
sha1_block_.parallelization_factor[Target.AVX512] = [1, 2]
# Build and run
generate_code()
build_and_run('C:/Program Files/CMake/bin/cmake.exe', run_benchmark=True, run_tests=True, 
              sde_test_cpus=['-knm'], 
              sde_exe='C:/Users/Alain/Downloads/sde-external-9.33.0-2024-01-07-win/sde.exe')
