input= b't2q}*\x7f&n[5V\xb42a\x7f3\xac\x87\xe6\xb4' # these are now bytes

a = lambda n: a(n-2) + a(n-1) if n >= 2 else (2 if n == 0 else 1)

flag = "sdctf{"

flag = ( input[i] ^ (a(i) & 0xff) for i in range(len(input)))
decode_flag = ''.join(list(map(lambda x: chr(x), flag)))
print(decode_flag)
