add_executable(test test.c)

add_executable(start_after_network start_after_network.c)

target_link_libraries(start_after_network LINK_PUBLIC cmd common)