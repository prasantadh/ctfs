### Collision

Preliminary:
```bash
$ ls
col     col.c   flag
$ cat flag
cat: flag: Permission denied
$ ls -la
total 36
drwxr-x---  5 root    col     4096 Oct 23  2016 .
drwxr-xr-x 87 root    root    4096 Dec 27 23:17 ..
d---------  2 root    root    4096 Jun 12  2014 .bash_history
-r-sr-x---  1 col_pwn col     7341 Jun 11  2014 col
-rw-r--r--  1 root    root     555 Jun 12  2014 col.c
-r--r-----  1 col_pwn col_pwn   52 Jun 11  2014 flag
dr-xr-xr-x  2 root    root    4096 Aug 20  2014 .irssi
drwxr-xr-x  2 root    root    4096 Oct 23  2016 .pwntools-cache
$ cat col.c
#include <stdio.h>
#include <string.h>
unsigned long hashcode = 0x21DD09EC;
unsigned long check_password(const char* p){
	int* ip = (int*)p;
	int i;
	int res=0;
	for(i=0; i<5; i++){
		res += ip[i];
	}
	return res;
}

int main(int argc, char* argv[]){
	if(argc<2){
		printf("usage : %s [passcode]\n", argv[0]);
		return 0;
	}
	if(strlen(argv[1]) != 20){
		printf("passcode length should be 20 bytes\n");
		return 0;
	}

	if(hashcode == check_password( argv[1] )){
		system("/bin/cat flag");
		return 0;
	}
	else
		printf("wrong passcode.\n");
	return 0;
}
```
Seems simple enough. Give in 20 bytes. This will be interpreted as integers and summed. If the sum is `0x21DD09EC`, I get the flag. Note that on given system, the byte ordering integer is little endian.

#### What did not work:

```sh
$ echo '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xEC\x09\xDD\x21' | ./col
```

Surprising the error was `usage : %s [passcode]\n`. Turns out what is piped  in is not counted as an extra argument. So, the alternative was:

```sh
$ ./col `echo '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xEC\x09\xDD\x21'`
```

Here I hit a couple extra problems. `echo` was putting in an extra new line character at the end. At the same time, echo was also not printing out bytes as I was expecting it to. It was just printing out each character as its own. So I  had to enable a couple other options.

```sh
$ ./col `echo -n -e '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xEC\x09\xDD\x21'`
```

Then I hit the next problem where the null bytes weren't being printed at all. So the input I was providing was not twenty bytes. So I had to finally stop being lazy and fire up a python console.

```python
>>> from struct import pack
>>> pack("<I", 0x21DD09EC // 5) * 4 + pack("<I", 0x21DD09EC // 5 + 0x21DD09EC % 5)
b'\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xcc\xce\xc5\x06'
```

Now to get the flag:

```sh
$ ./col `echo -n -e"\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xcc\xce\xc5\x06"`
```





