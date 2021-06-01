#! /usr/bin/env python3
FLAG = 'sdctf{a_v3ry_s3cur3_w4y_t0_st0r3_ur_FLAG}' # lol

a = lambda n: a(n-2) + a(n-1) if n >= 2 else (2 if n == 0 else 1)

b = lambda x: bytes.fromhex(x).decode()

h = eval(b('7072696e74')) # built in function "print"

def d():
    h(b('496e636f727265637420666c61672120596f75206e65656420746f206861636b206465657065722e2e2e')) # Incorrect flag! You need to hack deeper...
    eval(b('5f5f696d706f72745f5f282273797322292e65786974283129')) # exit function
    h(FLAG) # prints the flag

def e(f):
    h("Welcome to SDCTF's the first Reverse Engineering challenge.")
    flag_input = input("Input the correct flag: ")
    
    # RHS value is 73646374667b. Find x such that x.encode().hex() == RHS. The value is sdctf{
    if flag_input[:6].encode().hex() != '{2}3{0}{1}{0}3{2}{1}{0}{0}{2}b'.format(*map(str, [6, 4, 7])):
        d()
    # int(chr(45) + chr(49)) = -1 -> flag_input[-1] != }
    if flag_input[int(chr(45) + chr(49))] != chr(125):
        d()
   
    g = flag_input[6:-1].encode() # everything between { and }
    
    # length of the flag = 20. And this is XOR operation which cancels itself. So basically, we want g[i] = f[i] ^ (a(i) & 0xff)
    if bytes( (g[i] ^ (a(i) & 0xff) for i in range(len(g))) ) != f:
        d()
    h(b('4e696365206a6f622e20596f7520676f742074686520636f727265637420666c616721')) # Nice job. You got the correct flag!

if __name__ == "__main__":
    e(b't2q}*\x7f&n[5V\xb42a\x7f3\xac\x87\xe6\xb4') # the function call e
else:
    eval(b('5f5f696d706f72745f5f282273797322292e65786974283029')) # exit
