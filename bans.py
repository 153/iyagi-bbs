
#!/usr/bin/env python3

bans = {
    "36.250":"spam",
    "36.248":"spam",
    "46.16": "spam",
    "88.198.48":"nazi",
    "62.210":"spam"
}

def is_banned(ip):
    ip = str(ip)
    for b in bans.keys():
        if b in ip:
            return bans[b]
    return 0
