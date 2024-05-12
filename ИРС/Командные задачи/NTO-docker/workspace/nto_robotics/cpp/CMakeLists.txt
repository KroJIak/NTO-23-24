cmake_minimum_required(VERSION 3.8 FATAL_ERROR)
project(nto_sim LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_CXX_FLAGS "-Wall -Wextra -pipe -O2")
set(CMAKE_CXX_COMPILER g++)

## Find libraries and modules
find_package(OpenCV REQUIRED)
find_package(Threads)

include_directories(
    include
    ${OpenCV_INCLUDE_DIRS}
)
link_directories(/usr/local/lib/nto_sim)

## Executables
add_executable(solution1
    src/solution1.cpp
)
target_link_libraries(solution1
    nto_sim nto_task1 ${OpenCV_LIBS} Threads::Threads
)

add_executable(solution5
    src/solution5.cpp
)
target_link_libraries(solution5
    nto_sim nto_task5 ${OpenCV_LIBS} Threads::Threads
)

add_executable(solution6
    src/solution6.cpp
)
target_link_libraries(solution6
    nto_sim nto_task6 ${OpenCV_LIBS} Threads::Threads
)
