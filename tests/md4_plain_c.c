//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// This comment is copied to the C file
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Automatically generated code by SIMD-function library

#include <assert.h>
#include <stdint.h>

// This is md4 crypto function
// other comment line here
void md4_block(uint32_t state[4], uint32_t block[16]) {

	uint32_t a = state[0];
	uint32_t b = state[1];
	uint32_t c = state[2];
	uint32_t d = state[3];

	// Round 1

	a += (d ^ (b & (c ^ d))) + block[0];	a = _rotl(a, 3);	// Comment at end of line
	d += (c ^ (a & (b ^ c))) + block[1];	d = _rotl(d, 7);
	c += (b ^ (d & (a ^ b))) + block[2];	c = _rotl(c, 11);
	b += (a ^ (c & (d ^ a))) + block[3];	b = _rotl(b, 19);
	a += (d ^ (b & (c ^ d))) + block[4];	a = _rotl(a, 3);
	d += (c ^ (a & (b ^ c))) + block[5];	d = _rotl(d, 7);
	c += (b ^ (d & (a ^ b))) + block[6];	c = _rotl(c, 11);
	b += (a ^ (c & (d ^ a))) + block[7];	b = _rotl(b, 19);
	a += (d ^ (b & (c ^ d))) + block[8];	a = _rotl(a, 3);
	d += (c ^ (a & (b ^ c))) + block[9];	d = _rotl(d, 7);
	c += (b ^ (d & (a ^ b))) + block[10];	c = _rotl(c, 11);
	b += (a ^ (c & (d ^ a))) + block[11];	b = _rotl(b, 19);
	a += (d ^ (b & (c ^ d))) + block[12];	a = _rotl(a, 3);
	d += (c ^ (a & (b ^ c))) + block[13];	d = _rotl(d, 7);
	c += (b ^ (d & (a ^ b))) + block[14];	c = _rotl(c, 11);
	b += (a ^ (c & (d ^ a))) + block[15];	b = _rotl(b, 19);

	// Round 2

	a += ((b & (c | d)) | (c & d)) + block[0] + 0x5a827999;	a = _rotl(a, 3);
	d += ((a & (b | c)) | (b & c)) + block[4] + 0x5a827999;	d = _rotl(d, 5);
	c += ((d & (a | b)) | (a & b)) + block[8] + 0x5a827999;	c = _rotl(c, 9);
	b += ((c & (d | a)) | (d & a)) + block[12] + 0x5a827999;	b = _rotl(b, 13);
	a += ((b & (c | d)) | (c & d)) + block[1] + 0x5a827999;	a = _rotl(a, 3);
	d += ((a & (b | c)) | (b & c)) + block[5] + 0x5a827999;	d = _rotl(d, 5);
	c += ((d & (a | b)) | (a & b)) + block[9] + 0x5a827999;	c = _rotl(c, 9);
	b += ((c & (d | a)) | (d & a)) + block[13] + 0x5a827999;	b = _rotl(b, 13);
	a += ((b & (c | d)) | (c & d)) + block[2] + 0x5a827999;	a = _rotl(a, 3);
	d += ((a & (b | c)) | (b & c)) + block[6] + 0x5a827999;	d = _rotl(d, 5);
	c += ((d & (a | b)) | (a & b)) + block[10] + 0x5a827999;	c = _rotl(c, 9);
	b += ((c & (d | a)) | (d & a)) + block[14] + 0x5a827999;	b = _rotl(b, 13);
	a += ((b & (c | d)) | (c & d)) + block[3] + 0x5a827999;	a = _rotl(a, 3);
	d += ((a & (b | c)) | (b & c)) + block[7] + 0x5a827999;	d = _rotl(d, 5);
	c += ((d & (a | b)) | (a & b)) + block[11] + 0x5a827999;	c = _rotl(c, 9);
	b += ((c & (d | a)) | (d & a)) + block[15] + 0x5a827999;	b = _rotl(b, 13);

	// Round 3 

	a += ((d ^ c) ^ b) + block[0] + 0x6ed9eba1;	a = _rotl(a, 3);
	d += ((c ^ b) ^ a) + block[8] + 0x6ed9eba1;	d = _rotl(d, 9);
	c += ((b ^ a) ^ d) + block[4] + 0x6ed9eba1;	c = _rotl(c, 11);
	b += ((a ^ d) ^ c) + block[12] + 0x6ed9eba1;	b = _rotl(b, 15);
	a += ((d ^ c) ^ b) + block[2] + 0x6ed9eba1;	a = _rotl(a, 3);
	d += ((c ^ b) ^ a) + block[10] + 0x6ed9eba1;	d = _rotl(d, 9);
	c += ((b ^ a) ^ d) + block[6] + 0x6ed9eba1;	c = _rotl(c, 11);
	b += ((a ^ d) ^ c) + block[14] + 0x6ed9eba1;	b = _rotl(b, 15);
	a += ((d ^ c) ^ b) + block[1] + 0x6ed9eba1;	a = _rotl(a, 3);
	d += ((c ^ b) ^ a) + block[9] + 0x6ed9eba1;	d = _rotl(d, 9);
	c += ((b ^ a) ^ d) + block[5] + 0x6ed9eba1;	c = _rotl(c, 11);
	b += ((a ^ d) ^ c) + block[13] + 0x6ed9eba1;	b = _rotl(b, 15);
	a += ((d ^ c) ^ b) + block[3] + 0x6ed9eba1;	a = _rotl(a, 3);
	d += ((c ^ b) ^ a) + block[11] + 0x6ed9eba1;	d = _rotl(d, 9);
	c += ((b ^ a) ^ d) + block[7] + 0x6ed9eba1;	c = _rotl(c, 11);
	b += ((a ^ d) ^ c) + block[15] + 0x6ed9eba1;	b = _rotl(b, 15);

	state[0] = state[0] + a;
	state[1] = state[1] + b;
	state[2] = state[2] + c;
	state[3] = state[3] + d;
}

