//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// This file is part of 'SIMD-Function'
// 
// Copyright(c) 2024 by Alain Espinosa.
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

#pragma once

#include <stddef.h>
#include <stdint.h>

#ifdef _MSC_VER
    #include <intrin.h>
    #define SIMD_RESTRICT __restrict
    #define SIMD_INLINE __forceinline
#else
    #define SIMD_RESTRICT __restrict__
    #ifdef __OPTIMIZE__
        #define SIMD_INLINE inline __attribute__((always_inline))
    #else
        #define SIMD_INLINE inline
    #endif
#endif  // !_MSC_VER

namespace simd
{

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// x86 SSE2
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#include <emmintrin.h>
using Vec128u8     = __m128i;
using Vec128i8     = __m128i;
using Vec128u16    = __m128i;
using Vec128i16    = __m128i;
using Vec128u32    = __m128i;
using Vec128i32    = __m128i;
using Vec128u64    = __m128i;
using Vec128i64    = __m128i;
using Vec128Int    = __m128i;
using Vec128Float  = __m128 ;
using Vec128Double = __m128d;

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// x86 AVX/AVX2
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#include <immintrin.h>
#ifdef __clang__
    #include <avxintrin.h>
    // avxintrin defines __m256i and must come before avx2intrin.
    #include <avx2intrin.h>
    #include <bmi2intrin.h>  // _pext_u64
    #include <f16cintrin.h>
    #include <fmaintrin.h>
    #include <smmintrin.h>

