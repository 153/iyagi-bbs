#!/usr/bin/env python3

import cgi, os, cgitb
import time, crypt

cgitb.enable()

board_config = \
    [["b_name", "4x13 BBS"], \
     ["b_url", "/bbs/"], \
     ["mod_un", "Admin"], \
     ["mod_pw", ""], \
     ["theme", "alpha"], \
     ["t_dir", "./threads/"], \
     ["t_list", "./threads/list.txt"]]

functions = ["main", "thread", "admin", "list", "create", "reply"]
form = cgi.FieldStorage()

def main():
    select_func = form.getvalue('m')
    bbs_header()
    if select_func:
        if select_func in functions:
#            print("<h1>", select_func, "</h1>")
            print("<a href='.'>&lt;&lt; back</a><br>")
            print("----"*10, "<p>")
            if select_func == "admin":
                bbs_admin()
            elif select_func == "main":
                bbs_main()
            elif select_func == "thread":
                bbs_thread()
            elif select_func == "create":
                bbs_create()
            elif select_func == "list":
                bbs_list()
            elif select_func == "reply":
                do_reply()
        else:
            select_func = None
            
    if not select_func:
        bbs_main()

def bbs_header():
    print("Content-type: text/html\n")
    print("<title>{0}</title>".format(board_config[0][1]))
    print("""<style>
a {color:#153}
body {padding:2% 5%}
table {border-collapse: seperate;
  border-spacing: 0;
  border: 0px solid #000;}
th, td {border: 1px solid #000; 
  padding: 2px;}
</style>""")
    
def bbs_admin():
    for confg in board_config:
        print(confg[0]+":", confg[1], "<br>")

def bbs_main():
    print("<h2>{0}</h2>".format(board_config[0][1]))
    bbs_list()
    print("<p>")
    do_prev()
    print("<hr>")
    bbs_create()

def bbs_thread(t_id='', prev=0):
    if not t_id and form.getvalue('t'):
        t_id = cgi.escape(form.getvalue('t'))
    if t_id:
        if t_id.isdigit():
            t_fn = board_config[5][1] + t_id + ".txt"
        else:
            bbs_list()
            return
    else:
        bbs_list()
        return
    if os.path.isfile(t_fn):
        with open(t_fn, "r") as the_thread:
            the_thread = the_thread.readlines()
            r_cnt = str(len(the_thread) - 1)
            if prev == 0:
                print("<h3>", the_thread[0] + "[" + r_cnt + "]", "</h3>")
            print("<div style='width:520px;border-right:2px solid black;padding-right:10px'>")
            p_n = 0
            replies=[]
            for reply in the_thread[1:]:
                p_n += 1
                reply = reply.split(' >< ')
                if len(reply) > 4:
                    reply[3] = " >< ".join(reply[3:])
                if reply[2]:
                    reply.pop(2)
                    reply[0] = "<i style='color:#444'>" \
                        + reply[0] + "</i>"
                else:
                    reply.pop(2) #30c
                    reply[0] = "<b style='color:#153'>" \
                        + reply[0] + "</b>"
                if prev == 0:
                    print("<p> #" + str(p_n), "//")
                    print("Name: {0} :\n Date: {1} \n<br>{2}".format(*reply))
                replies.append(reply)
            print("</div>")
            if prev == 0:
                bbs_reply(t_fn)
            return replies
            
    else:
        bbs_list()
        return
            
def bbs_create():
    thread_attrs = {'title':'', 'name':'', 'content':''}
    for key in thread_attrs.keys():
        if form.getvalue(key):
            thread_attrs[key] = form.getvalue(key)
    if thread_attrs['title'] and thread_attrs['content']:
        thread_attrs['title'] = cgi.escape(thread_attrs['title'])[:25].strip()
        if thread_attrs['name']:
            thread_attrs['name'] = \
                cgi.escape(thread_attrs['name'])[:14].strip()
            if '#' in thread_attrs['name']:
                namentrip = thread_attrs['name'].split('#')
                namentrip[1] = tripcode(namentrip[1])
                thread_attrs['name'] = ''.join(namentrip)
        thread_attrs['content'] = cgi.escape(thread_attrs['content']).replace('\r\n', "<br>")[:2000]
        thread_attrs['dt'] = str(time.time())[:10]
        if not thread_attrs['name']:
            thread_attrs['name'] = 'Anonymous'
        local_dt = time.localtime(int(thread_attrs['dt']))
        date_str = "%Y-%m-%d [%a] %H:%M"
        thread_attrs['ldt'] = time.strftime(date_str, local_dt)
        t_fn = board_config[5][1] + thread_attrs['dt'] + ".txt"
        with open(t_fn, "x") as new_thread:
            new_thread.write(thread_attrs['title'] + "\n" \
                + thread_attrs['name'] + " >< " \
                + thread_attrs['ldt'] + " ><  >< " \
                + thread_attrs['content'] + "\n" )
            print("Thread <i>{0}</i> posted successfully!".format(thread_attrs['title']))
        with open(board_config[6][1]) as t_list:
            t_list = t_list.read().splitlines()
            new_t = " >< ".join([thread_attrs['dt'], \
                thread_attrs['ldt'], thread_attrs['title'], \
                "1"])
            t_list.insert(0, new_t)
        with open(board_config[6][1], "w") as upd_list:
            upd_list.write('\n'.join(t_list))
            
    else:
        if not thread_attrs['title']:
            if thread_attrs['content']:
                print("You need to enter a title to post a new thread.<br>")
        elif not thread_attrs['content']:
            print("You need to write a message to post a new thread.<br>")
        with open("create.html") as c_thread:
            print(c_thread.read())

