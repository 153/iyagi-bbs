#!/usr/bin/env python3

import os, cgi, cgitb
import time, re, crypt
import html, mistune

markdown = mistune.markdown
cgitb.enable()

# To generate a mod password, use tripcode.py3 to generate a tripkey.
# What comes out is the result of a code that generates something like
# a public key. Type #password in the name field to have your post
# render as the mod_un using a special color. Save your !tripcode in the
# mod_pw field to do so, without an exclamation mark in front. Your tripkey
# should be 10 letters long, the result of an 8 character secure password
# that you know others can't guess easily.
#
# b_url and theme currently are unused.

with open("settings.txt", "r") as bconf:
    b_conf = []
    bconf = bconf.read().splitlines()
    for s in bconf:
        if len(s) == 0:
            continue
        elif s[0] == "#":
            continue
        s = s.split(": ")
        if len(s) > 2:
            s[1] = ": ".join(s[1:])
        try:
            s[1] = int(s[1])
        except:
            pass
        b_conf += [s]

functions = ["main", "thread", "admin", "list", "create", "reply", "atom"]

t_modes = {"0":"", \
    "1":"<img src='./img/lock.png' alt='Lock'>", \
    "2":"<img src='./img/sticky.png' alt='Sticky'>", \
    "3":"<img src='./img/sticky.png'><img src='./img/lock.png'>", \
    "4":"<img src='./img/ghost.png' alt='Nobump'>"}

form = cgi.FieldStorage()

a_modes = {'p': "admin_posts()", 't': 'admin_threads()', 's': 'admin_config()'}

def main():
    select_func = form.getvalue('m')
    if select_func == 'atom':
        bbs_atom()
        return
    bbs_header()
    if select_func:
        if select_func in functions:
            print("<a href='.'>&lt;&lt; back</a><br>")
            print("----"*10, "<p>")
            if select_func == "admin":
                if form.getvalue('n') in a_modes.keys():
                    print(a_modes[form.getvalue('n')])
                else:
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

    bbs_foot()

def bbs_header():
    print("Content-type: text/html\n")
    with open("./html/head.html", "r") as head:
        print(head.read().format(b_conf[0][1]))

def bbs_admin():
    a_pass = ''
    if form.getvalue('p'):
        a_pass = tripcode(cgi.escape(form.getvalue('p')))[2:]
    if a_pass != b_conf[3][1]:
        print("<form method='post' action='.'>")
        print("<b>Please enter your password.</b>")
        print("<input type='hidden' name='m' value='admin'>")
        print("<input type='text' name='p'>")
        print("<input type='submit' value='Login'>")
        print("</form>")
    else:
        print("<h2>Config</h2>")
        print("welcome, user!", a_pass, "<p>")
        for confg in b_conf:
            print(confg[0]+":", confg[1], "<br>")
        print("<div class='front'>")
        print("View recent posts")
        admin_posts(cgi.escape(form.getvalue('p')))

def admin_posts(p=''):
    print(tripcode(p)[2:])
    if tripcode(p)[2:] == b_conf[3][1]:
        print("<h2>Last 40 posts</h2>")
        with open(b_conf[10][1]) as ip_l:
            ip_l = ip_l.read().splitlines()
            ip_t = len(ip_l)
            for n, ip in enumerate(ip_l[-1:-41:-1]):
                ip = ip.split('|')
                if len(ip) > 3:
                    ip[2] = "|".join(ip[3:])
                p_stuff = ip[2].split(' >< ')
                if len(p_stuff) > 4:
                    p_stuff[3] = " >< ".join(p_stuff[3:])
                print("<div class='thread'><input type='checkbox'>")
                print("#{0}:".format(ip_t - n))
                print("<a href>edit</a> .")
                print("<a href>delete</a> .")
                print("<u style='color:red'>ban</u>")
                print("<hr><table style='margin: auto'>")
                print("<tr><td>thread:<td>", ip[1])
                print("<tr><td>ip:<td>", ip[0])
                print("<tr><td>name:<td>", cgi.escape(p_stuff[0]))
                print("<tr><td>time:<td>", p_stuff[1])
                print("</table>")
                print("<hr><p>", do_format(p_stuff[3]))
                print("</div><br>")

