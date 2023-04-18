/*
 * Created by Young on 2023/4/19.
 */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "../include/cmd/ping.h"
#include "../include/cmd/start.h"
#include "../include/common/window.h"

typedef enum {
    PARAM_EMPTY, PARAM_MINIMIZE, PARAM_HIDE,
} PARAM;

const static struct {
    PARAM p;
    const char *str;
} map[] = {
        {PARAM_MINIMIZE, "-m"},
        {PARAM_MINIMIZE, "--minimized"},
        {PARAM_HIDE,     "-h"},
        {PARAM_HIDE,     "--hide"},
};

PARAM str2param(const char *str) {
    int j;
    for (j = 0; j < sizeof(map) / sizeof(map[0]); ++j)
        if (!strcmp(str, map[j].str))
            return map[j].p;
    fprintf(stderr, "invalid param: %s", str);
    return PARAM_EMPTY;
}

int main(int argc, char *argv[]) {
    for (int i = 1; i < argc; ++i) {
        switch (str2param(argv[i])) {
            case PARAM_EMPTY:
                break;
            case PARAM_MINIMIZE:
                minimize_window();
                break;
            case PARAM_HIDE:
                hide_window();
                break;
        }
    }

    // test network until pass
    for (int i = 0; i < 12 && ping("www.baidu.com"); ++i) {
        sleep(5);
        if (i == 11) {
            fprintf(stdout, "Network Error");
            return EXIT_FAILURE;
        }
    }

    char buf[1 << 10];
    memset(buf, 0, 1 << 10);

    static char path[1 << 9];
    snprintf(path, sizeof(path), "%s%s", getenv("userprofile"), "\\start_after_network.list");
    const char *config_list[] = {
            "./start_after_network.list",
            "./conf/start_after_network.list",
            "../conf/start_after_network.list",
            path
    };

    FILE *list;
    for (int j = 0; j < (sizeof(config_list) / sizeof(const char *)); ++j) {
        if (NULL != (list = fopen(config_list[j], "r"))) {
            fprintf(stdout, "\nConfig find: %s\n", config_list[j]);
            break;
        }

        if (j == (sizeof(config_list) / sizeof(const char *) - 1)) {
            fprintf(stderr, "\nNot Found Config: start_after_network.list\n");
            return EXIT_FAILURE;
        }
    }

    char *line;
    while (NULL != (line = fgets(buf, 1 << 10, list))) {
        if (line[strlen(line) - 1] == '\n') {
            line[strlen(line) - 1] = '\0';
        }
        if (start(line)) {
            fprintf(stderr, "Open failed: %s", line);
            return EXIT_FAILURE;
        }
    }

    fclose(list);
    return EXIT_SUCCESS;
}