#!/usr/bin/env python3

import os, cgi, cgitb
import time, re, crypt
import webtools as wt
import backlink, bans

form = cgi.FieldStorage()
settings = "./settings.txt"
cgitb.enable()

with open("spam.txt", "r") as spam:
    spam = spam.read().splitlines()
bad_words = spam

# To generate a mod password, use tripcode.py3 to generate a tripkey.
# What comes out is the result of a code that generates something like
# a public key. Type #password in the name field to have your post
# render as the mod_un using a special color. Save your !tripcode in the
# mod_pw field to do so, without an exclamation mark in front. Your tripkey
# should be 10 letters long, the result of an 8 character secure password
# that you know others can't guess easily.

# list(conf) settings are:
# 0 - name, 1 - web path, 2 - admin name,
# 3 - mod pw hash, 5 - thread storage,
# 6 - thread list, 7 - reply limit,
# 8 - full web path, # 9 - timezone
# 10 - post IPs log, # 11 - thread IP log
# 12 - threads to show, # 13 - replies to show

with open(settings, "r") as settings:
    conf = []
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
        conf.append(s[1])

f = {"main":"bbs_main()",  "thread":"bbs_thread()",
     "list":"bbs_list()", "create":"bbs_create()",
     "reply":"do_reply()", "atom":"bbs_atom()"
     }

t_modes = {"0":"", \
    "1":"<img src='./img/lock.png' alt='Lock'>", 
    "2":"<img src='./img/sticky.png' alt='Sticky'>", 
    "3":"<img src='./img/sticky.png'><img src='./img/lock.png'>",
    "4":"<img src='./img/ghost.png' alt='Nobump'>"}

def main():
    select_func = wt.get_form('m')
    if select_func == 'atom':
        bbs_atom()
        return
    bbs_header()
    if select_func in f.keys():
        print("<a href='.'>&lt;&lt; back</a><br>")
        print("----"*10, "<p>")
        eval(f[select_func])
    else:
        try:
            x = 1 / int(wt.raw_query())
            print("<a href='.'>&lt;&lt; back</a><br>")
            print("----"*10, "<p>")
            bbs_thread(wt.raw_query())

        except:
            bbs_main()
    bbs_foot()
    print("</div></div>")

def bbs_header():
    with open("./html/head.html", "r") as head:
        print(head.read().format(conf[0]))
    print("""<style>
  .x {visibility: hidden;width:0;height:0;display:none}
</style>""")
        
def bbs_main():
    print("<div class='front'>")
    print("""Styles: 
    [<a href="javascript:setActiveStyleSheet('4x13');">4x13</a>]
    [<a href="javascript:setActiveStyleSheet('7ch');">7ch</a>]
    [<a href="javascript:setActiveStyleSheet('vba');">vba</a>]
    [<a href="javascript:setActiveStyleSheet('geocities');">Geocities</a>]
    [<a href="javascript:setActiveStyleSheet('0ch');">0ch</a>]""")
    print(f"<h2><a href='#tbox'>&#9632;</a> {conf[0]}</h2>")
    with open('./html/motd.html', 'r') as motd:
        print(motd.read())
    bbs_list(1)
    print("<p><hr>")
    do_prev()
    print("<hr>")
    bbs_create()
    print("</div>")

