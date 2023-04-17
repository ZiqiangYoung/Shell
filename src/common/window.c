/*
 * Created by Young on 2023/4/19.
 */
#include <windows.h>

#include "../../include/common/window.h"

void hide_window() {
    ShowWindow(GetConsoleWindow(), SW_HIDE);
}

void minimize_window() {
    ShowWindow(GetConsoleWindow(), SW_SHOWMINNOACTIVE);
}

void show_window() {
    ShowWindow(GetConsoleWindow(), SW_SHOW);
}
