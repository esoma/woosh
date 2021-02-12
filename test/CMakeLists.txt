cmake_minimum_required(VERSION 3.10)

project(WooshTests)

add_executable(test_fifobuffer test_fifobuffer.c)
add_executable(test_lifobuffer test_lifobuffer.c)

target_include_directories(test_fifobuffer PUBLIC
                           "../src/")
target_include_directories(test_lifobuffer PUBLIC
                           "../src/")