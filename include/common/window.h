/*
 * Created by Young on 2023/4/19.
 */

#ifndef SHELL_WINDOW_H
#define SHELL_WINDOW_H

void hide_window();

void minimize_window();

__attribute__((destructor))
void show_window();

#endif //SHELL_WINDOW_H
