### Crack the Hash

```html
Challenge: A hacker leaked the below hash online. Can you crack it to know the password of the CEO? 1ab566b9fa5c0297295743e7c2a6ec27
```

Head over to a website ([like this one](https://www.onlinehashcrack.com/hash-identification.php)) that can identify what hash was used. For this one, it becomes obvious some variation of ```MD5``` was used. Head over to another website([like this one](https://md5.gromweb.com/)) that can do reverse look up for a ```MD5 hash```. Doing the reverse look up for the hash will produce the flag.



###  Guess the Password

```html
Challenge: A hacker leaked the below hash online. Can you crack it to know the password of the CEO? the flag is the password Hash: 06f8aa28b9237866e3e289f18ade19e1736d809d
```

Head over to a website ([like this one](https://www.onlinehashcrack.com/hash-identification.php)) that can identify what hash was used. For this one, it becomes obvious some variation of ```SHA1``` was used. Head over to another website([like this one](https://sha1.gromweb.com/)) that can do reverse look up for a ```SHA1 hash```. Doing the reverse look up for the hash will produce the flag.

### Lineq

```tex
Challenge: Can you solve some equations for us? Hint: For modular inverse function. use (from Crypto.Util.number import inverse)
```

And the given file has the text:

```tex
15345857135052644158 * x[0] mod 15914389274045831441 = 10753153698913165324
10107862342967460188 * x[1] mod 12471333000718257439 = 8412981602133999892
15514951512896411 * x[2] mod 11189085043185963643 = 1482464683316586574
4918093547848646552 * x[3] mod 14953553045254805869 = 2025900790652430240
9458472078791077712 * x[4] mod 16969044464796096757 = 5398900907079313999
10389810153032407159 * x[5] mod 12219369241978883401 = 7029759589492702570
10317166141181737080 * x[6] mod 11051035063490494121 = 3468633932944308360
4739071230119101568 * x[7] mod 12446419077417014895 = 8675623443003281737
5602877978471499087 * x[8] mod 17033822019842116078 = 10322234074859615825
6817739495547298027 * x[9] mod 9516363895804911673 = 4437950083761802261
6427678547440599488 * x[10] mod 15079736889469193431 = 3279819731898553304
9457480281190568299 * x[11] mod 10650632135951148921 = 9305609025967996118
3811243068786264022 * x[12] mod 17812647846133398533 = 11526794456945961531
775941643434169870 * x[13] mod 11412472367550805013 = 4738382726559211541
7024610526778714279 * x[14] mod 9778393688778074575 = 5323545124401969226
11651575732234344955 * x[15] mod 16630642531754496501 = 2873213552124115822
6625087805180364133 * x[16] mod 9364964556418467329 = 2787565658998643270
3669801280657684382 * x[17] mod 14097382369878612419 = 7567005815588497736
5443984100737085739 * x[18] mod 10512797518085747507 = 7873334411288369657
12346616364541216766 * x[19] mod 15943449689777265613 = 3904160665454908058
8986565623928863916 * x[20] mod 18324134584075223407 = 188593124624644258
944611705353292388 * x[21] mod 11593718893451959913 = 5953933343058555785
9480419754515455118 * x[22] mod 14797616246348898583 = 13228205597299662061
6357470584650383564 * x[23] mod 10888050221402213645 = 3331190950406564692
4804105847411349449 * x[24] mod 15964574501738046999 = 9808705001033677355
The flag is chr(x[0]%256)+chr(x[1]%256)+...
```

The challenge relies on finding modular inverse. For given integers `a` and `m`, `x` is said to be the modular inverse of `a` and `m` if `(a*x) % m = 1`. In our situation, `a*x mod m = c`. We just need to note `(a *inv(a, m) *c) % m = c` to solve the problem. That is `x = inv(a, m) * c`. However, the developers inserted a little trick and you need to do `x = (inv(a, m) *c) % m` to get the correct flag. I wrote a python script to print out the flag:

```python
def inverse(a, m):
	mm = m 
	y = 0
	x = 1
	if (m == 1) :
		return 0
	while (a > 1) :
		# q is quotient 
		q = a // m
		t = m
		# m is remainder now, process 
		# same as Euclid's algo 
		m = a % m
		a = t
		t = y
		# Update x and y
		y = x - q * y
		x = t
		# Make x positive
	if (x < 0) :
		x = x + mm

	return x

with open('assets/lineq.txt') as f:
	content = f.readlines()
	f.close()
	content = content[:-1]
	content = [line.strip() for line in content]
	for line in content:
		line = line.split(' ');
		inv = inverse(int(line[0]), int(line[4]))
		x = (inv * int(line[6])) % int(line[4])
		print(chr(x % 256), end='')
```

### Arithmetic

Solved in collaboration with [wleightond](https://github.com/wleightond).

```tex
Challenge: SHA256 is safe, the cipher is not?
```

We are given a cipher text and the file used to encrypt the text.

```python
#-*- coding:utf-8 -*-

import os
from hashlib import sha256

def H(v):
    return int(sha256(str(v)).hexdigest(), 16)

def STEP(v):
    return (31338 * v**3 + 17 * v**2 + 2017 * v + 10) % 2**256

def encrypt(pt, key):
    state = H(key)
    ct = ""
    for c in pt:
        c = ord(c)
        for i in xrange(32):
            op = state % 4
            state = STEP(state)

            v = state % 256
            state = STEP(state)

            if op == 0:
                c = (c + v) % 256
            elif op == 1:
                c = (c ^ v) % 256
            elif op == 2:
                c = (c - v) % 256
            elif op == 3:
                c = (c * (v | 1)) % 256
        state ^= c
        ct += chr(c)
    return ct


print encrypt(open("flag.txt").read().strip(), os.urandom(32)).encode("hex")
## ciphertext: 868c017b7bef15e04ccc5f2d6b4c372fdff881080155
```

After a bit of playing around, we noticed that `op` was only producing `0` or `2` after the first random value. We also noticed that `STEP` function had a cycle and also always returned an even number. Both of these were observations that did not help.

[wleightond](https://github.com/wleightond) had the hunch that perhaps as long as we keep the final byte of the key constant, the subsequent final bytes were going to be the same on the output of the `STEP` function. So we verified it:

```python
 import os
 from hashlib import sha256
 
 ct = "868c017b7bef15e04ccc5f2d6b4c372fdff881080155".decode('hex')
 
 def H(v):
     return int(sha256(str(v)).hexdigest(), 16)
 
 def STEP(v):
     return (31338 * v**3 + 17 * v**2 + 2017 * v + 10) % 2**256
 
 # verify suspicion that as long as the last byte is the same
 # the step function will give us exactly the same sequence
 # of last bytes afterwards
 x = H(os.urandom(32))
 y = x % 256
 for i in range(100):
     if STEP(x) % 256 != STEP(y) % 256:
         print "wrong direction"
 print "suspicion verified"
```

From here, we knew that the first four bytes probably were `flag`. We could use that information to get the initial state. So we did.

```python
l = [encrypt('flag', i).encode('hex') for i in range(0, 256)]
l.index('868c017b')
```

This raised a `ValueError` because none of the initial state encrypted the text to that value. So we tried a little tweak.

```python
l = [encrypt('flag', i).encode('hex') for i in range(0, 256)]
l.index('868c017b')
```

This worked! The initial state was `47`.  So we wrote a script to brute force the rest of the flag.

```python
### ....
def encrypt(pt):
    state = 47
	### ...
ct = "868c017b7bef15e04ccc5f2d6b4c372fdff881080155".decode('hex')
pt = 'FLAG{'
while len(pt) < len(ct):
    c = chr(32)
    while encrypt(pt + c) != ct[:len(pt) + 1]: ## here you have to run the check for 
        ## for whole string (and not just single character) due to collision issue
        c = chr(ord(c) + 1)
    pt += c
print(pt)
```

Caveat: Use `python2` for running all programs. 

### genfei

#####  Solved in collaboration with [moni286](https://github.com/moni286)

The code we get from the organizers is

```python
import sys
from struct import pack, unpack

def F(w):
	return ((w * 31337) ^ (w * 1337 >> 16)) % 2**32

def encrypt(block):
	a, b, c, d = unpack("<4I", block)
	for rno in xrange(32):
		a, b, c, d = b ^ F(a | F(c ^ F(d)) ^ F(a | c) ^ d), c ^ F(a ^ F(d) ^ (a | d)), d ^ F(a | F(a) ^ a), a ^ 31337
		a, b, c, d = c ^ F(d | F(b ^ F(a)) ^ F(d | b) ^ a), b ^ F(d ^ F(a) ^ (d | a)), a ^ F(d | F(d) ^ d), d ^ 1337
	return pack("<4I", a, b, c, d)

pt = open(sys.argv[1]).read()
while len(pt) % 16: pt += "#"

ct = "".join(encrypt(pt[i:i+16]) for i in xrange(0, len(pt), 16))
open(sys.argv[1] + ".enc", "w").write(ct)
```

It's a Feistel Network and hence the name **gen**eralized **fei**stel. Basically chain rule. We can start by decrypting the d in the second step of encryption. From there it is easy to follow the chain and undo it. Here's the python script to decrypt the flag:

```python
## run with python2
from struct import pack, unpack

def F(w):
    return ((w * 31337) ^ (w * 1337 >> 16)) % 2**32

def decrypt(block):
    a, b, c, d = unpack("<4I", block)
    for i in xrange(32):
        # decrypting the second step in encrypt
        tempa = a
        d = d ^ 1337
        a = c ^ (F(d | F(d) ^ d))
        b = b ^ (F(d ^ F(a) ^ (d | a)))
        c = tempa ^ (F(d | F(b ^ F(a)) ^ F(d | b) ^ a))
        # decrypting the frist step in encrypt
        tempa = a
        a = d ^ 31337
        d = c ^ (F(a | F(a) ^ a))
        c = b ^ (F(a ^ F(d) ^ (a | d)))
        b = tempa ^ (F(a | F(c ^ F(d)) ^ F(a | c) ^ d))
    return pack("<4I", a, b, c, d)

ct = open("flag.enc").read()
pt = "".join(decrypt(ct[i:i+16]) for i in xrange(0,len(ct), 16))
print pt
```
