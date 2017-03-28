#!/usr/bin/env python3

import cgi, os, time
form = cgi.FieldStorage()

time_form = '%Y.%m.%d [%a] %H:%M'
long_time = '%A, %B %d @ %H:%M'
short_time = '%m-%d @ %H:%M'

# print headers, receive CGI form info, create CGI
# forms, basic cookie handling, and translate UNIX time
# to the preferred timestamp format. 

def head(title=''):
    header = ["Content-type: text/html\n\n"]
    header.append("<title>{0}</title>".format(title))
    return "\n".join(header)

def get_form(val):
    if form.getvalue(val):
        if len(form.getvalue(val)[0]) > 1:
#            print('\n'.join(form.getlist(val)))
            return cgi.escape('\n'.join(form.getlist(val))).strip()
        return cgi.escape(form.getvalue(val)).strip()
    else:
        return ''

def put_form(ty='', na='', va='', re=''):
    inps = [ty, na, va]
    if ty != "textarea":
        exform = "<input type='{0}' name='{1}' value='{2}'>".format(*inps)
    else:
        exform = "<textarea name='{1}'>{2}</textarea>".format(*inps)
    if re:
        exform.replace(">", " required>")
    return exform

def dropdown(na='', val=[], nam=[]):
    dropdown = ["<select name='{0}'>".format(na)]
    if len(val) > len(nam) or not nam:
        nam = val
    for n, i in enumerate(val):
        dropdown.append("<option value='{0}'>{1}</option>".format(val[n], \
                                                                nam[n]))
    dropdown.append("</select>")
    return "\n".join(dropdown)
        

def new_form(act='.', met='post'):
    formhead = "<form action='{0}' method='{1}'>".format(act, met)
    return formhead

def put_cookie(name='', data=''):
    content = name+"="+data+";"
    c_string = "<meta http-equiv='set-cookie' content='{0}'>".format(content)
    return c_string

def get_cookie():
    c_dict = {}
    if "HTTP_COOKIE" in os.environ:
        cookies = os.environ["HTTP_COOKIE"]
        cookies = cookies.split("; ")
        for c in cookies:
            c = c.split("=")
            c_dict[c[0]] = "=".join(c[1:])
    return c_dict

def get_ip():
    return os.environ["REMOTE_ADDR"]

def fancy_time(utime='', mode=''):
    if not utime:
        utime = int(time.time())
    else:
        utime = int(utime)
    if mode == 'unix':
        return str(utime)
    htime = time.localtime(utime)
    if mode == "human":
        htime = time.strftime(time_form, htime)
        return htime
    elif mode == "lt":
        return time.strftime(long_time, htime)
    elif mode == "st":
        return time.strftime(short_time, htime)
    else:
        htime = time.strftime(time_form, htime)
        return [utime, htime]

def grab_html(fn=''):
    with open('./html/' + fn + '.html', 'r') as html:
        html = html.read()
    return html

def redirect(sec=5, loc='.'):
    return "<meta http-equiv='refresh' content='" \
        + str(sec) + ";" + loc + "'>"