def bbs_thread(t_id='', prev=0):
    if not t_id and wt.get_form('t'):
        t_id = wt.get_form('t')
    if t_id:
        if t_id.isdigit():
            t_fn = conf[5] + t_id + ".txt"
        else:
            bbs_list(0)
            return
    else:
        bbs_list(0)
        return
    
    if not os.path.isfile(t_fn):
        bbs_list(0)
        return
    
    with open(t_fn, "r") as the_thread:
        the_thread = the_thread.readlines()
    r_cnt = str(len(the_thread) - 1)
    t_m = ''
    if "><" in the_thread[0]:
        t_m = the_thread[0].split("><")[1].strip()
        if t_m in t_modes.keys():
            t_m = t_modes[t_m]
        else:
            t_m = ''
        the_thread[0] = the_thread[0].split("><")[0]
    elif int(r_cnt) >= conf[7]:
        t_m = t_modes['1']
    bld = {}
    if prev == 0:
        bld = backlink.do_backlink(t_id)
        print("<div class='thread'>")
        print(f"<h3> {t_m} {the_thread[0]} [{r_cnt}]</h3>")
    p_n = 0
    replies=[]
    for reply in the_thread[1:]:
        p_n += 1
        reply = reply.split(' >< ')
        if len(reply) > 4:
            reply[3] = " >< ".join(reply[3:])
        if reply[2]:
            reply.pop(2)
            reply[0] = f"<span class='sage'>{reply[0]}</span>"

        else:
            reply.pop(2) #30c
            reply[0] = f"<span class='bump'>{reply[0]}</span>"

        # Viewing thread in threadview
        if prev == 0:
            if re.compile(r'&gt;&gt;[\d]').search(reply[2]):
                reply[2] = re.sub(r'&gt;&gt;([\d]+)', \
                                  r'<a href="#\1">&gt;&gt;\1</a>', \
                                  reply[2])
            reply[2] = do_format(reply[2])
            print("<div class='reply'><div class='title'>")
            print("<a name='{0}' href='#reply'".format(p_n))
            print("onclick='addText(\"{1}\", \"{0}\")'>"\
                  .format(p_n, t_id))
            print("#{0}</a> //".format(p_n))
            print("Name: {0} :\nDate: {1} \n"\
                  .format(reply[0], reply[1]))
            if str(p_n) in bld.keys():
                print("<div class='bl'>Replies: ")
                aref = "<a href='#{0}'><i>&gt;&gt;{0}</a></i>"
                print(", ".join([aref.format(r) \
                            for r in bld[str(p_n)]]))
                print("</div>")
            print("</div><div class='comment'>")
            print("<p>", reply[2], "</p></div></div>")

        # Viewing preview on front page
        else:
            if re.compile(r'&gt;&gt;[\d]').search(reply[2]):
                reply[2] = re.sub(r'&gt;&gt;([\d]+)', 
                                  r'<a href="?{0}#\1">'\
                                    .format(t_id) + r'&gt;&gt;\1</a>',
                                  reply[2])
                                  
            reply[2] = do_format(reply[2])
            if len(reply[2].split('<br>')) > 12:
                reply[2] = '<br>'.join(reply[2].split('<br>')[:12])[:850]
                if "<pre" and not "</pre>" in reply[2]:
                    reply[2] += "</pre>"
                if "<code" and not "</code>" in reply[2]:
                    reply[2] += "</code>"
                reply[2] += "</p><div class='rmr'>Post shortened. "
                reply[2] += f"<a href='?{t_id}'>["
                reply[2] += "View full thread]</a></div>"
            elif len(reply[2].split('<span class="youtube" ')) > 2:
                reply[2] = '<span class="youtube"'.join(reply[2]\
                                .split('<span class="youtube"')[:2])
                if "<pre" and not "</pre>" in reply[2]:
                    reply[2] += "</pre>"
                if "<code" and not "</code>" in reply[2]:
                    reply[2] += "</code>"
                reply[2] += "</p><div class='rmr'>Post shortened. "
                reply[2] += "<a href='?{t_id}'>["
                reply[2] += "View full thread]</a></div>"
            elif len(reply[2]) > 1400:
                reply[2] = reply[2][:1400]
                if "<pre" and not "</pre>" in reply[2]:
                    reply[2] += "</pre>"
                if "<code" and not "</code>" in reply[2]:
                    reply[2] += "</code>"
                reply[2] += "</p><div class='rmr'>Post shortened. "
                reply[2] += f"<a href='?{t_id}'>"
                reply[2] += "[View full thread]</a></div>"
            show_r = conf[13]
            if (int(r_cnt) - 1) > show_r and p_n == int(r_cnt):
                reply[2] += "</p><br><div class='rmr'>" 
                reply[2] += f"<a href='?{t_id}'"
                reply[2] += ">[Read all posts]</a></div><br>"
            reply[2] += "</div>"
        replies.append(reply)

    if "lock" in t_m.strip() and prev == 0:
        print("<div class='rmr'>")
        print(t_m.strip())
        print("<b>This thread is locked.</b>")
        print("<p>No more replies can be added.")
        print("</div>")
    elif int(r_cnt) >= conf[7]:
        print("<div class='closed'>", t_modes['1'])
        print("This thread is locked. Reply limit hit.")
        print("</div>")
    elif prev == 0:
        bbs_reply(t_fn, t_id)
    return replies

            
