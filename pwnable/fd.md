#### fd

```sh
Challenge: Mommy! what is a file descriptor in Linux?

* try to play the wargame your self but if you are ABSOLUTE beginner, follow this tutorial link:
https://youtu.be/971eZhMHQQw

$ ssh fd@pwnable.kr -p2222 (pw:guest)
$ ls
$ flag fd fd.c
# cat flag gives permission denied
$ cat flag.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char buf[32];
int main(int argc, char* argv[], char* envp[]){
    if(argc<2){
        printf("pass argv[1] a number\n");
        return 0;
    }
    int fd = atoi( argv[1] ) - 0x1234;
    int len = 0;
    len = read(fd, buf, 32);
    if(!strcmp("LETMEWIN\n", buf)){
        printf("good job :)\n");
        system("/bin/cat flag");
        exit(0);
    }
    printf("learn about Linux file IO\n");
    return 0;
}
$ # we need to give it 0x1234 to read from STDIN
$ echo $(( 16#1234 ))
4660
$ ./fd 4660
LETMEWIN
good job :)
# the flag will be printed on this line.
```