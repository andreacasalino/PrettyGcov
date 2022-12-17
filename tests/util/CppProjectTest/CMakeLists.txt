cmake_minimum_required(VERSION 3.0 FATAL_ERROR)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

project(CppSample)

option(ENABLE_GCOV "Enable gcov report generation" ON)
if(ENABLE_GCOV)
  message(STATUS "gcov enabled")
  # # This is required to generate coverage report
  SET(GCC_COVERAGE_COMPILE_FLAGS "-fprofile-arcs -ftest-coverage")
	SET(GCC_COVERAGE_LINK_FLAGS "-lgcov --coverage")
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${GCC_COVERAGE_COMPILE_FLAGS}")
	set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${GCC_COVERAGE_LINK_FLAGS}")
else()
    message(STATUS "gcov NOT enabled")
endif()

include(FetchContent)
message(STATUS "fetching deps")
SET(BUILD_XML_Parser_SAMPLES OFF CACHE BOOL "samples OFF" FORCE)
SET(BUILD_XML_Parser_TESTS ON CACHE BOOL "tests ON" FORCE)
FetchContent_Declare(
  xml-parser
  GIT_REPOSITORY https://github.com/andreacasalino/XML-parser.git
  GIT_TAG        d3f2810bd5b1e278d0fb2e8eadd2b24ff533f11e
)
FetchContent_MakeAvailable(xml-parser)
