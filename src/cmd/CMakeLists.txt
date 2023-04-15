add_library(cmd ping.c start.c)

target_include_directories (cmd PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})