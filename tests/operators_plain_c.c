//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Simple operator tests
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Automatically generated code by SIMD-function library

#include <assert.h>
#include <stdint.h>

// Addition operator
uint32_t add(uint32_t op1, uint32_t op2) {
	return (op1 + op2);
}

// Substraction operator
uint32_t sub(uint32_t op1, uint32_t op2) {
	return (op1 - op2);
}

// Product operator
uint32_t prod(uint32_t op1, uint32_t op2) {
	return (op1 * op2);
}

// Division operator
uint32_t div(uint32_t op1, uint32_t op2) {
	return (op1 / op2);
}

uint32_t div1(uint32_t op1, uint32_t op2) {
	return (op1 / op2);
}

uint32_t mod(uint32_t op1, uint32_t op2) {
	return (op1 % op2);
}

// Power operator 
uint32_t pow(uint32_t op1) {
	return (op1 * op1);
}

// Shift left operator 
uint32_t shiftl(uint32_t op1, uint32_t op2_scalar) {
	return (op1 << op2_scalar);
}

// Shift right operator 
uint32_t shiftr(uint32_t op1, uint32_t op2_scalar) {
	return (op1 >> op2_scalar);
}

