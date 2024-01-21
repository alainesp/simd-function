###############################################################################################################
# This file is part of 'simd-function'
###############################################################################################################
cmake_minimum_required (VERSION 3.12)

project (bool_function_optimization VERSION 1.0.0.0 DESCRIPTION "Optimize boolean functions" LANGUAGES CXX)

# Enable Hot Reload for MSVC compilers if supported.
if (POLICY CMP0141)
  cmake_policy(SET CMP0141 NEW)
  set(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT "$<IF:$<AND:$<C_COMPILER_ID:MSVC>,$<CXX_COMPILER_ID:MSVC>>,$<$<CONFIG:Debug,RelWithDebInfo>:EditAndContinue>,$<$<CONFIG:Debug,RelWithDebInfo>:ProgramDatabase>>")
endif()

###############################################################################################################
# Optimize
###############################################################################################################
add_executable(optimize optimize.cpp)
set_property(TARGET optimize PROPERTY CXX_STANDARD 20)	 # C++ language to use
