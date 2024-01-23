#######################################################
# This comment is copied to the C file
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
    
# This is md4 crypto function
# other comment line here
with Function(void)(state, block) as md4_block:
    
    a = state[0]
    b = state[1]
    c = state[2]
    d = state[3]

    # Round 1
    for i in range(0, 16, 4):
        a += (d ^ (b & (c ^ d))) + block[i+0] ; a = rotl(a, 3);# Comment at end of line
        d += (c ^ (a & (b ^ c))) + block[i+1] ; d = rotl(d, 7);
        c += (b ^ (d & (a ^ b))) + block[i+2] ; c = rotl(c, 11);
        b += (a ^ (c & (d ^ a))) + block[i+3] ; b = rotl(b, 19);

    # Round 2
    for i in range(0, 4):
        a += ((b & (c | d)) | (c & d)) + block[i+0] + SQRT_2; a = rotl(a, 3 );
        d += ((a & (b | c)) | (b & c)) + block[i+4] + SQRT_2; d = rotl(d, 5 );
        c += ((d & (a | b)) | (a & b)) + block[i+8] + SQRT_2; c = rotl(c, 9 );
        b += ((c & (d | a)) | (d & a)) + block[i+12]+ SQRT_2; b = rotl(b, 13);

    # Round 3 
    for i in [0, 2, 1, 3]:
        a += (d ^ c ^ b) + block[i+0]  + SQRT_3; a = rotl(a, 3 );
        d += (c ^ b ^ a) + block[i+8]  + SQRT_3; d = rotl(d, 9 );
        c += (b ^ a ^ d) + block[i+4]  + SQRT_3; c = rotl(c, 11);
        b += (a ^ d ^ c) + block[i+12] + SQRT_3; b = rotl(b, 15);

    state[0] = a + state[0];
    state[1] = b + state[1];
    state[2] = c + state[2];
    state[3] = d + state[3];
    
    
generate_code()