def bbs_main():
    print("<div class='front'>")
    print("""Styles: [<a href="javascript:setActiveStyleSheet('4x13');">4x13</a>]
[<a href="javascript:setActiveStyleSheet('mob');">mob</a>
    [<a href="javascript:setActiveStyleSheet('0ch');">0ch</a>]""")
    print(" // [<a href='/wiki/'>wiki</a>]")
    print("<h2>{0}</h2>".format(b_conf[0][1]))
    with open('./html/motd.html', 'r') as motd:
        print(motd.read())
    bbs_list(prev='1')
    print("<p><hr>")
    do_prev()
    print("<hr>")
    bbs_create()
    print("</div>")

def bbs_thread(t_id='', prev=0):
    if not t_id and form.getvalue('t'):
        t_id = cgi.escape(form.getvalue('t'))
    if t_id:
        if t_id.isdigit():
            t_fn = b_conf[5][1] + t_id + ".txt"
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
            t_m = ''
            if prev == 0:
                if "[<" in the_thread[0]:
                    t_m = the_thread[0].split("[<")[1].strip()
                    if t_m in t_modes.keys():
                        t_m = t_modes[t_m]
                    else:
                        t_m = ''
                    the_thread[0] = the_thread[0].split("[<")[0]
                elif int(r_cnt) >= b_conf[7][1]:
                    t_m = t_modes['1']
                    
                print("<h3>", t_m, the_thread[0] + "[" + r_cnt + "]", "</h3>")
                print("<div class='thread'>")
            p_n = 0
            replies=[]
            for reply in the_thread[1:]:
                p_n += 1
                reply = reply.split(' >< ')
                if len(reply) > 4:
                    reply[3] = " >< ".join(reply[3:])
                if reply[2]:
                    reply.pop(2)
                    reply[0] = "<span class='sage'>" \
                        + reply[0] + "</span>"
                else:
                    reply.pop(2) #30c
                    reply[0] = "<span class='bump'>" \
                        + reply[0] + "</span>"
                
                if prev == 0:
                    if re.compile(r'&gt;&gt;[\d]').search(reply[2]):
                        reply[2] = re.sub(r'&gt;&gt;([\d]+)', \
                            r'<a href="#\1">&gt;&gt;\1</a>', reply[2])
                    reply[2] = do_format(reply[2])
                    if p_n > 1:
                        print("</p>")
                    print("<a name='{0}' href='#reply'".format(p_n))
                    print("onclick='addText(\"{1}\", \"{0}\")'>".format(p_n, t_id))
                    print("#{0}</a> //".format(p_n))
                    print("Name: {0} :\n Date: {1} \n<p>{2}".format(*reply))
                else:
                    if re.compile(r'&gt;&gt;[\d]').search(reply[2]):
                        reply[2] = re.sub(r'&gt;&gt;([\d]+)', \
                            r'<a href="?m=thread;t={0}#\1">&gt;&gt;\1</a>'.format(t_id), reply[2])
                    reply[2] = do_format(reply[2])
                    if len(reply[2].split('<br>')) > 8:
                        reply[2] = '<br>'.join(reply[2].split('<br>')[:9])[:850]
                        if "<pre" and not "</pre>" in reply[2]:
                            reply[2] += "</pre>"
                        if "<code" and not "</code>" in reply[2]:
                            reply[2] += "</code>"
                        reply[2] += "</p><div class='rmr'>Post shortened. " \
                            + "<a href='?m=thread;t={0}'>[".format(t_id) \
                            + "View full thread]</a></div>"
                    elif len(reply[2].split('<span class="youtube" ')) > 2:
                        reply[2] = '<span class="youtube"'.join(reply[2].split('<span class="youtube"')[:2])
                        if "<pre" and not "</pre>" in reply[2]:
                            reply[2] += "</pre>"
                        if "<code" and not "</code>" in reply[2]:
                            reply[2] += "</code>"
                        reply[2] += "</p><div class='rmr'>Post shortened. " \
                            + "<a href='?m=thread;t={0}'>[".format(t_id) \
                            + "View full thread]</a></div>"
                    elif len(reply[2]) > 850:
                        reply[2] = reply[2][:850]
                        if "<pre" and not "</pre>" in reply[2]:
                            reply[2] += "</pre>"
                        if "<code" and not "</code>" in reply[2]:
                            reply[2] += "</code>"
                        reply[2] += "</p><div class='rmr'>Post shortened. " +\
                            "<a href='?m=thread;t={0}'>".format(t_id) \
                            + "[View full thread]</a></div>"
                    print(int(r_cnt))
                    show_r = b_conf[13][1]
                    if int(r_cnt) > show_r and p_n == int(r_cnt):
                        reply[2] = reply[2] + "</p><div class='rmr'>" \
                            +"<a href='?m=thread;t={0}'".format(t_id) \
                            +">[Read all posts]</a></div>"
                            
                replies.append(reply)
            if prev == 0:
                print("</div>")
                if t_m.strip() in ["1", "3"]:
                    print(t_modes[t_m.strip()])
                    print("This thread is locked. No more comments can be added.")
                elif int(r_cnt) < b_conf[7][1]:
                    bbs_reply(t_fn, t_id)
                else:
                    print("<hr>", t_modes['1'])
                    print("No more replies; thread limit reached!")
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
        thread_attrs['title'] = cgi.escape(thread_attrs['title'])[:30].strip()
        if thread_attrs['name']:
            thread_attrs['name'] = \
                cgi.escape(thread_attrs['name'])[:18].strip()
            if '#' in thread_attrs['name']:
                namentrip = thread_attrs['name'].split('#')[:2]
                namentrip[1] = tripcode(namentrip[1])
                thread_attrs['name'] = '</span> <span class="trip">'.join(namentrip)
        thread_attrs['content'] = cgi.escape(thread_attrs['content']).strip().replace('\r\n', "<br>")[:2000]
        thread_attrs['dt'] = str(time.time())[:10]
        if not thread_attrs['name']:
            thread_attrs['name'] = 'Anonymous'
        local_dt = time.localtime(int(thread_attrs['dt']))
        date_str = "%Y-%m-%d [%a] %H:%M"
        thread_attrs['ldt'] = time.strftime(date_str, local_dt)
        t_fn = b_conf[5][1] + thread_attrs['dt'] + ".txt"
        with open(t_fn, "x") as new_thread:
            new_thread.write(thread_attrs['title'] + "\n" \
                + thread_attrs['name'] + " >< " \
                + thread_attrs['ldt'] + " ><  >< " \
                + thread_attrs['content'] + "\n" )
            print("Thread <i>{0}</i> posted successfully!".format(thread_attrs['title']))
        with open(b_conf[11][1], "a") as log:
            ip = os.environ["REMOTE_ADDR"]
            # IP | location | filename | ldt | comment
            log_data = " | ".join([ip, t_fn, thread_attrs['ldt'], \
                                   thread_attrs['title'], thread_attrs['name'], thread_attrs['content']+"\n"])
            log.write(log_data)
            print("Redirecting you in 5 seconds...")
            print("<meta http-equiv='refresh' content='5;.'")
        with open(b_conf[6][1], "r") as t_list:
            t_list = t_list.read().splitlines()
            new_t = " >< ".join([thread_attrs['dt'], \
                thread_attrs['ldt'], thread_attrs['title'], \
                    "1", "0"])
            for n, t in enumerate(t_list):
                t = t.split(" >< ")
                if len(t) == 5 and t[4] not in ["2", "3"] or len(t) == 4:
                    t_list.insert(n, new_t)
                    break
        with open(b_conf[6][1], "w") as upd_list:
            upd_list.write('\n'.join(t_list))
            
    else:
        if not thread_attrs['title']:
            if thread_attrs['content']:
                print("You need to enter a title to post a new thread.<br>")
        elif not thread_attrs['content']:
            print("You need to write a message to post a new thread.<br>")
        with open("./html/create.html") as c_thread:
            print(c_thread.read())

