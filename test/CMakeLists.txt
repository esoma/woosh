cmake_minimum_required(VERSION 3.10)

project(WooshTests)

set(GCC_COVERAGE_COMPILE_FLAGS "-fprofile-arcs -ftest-coverage")
set(GCC_COVERAGE_LINK_FLAGS    "-fprofile-arcs")

set(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} ${GCC_COVERAGE_COMPILE_FLAGS}")
set(CMAKE_EXE_LINKER_FLAGS  "${CMAKE_EXE_LINKER_FLAGS} ${GCC_COVERAGE_LINK_FLAGS}")

add_executable(test_fifobuffer ../src/fifobuffer.c test_fifobuffer.c)
add_executable(test_lifobuffer ../src/lifobuffer.c test_lifobuffer.c)

target_include_directories(test_fifobuffer PUBLIC
                           "../src/")
target_include_directories(test_lifobuffer PUBLIC
                           "../src/")