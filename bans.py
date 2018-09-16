#!/usr/bin/env python3

with open("bans.txt", "r") as ban:
    ban = ban.read().splitlines()

bans = {}
for b in ban:
    b = b.split(" ")
    b[1] = " ".join(b[1:])
    bans[b[0]] = b[1]


def is_banned(ip):
    ip = str(ip)
    for b in bans.keys():
        if ip.startswith(b):
            return bans[b]
    return 0
