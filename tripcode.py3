#!/usr/bin/env python3
import crypt

def mktripcode(pw):
    pw = pw[:8]
    salt = (pw + "H.")[1:3]
    trip = crypt.crypt(pw, salt)
    print(name, "!" + trip[-10:])

name = input("What's your name?\n")
pazz = input("What's your tripkey?\n#")
mktripcode(pazz)