def bbs_list(prev='0', rss=False):
    if prev == '0':
        s_ts = None
    else:
        s_ts = b_conf[12][1]
    with open(b_conf[6][1]) as t_list:
        t_list = t_list.read().splitlines()
        t_cnt = len(t_list)
        cnt = 1
        if not rss:
            print("<a name='tbox'></a><table>")
            print("<th>{0} <th>Title <th>Posts <th>Last post".format(t_cnt))
        else:
            rss_list = []
        for t in t_list[:s_ts]:
            t = t.split(" >< ")
            if not rss:
                print("<tr><td><a href='?m=thread;t={0}'>{1}.".format(t[0], cnt))
            if int(t[3]) >= b_conf[7][1] and t[4] not in ["1", "3"]:
                t[2] = t_modes['1'] + t[2]
            elif int(t[3]) >= b_conf[7][1] and t[4] == "2":
                t[2] = t_modes['3'] + t[2]
            elif t[4] in t_modes.keys():
                t[2] = t_modes[t[4]] + t[2]
            if prev == '1':
                print("</a><td><a href='#" \
                    + "{0}'>{2}</a>&nbsp; <td>{3} <td>{1} &nbsp;".format(*t))
            elif rss:
                rss_list.append(t)
            else:
                print("</a><td><a href='?m=thread;t=" \
                    + "{0}'>{2}</a>&nbsp; <td>{3} <td>{1} &nbsp;".format(*t))
            cnt += 1
        if prev != "0":
            print("<tr><td>")
            if (t_cnt - s_ts) > 0:
                print("<td colspan='2'><a href='?m=list'>")
                print("View all threads</a> ({0} hidden)".format(t_cnt - s_ts))
                print("<td>")
            else:
                print("<td colspan='3'>")
            print("<a href='#create'>Create new thread</a>")
        elif rss:
            return rss_list
        print("</table>")

