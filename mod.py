#!/usr/bin/env python3
import os

thread_dir = "./threads/"

with open("list.txt", "r") as lis:
    lis = lis.read().splitlines()    
with open("ips.txt", "r") as ips:
    ips = ips.read().splitlines()
with open("ips2.txt", "r") as ips2:
    ips2 = ips2.read().splitlines()

def menu():
    # delete a thread, moderate a post, or moderate a thread
    
    modes = ["del_thread", "mod_post", "mod_thread"]
    for n, i in enumerate(modes):
        print(n+1, " - ", i)
    pic_mode = input("Pick a mode.\n")
    if modes[int(pic_mode) -1]:
        m_mod = modes[int(pic_mode) -1]
        print(m_mod)
    thr = input("Thread to load:\n> ")
    eval(str(m_mod + "(" + thr + ")"))

def mod_thread(thr=''):
    # open a thread, pick a mode [0-4], then write thread
    # and update list
    
    modes = ["normal", "lock", "sticky", "stickylock", "nobump"]
    tmod = -1
    thr = str(thr)
    with open(thread_dir + thr + ".txt") as tth:
        tth = tth.read().splitlines()
    if len(tth[0].split("><")) > 1:
        tmod = int(tth[0].split("><")[1])
    if tmod > 0:
        print("Thread is currently", modes[tmod])
    for n, i in enumerate(modes):
        modes[n] = str(n) + " ~ " + i
    print("New mode?\n *", "\n * ".join(modes))
    nmod = input("[0-4] ")
    tth[0] = tth[0].split(" >< ")[0] + " >< " + nmod
    print("\n".join(tth))
    with open(thread_dir + thr + ".txt", 'w') as th:
        th.write("\n".join(tth) + "\n")
    for n, i in enumerate(lis):
        if i.startswith(thr):
            i = i[:-1]
            i += str(nmod)
            lis[n] = i
    with open("list.txt", "w") as listw:
        listw.write("\n".join(lis))
            
def del_thread(thr=''):
    # thread_dir + thr + txt
    # delete it, then remove thr from list
    # confirm before writing
    
    thr = str(thr) 
    
    if os.path.exists(thread_dir + thr + ".txt"):
        print(thread_dir + thr + ".txt")
    for n, line in enumerate(lis):
        if line.startswith(thr):
            print(n, line)
            magic = line.split(" >< ")
            print(magic)
            break
    doy = "Do you want to remove " + magic[2] + "?\n> "
    conf = input(doy)
    if conf.strip().lower()[0] is "y":
        lis.pop(n)
        liss = "\n".join(lis)
        with open("list.txt", "w") as lisss:
            lisss.write(liss)
        os.remove(thread_dir + thr + ".txt")

def mod_post(thr):
    # either "r" (remove) or "w" (warn) a reply # in thread #
    
    thr = str(thr)
    with open(thread_dir + thr + ".txt", "r") as tthr:
        tthr = tthr.read().splitlines()
    pcnt = len(tthr) - 1
    pos = input(f"Post to Modify\n[1-{pcnt}] ")
    pos = int(pos)
    rw = input("Remove or warn?\n[r/w]  ").strip()
    if 0 < pos < (len(tthr)):
        print(tthr[pos])
        if rw == "r":
            tthr[pos] =  "- >< - ><  >< <i>post removed by moderator</i>"
        elif rw == "w":
            tthr[pos] += "<br><br><b style='color:red'>(USER WAS BANNED FOR THIS POST)</b>"
        with open(thread_dir + thr + ".txt", "w") as thrt:
            thrt.write("\n".join(tthr) + "\n")
    else:
        print("Post not found:", (len(tthr) - 1),
              "vs", pos)

def scan_badword():
    # grep -Hn string *
    # returns thread filename & linenum + 1
    print("h")

if __name__ == "__main__":
    menu()
