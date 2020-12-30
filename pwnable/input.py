from sys import stdout
from pwn import *
from struct import pack, unpack
session = ssh(host='pwnable.kr',
                port=2222,
                user='input2',
                password='guest')
# stage 1
argv = ['a'] * 100
argv[0] = '/home/input2/input'
argv[ord('A')] = '\x00'
argv[ord('B')] = '\x20\x0a\x0d'

# stage 2
# on the server run
# python3
# with open('input2Stdin', 'wb') as f:
#   f.write(b'\x00\x0a\x00\xff')
# with open('input2Stdin', 'wb') as f:
#   f.write(b'\x00\x0a\x02\xff')

# stage 3
env = { pack('>I', 0xdeadbeef) : pack('>I', 0xcafebabe) }

# stage 4
# on the server run
# python3
# with open('\x0A', 'wb') as f: f.write(b'\x00' * 4)

# stage 5
# because we have changed the cwd, in order to get the flag:
# cd /tmp/bhakku
# ln -s /home/input2/flag flag
from random import randint
port = str(randint(10000, 20000))
argv[ord('C')] = port
print('Open port: %s' % port)
p = session.process(argv=argv,
                    env=env,
                    stdin='/tmp/bhakku/input2Stdin',
                    stderr='/tmp/bhakku/input2Stderr',
                    cwd='/tmp/bhakku/')
# echo -e "\xde\xad\xbe\ef" | nc localhost <port>
session.interactive()
print(p.recv())
session.close()