def bbs_reply(t_fn='', t_id=''):
    with open("./html/reply.html") as r_thread:
        print(r_thread.read().format(t_fn, t_id))


def bbs_atom(m='t'):
    amode = form.getvalue('r')
    if amode == 'p':
        print("Content-type: application/atom+xml\r\n")
        print('<?xml version="1.0" encoding="utf-8"?>')
        print('<feed xmlns="http://www.w3.org/2005/Atom">')
        print("<title>{0}: 50 latest posts</title>".format(b_conf[0][1]))
        print("<link rel='self' href='" + b_conf[8][1] + "?m=atom;r=p' />")
        print("<id>{0}#posts</id>".format(b_conf[8][1]))
        isot = "%Y-%m-%dT%H:%M:00%z"
        with open(b_conf[10][1]) as ip_l:
            ip_l = ip_l.read().splitlines()[::-1][:50]
            l_upd = ip_l[0].split(" >< ")[1].replace(" ", "").replace(".", "-")
            l_upd = re.sub(r'\[(.*?)\]', 'T', l_upd)
            print("<updated>" + l_upd + b_conf[9][1] + "</updated>")
            for p in ip_l:
                print("\n<entry>")
                p = p.split(" >< ")
                p = [p[0].split(" | ")[1], p[1], p[3]]
                p[1] = p[1].replace(" ", "").replace(".", "-")
                p[1] = re.sub(r'\[(.*?)\]', 'T', p[1])
                p[1] += b_conf[9][1]
                p[0] = p[0].split("/")[-1].split(".")[0]
                p_url = b_conf[8][1] + "?m=thread;t=" + p[0]
                print("<updated>" + p[1] + "</updated>")
                print("<id>" + p_url + "#" + p[1] + "</id>")
                print("<title>reply in thread", p_url + "</title>")
                print("<link rel='alternate' href='" + p_url + "'/>")
                p[2] = cgi.escape(p[2])
                print("<content type='html'>", p[2], "</content>")
                print("</entry>\n")
            print("</feed>")
    elif amode == 't':
        print("Content-type: application/atom+xml\r\n")
        print('<?xml version="1.0" encoding="utf-8"?>')
        print('<feed xmlns="http://www.w3.org/2005/Atom">')
        print("<title>{0} latest threads</title>".format(b_conf[0][1]))
        print("<link rel='self' href='" + b_conf[8][1] + "?m=atom;r=t' />")
        print("<id>{0}#threads</id>".format(b_conf[8][1]))
        t_list = bbs_list('0', "1")
        t_list.sort(key=lambda t_list:t_list[0])
        upd = t_list[-1][0]
        l_upd = time.localtime(int(upd))
        isot = "%Y-%m-%dT%H:%M" + b_conf[9][1]
        l_upd = time.strftime(isot, l_upd)
        print("<updated>" + l_upd + "</updated>")
        for t in t_list[::-1]:
            print("\n<entry>")
            upd = time.localtime(int(t[0]))
            t_url = b_conf[8][1] + "?m=thread;t=" + t[0]
            print("<updated>" + time.strftime(isot, upd) + "</updated>")
            print("<id>" + t_url + "</id>")
            print("<link rel='alternate' href='" + t_url + "' />")
            print("<title>", cgi.escape(t[2]), "</title>")
            with open(b_conf[5][1] + t[0] + ".txt", "r") as tt:
                tt = tt.read().splitlines()[1]
                tt = " >< ".join(tt.split(" >< ")[3:])
                tt = cgi.escape(tt)
            print("<content type='html'>", tt, "</content>")
            print("</entry>")
        print("</feed>")
    else:
        bbs_header()
        print(b_conf[8])
