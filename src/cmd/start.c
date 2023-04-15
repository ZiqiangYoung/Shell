/*
 * Created by Young on 2023/4/16.
 */
#include <stdio.h>
#include <stdlib.h>

#include "../../include/cmd/start.h"

int start(const char *program_path) {
    char command[1 << 9];
    snprintf(command, sizeof(command), "%s%s", "start \"start program\" ", program_path);
    return system(command) ? EXIT_FAILURE : EXIT_SUCCESS;
}

