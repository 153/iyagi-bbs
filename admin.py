#/usr/bin/env python3
import webtools as wt
import os, crypt, cgitb
cgitb.enable()

modes = {"0": "no mode", 
         "1": "lock",
         "2": "sticky",
         "3": "stickylock",
         "4": "permasage"
         }

settings = "./settings.txt"
b_conf = []
cd = {}

with open(settings, "r") as settings:
    settings = settings.read().splitlines()
    for s in settings:
        if len(s) == 0 or s[0] == "#" or ": " not in s:
            continue
        elif "#" in s:
            s = s.split("#")[0]
        s = s.split(": ")
        if len(s) > 2:
            s[1] = ": ".join(s[1:])
        try:
            s[1] = int(s[1])
        except:
            pass
        b_conf.append(s[1])
        cd[s[0]] = s[1]

with open("./admin/op.html", 'r') as op:
    op = op.read()

def mode_icons(mo=""):
    micons = ["", "lock.png", "sticky.png",
              ["lock.png", "sticky.png"], "ghost.png"]
    ic = micons[int(mo)]
    if len(ic) == 2:
        ic = ["./img/" + i for i in ic if len(ic) == 2]
    elif len(ic):
        ic = ["./img/" + ic]
    return ic
    
def login_admin():
#    if wt.get_cookie():
    cookies = wt.get_cookie()
    if 'pw' in cookies.keys():
        if tripcode(cookies['pw']) == b_conf[3]:
            return 1
    elif wt.get_form('pw') and \
         tripcode(wt.get_form('pw')) == b_conf[3]:
        print(wt.put_cookie('pw', wt.get_form('pw')))
        return 1
    else:
        if wt.get_form('pw'):
            print("Password incorrect.<br>")
        print("<h1>Login</h1>")
        print("<p>", wt.new_form('admin.py', 'post'))
        print("#" + wt.put_form('password', 'pw'))
        print(wt.put_form('submit', '', 'Submit'))
        print("</form><p>")
        return 0

def admin_splash():
    print("""<pre>
- change settings
- moderate threads
- modify wordfilter
</pre>""")
    if not wt.get_form('mode') or not wt.get_form('thread'):
        print("<h2>Settings</h2>")
        print("\n".join(["<br> - "+str(i) for i in b_conf]))
        for s in cd.keys():
            print("<p>",s + ":<br>&emsp;", cd[s])
    print("<h2>Threads</h2>")
    if wt.get_form('more'):
        print("<a href='.'>Back</a><br>")
        print(wt.get_form('thread'), "<hr>")
#        print(load_thread(wt.get_form('thread')))
        show_thread(load_thread(wt.get_form('thread')))
    else:
        mod_threads()

def mod_threads():
    print("<pre>")
    with open(b_conf[6]) as t_list:
        print(t_list.read())
    print("</pre>")
    ti = thread_index()
    for t in ti["ti"]:
        # t = filename 
        # t[0] last reply time, t[1] thread title
        # t[2] reply count, t[3] thread mode
        mic = mode_icons(ti[t][3])
        tm = [f"<img src='{m}'>" for m in mic]
        if ti[t][3] in modes:
           ti[t][3] = modes[ti[t][3]]
        mk = list(modes.keys())
        mv = [modes[i] for i in mk]
        dropdown = wt.dropdown("mode", mk, mv)
        ti[t][3] = dropdown.replace(f">{ti[t][3]}", \
                                    f" selected>{ti[t][3]}")
        print(op.format(t, ti[t], " ".join(tm)))

def thread_index():
    with open(b_conf[6]) as t_list:
        t_list = t_list.read().splitlines()
    t = {}
    t["ti"] = []
    for th in t_list:
        th = th.split(" >< ")
        t["ti"].append(th[0])
        t[th[0]] = th[1:]
    return t

def load_thread(thr='0'):
#    print(b_conf[5] + thr)
    with open(b_conf[5] + thr, 'r') as thr:
        thr = thr.read().splitlines()
    for n, th in enumerate(thr):
        thr[n] = th.split(' >< ')
    return thr

def show_thread(thr=[]):
    if not thr:
        return None
    table = ["<table>"]
    table.append("<tr><td><td>Name<td>Date<td>Comment")
    print("<tr><th colspan='4'>", thr.pop(0)[0])
    for n, t in enumerate(thr):
        t.pop(2)
        t = f"<tr><td>{n+1}.<td>" + "<td>".join(t)
        table.append(t)
    print("\n".join(table), "</table>")

def tripcode(pw):
    pw = pw[:8]
    salt = (pw + "H..")[1:3]
    trip = crypt.crypt(pw, salt)
    return (trip[-10:])

def main():
    print(wt.head(b_conf[0]))
    print("<h2>", b_conf[0], "admin</h2>")
#    print(wt.get_cookie())
    if login_admin() == 1:
        admin_splash()

main()
