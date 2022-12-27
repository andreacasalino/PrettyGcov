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
$OPTIONS
FetchContent_Declare(
  $NAME
  GIT_REPOSITORY $URL
  GIT_TAG        $TAG
)
FetchContent_MakeAvailable($NAME)