def bbs_foot():
    with open("./html/foot.html") as b_foot:
        print(b_foot.read())
        
def do_reply():
    reply_attrs = {'name':'', 'bump':'', 'comment':'', 't':''}
    for key in reply_attrs.keys():
        if form.getvalue(key):
            reply_attrs[key] = form.getvalue(key)
    if reply_attrs['t'] and reply_attrs['comment']:
        reply_attrs['comment'] = cgi.escape(reply_attrs['comment']).strip().replace('\r\n', "<br>")[:5000]
#        reply_attrs['comment'] = reply_attrs['comment'].encode('utf-8', 'xmlcharrefreplace').decode()
#        reply_attrs['comment'] = re.sub(r'(<br>{3,})', r'<br><br><br>', reply_attrs['comment'])
#        reply_attrs['comment']
        if reply_attrs['name']:
            reply_attrs['name'] = \
                cgi.escape(reply_attrs['name'][:18]).strip()
            if '#' in reply_attrs['name']:
                namentrip = reply_attrs['name'].split('#')[:2]
                namentrip[1] = tripcode(namentrip[1])
                if b_conf[3][1] in namentrip[1]:
                    namentrip[1] = b_conf[2][1]
                    reply_attrs['name'] = '</span> <span class="admin">'.join(namentrip)
                else:
                    reply_attrs['name'] = '</span> <span class="trip">'.join(namentrip)
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
        fale = 0
        with open(reply_attrs['t'], "r") as the_thread:
            ter = the_thread.read().splitlines()
            if "[<" in ter[0]:
                if ter[0].split("[< ")[1] in ["1", "3"]:
                    fale = 3
            elif (len(ter) - 1) >= b_conf[7][1]:
                fale = 1
            else:
                ter = ter[-1].split(' >< ')
                if ter[-1] == reply_string.split(' >< ')[-1][:-1]:
                    fale = 2
                
        with open(reply_attrs['t'], "a+") as the_thread:
            if fale == 0:
                the_thread.write(reply_string)
            elif fale == 1:
                print("Sorry, thread limit reached!")
            elif fale == 2:
                print("Sorry, you already posted that.")
            elif fale == 3:
                print("Sorry, the thread is locked.")
            else:
                print("Please clean ur html")
                
        with open(b_conf[10][1], "a") as log:
            if fale == 0:
                ip = os.environ["REMOTE_ADDR"]
                log_data = " | ".join([ip, reply_attrs['t'], reply_string])
                log.write(log_data)
                print("comment successfully posted<p>")
                print("Redirecting you in 5 seconds...")
                print("<meta http-equiv='refresh' content='5;.'")
            
        with open(b_conf[6][1]) as t_list:
            reply_attrs['t'] = ''.join([i for i in reply_attrs['t'] if i.isdigit()])
            t_line = [reply_attrs['t'], reply_attrs['ldt'], reply_attrs['bump']]
            t_list = t_list.read().splitlines()
            nt_list = []
            new_t = []
            sage = 0
            for n, t in enumerate(t_list):
                t = t.split(' >< ')
                nt_list.append(t)
                if t[0] == t_line[0]:
                    if len(t) is 4 and t[4] in ["1", "3"]:
                        print("you should not be posting in a locked thread")
                        fale = 1
                        break
                    elif t_line[2] == "1" or t[4] in ("2", "4"):
                        sage = 1
                    t_line.pop(2)
                    t_line.insert(2, t[2])
                    t_line.insert(3, str(int(t[3])+1))
                    t_line.insert(4, t[4])
                    new_t = [' >< '.join(t), ' >< '.join(t_line)]

            print("<hr>")
            posted = 0
            for n, t in enumerate(nt_list):
                if fale == 1:
                    print("failure!")
                    break
                elif sage == 0:
                    if posted == 0:
                        if t[4] not in ["2", "3"]:
                            nt_list.insert(n, new_t[1].split(" >< "))
                            posted = 1
                    else:
                        if t == new_t[0].split(" >< "):
                            nt_list.remove(t)
                            break
                else:
                    if t[0] == new_t[0].split(" >< ")[0]:
                        nt_list[n] = new_t[1].split(" >< ")
                        break
                
            for n, l in enumerate(nt_list):
                nt_list[n] = " >< ".join(l)

            if fale == 0:
                with open(b_conf[6][1], "w") as new_tl:
                    new_tl.write('\n'.join(nt_list))

    else: 
        if not reply_attrs['comment']:
            print("You need to write something to post a comment.")

