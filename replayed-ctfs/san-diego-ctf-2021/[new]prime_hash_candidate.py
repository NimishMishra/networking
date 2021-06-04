#!/usr/bin/env python3

PASSWD = "59784015375233083673486266"

def hash(data):
    out = 0
    for c in data:
        out *= 31
        out += ord(c)
    return str(out)

