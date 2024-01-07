#######################################################
# Testing example
#######################################################

# Note: above comment is added to the C file but this one not
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
    a += (d ^ (b & (c ^ d))) + block[0] ; a = ROTATE(a, 3);
    d += (c ^ (a & (b ^ c))) + block[1] ; d = ROTATE(d, 7);
    c += (b ^ (d & (a ^ b))) + block[2] ; c = ROTATE(c, 11);
    b += (a ^ (c & (d ^ a))) + block[3] ; b = ROTATE(b, 19);

    a += (d ^ (b & (c ^ d))) + block[4] ; a = ROTATE(a, 3 );# Comment at end of line
    d += (c ^ (a & (b ^ c))) + block[5] ; d = ROTATE(d, 7 );
    c += (b ^ (d & (a ^ b))) + block[6] ; c = ROTATE(c, 11);
    b += (a ^ (c & (d ^ a))) + block[7] ; b = ROTATE(b, 19);

    a += (d ^ (b & (c ^ d))) + block[8] ; a = ROTATE(a, 3 );
    d += (c ^ (a & (b ^ c))) + block[9] ; d = ROTATE(d, 7 );
    c += (b ^ (d & (a ^ b))) + block[10]; c = ROTATE(c, 11);
    b += (a ^ (c & (d ^ a))) + block[11]; b = ROTATE(b, 19);

    a += (d ^ (b & (c ^ d))) + block[12]; a = ROTATE(a, 3 );
    d += (c ^ (a & (b ^ c))) + block[13]; d = ROTATE(d, 7 );
    c += (b ^ (d & (a ^ b))) + block[14]; c = ROTATE(c, 11);
    b += (a ^ (c & (d ^ a))) + block[15]; b = ROTATE(b, 19);

    # Round 2
    a += ((b & (c | d)) | (c & d)) + block[0] + SQRT_2; a = ROTATE(a, 3 );
    d += ((a & (b | c)) | (b & c)) + block[4] + SQRT_2; d = ROTATE(d, 5 );
    c += ((d & (a | b)) | (a & b)) + block[8] + SQRT_2; c = ROTATE(c, 9 );
    b += ((c & (d | a)) | (d & a)) + block[12]+ SQRT_2; b = ROTATE(b, 13);

    a += ((b & (c | d)) | (c & d)) + block[1] + SQRT_2; a = ROTATE(a, 3 );
    d += ((a & (b | c)) | (b & c)) + block[5] + SQRT_2; d = ROTATE(d, 5 );
    c += ((d & (a | b)) | (a & b)) + block[9] + SQRT_2; c = ROTATE(c, 9 );
    b += ((c & (d | a)) | (d & a)) + block[13]+ SQRT_2; b = ROTATE(b, 13);

    a += ((b & (c | d)) | (c & d)) + block[2] + SQRT_2; a = ROTATE(a, 3 );
    d += ((a & (b | c)) | (b & c)) + block[6] + SQRT_2; d = ROTATE(d, 5 );
    c += ((d & (a | b)) | (a & b)) + block[10]+ SQRT_2; c = ROTATE(c, 9 );
    b += ((c & (d | a)) | (d & a)) + block[14]+ SQRT_2; b = ROTATE(b, 13);

    a += ((b & (c | d)) | (c & d)) + block[3] + SQRT_2; a = ROTATE(a, 3 );
    d += ((a & (b | c)) | (b & c)) + block[7] + SQRT_2; d = ROTATE(d, 5 );
    c += ((d & (a | b)) | (a & b)) + block[11]+ SQRT_2; c = ROTATE(c, 9 );
    b += ((c & (d | a)) | (d & a)) + block[15]+ SQRT_2; b = ROTATE(b, 13);

    # Round 3 
    a += (d ^ c ^ b) + block[0]  + SQRT_3; a = ROTATE(a, 3 );
    d += (c ^ b ^ a) + block[8]  + SQRT_3; d = ROTATE(d, 9 );
    c += (b ^ a ^ d) + block[4]  + SQRT_3; c = ROTATE(c, 11);
    b += (a ^ d ^ c) + block[12] + SQRT_3; b = ROTATE(b, 15);

    a += (d ^ c ^ b) + block[2]  + SQRT_3; a = ROTATE(a, 3 );
    d += (c ^ b ^ a) + block[10] + SQRT_3; d = ROTATE(d, 9 );
    c += (b ^ a ^ d) + block[6]  + SQRT_3; c = ROTATE(c, 11);
    b += (a ^ d ^ c) + block[14] + SQRT_3; b = ROTATE(b, 15);

    a += (d ^ c ^ b) + block[1]  + SQRT_3; a = ROTATE(a, 3 );
    d += (c ^ b ^ a) + block[9]  + SQRT_3; d = ROTATE(d, 9 );
    c += (b ^ a ^ d) + block[5]  + SQRT_3; c = ROTATE(c, 11);
    b += (a ^ d ^ c) + block[13] + SQRT_3; b = ROTATE(b, 15);

    a += (d ^ c ^ b) + block[3]  + SQRT_3; a = ROTATE(a, 3 );
    d += (c ^ b ^ a) + block[11] + SQRT_3; d = ROTATE(d, 9 );
    c += (b ^ a ^ d) + block[7]  + SQRT_3; c = ROTATE(c, 11);
    b += (a ^ d ^ c) + block[15] + SQRT_3; b = ROTATE(b, 15);

    state[0] += a;
    state[1] += b;
    state[2] += c;
    state[3] += d;
    
    
generate_code('tests/md4_plain_c.c')