def do_prev(bbt=[]):
    if not bbt:
        with open(b_conf[6][1]) as t_list:
            t_list = t_list.read().splitlines()[:b_conf[12][1]]
            for n, t in enumerate(t_list):
                t = t.split(" >< ")
                bbs = bbs_thread(t[0], 1)
                print("<div class='thread'><a name={0}>".format(t[0]))
                print("<h3><a>" + str(n+1)+".</a>")
                do_prev([bbs, t[0]])

    if bbt:
        pstcnt = 0
        bbn = len(bbt[0])
        if bbn > b_conf[13][1]:
            bbn = len(bbt[0]) - b_conf[13][1] + 1
        else:
            bbn = 1
        with open(b_conf[5][1] + str(bbt[1]) + ".txt") as t:
            t_t = t.readline()[:-1]
            t_r = len(t.read().splitlines())

        t_m = ''
        if "[<" in t_t:
            print(t_modes[t_t.split("[< ")[1]])
            t_m = t_modes[t_t.split("[< ")[1]]
            if t_m in t_modes.keys():
                t_t = t_t.split(" [< ")[0] + t_m
            else:
                t_t = t_t.split(" [< ")[0]
        print("<a href='?m=thread;t={0}'>{1} [{2}]".format(bbt[1], t_t, len(bbt[0])))
        print("</a></h3>")
        for replies in bbt[0]:
            pstcnt += 1
            if pstcnt == 1 or pstcnt >= bbn:
                if pstcnt > bbn:
                    print("</p>")
                print("#{0} //".format(pstcnt))
                print("Name: {0} \n: Date: {1} \n<p>{2}".format(*replies))
            if pstcnt == 1 and len(bbt[0]) > b_conf[13][1]:
                print("<hr width='420px' align='left'>")
            elif pstcnt == len(bbt[0]):
                if "lock" in t_m:
                    print("<br><div class='reply'>")
                    print("<br><div class='closed'>", t_m)
                    print("Thread locked. No more comments allowed")
                    print("</div><br></div></div>")
                elif t_r < b_conf[7][1]:
                    print("<hr width='420px' align='left'>")
                    bbs_reply(b_conf[5][1] + bbt[1]+".txt")
                else:
                    print("<hr><div class='closed'>", t_modes['1'])
                    print("<i>Thread limit reached.</i></div><p>")
                    print("</div>")


def do_format(urp=''):
    urp = urp.split('[yt]')
    urp = urp[:3]
    urp = '[yt]'.join(urp)
    urp = re.sub(r'\[yt\]http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?[\w\?=]*)?\[/yt\]', r'<div style="width:480; height:320" class="youtube" id="\1"></div><p>', urp)
    Urp = re.sub(r'\[aa\](.*?)\[/aa\]', r'<pre class="aa"><b>Ascii Art:</b><hr>\1</pre><p>', urp)
    urp = re.sub(r'\[spoiler\](.*?)\[/spoiler\]', r'<span class="spoiler">\1</span>', urp)
    urp = urp.split("<br>")
    for n, l in enumerate(urp):
        if l[:4] == '&gt;':
            urp[n] = "<span class='quote'>" + l + "</span>"
    urp = "<br>".join(urp)
    urp = re.sub(r'(<br>{4,})', r'<br>', urp)
    urp = re.sub(r'\[code\](.*?)\[/code\]', r'<pre><b>Code:</b><hr><code>\1</code></pre><p>', urp)
    urp = urp.replace('&amp;', '&').encode('ascii', 'xmlcharrefreplace').decode()
    return urp

def tripcode(pw):
    pw = pw[:8]
    salt = (pw + "H..")[1:3]
    trip = crypt.crypt(pw, salt)
    return (" !" + trip[-10:])

main()
