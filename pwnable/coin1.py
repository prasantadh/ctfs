# written in python3
# the challenge is a simple binary search problem
# might require a couple runs before it gets the flag
# this is because data gets corrupt in transit
from pwn import *

conn = remote('pwnable.kr', 9007)
resp = conn.recv()
print(resp)

for i in range(100):

    resp = conn.recvline().strip().split(b' ')
    print(resp)
    N = int(resp[0].split(b'=')[1])
    C = int(resp[1].split(b'=')[1])
    print(N, C)

    l, m , r = 0, N // 2, N - 1
    for i in range(C):
        m = l + ((r - l) // 2)
        payload = b' '.join(str(k).encode() for k in range(l, m + 1))
        print(l, m, r, ': sending', payload)
        conn.sendline(payload)
        resp = int(conn.recv().strip())
        print(resp)
        if (r == l + 1):
            if resp == 10: ans = r
            else: ans = l
        if resp == (m - l + 1) * 10:
            l = m + 1
            if (l == r): ans = l
        else:
            r = m
    payload = str(ans).encode()
    print(l, m, r, ': sending ans: ', payload)
    conn.sendline(payload)
    resp = conn.recv()
    print(resp)
resp = conn.recv()
print(resp)

conn.close()
