import os
import re
from collections import defaultdict
import webtools as wt

with open('./set.txt', 'r') as sett:
    sett = sett.read().splitlines()

sd = {}
for n, s in enumerate(sett):
    if len(s) > 1 and s[0] not in ["", "#", " "]:
        s = s.split(':')
        if len(s) > 2:
            s[1] = ":".join(s[1:])
        sd[s[0]] = s[1]
        sett[n] = s[0]
    else:
        sett[n] = ''
sett = [i for i in sett if i]

def load_thread(th):
    th = int(th)
    thp = str(sd['thrdb'] + str(th) + '.txt')
    if not os.path.exists(thp):
        return None
    with open(thp, 'r') as mt:
        mt = mt.read().splitlines()
    return mt
        
def do_backlink(th='0'):
    mt = load_thread(th)
    bld = defaultdict(list)
    for n, t in enumerate(mt):
        repl = re.findall(r'\&gt;\&gt;[1-9][00-99]*', t)
        repl = [r[8:] for r in repl if r]
        for r in repl:
            if int(r) >= len(mt) or str(n) in bld[r]:
                continue
            bld[r].append(str(n))

    for r in sorted([int(k) for k in bld.keys()]):
        r = str(r)
    return bld
    
def main():
    print(" ")

if __name__ == "__main__":
    main()