    #include <avx512fintrin.h>
    #include <avx512vlintrin.h>
    #include <avx512bwintrin.h>
    #include <avx512vlbwintrin.h>
    #include <avx512dqintrin.h>
    #include <avx512vldqintrin.h>
    #include <avx512cdintrin.h>
    #include <avx512vlcdintrin.h>
#endif
using Vec256u8     = __m256i;
using Vec256i8     = __m256i;
using Vec256u16    = __m256i;
using Vec256i16    = __m256i;
using Vec256u32    = __m256i;
using Vec256i32    = __m256i;
using Vec256u64    = __m256i;
using Vec256i64    = __m256i;
using Vec256Int    = __m256i;
using Vec256Float  = __m256 ;
using Vec256Double = __m256d;

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// x86 AVX512
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
using Vec512u8     = __m512i;
using Vec512i8     = __m512i;
using Vec512u16    = __m512i;
using Vec512i16    = __m512i;
using Vec512u32    = __m512i;
using Vec512i32    = __m512i;
using Vec512u64    = __m512i;
using Vec512i64    = __m512i;
using Vec512Int    = __m512i;
using Vec512Float  = __m512 ;
using Vec512Double = __m512d;

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Zero initilization
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
template<class Vector> static SIMD_INLINE Vector Zero() noexcept {}
// SSE2
template<> SIMD_INLINE Vec128Int    Zero() noexcept { return _mm_setzero_si128(); }
template<> SIMD_INLINE Vec128Float  Zero() noexcept { return _mm_setzero_ps();    }
template<> SIMD_INLINE Vec128Double Zero() noexcept { return _mm_setzero_pd();    }
// AVX/AVX2
template<> SIMD_INLINE Vec256Int    Zero() noexcept { return _mm256_setzero_si256(); }
template<> SIMD_INLINE Vec256Float  Zero() noexcept { return _mm256_setzero_ps();    }
template<> SIMD_INLINE Vec256Double Zero() noexcept { return _mm256_setzero_pd();    }
// AVX512
template<> SIMD_INLINE Vec512Int    Zero() noexcept { return _mm512_setzero_si512(); }
template<> SIMD_INLINE Vec512Float  Zero() noexcept { return _mm512_setzero_ps();    }
template<> SIMD_INLINE Vec512Double Zero() noexcept { return _mm512_setzero_pd();    }

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Set
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
template<class T, class Vector> static SIMD_INLINE Vector Set(const T value) noexcept {}
// SSE2
template<> SIMD_INLINE Vec128u8     Set(const uint8_t  value) noexcept { return _mm_set1_epi8  (value); }
template<> SIMD_INLINE Vec128i8     Set(const int8_t   value) noexcept { return _mm_set1_epi8  (value); }
template<> SIMD_INLINE Vec128u16    Set(const uint16_t value) noexcept { return _mm_set1_epi16 (value); }
template<> SIMD_INLINE Vec128i16    Set(const int16_t  value) noexcept { return _mm_set1_epi16 (value); }
template<> SIMD_INLINE Vec128u32    Set(const uint32_t value) noexcept { return _mm_set1_epi32 (value); }
template<> SIMD_INLINE Vec128i32    Set(const int32_t  value) noexcept { return _mm_set1_epi32 (value); }
template<> SIMD_INLINE Vec128u64    Set(const uint64_t value) noexcept { return _mm_set1_epi64x(value); }
template<> SIMD_INLINE Vec128i64    Set(const int64_t  value) noexcept { return _mm_set1_epi64x(value); }
template<> SIMD_INLINE Vec128Float  Set(const float    value) noexcept { return _mm_set1_ps    (value); }
template<> SIMD_INLINE Vec128Double Set(const double   value) noexcept { return _mm_set1_pd    (value); }
// AVX/AVX2
template<> SIMD_INLINE Vec256u8     Set(const uint8_t  value) noexcept { return _mm256_set1_epi8  (value); }
template<> SIMD_INLINE Vec256i8     Set(const int8_t   value) noexcept { return _mm256_set1_epi8  (value); }
template<> SIMD_INLINE Vec256u16    Set(const uint16_t value) noexcept { return _mm256_set1_epi16 (value); }
template<> SIMD_INLINE Vec256i16    Set(const int16_t  value) noexcept { return _mm256_set1_epi16 (value); }
template<> SIMD_INLINE Vec256u32    Set(const uint32_t value) noexcept { return _mm256_set1_epi32 (value); }
template<> SIMD_INLINE Vec256i32    Set(const int32_t  value) noexcept { return _mm256_set1_epi32 (value); }
template<> SIMD_INLINE Vec256u64    Set(const uint64_t value) noexcept { return _mm256_set1_epi64x(value); }
template<> SIMD_INLINE Vec256i64    Set(const int64_t  value) noexcept { return _mm256_set1_epi64x(value); }
template<> SIMD_INLINE Vec256Float  Set(const float    value) noexcept { return _mm256_set1_ps    (value); }
template<> SIMD_INLINE Vec256Double Set(const double   value) noexcept { return _mm256_set1_pd    (value); }
// AVX512
template<> SIMD_INLINE Vec512u8     Set(const uint8_t  value) noexcept { return _mm512_set1_epi8 (value); }
template<> SIMD_INLINE Vec512i8     Set(const int8_t   value) noexcept { return _mm512_set1_epi8 (value); }
template<> SIMD_INLINE Vec512u16    Set(const uint16_t value) noexcept { return _mm512_set1_epi16(value); }
template<> SIMD_INLINE Vec512i16    Set(const int16_t  value) noexcept { return _mm512_set1_epi16(value); }
template<> SIMD_INLINE Vec512u32    Set(const uint32_t value) noexcept { return _mm512_set1_epi32(value); }
template<> SIMD_INLINE Vec512i32    Set(const int32_t  value) noexcept { return _mm512_set1_epi32(value); }
template<> SIMD_INLINE Vec512u64    Set(const uint64_t value) noexcept { return _mm512_set1_epi64(value); }
template<> SIMD_INLINE Vec512i64    Set(const int64_t  value) noexcept { return _mm512_set1_epi64(value); }
template<> SIMD_INLINE Vec512Float  Set(const float    value) noexcept { return _mm512_set1_ps   (value); }
template<> SIMD_INLINE Vec512Double Set(const double   value) noexcept { return _mm512_set1_pd   (value); }

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Load
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// SSE2
static SIMD_INLINE Vec128Int    Load (const Vec128Int   * SIMD_RESTRICT   aligned) noexcept { return _mm_load_si128(aligned); }
static SIMD_INLINE Vec128Float  Load (const Vec128Float * SIMD_RESTRICT   aligned) noexcept { return _mm_load_ps(reinterpret_cast<const float*>(aligned)); }
static SIMD_INLINE Vec128Double Load (const Vec128Double* SIMD_RESTRICT   aligned) noexcept { return _mm_load_pd(reinterpret_cast<const double*>(aligned)); }
static SIMD_INLINE Vec128Int    LoadU(const Vec128Int   * SIMD_RESTRICT unaligned) noexcept { return _mm_loadu_si128(unaligned); }
static SIMD_INLINE Vec128Float  LoadU(const Vec128Float * SIMD_RESTRICT unaligned) noexcept { return _mm_loadu_ps(reinterpret_cast<const float*>(unaligned)); }
static SIMD_INLINE Vec128Double LoadU(const Vec128Double* SIMD_RESTRICT unaligned) noexcept { return _mm_loadu_pd(reinterpret_cast<const double*>(unaligned)); }
// AVX/AVX2
static SIMD_INLINE Vec256Int    Load (const Vec256Int   * SIMD_RESTRICT   aligned) noexcept { return _mm256_load_si256(aligned); }
static SIMD_INLINE Vec256Float  Load (const Vec256Float * SIMD_RESTRICT   aligned) noexcept { return _mm256_load_ps(reinterpret_cast<const float*>(aligned)); }
static SIMD_INLINE Vec256Double Load (const Vec256Double* SIMD_RESTRICT   aligned) noexcept { return _mm256_load_pd(reinterpret_cast<const double*>(aligned)); }
static SIMD_INLINE Vec256Int    LoadU(const Vec256Int   * SIMD_RESTRICT unaligned) noexcept { return _mm256_loadu_si256(unaligned); }
static SIMD_INLINE Vec256Float  LoadU(const Vec256Float * SIMD_RESTRICT unaligned) noexcept { return _mm256_loadu_ps(reinterpret_cast<const float*>(unaligned)); }
static SIMD_INLINE Vec256Double LoadU(const Vec256Double* SIMD_RESTRICT unaligned) noexcept { return _mm256_loadu_pd(reinterpret_cast<const double*>(unaligned)); }
// AVX512
static SIMD_INLINE Vec512Int    Load (const Vec512Int   * SIMD_RESTRICT   aligned) noexcept { return _mm512_load_si512 (  aligned); }
static SIMD_INLINE Vec512Float  Load (const Vec512Float * SIMD_RESTRICT   aligned) noexcept { return _mm512_load_ps    (  aligned); }
static SIMD_INLINE Vec512Double Load (const Vec512Double* SIMD_RESTRICT   aligned) noexcept { return _mm512_load_pd    (  aligned); }
static SIMD_INLINE Vec512Int    LoadU(const Vec512Int   * SIMD_RESTRICT unaligned) noexcept { return _mm512_loadu_si512(unaligned); }
static SIMD_INLINE Vec512Float  LoadU(const Vec512Float * SIMD_RESTRICT unaligned) noexcept { return _mm512_loadu_ps   (unaligned); }
static SIMD_INLINE Vec512Double LoadU(const Vec512Double* SIMD_RESTRICT unaligned) noexcept { return _mm512_loadu_pd   (unaligned ); }

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Store
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// SSE2
static SIMD_INLINE void Store (Vec128Int   * SIMD_RESTRICT   aligned, const Vec128Int    v) noexcept { _mm_store_si128(aligned, v); }
static SIMD_INLINE void Store (Vec128Float * SIMD_RESTRICT   aligned, const Vec128Float  v) noexcept { _mm_store_ps(reinterpret_cast<float*>(aligned) , v); }
static SIMD_INLINE void Store (Vec128Double* SIMD_RESTRICT   aligned, const Vec128Double v) noexcept { _mm_store_pd(reinterpret_cast<double*>(aligned), v); }
static SIMD_INLINE void StoreU(Vec128Int   * SIMD_RESTRICT unaligned, const Vec128Int    v) noexcept { _mm_storeu_si128(unaligned, v); }
static SIMD_INLINE void StoreU(Vec128Float * SIMD_RESTRICT unaligned, const Vec128Float  v) noexcept { _mm_storeu_ps(reinterpret_cast<float*>(unaligned) , v) ; }
static SIMD_INLINE void StoreU(Vec128Double* SIMD_RESTRICT unaligned, const Vec128Double v) noexcept { _mm_storeu_pd(reinterpret_cast<double*>(unaligned), v) ; }
// AVX/AVX2
static SIMD_INLINE void Store (Vec256Int   * SIMD_RESTRICT   aligned, const Vec256Int    v) noexcept { _mm256_store_si256(aligned, v); }
static SIMD_INLINE void Store (Vec256Float * SIMD_RESTRICT   aligned, const Vec256Float  v) noexcept { _mm256_store_ps(reinterpret_cast<float*>(aligned) , v); }
static SIMD_INLINE void Store (Vec256Double* SIMD_RESTRICT   aligned, const Vec256Double v) noexcept { _mm256_store_pd(reinterpret_cast<double*>(aligned), v); }
static SIMD_INLINE void StoreU(Vec256Int   * SIMD_RESTRICT unaligned, const Vec256Int    v) noexcept { _mm256_storeu_si256(unaligned, v); }
static SIMD_INLINE void StoreU(Vec256Float * SIMD_RESTRICT unaligned, const Vec256Float  v) noexcept { _mm256_storeu_ps(reinterpret_cast<float*>(unaligned) , v); }
static SIMD_INLINE void StoreU(Vec256Double* SIMD_RESTRICT unaligned, const Vec256Double v) noexcept { _mm256_storeu_pd(reinterpret_cast<double*>(unaligned), v); }
// AVX512
static SIMD_INLINE void Store (Vec512Int   * SIMD_RESTRICT   aligned, const Vec512Int    v) noexcept { _mm512_store_si512 (  aligned, v); }
static SIMD_INLINE void Store (Vec512Float * SIMD_RESTRICT   aligned, const Vec512Float  v) noexcept { _mm512_store_ps    (  aligned, v); }
static SIMD_INLINE void Store (Vec512Double* SIMD_RESTRICT   aligned, const Vec512Double v) noexcept { _mm512_store_pd    (  aligned, v); }
static SIMD_INLINE void StoreU(Vec512Int   * SIMD_RESTRICT unaligned, const Vec512Int    v) noexcept { _mm512_storeu_si512(unaligned, v); }
static SIMD_INLINE void StoreU(Vec512Float * SIMD_RESTRICT unaligned, const Vec512Float  v) noexcept { _mm512_storeu_ps   (unaligned, v); }
static SIMD_INLINE void StoreU(Vec512Double* SIMD_RESTRICT unaligned, const Vec512Double v) noexcept { _mm512_storeu_pd   (unaligned, v); }

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// And
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// SSE2
static SIMD_INLINE Vec128Int    operator&(const Vec128Int    a, const Vec128Int    b) noexcept { return _mm_and_si128(a, b); }
static SIMD_INLINE Vec128Float  operator&(const Vec128Float  a, const Vec128Float  b) noexcept { return _mm_and_ps   (a, b); }
static SIMD_INLINE Vec128Double operator&(const Vec128Double a, const Vec128Double b) noexcept { return _mm_and_pd   (a, b); }
// AVX/AVX2
static SIMD_INLINE Vec256Int    operator&(const Vec256Int    a, const Vec256Int    b) noexcept { return _mm256_and_si256(a, b); }
static SIMD_INLINE Vec256Float  operator&(const Vec256Float  a, const Vec256Float  b) noexcept { return _mm256_and_ps   (a, b); }
static SIMD_INLINE Vec256Double operator&(const Vec256Double a, const Vec256Double b) noexcept { return _mm256_and_pd   (a, b); }
// AVX512
static SIMD_INLINE Vec512Int    operator&(const Vec512Int    a, const Vec512Int    b) noexcept { return _mm512_and_si512(a, b); }
static SIMD_INLINE Vec512Float  operator&(const Vec512Float  a, const Vec512Float  b) noexcept { return _mm512_and_ps   (a, b); }
static SIMD_INLINE Vec512Double operator&(const Vec512Double a, const Vec512Double b) noexcept { return _mm512_and_pd   (a, b); }
// &=
template<class Vector, class T> static SIMD_INLINE Vector operator&=(Vector& a, const T b) noexcept { return (a = a & b);}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Andn
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// SSE2
static SIMD_INLINE Vec128Int    andn(const Vec128Int    a, const Vec128Int    b) noexcept { return _mm_andnot_si128(a, b); }
static SIMD_INLINE Vec128Float  andn(const Vec128Float  a, const Vec128Float  b) noexcept { return _mm_andnot_ps(a, b); }
static SIMD_INLINE Vec128Double andn(const Vec128Double a, const Vec128Double b) noexcept { return _mm_andnot_pd(a, b); }
// AVX/AVX2
static SIMD_INLINE Vec256Int    andn(const Vec256Int    a, const Vec256Int    b) noexcept { return _mm256_andnot_si256(a, b); }
static SIMD_INLINE Vec256Float  andn(const Vec256Float  a, const Vec256Float  b) noexcept { return _mm256_andnot_ps(a, b); }
static SIMD_INLINE Vec256Double andn(const Vec256Double a, const Vec256Double b) noexcept { return _mm256_andnot_pd(a, b); }
// AVX512
static SIMD_INLINE Vec512Int    andn(const Vec512Int    a, const Vec512Int    b) noexcept { return _mm512_andnot_si512(a, b); }
static SIMD_INLINE Vec512Float  andn(const Vec512Float  a, const Vec512Float  b) noexcept { return _mm512_andnot_ps(a, b); }
static SIMD_INLINE Vec512Double andn(const Vec512Double a, const Vec512Double b) noexcept { return _mm512_andnot_pd(a, b); }

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// OR
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// SSE2
static SIMD_INLINE Vec128Int    operator|(const Vec128Int    a, const Vec128Int    b) noexcept { return _mm_or_si128(a, b); }
static SIMD_INLINE Vec128Float  operator|(const Vec128Float  a, const Vec128Float  b) noexcept { return _mm_or_ps   (a, b); }
static SIMD_INLINE Vec128Double operator|(const Vec128Double a, const Vec128Double b) noexcept { return _mm_or_pd   (a, b); }
// AVX/AVX2
static SIMD_INLINE Vec256Int    operator|(const Vec256Int    a, const Vec256Int    b) noexcept { return _mm256_or_si256(a, b); }
static SIMD_INLINE Vec256Float  operator|(const Vec256Float  a, const Vec256Float  b) noexcept { return _mm256_or_ps   (a, b); }
static SIMD_INLINE Vec256Double operator|(const Vec256Double a, const Vec256Double b) noexcept { return _mm256_or_pd   (a, b); }
// AVX512
static SIMD_INLINE Vec512Int    operator|(const Vec512Int    a, const Vec512Int    b) noexcept { return _mm512_or_si512(a, b); }
static SIMD_INLINE Vec512Float  operator|(const Vec512Float  a, const Vec512Float  b) noexcept { return _mm512_or_ps   (a, b); }
static SIMD_INLINE Vec512Double operator|(const Vec512Double a, const Vec512Double b) noexcept { return _mm512_or_pd   (a, b); }
// |=
template<class Vector, class T> static SIMD_INLINE Vector operator|=(Vector& a, const T b) noexcept { return (a = a | b); }

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// XOR
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// SSE2
static SIMD_INLINE Vec128Int    operator^(const Vec128Int    a, const Vec128Int    b) noexcept { return _mm_xor_si128(a, b); }
static SIMD_INLINE Vec128Float  operator^(const Vec128Float  a, const Vec128Float  b) noexcept { return _mm_xor_ps   (a, b); }
static SIMD_INLINE Vec128Double operator^(const Vec128Double a, const Vec128Double b) noexcept { return _mm_xor_pd   (a, b); }
// AVX/AVX2
static SIMD_INLINE Vec256Int    operator^(const Vec256Int    a, const Vec256Int    b) noexcept { return _mm256_xor_si256(a, b); }
static SIMD_INLINE Vec256Float  operator^(const Vec256Float  a, const Vec256Float  b) noexcept { return _mm256_xor_ps   (a, b); }
static SIMD_INLINE Vec256Double operator^(const Vec256Double a, const Vec256Double b) noexcept { return _mm256_xor_pd   (a, b); }
// AVX512
static SIMD_INLINE Vec512Int    operator^(const Vec512Int    a, const Vec512Int    b) noexcept { return _mm512_xor_si512(a, b); }
static SIMD_INLINE Vec512Float  operator^(const Vec512Float  a, const Vec512Float  b) noexcept { return _mm512_xor_ps   (a, b); }
static SIMD_INLINE Vec512Double operator^(const Vec512Double a, const Vec512Double b) noexcept { return _mm512_xor_pd   (a, b); }
// ^=
template<class Vector, class T> static SIMD_INLINE Vector operator^=(Vector& a, const T b) noexcept { return (a = a ^ b); }

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Sum
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Vector + Vector
// SSE2
static SIMD_INLINE Vec128Int operator+(const Vec128Int a, const Vec128Int b) noexcept {
    if constexpr (sizeof(SimdScalarType) == 1)      return _mm_add_epi8 (a, b);
    else if constexpr (sizeof(SimdScalarType) == 2) return _mm_add_epi16(a, b);
    else if constexpr (sizeof(SimdScalarType) == 4) return _mm_add_epi32(a, b);
    else if constexpr (sizeof(SimdScalarType) == 8) return _mm_add_epi64(a, b);
}
static SIMD_INLINE Vec128Float  operator+(const Vec128Float  a, const Vec128Float  b) noexcept { return _mm_add_ps(a, b); }
static SIMD_INLINE Vec128Double operator+(const Vec128Double a, const Vec128Double b) noexcept { return _mm_add_pd(a, b); }
// AVX/AVX2
static SIMD_INLINE Vec256Int operator+(const Vec256Int a, const Vec256Int b) noexcept {
    if constexpr (sizeof(SimdScalarType) == 1)      return _mm256_add_epi8(a, b);
    else if constexpr (sizeof(SimdScalarType) == 2) return _mm256_add_epi16(a, b);
    else if constexpr (sizeof(SimdScalarType) == 4) return _mm256_add_epi32(a, b);
    else if constexpr (sizeof(SimdScalarType) == 8) return _mm256_add_epi64(a, b);
}
static SIMD_INLINE Vec256Float  operator+(const Vec256Float  a, const Vec256Float  b) noexcept { return _mm256_add_ps(a, b); }
static SIMD_INLINE Vec256Double operator+(const Vec256Double a, const Vec256Double b) noexcept { return _mm256_add_pd(a, b); }
// AVX512
static SIMD_INLINE Vec512Int operator+(const Vec512Int a, const Vec512Int b) noexcept {
    if constexpr (sizeof(SimdScalarType) == 1)      return _mm512_add_epi8(a, b);
    else if constexpr (sizeof(SimdScalarType) == 2) return _mm512_add_epi16(a, b);
    else if constexpr (sizeof(SimdScalarType) == 4) return _mm512_add_epi32(a, b);
    else if constexpr (sizeof(SimdScalarType) == 8) return _mm512_add_epi64(a, b);
}
static SIMD_INLINE Vec512Float  operator+(const Vec512Float  a, const Vec512Float  b) noexcept { return _mm512_add_ps(a, b); }
static SIMD_INLINE Vec512Double operator+(const Vec512Double a, const Vec512Double b) noexcept { return _mm512_add_pd(a, b); }

// Vector + Scalar
// SSE2
static SIMD_INLINE Vec128u8     operator+(const Vec128u8     a, const uint8_t  b) noexcept { return _mm_add_epi8 (a, Set<uint8_t , Vec128u8    >(b)); }
static SIMD_INLINE Vec128i8     operator+(const Vec128i8     a, const int8_t   b) noexcept { return _mm_add_epi8 (a, Set<int8_t  , Vec128i8    >(b)); }
static SIMD_INLINE Vec128u16    operator+(const Vec128u16    a, const uint16_t b) noexcept { return _mm_add_epi16(a, Set<uint16_t, Vec128u16   >(b)); }
static SIMD_INLINE Vec128i16    operator+(const Vec128i16    a, const int16_t  b) noexcept { return _mm_add_epi16(a, Set<int16_t , Vec128i16   >(b)); }
static SIMD_INLINE Vec128u32    operator+(const Vec128u32    a, const uint32_t b) noexcept { return _mm_add_epi32(a, Set<uint32_t, Vec128u32   >(b)); }
static SIMD_INLINE Vec128i32    operator+(const Vec128i32    a, const int32_t  b) noexcept { return _mm_add_epi32(a, Set<int32_t , Vec128i32   >(b)); }
static SIMD_INLINE Vec128u64    operator+(const Vec128u64    a, const uint64_t b) noexcept { return _mm_add_epi64(a, Set<uint64_t, Vec128u64   >(b)); }
static SIMD_INLINE Vec128i64    operator+(const Vec128i64    a, const int64_t  b) noexcept { return _mm_add_epi64(a, Set<int64_t , Vec128i64   >(b)); }
static SIMD_INLINE Vec128Float  operator+(const Vec128Float  a, const float    b) noexcept { return _mm_add_ps   (a, Set<float   , Vec128Float >(b)); }
static SIMD_INLINE Vec128Double operator+(const Vec128Double a, const double   b) noexcept { return _mm_add_pd   (a, Set<double  , Vec128Double>(b)); }
// AVX/AVX2
static SIMD_INLINE Vec256u8     operator+(const Vec256u8     a, const uint8_t  b) noexcept { return _mm256_add_epi8 (a, Set<uint8_t , Vec256u8    >(b)); }
static SIMD_INLINE Vec256i8     operator+(const Vec256i8     a, const int8_t   b) noexcept { return _mm256_add_epi8 (a, Set<int8_t  , Vec256i8    >(b)); }
static SIMD_INLINE Vec256u16    operator+(const Vec256u16    a, const uint16_t b) noexcept { return _mm256_add_epi16(a, Set<uint16_t, Vec256u16   >(b)); }
static SIMD_INLINE Vec256i16    operator+(const Vec256i16    a, const int16_t  b) noexcept { return _mm256_add_epi16(a, Set<int16_t , Vec256i16   >(b)); }
static SIMD_INLINE Vec256u32    operator+(const Vec256u32    a, const uint32_t b) noexcept { return _mm256_add_epi32(a, Set<uint32_t, Vec256u32   >(b)); }
static SIMD_INLINE Vec256i32    operator+(const Vec256i32    a, const int32_t  b) noexcept { return _mm256_add_epi32(a, Set<int32_t , Vec256i32   >(b)); }
static SIMD_INLINE Vec256u64    operator+(const Vec256u64    a, const uint64_t b) noexcept { return _mm256_add_epi64(a, Set<uint64_t, Vec256u64   >(b)); }
static SIMD_INLINE Vec256i64    operator+(const Vec256i64    a, const int64_t  b) noexcept { return _mm256_add_epi64(a, Set<int64_t , Vec256i64   >(b)); }
static SIMD_INLINE Vec256Float  operator+(const Vec256Float  a, const float    b) noexcept { return _mm256_add_ps   (a, Set<float   , Vec256Float >(b)); }
static SIMD_INLINE Vec256Double operator+(const Vec256Double a, const double   b) noexcept { return _mm256_add_pd   (a, Set<double  , Vec256Double>(b)); }
// AVX512
static SIMD_INLINE Vec512u8     operator+(const Vec512u8     a, const uint8_t  b) noexcept { return _mm512_add_epi8 (a, Set<uint8_t , Vec512u8    >(b)); }
static SIMD_INLINE Vec512i8     operator+(const Vec512i8     a, const int8_t   b) noexcept { return _mm512_add_epi8 (a, Set<int8_t  , Vec512i8    >(b)); }
static SIMD_INLINE Vec512u16    operator+(const Vec512u16    a, const uint16_t b) noexcept { return _mm512_add_epi16(a, Set<uint16_t, Vec512u16   >(b)); }
static SIMD_INLINE Vec512i16    operator+(const Vec512i16    a, const int16_t  b) noexcept { return _mm512_add_epi16(a, Set<int16_t , Vec512i16   >(b)); }
static SIMD_INLINE Vec512u32    operator+(const Vec512u32    a, const uint32_t b) noexcept { return _mm512_add_epi32(a, Set<uint32_t, Vec512u32   >(b)); }
static SIMD_INLINE Vec512i32    operator+(const Vec512i32    a, const int32_t  b) noexcept { return _mm512_add_epi32(a, Set<int32_t , Vec512i32   >(b)); }
static SIMD_INLINE Vec512u64    operator+(const Vec512u64    a, const uint64_t b) noexcept { return _mm512_add_epi64(a, Set<uint64_t, Vec512u64   >(b)); }
static SIMD_INLINE Vec512i64    operator+(const Vec512i64    a, const int64_t  b) noexcept { return _mm512_add_epi64(a, Set<int64_t , Vec512i64   >(b)); }
static SIMD_INLINE Vec512Float  operator+(const Vec512Float  a, const float    b) noexcept { return _mm512_add_ps   (a, Set<float   , Vec512Float >(b)); }
static SIMD_INLINE Vec512Double operator+(const Vec512Double a, const double   b) noexcept { return _mm512_add_pd   (a, Set<double  , Vec512Double>(b)); }
// Vector += T
template<class Vector, class T> static SIMD_INLINE Vector operator+=(Vector& a, const T b) noexcept { return (a = a + b); }

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Substration
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// SSE2
static SIMD_INLINE Vec128Int operator-(const Vec128Int a, const Vec128Int b) noexcept {
    if constexpr (sizeof(SimdScalarType) == 1)      return _mm_sub_epi8(a, b);
    else if constexpr (sizeof(SimdScalarType) == 2) return _mm_sub_epi16(a, b);
    else if constexpr (sizeof(SimdScalarType) == 4) return _mm_sub_epi32(a, b);
    else if constexpr (sizeof(SimdScalarType) == 8) return _mm_sub_epi64(a, b);
}
static SIMD_INLINE Vec128Float  operator-(const Vec128Float  a, const Vec128Float  b) noexcept { return _mm_sub_ps(a, b); }
static SIMD_INLINE Vec128Double operator-(const Vec128Double a, const Vec128Double b) noexcept { return _mm_sub_pd(a, b); }
// AVX/AVX2
static SIMD_INLINE Vec256Int operator-(const Vec256Int a, const Vec256Int b) noexcept {
    if constexpr (sizeof(SimdScalarType) == 1)      return _mm256_sub_epi8(a, b);
    else if constexpr (sizeof(SimdScalarType) == 2) return _mm256_sub_epi16(a, b);
    else if constexpr (sizeof(SimdScalarType) == 4) return _mm256_sub_epi32(a, b);
    else if constexpr (sizeof(SimdScalarType) == 8) return _mm256_sub_epi64(a, b);
}
static SIMD_INLINE Vec256Float  operator-(const Vec256Float  a, const Vec256Float  b) noexcept { return _mm256_sub_ps(a, b); }
static SIMD_INLINE Vec256Double operator-(const Vec256Double a, const Vec256Double b) noexcept { return _mm256_sub_pd(a, b); }
// AVX512
static SIMD_INLINE Vec512Int operator-(const Vec512Int a, const Vec512Int b) noexcept {
    if constexpr (sizeof(SimdScalarType) == 1)      return _mm512_sub_epi8(a, b);
    else if constexpr (sizeof(SimdScalarType) == 2) return _mm512_sub_epi16(a, b);
    else if constexpr (sizeof(SimdScalarType) == 4) return _mm512_sub_epi32(a, b);
    else if constexpr (sizeof(SimdScalarType) == 8) return _mm512_sub_epi64(a, b);
}
static SIMD_INLINE Vec512Float  operator-(const Vec512Float  a, const Vec512Float  b) noexcept { return _mm512_sub_ps(a, b); }
static SIMD_INLINE Vec512Double operator-(const Vec512Double a, const Vec512Double b) noexcept { return _mm512_sub_pd(a, b); }
// Vector -= T
template<class Vector, class T> static SIMD_INLINE Vector operator-=(Vector& a, const T b) noexcept { return (a = a - b); }

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Multiplication
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// SSE2
static SIMD_INLINE Vec128Int operator*(const Vec128Int a, const Vec128Int b) noexcept {
    if constexpr (sizeof(SimdScalarType) == 2)      return _mm_mullo_epi16(a, b);
    else if constexpr (sizeof(SimdScalarType) == 4) return _mm_mullo_epi32(a, b);// highway gave a SSSE3 version
}
static SIMD_INLINE Vec128Float  operator*(const Vec128Float  a, const Vec128Float  b) noexcept { return _mm_mul_ps(a, b); }
static SIMD_INLINE Vec128Double operator*(const Vec128Double a, const Vec128Double b) noexcept { return _mm_mul_pd(a, b); }
// AVX/AVX2
static SIMD_INLINE Vec256Int operator*(const Vec256Int a, const Vec256Int b) noexcept {
    if constexpr (sizeof(SimdScalarType) == 2)      return _mm256_mullo_epi16(a, b);
    else if constexpr (sizeof(SimdScalarType) == 4) return _mm256_mullo_epi32(a, b);
}
static SIMD_INLINE Vec256Float  operator*(const Vec256Float  a, const Vec256Float  b) noexcept { return _mm256_mul_ps(a, b); }
static SIMD_INLINE Vec256Double operator*(const Vec256Double a, const Vec256Double b) noexcept { return _mm256_mul_pd(a, b); }
// AVX512
static SIMD_INLINE Vec512Int operator*(const Vec512Int a, const Vec512Int b) noexcept {
    if constexpr (sizeof(SimdScalarType) == 2)      return _mm512_mullo_epi16(a, b);
    else if constexpr (sizeof(SimdScalarType) == 4) return _mm512_mullo_epi32(a, b);
    else if constexpr (sizeof(SimdScalarType) == 8) return _mm512_mullo_epi64(a, b);
}
static SIMD_INLINE Vec512Float  operator*(const Vec512Float  a, const Vec512Float  b) noexcept { return _mm512_mul_ps(a, b); }
static SIMD_INLINE Vec512Double operator*(const Vec512Double a, const Vec512Double b) noexcept { return _mm512_mul_pd(a, b); }
// Vector *= T
template<class Vector, class T> static SIMD_INLINE Vector operator*=(Vector& a, const T b) noexcept { return (a = a * b); }

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Division
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// SSE2
static SIMD_INLINE Vec128Float  operator/(const Vec128Float  a, const Vec128Float  b) noexcept { return _mm_div_ps(a, b); }
static SIMD_INLINE Vec128Double operator/(const Vec128Double a, const Vec128Double b) noexcept { return _mm_div_pd(a, b); }
// AVX/AVX2
static SIMD_INLINE Vec256Float  operator/(const Vec256Float  a, const Vec256Float  b) noexcept { return _mm256_div_ps(a, b); }
static SIMD_INLINE Vec256Double operator/(const Vec256Double a, const Vec256Double b) noexcept { return _mm256_div_pd(a, b); }
// AVX512
static SIMD_INLINE Vec512Float  operator/(const Vec512Float  a, const Vec512Float  b) noexcept { return _mm512_div_ps(a, b); }
static SIMD_INLINE Vec512Double operator/(const Vec512Double a, const Vec512Double b) noexcept { return _mm512_div_pd(a, b); }
// Vector /= T
template<class Vector, class T> static SIMD_INLINE Vector operator/=(Vector& a, const T b) noexcept { return (a = a / b); }

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Shifts
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Vector << Vector
// SSE2
static SIMD_INLINE Vec128Int operator<<(const Vec128Int a, const Vec128Int b) noexcept {
    if constexpr (sizeof(SimdScalarType) == 2)      return _mm_sll_epi16(a, b);
    else if constexpr (sizeof(SimdScalarType) == 4) return _mm_sll_epi32(a, b);
    else if constexpr (sizeof(SimdScalarType) == 8) return _mm_sll_epi64(a, b);
}
// AVX/AVX2
static SIMD_INLINE Vec256Int operator<<(const Vec256Int a, const Vec128Int b) noexcept {
    if constexpr (sizeof(SimdScalarType) == 2)      return _mm256_sll_epi16(a, b);
    else if constexpr (sizeof(SimdScalarType) == 4) return _mm256_sll_epi32(a, b);
    else if constexpr (sizeof(SimdScalarType) == 8) return _mm256_sll_epi64(a, b);
}
// AVX512
static SIMD_INLINE Vec512Int operator<<(const Vec512Int a, const Vec128Int b) noexcept {
    if constexpr (sizeof(SimdScalarType) == 2)      return _mm512_sll_epi16(a, b);
    else if constexpr (sizeof(SimdScalarType) == 4) return _mm512_sll_epi32(a, b);
    else if constexpr (sizeof(SimdScalarType) == 8) return _mm512_sll_epi64(a, b);
}

// Vector << int
// SSE2
static SIMD_INLINE Vec128Int operator<<(const Vec128Int a, const int b) noexcept {
    if constexpr (sizeof(SimdScalarType) == 2)      return _mm_slli_epi16(a, b);
    else if constexpr (sizeof(SimdScalarType) == 4) return _mm_slli_epi32(a, b);
    else if constexpr (sizeof(SimdScalarType) == 8) return _mm_slli_epi64(a, b);
}
// AVX/AVX2
static SIMD_INLINE Vec256Int operator<<(const Vec256Int a, const int b) noexcept {
    if constexpr (sizeof(SimdScalarType) == 2)      return _mm256_slli_epi16(a, b);
    else if constexpr (sizeof(SimdScalarType) == 4) return _mm256_slli_epi32(a, b);
    else if constexpr (sizeof(SimdScalarType) == 8) return _mm256_slli_epi64(a, b);
}
// AVX512
static SIMD_INLINE Vec512Int operator<<(const Vec512Int a, const int b) noexcept {
    if constexpr (sizeof(SimdScalarType) == 2)      return _mm512_slli_epi16(a, b);
    else if constexpr (sizeof(SimdScalarType) == 4) return _mm512_slli_epi32(a, b);
    else if constexpr (sizeof(SimdScalarType) == 8) return _mm512_slli_epi64(a, b);
}

// Vector >> Vector
// SSE2
static SIMD_INLINE Vec128Int operator>>(const Vec128Int a, const Vec128Int b) noexcept {
    if constexpr (sizeof(SimdScalarType) == 2)      return _mm_srl_epi16(a, b);
    else if constexpr (sizeof(SimdScalarType) == 4) return _mm_srl_epi32(a, b);
    else if constexpr (sizeof(SimdScalarType) == 8) return _mm_srl_epi64(a, b);
}
// AVX/AVX2
static SIMD_INLINE Vec256Int operator>>(const Vec256Int a, const Vec128Int b) noexcept {
    if constexpr (sizeof(SimdScalarType) == 2)      return _mm256_srl_epi16(a, b);
    else if constexpr (sizeof(SimdScalarType) == 4) return _mm256_srl_epi32(a, b);
    else if constexpr (sizeof(SimdScalarType) == 8) return _mm256_srl_epi64(a, b);
}
// AVX512
static SIMD_INLINE Vec512Int operator>>(const Vec512Int a, const Vec128Int b) noexcept {
    if constexpr (sizeof(SimdScalarType) == 2)      return _mm512_srl_epi16(a, b);
    else if constexpr (sizeof(SimdScalarType) == 4) return _mm512_srl_epi32(a, b);
    else if constexpr (sizeof(SimdScalarType) == 8) return _mm512_srl_epi64(a, b);
}

// Vector >> int
// SSE2
static SIMD_INLINE Vec128Int operator>>(const Vec128Int a, const int b) noexcept {
    if constexpr (sizeof(SimdScalarType) == 2)      return _mm_srli_epi16(a, b);
    else if constexpr (sizeof(SimdScalarType) == 4) return _mm_srli_epi32(a, b);
    else if constexpr (sizeof(SimdScalarType) == 8) return _mm_srli_epi64(a, b);
}
// AVX/AVX2
static SIMD_INLINE Vec256Int operator>>(const Vec256Int a, const int b) noexcept {
    if constexpr (sizeof(SimdScalarType) == 2)      return _mm256_srli_epi16(a, b);
    else if constexpr (sizeof(SimdScalarType) == 4) return _mm256_srli_epi32(a, b);
    else if constexpr (sizeof(SimdScalarType) == 8) return _mm256_srli_epi64(a, b);
}
// AVX512
static SIMD_INLINE Vec512Int operator>>(const Vec512Int a, const int b) noexcept {
    if constexpr (sizeof(SimdScalarType) == 2)      return _mm512_srli_epi16(a, b);
    else if constexpr (sizeof(SimdScalarType) == 4) return _mm512_srli_epi32(a, b);
    else if constexpr (sizeof(SimdScalarType) == 8) return _mm512_srli_epi64(a, b);
}

// Vector <<= T, Vector >>= T
template<class Vector, class T> static SIMD_INLINE Vector operator<<=(Vector& a, const T b) noexcept { return (a = a << b); }
template<class Vector, class T> static SIMD_INLINE Vector operator>>=(Vector& a, const T b) noexcept { return (a = a >> b); }

// Rotation
template<class Vector> static SIMD_INLINE Vector rotl(const Vector a, const int b) noexcept { return (a << b) | (a >> (sizeof(SimdScalarType) * 8 - b)); }
template<class Vector> static SIMD_INLINE Vector rotr(const Vector a, const int b) noexcept { return (a >> b) | (a << (sizeof(SimdScalarType) * 8 - b)); }

}