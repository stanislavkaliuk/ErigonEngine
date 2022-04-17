set(CMAKE_LEGACY_CYGWIN_WIN32 0)
cmake_minimum_required(VERSION 3.9)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)



project(ErigonEngine CXX)

set(ENGINE_VERSION_MAJOR 1)
set(ENGINE_VERSION_MINOR 0)
set(ENGINE_VERSION_PATCH 0)

enable_testing()

set(WERROR ON CACHE BOOL "Warnings as Errors.")
set(ENGINE_EXPORT_DIR cmake/engine CACHE STRING "Directory to install cmake config files.")

set(BUILD_SHARED_LIBS ON CACHE BOOL "Build modules as shared libraries")
set(BUILD_TESTS ON CACHE BOOL "Build tests.")
set(BUILD_SAMPLE ON CACHE BOOL "Build sample project")

set(CMAKE_DEBUG_POSTFIX "" CACHE STRING "Default filename postfix for libraries under configuration DEBUG")

if(WIN32)
    set(TOOLSET)
    if(CMAKE_VS_PLATFORM_TOOLSET)
    string(REGEX REPLACE "^v" "" TOOLSET "${CMAKE_VS_PLATFORM_TOOLSET}")
    endif()
    set(API_TAG "${TOOLSET}_${ENGINE_VERSION_MAJOR}_${ENGINE_VERSION_MINOR}" CACHE STRING "Postfix tag for engine abi")
else()
set(API_TAG "" CACHE STRING "Postfix tag for engine abi")
endif()

if(NOT BUILD_SHARED_LIBS)
set(TEST_LIBRARY_TARGET_TYPE OBJECT)
endif()

set(WARNINGS)

if(CMAKE_CXX_COMPILER_ID MATCHES "Clang" OR IOS)
message("-- Setting clang options")
    set(WARNINGS -Wall -Wextra -Wcast-qual -Wconversion -Wformat=2 -Winit-self -Winvalid-pch -Wmissing-format-attribute -Wmissing-include-dirs -Wpacked -Wredundant-decls)
    set(OSX_SUPPRESSIONS -Wno-overloaded-virtual -Wno-sign-conversion -Wno-deprecated -Wno-unknown-pragmas -Wno-reorder -Wno-char-subscripts -Wno-switch -Wno-unused-parameter -Wno-unused-variable -Wno-deprecated -Wno-unused-value -Wno-unknown-warning-option -Wno-return-type-c-linkage -Wno-unused-function -Wno-sign-compare -Wno-shorten-64-to-32 -Wno-unused-local-typedefs)
    set(WARNINGS ${WARNINGS} ${OSX_SUPPRESSIONS})
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -stdlib=libc++ -Wno-return-type-c-linkage -Wno-unneeded-internal-declaration")
    set(CMAKE_XCODE_ATTRIBUTE_CLANG_CXX_LIBRARY "libc++")
    set(CMAKE_XCODE_ATTRIBUTE_CLANG_CXX_LANGUAGE_STANDARD "c++17")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -fno-strict-aliasing")
elseif(CMAKE_CXX_COMPILER_ID MATCHES "GNU")
    message("-- Setting gcc options")
    set(WARNINGS -Wall -Wextra -Wunused-parameter -Wcast-align -Wcast-qual -Wconversion -Wformat=2 -Winit-self -Winvalid-pch -Wmissing-format-attribute -Wmissing-include-dirs -Wpacked -Wredundant-decls -Wunreachable-code)
    set(LD_FLAGS "${LD_FLAGS} -Wl,-z,defs")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -fno-strict-aliasing")
    if(CMAKE_CXX_COMPILER_VERSION VERSION_LESS 4.8)
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fpermissive -D_GLIBCXX_USE_SCHED_YIELD -D_GLIBCXX_USE_NANOSLEEP")
    endif()
elseif(CMAKE_CXX_COMPILER_ID MATCHES "MSVC")
    message("-- Setting msvc options")
    set(WARNINGS)
    set(CMAKE_STATIC_LINKER_FLAGS "${CMAKE_STATIC_LINKER_FLAGS} /ignore:4264")
    add_compile_options(/bigobj)
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /MP /Oi /fp:fast")
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /MP /fp:fast")
    set(CMAKE_SHARED_LINKER_FLAGS_RELEASE "${CMAKE_SHARED_LINKER_FLAGS_RELEASE} /profile /OPT:REF /OPT:ICF")
    if (NOT (MSVC_VERSION LESS 1920))
        add_compile_options(/permissive-)
    endif()
else()
    message("-- Unknown compiler, success is doubtful.")
    message("CMAKE_CXX_COMPILER_ID=${CMAKE_CXX_COMPILER_ID}")
endif()

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}/bin")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}/lib")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY "${PROJECT_BINARY_DIR}/lib")

add_subdirectory(src)

if(BUILD_TEST)
    add_subdirectory(tests)
endif()

if(BUILD_SAMPLE)
    add_subdirectory(sampleProject)
endif()