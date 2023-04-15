/*
 * Created by Young on 2023/4/19.
 */
#include <stdio.h>
#include <stdlib.h>

#include "../../include/cmd/ping.h"

int ping(const char *url) {
    char command[1 << 9];
    snprintf(command, sizeof(command), "%s%s", "ping ", url);

    return system(command) ? EXIT_FAILURE : EXIT_SUCCESS;
}