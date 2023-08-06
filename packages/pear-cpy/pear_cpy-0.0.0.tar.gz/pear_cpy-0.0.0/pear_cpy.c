#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <limits.h>
#include <string.h>
#include <errno.h>

char cpy_out[4096] = {0};

char * pear_cpy(char * input, size_t length)
{
    char cmd[length + 1];
    memcpy(cmd, input, length);
    cmd[length] = 0;

    memset(cpy_out, 0, 4096);

    int pipefds[2];
    if (pipe(pipefds) != 0) {
        return "Unable to create pipe";
    }

    int status;
    pid_t pid = fork();

    if (pid == 0) {
        // In child

        while ((dup2(pipefds[1], STDOUT_FILENO) == -1) && (errno == EINTR));

        close(pipefds[0]);

        execv("/usr/bin/python3", (char * const []) { "/usr/bin/python3", "-c", cmd, NULL });

    } else if (pid > 0) {
        // In parent
        close(pipefds[1]);
        pid = wait(&status);

        read(pipefds[0], cpy_out, 4096);
 
   } else {
        // Error
        return "Unable to fork";
    }

    return cpy_out;
}

int main() {

    char cmd[] = "print('test')";
    printf("res:%s\n", pear_cpy(cmd, strlen(cmd)));

    return 0;
}