import itertools, sys, time

# py sol.py [ciphertext file]
def main():
	W = 7
	perm = [0,1,2,3,4,5,6]
	perm2 = []
	output = open('qq.txt', 'wt')
	l = itertools.permutations(perm, 7)



	print(" ... xCrIpT bY [70RP3D0] aka [F34R_0x00] ... \n\n")
	time.sleep(5)
	print("Transposition Key unknown!! . . . \n\n")
	time.sleep(2)
	print("iNiTiATiNg Key brutefOrCiNg SeQuEnCe!! . . .\n\n")
	time.sleep(3)

	for pack in l:
		res=""
		msg = "FLAG{lets_find_a_kind_of_reverse_logic_}.." #Known plaintext attack!!! FLAG{----------------------------------}..
		perm = list(pack)
		for i in range(100):
		    msg = msg[1:] + msg[:1]
		    msg = msg[0::2] + msg[1::2]
		    msg = msg[1:] + msg[:1]
		    res = ""
		    for j in range(0, len(msg), W):
		        for k in range(W):
		            res += msg[j:j+W][perm[k]]
		    msg = res
		print(msg, perm)
		output.writelines(f"res[{msg}]		perm[{perm}]\n\n")
		if msg[12] == "." and msg[40] == "." and msg[0:2] == "L{" and msg[28] == "}":
			output.writelines(f"match found! ...res[{msg}]		 perm[{perm}]\n\n")
			perm2 = perm

	time.sleep(2)
	print("\n\nTransposition Key found!!! ... => ",perm2)
	time.sleep(2)
	print("\n\nXtarting Reverse Sequence!! . . .")
	time.sleep(3)
	msg =  open(f'{sys.argv[1]}', 'rt').read().strip()

	for z in range(100):
		char = []
		res=""
		for x in range(42):
			char.append(" ")
		for x in range(0,42,7):
			sl = msg[x:x+7]
			for y,z in enumerate(sl):
				char[perm2[y]+x] = z
		msg = "".join(char)
		msg = msg[-1::]+msg[:-1]
		for x in range(0,len(msg),21):
			slc = msg[x:x+21]
			if x == 0:
				print("slice even - ",slc)
				count = 0
				for y in slc:
					char[count] = y
					count += 2
			if x == 21:
				print("slice odd - ",slc)
				count = 1
				for y in slc:
					char[count] = y
					count += 2

		msg = "".join(char)
		msg = msg[-1::]+msg[:-1]

	time.sleep(1)
	print("\n\n ... Reverse Sequence Completed! ... \n\n")
	time.sleep(2)
	print(" ... yEa ... glad yOu foUnd It useFuL ...siMplE iSn'T iT? ... \n ... rUn A xCrIpT = gEt A fLaG ... \n ... It oNlY tOoK aBoUt 30!!hours! of frustration!! and code restructuring!! ... \n ... anyWaYs ... hErE's ThE fLaG ... \n ... hElP yOuRsElF oR wAiT FoR mE tO pRiNt It In 30!hOuRs! TiMe!! ... \n ... 70RP3D0 ... ")
	time.sleep(108000)
	print("\n [",msg,"]")



if __name__ == '__main__':

	print(""" 
  ______  ___   _____   _____  ____       _   ___  
 |____  |/ _ \ |  __ \ |  __ \|___ \     | | / _ \ 
     / /| | | || |__) || |__) | __) |  __| || | | |
    / / | | | ||  _  / |  ___/ |__ <  / _` || | | |
   / /  | |_| || | \ \ | |     ___) || (_| || |_| |
  /_/    \___/ |_|  \_\|_|    |____/  \__,_| \___/ 
                                                   """)

	main()



# THIS EMAIL CONTAINS THE EICAR TEST FILE

# (See attached file: eicar.com)

# THIS EMAIL CONTAINS THE EICAR TEST FILE
# --1__=09BBF621DFF91C838f9e8a93df938690918c09BBF621DFF91C83
# Content-type: text/html; charset=US-ASCII
# Content-Disposition: inline

# <html><body>
# <p><font size="2" face="sans-serif">THIS EMAIL CONTAINS THE EICAR TEST FILE</font><br>
# <br>
# <i>(See attached file: eicar.com)</i><br>
# <br>
# <font size="2" face="sans-serif">THIS EMAIL CONTAINS THE EICAR TEST FILE</font></body></html>

# --1__=09BBF621DFF91C838f9e8a93df938690918c09BBF621DFF91C83--


# --0__=09BBF621DFF91C838f9e8a93df938690918c09BBF621DFF91C83
# Content-type: application/octet-stream; 
# 	name="eicar.com"
# Content-Disposition: attachment; filename="eicar.com"
# Content-ID: <1__=09BBF621DFF91C838f9e8a93df93@maysoft.com>
# Content-transfer-encoding: base64

# WDVPIVAlQEFQWzRcUFpYNTQoUF4pN0NDKTd9JEVJQ0FSLVNUQU5EQVJELUFOVElWSVJVUy1URVNU
# LUZJTEUhJEgrSCo=

