f = open("shellcode.s", "a")

for _ in range(151):
	f.write("nop\n")
