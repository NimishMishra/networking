#!/usr/bin/env python3

ERROR = "Wrong password with hash "
SUCCESS = "Login successful!\nFlag: REDACTED\n"
PASSWD = 91918419847262345220747548257014204909656105967816548490107654667943676632784144361466466654437911844
secret1 = "REDACTED"
secret2 = "REDACTED"
secret3 = int("xxx")

def hash(data):
    out = 0
    data = [ord(x) ^ ord(y) for x,y in zip(data,secret1*len(data))]
    data.extend([ord(c) for c in secret2])
    for c in data:
        out *= secret3
        out += c
    return out

data = input("Please enter password below\n")

try:
    while True:
        if hash(data) == PASSWD:
            print(SUCCESS)
            break
        else:
            print(ERROR + str(hash(data)))
            data = input("Please enter password below\n")
except EOFError:
    pass