def bbs_create(prev=0):
    thread_attrs = {'title':'', 'name':'', 'content':''}
    thread_attrs = {k: wt.get_form(k) for k in thread_attrs.keys()}
    if wt.get_form('m') == "create" \
       and None in [thread_attrs['title'], thread_attrs['content']]:
        if not thread_attrs['title']:
            print("You need to enter a title to post a new thread.<br>")
        if not thread_attrs['content']:
            print("You need to write a message to post a new thread.<br>")
        with open("./html/create.html") as c_thread:
            print(c_thread.read())
        return
    elif wt.get_form('m') != "create":
        with open("./html/create.html") as c_thread:
            print(c_thread.read())
        return

    if bans.is_banned(wt.get_ip()):
        print("<center>")
        print("<h1>You are banned!</h1>")
        print("<h3>", bans.is_banned(wt.get_ip()), "</h3>")
        return
    for word in bad_words:
        if word in [thread_attrs["title"].lower(), 
                   thread_attrs["content"].lower()]:
            print("<center><h2>Bad word error.</h2></center>")
            return
    
    thread_attrs['title'] = thread_attrs['title'][:30].strip()
    if thread_attrs['name']:
        thread_attrs['name'] = thread_attrs['name'][:18].strip()
        if '#' in thread_attrs['name']:
            namentrip = thread_attrs['name'].split('#')[:2]
            namentrip[1] = tripcode(namentrip[1])
            thread_attrs['name'] = '</span> <span class="trip">'\
                                        .join(namentrip)
    else:
        thread_attrs['name'] = 'Anonymous'
    thread_attrs['content'] = thread_attrs['content']\
                            .strip().replace('\r\n', "<br>")[:2000] +'\n'
    dt = wt.fancy_time('', 'unix')
    ldt = wt.fancy_time(dt, 'human')
    t_fn = dt + ".txt"
    with open(conf[5] + t_fn, "x") as new_thread:
        new_thread.write(thread_attrs['title'] + "\n" \
            + thread_attrs['name'] + " >< " \
            + ldt + " ><  >< " \
            + thread_attrs['content'])
        print("Thread <i>{0}</i> posted successfully!"\
              .format(thread_attrs['title']))
    with open(conf[11], "a") as log:
        ip = os.environ["REMOTE_ADDR"]
        # IP | location | filename | ldt | comment
        log_data = " | ".join([ip, t_fn, ldt, thread_attrs['name'],
                               thread_attrs['title'], 
                               thread_attrs['content']])
        log.write(log_data)
        print("Redirecting you in 5 seconds...", wt.redirect())

    new_t = " >< ".join([dt, ldt, thread_attrs['title'], "1", "0"])
    # load list.txt
    with open(conf[6], "r") as t_list:
        t_list = t_list.read().splitlines()

    for n, t in enumerate(t_list):
        t = t.split(" >< ")
        if len(t) == 5 and t[4] not in ["2", "3"] or len(t) == 4:
            t_list.insert(n, new_t)
            break
        else:
            pass
    else:
        t_list.insert(len(t_list), new_t)
    with open(conf[6], "w") as upd_list:
        upd_list.write('\n'.join(t_list))

