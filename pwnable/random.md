### random

Here's the challenge:

```c
#include <stdio.h>

int main(){
	unsigned int random;
	random = rand();	// random value!

	unsigned int key=0;
	scanf("%d", &key);

	if( (key ^ random) == 0xdeadbeef ){
		printf("Good!\n");
		system("/bin/cat flag");
		return 0;
	}

	printf("Wrong, maybe you should try 2^32 cases.\n");
	return 0;
}
```

_Note: the authors do not seem to actually use these `c` files for compilation as they would have needed `<stdlib.h>` for using rand() function._ Anyway, the vulnerability is that `rand()` function does not return a random value. It returns the same value every single time for a system. To find out what value is returned for this system, browse to `/tmp/` and create a test file:

```c
/* $ vi /tmp/test.c */
#include <stdio.h>
#include <stdlib.h>
int main() {
	printf("%d\n", rand());
}
/* $ gcc /tmp/test.c && ./a.out */
```

This returned the value 1804289383. From here all we had to do to get the flag was:

```sh
$ echo $(( 1804289383 ^ 0xdeadbeef )) | ./random
```