def bbs_list():
    with open(board_config[6][1]) as t_list:
        t_list = t_list.read().splitlines()
        cnt = 1
        print("<table>")
        print("<th> <th>Title <th>Posts <th>Last post")
        for t in t_list:
            print("<tr><td>{0}.".format(cnt))
            t = t.split(" >< ")
            print("<td><a href='?m=thread;t=" \
            + "{0}'>{2}</a>&nbsp; <td>{3} <td>{1} &nbsp;".format(*t))
            cnt += 1
        print("</table>")

def bbs_reply(t_fn=''):
    with open("reply.html") as r_thread:
        print(r_thread.read().format(t_fn))

def do_reply():
    reply_attrs = {'name':'', 'bump':'', 'comment':'', 't':''}
    for key in reply_attrs.keys():
        if form.getvalue(key):
            reply_attrs[key] = form.getvalue(key)
    if reply_attrs['t'] and reply_attrs['comment']:
        reply_attrs['comment'] = cgi.escape(reply_attrs['comment']).replace('\r\n', "<br>")[:2000]
        if reply_attrs['name']:
            reply_attrs['name'] = \
                cgi.escape(reply_attrs['name'][:14]).strip()
            if '#' in reply_attrs['name']:
                namentrip = reply_attrs['name'].split('#')
                namentrip[1] = tripcode(namentrip[1])
                reply_attrs['name'] = '</i>'.join(namentrip)
        else:
            reply_attrs['name'] = "Anonymous"
        if not reply_attrs['bump']:
            reply_attrs['bump'] = "1"
        if reply_attrs['bump'] != "1":
            reply_attrs['bump'] = ''
        local_dt = time.localtime()
        date_str = "%Y-%m-%d [%a] %H:%M"
        reply_attrs['ldt'] = time.strftime(date_str, local_dt)
        reply_string = reply_attrs['name'] + " >< " \
              + reply_attrs['ldt'] + " >< " \
              + reply_attrs['bump'] + " >< " \
              + reply_attrs['comment'] + "\n"
        with open(reply_attrs['t'], "a") as the_thread:
            the_thread.write(reply_string)
            print("comment successfully posted :)<br>")
            
        with open(board_config[6][1]) as t_list:
            reply_attrs['t'] = ''.join([i for i in reply_attrs['t'] if i.isdigit()])
            t_line = [reply_attrs['t'], reply_attrs['ldt'], reply_attrs['bump']]
            t_list = t_list.read().splitlines()
            nt_list = []
            new_t = []
            for t in t_list:
                t = t.split(' >< ')
                nt_list.append(t)
                if t[0] == t_line[0]:
                    t_line.insert(2, t[2])
                    t_line.insert(3, str(int(t[3])+1))
                    new_t = [' >< '.join(t), ' >< '.join(t_line)]
            sage = 0
            if new_t[1].split(" >< ")[4]:
                new_t[1] = new_t[1][:-4]
                sage = 1
            for n, t in enumerate(nt_list):
                if t[0] == new_t[1].split(" >< ")[0]:
                    if sage == 1:
                        nt_list[n] = new_t[1].split(" >< ")
                        pass
                    else:
                        nt_list.remove(t)
                        nt_list.insert(0, new_t[1].split(" >< "))
                        pass
            for n, l in enumerate(nt_list):
                nt_list[n] = " >< ".join(l)
            with open(board_config[6][1], "w") as new_tl:
                new_tl.write('\n'.join(nt_list))

    else: 
        if not reply_attrs['comment']:
            print("You need to write something to post a comment.")

def do_prev(bbt=[]):
    if not bbt:
        with open(board_config[6][1]) as t_list:
            t_list = t_list.read().splitlines()
            t_list = t_list[:10]
            for t in t_list:
                t = t.split(" >< ")
                bbs = bbs_thread(t[0], 1)
                do_prev([bbs, t[0]])

    if bbt:
        pstcnt = 0
        bbn = len(bbt[0])
        if bbn > 4:
            bbn = len(bbt[0]) - 2
        else:
            bbn = 1
        with open("./threads/" + str(bbt[1]) + ".txt") as t_t:
            t_t = t_t.readline()
        print("<h3><a href='?m=thread;t={0}'>{1} [{2}]".format(bbt[1], t_t, len(bbt[0])))
        print("</a></h3>")
        for replies in bbt[0]:
            pstcnt += 1
            if pstcnt == 1 or pstcnt >= bbn:
                print("<p>#{0}".format(pstcnt))
                print("Name: {0} \n: Date: {1} \n<br>{2}".format(*replies))
            if pstcnt == 1 and len(bbt[0]) > 4:
                print("<hr width='420px' align='left'>")
            elif pstcnt == len(bbt[0]):
                print("<hr width='420px' align='left'>")
                bbs_reply(board_config[5][1] + bbt[1]+".txt")
        
def tripcode(pw):
    pw = pw[:8]
    salt = (pw + "H..")[1:3]
    trip = crypt.crypt(pw, salt)
    return ("!" + trip[-10:])

main()