def bbs_list(prev=0, rss=False):
    with open(conf[6]) as t_list:
        t_list = t_list.read().splitlines()
    t_cnt = len(t_list)
    if not prev:
        s_ts = t_cnt
    else:
        s_ts = conf[12]
    cnt = 1
    if not rss:
        print("<a name='tbox'></a><table class='sortable'><thead>")
        print("<th>{0} <th>Title <th>Posts <th>Last post</thead>".format(t_cnt))
    else:
        rss_list = []
    for t in t_list[:s_ts]:
        t = t.split(" >< ")
        if not rss:
            print("<tr><td><a href='?{0}'>{1}.".format(t[0], cnt))
        if int(t[3]) >= conf[7] and t[4] not in ["1", "3"]:
            t[2] = t_modes['1'] + t[2]
        elif int(t[3]) >= conf[7] and t[4] == "2":
            t[2] = t_modes['3'] + t[2]
        elif t[4] in t_modes.keys():
            t[2] = t_modes[t[4]] + t[2]
        if not rss and prev:
            print("</a><td><a href='#" \
                  + "{0}'>{2}</a>&nbsp; <td>{3} <td>{1} &nbsp;".format(*t))
        elif not rss:
            print("</a><td><a href='?" \
            + "{0}'>{2}</a>&nbsp; <td>{3} <td>{1} &nbsp;".format(*t))
        else:
            rss_list.append(t)
        cnt += 1
    if rss:
        return rss_list
    print("<tr><td>")
    if prev and (t_cnt - s_ts) > 0:
        print("<td colspan='2'>")
        print(f"<a href='?m=list'>View all threads</a> ({t_cnt - s_ts} hidden)<td>")
    else:
        print("<td colspan='3'>")
    print("<a href='#create'>Create new thread</a>")
    print("</table>")

def bbs_reply(t_fn='', t_id=''):
    with open("./html/reply.html") as r_thread:
        print(r_thread.read().format(t_fn, t_id))

def bbs_atom(m='t'):
    amode = wt.get_form('r')
    if amode not in ['p', 't']:
        bbs_header()
        print(conf[8])
        return
    print("""Content-type: application/atom+xml\r\n
<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">""")
    if amode == 'p':
        print("<title>{0}: 50 latest posts</title>".format(conf[0]))
        print(f"<link rel='self' href='{conf[8]}?m=atom;r=p' />")
        print("<id>{0}#posts</id>".format(conf[8]))
        isot = "%Y-%m-%dT%H:%M:00%z"
        with open(conf[6], 'r') as tlist:
            tlist = tlist.read().splitlines()
        tdict = {}
        for t in tlist:
            t = t.split(" >< ")
            tdict[t[0]] = t[2]
        with open(conf[10]) as ip_l:
            ip_l = ip_l.read().splitlines()[::-1][:50]
        l_upd = ip_l[0].split(" >< ")[1].replace(" ", "").replace(".", "-")
        l_upd = re.sub(r'\[(.*?)\]', 'T', l_upd)
        print("<updated>" + l_upd + conf[9] + "</updated>")
        for p in ip_l:
            print("\n<entry>")
            # 0: thread fn, 1: time, 2: post,
            # 3: thread title, 4: link
            p = p.split(" >< ")
            p = [p[0].split(" | ")[1], p[1], cgi.escape(p[3])]
            p[0] = p[0].split(".")[0]
            p[1] = p[1].replace(" ", "").replace(".", "-")
            p[1] = re.sub(r'\[(.*?)\]', 'T', p[1]) + conf[9]
            p.append('"' + cgi.escape(tdict[p[0]]) + '"')
            p.append(conf[8] + "?" + p[0])
            print(f"<updated>{p[1]}</updated>",
                  f"<id>{p[4]}#{p[1]}</id>",
                  f"<title>reply in thread {p[3]}</title>",
                  f"<link rel='alternate' href='{p[4]}'/>",
                  f"<content type='html'>{p[2]}</content>\n</entry>\n")
        print("</feed>")
    elif amode == 't':
        print("<title>{0}: 50 latest threads</title>".format(conf[0]))
        print("<link rel='self' href='" + conf[8] + "?m=atom;r=t' />")
        print("<id>{0}#threads</id>".format(conf[8]))
        t_list = bbs_list(0, 1)
        t_list.sort(key=lambda t_list:t_list[0])
        upd = t_list[-1][0]
#        print(t_list)
        l_upd = time.localtime(int(upd))
        isot = "%Y-%m-%dT%H:%M" + conf[9]
        l_upd = time.strftime(isot, l_upd)
        print(f"<updated>{l_upd}</updated>")
        for t in t_list[::-1]:
            print("\n<entry>")
            upd = time.localtime(int(t[0]))
            t_url = conf[8] + "?" + t[0]
            print(f"<updated>{time.strftime(isot, upd)}</updated>",
                  f"<id>{t_url}</id>",
                  f"<link rel='alternate' href='{t_url}' />",
                  f"<title>{cgi.escape(t[2])}</title>")
            with open(conf[5] + t[0] + ".txt", "r") as tt:
                tt = tt.read().splitlines()[1]
                tt = " >< ".join(tt.split(" >< ")[3:])
                tt = cgi.escape(tt)
            print(f"<content type='html'>{tt}</content>\n</entry>")
        print("</feed>")

def bbs_foot():
    with open("./html/foot.html") as b_foot:
        print(b_foot.read())
        
def do_reply():
    reply_attrs = {'name':'', 'bump':'', 'comment':'', 't':''}
    if bans.is_banned(wt.get_ip()):
        print("<center>")
        print("<h1>You are banned!</h1>")
        print("<h3>", bans.is_banned(wt.get_ip()), "</h3>")
        return
    for key in reply_attrs.keys():
        if wt.get_form(key):
            reply_attrs[key] = wt.get_form(key)
    for word in bad_words:
        if word in reply_attrs["comment"].lower():
            print("<center><h2>Bad word error.</h2></center>")
            return
    if wt.get_form('rname') or wt.get_form('email'):
        return reply_attrs[comment]
    # Comment and thread are necessary params 
    if not reply_attrs['comment']:
        print("You need to write something to post a comment.")
        return None
    elif not reply_attrs['t']:
        return None
    reply_attrs['comment'] = reply_attrs['comment']\
                        .strip().replace('\r\n', "<br>")[:5000]\
                        .encode("ascii", "ignore").decode()
    
    # Get the name, generating trip / capcoding admin as needed
    if not reply_attrs['name']:
        reply_attrs['name'] = "Anonymous"
    elif '#' in reply_attrs['name']:
        namentrip = reply_attrs['name'][:18].split('#')[:2]
        namentrip[1] = tripcode(namentrip[1])
        if not namentrip[0]:
            namentrip[0] = "Anonymous"
        if conf[3] == namentrip[1][2:]:
            namentrip = ['', conf[2]]
            reply_attrs['name'] = '</span> <span class="admin">'\
                                                    .join(namentrip)
        else:
            reply_attrs['name'] = '</span> <span clas="trip">'\
                                                    .join(namentrip)
    else:
        reply_attrs['name'] = reply_attrs['name'][:18]

    # Check if sage or not
    if not reply_attrs['bump']:
        reply_attrs['bump'] = "1"
    elif reply_attrs['bump'] != "1":
        reply_attrs['bump'] = ''
        
    reply_attrs['ldt'] = wt.fancy_time(None, "human") 

    reply_string = " >< ".join([reply_attrs['name'], \
            reply_attrs['ldt'], reply_attrs['bump'], \
            reply_attrs['comment'] + "\n"])
        
    fale = 0
    with open(reply_attrs['t'], "r") as the_thread:
        ter = the_thread.read().splitlines()
    num_replies = len(ter) - 1
    if "><" in ter[0] and ter[0].split(">< ")[1] in ["1", "3"]:
        fale = 3
    elif num_replies >= conf[7]:
        fale = 1
    else:
        ter = ter[-1].split(' >< ')
        if ter[-1] == reply_string.split(' >< ')[-1][:-1]:
            fale = 2

    f_mesg = {1:"Sorry, thread limit reached.",
        2:"Sorry, you already posted that.",
        3:"Sorry, the thread is locked."}

    # Update thread with latest post by appending to the file.
    if fale == 0:
        with open(reply_attrs['t'], "a+") as the_thread:
            the_thread.write(reply_string)
    else:
        print(f_mesg[fale])
        return None

    ip = os.environ["REMOTE_ADDR"]
    reply_attrs['t'] = reply_attrs['t'][len(conf[5]):]
    log_data = " | ".join([ip, reply_attrs['t'],
                           f"#{num_replies} | {reply_string}"])

    # update ips.txt (log of posts + ips)
    with open(conf[10], "a") as log:
            log.write(log_data)
    print("comment successfully posted<p>Redirecting you in"
          " 5 seconds...", wt.redirect())

    reply_attrs['t'] = ''.join([i for i in reply_attrs['t'] \
                                if i.isdigit()])
    t_line = [reply_attrs['t'], reply_attrs['ldt'], reply_attrs['bump']]
    nt_list = []
    new_t = []
    sage = 0
    # load list.txt
    with open(conf[6]) as t_list:
        t_list = t_list.read().splitlines()
    for n, t in enumerate(t_list):
        t = t.split(' >< ')
        nt_list.append(t)
        if t[0] == t_line[0]:
            if t[4] in ["1", "3"]:
                print("you should not be posting in a locked thread")
                return None
            elif t_line[2] == "1" or t[4] in ("2", "4"):
                # Sage, posting in sticky, posting in permasage
                # does not affect the thread's position 
                sage = 1
            t_line.pop(2)
            t_line.insert(2, t[2])
            t_line.insert(3, str(int(t[3])+1))
            t_line.insert(4, t[4])
            new_t = [' >< '.join(t), ' >< '.join(t_line)]

    # Update list.txt
    posted = 0
    for n, t in enumerate(nt_list):
        # Maintain position of sage/stickies
        if sage:
            if t[0] == new_t[0].split(" >< ")[0]:
                nt_list[n] = new_t[1].split(" >< ")
                break
        # Do not move a bumped thread above stickied threads
        elif posted == 0 and t[4] not in ["2", "3"]:
            nt_list.insert(n, new_t[1].split(" >< "))
            posted = 1
        elif t == new_t[0].split(" >< "):
            nt_list.remove(t)
            break
    for n, l in enumerate(nt_list):
        nt_list[n] = " >< ".join(l)        
    with open(conf[6], "w") as new_tl:
        new_tl.write('\n'.join(nt_list))

def do_prev(bbt=[]):
    if not bbt:
        with open(conf[6]) as t_list:
            t_list = t_list.read().splitlines()[:conf[12]]
        for n, t in enumerate(t_list):
            t = t.split(" >< ")
            bbs = bbs_thread(t[0], 1)
            print("<div class='thread'><a name={0}>".format(t[0]))
            print("<h3><a>" + str(n+1)+".</a>")
            do_prev([bbs, t[0]])
        return
    pstcnt = 0
    bbn = len(bbt[0])
    if bbn > conf[13]:
        bbn = len(bbt[0]) - conf[13] + 1
    else:
        bbn = 1
    with open(conf[5] + str(bbt[1]) + ".txt") as t:
        t_t = t.readline()[:-1]
        t_r = len(t.read().splitlines())
        
    t_m = ''
    if "><" in t_t:
        print(t_modes[t_t.split(">< ")[1]])
        t_m = t_modes[t_t.split(">< ")[1]]
        if t_m in t_modes.keys():
            t_t = t_t.split(" >< ")[0] + t_m
        else:
            t_t = t_t.split(" >< ")[0]
    print("<a href='?{0}'>{1} [{2}]"\
          .format(bbt[1], t_t, len(bbt[0])))
    print("</a></h3>")

    for replies in bbt[0]:
        pstcnt += 1
        if pstcnt == 1 or pstcnt >= bbn:
            print("<div class='reply'><div class='title'>")
            print("#{0} //".format(pstcnt))
            print("Name: {0} \n: Date: {1} \n</div>"
                  "<div class='comment'>{2}</div>".format(*replies))
        elif pstcnt == (bbn - 1):
            print("<hr>")    
    if "lock" in t_m or t_r >= conf[7]:
        print("""<div class='reply'>
        <div class='rmr'><br>{0}
        Thread locked.<p>
        No more comments allowed
        </div><br></div></div>""".format(t_m))
    elif t_r < conf[7]:
        print("<p>")
#        print("<hr width='420px' align='left'>")
        bbs_reply(conf[5] + bbt[1]+".txt")

def do_format(urp=''):
    x = "(text omitted)<br>" + urp.split('[/yt]')[-1] \
        if len(urp.split('[yt]')) > 3 \
        else ''
    urp = '[yt]'.join(urp.split('[yt]')[:3])
    urp += x
#    urp += if len(urpl.split('[yt]')) > 3 urp.split('[/yt]')[-1]
    urp = re.sub(r'\[yt\]http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?[\w\?=]*)?\[/yt\]', 
                 r'<div style="width:480; height:320" class="youtube" id="\1"></div><p>', urp)

    urp = re.sub(r'\[spoiler\](.*?)\[/spoiler\]',
                 r'<span class="spoiler">\1</span>', urp)
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

if __name__ == "__main__":
    main()
