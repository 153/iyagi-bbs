# iyagi
Python web board system (textboard, CGI, flatfile)

Inspired by [Kareha](http://wakaba.c3.cx/s/web/wakaba_kareha), 
[Shiichan](https://wakaba.c3.cx/shii/shiichan),
[Tablecat BBS](http://tablecat.ipyo.heliohost.org/bbs/), 
and others. 

Requires python 3.6+, collections (for defaultdict)

1. Features
2. Screenshots
3. Installation
4. Settings / config
5. To-do 

## 1. Features
The script iyagi (이야기,  "chat") is approaching a nicer cleaner
refactor with more features. But it works, and it can do some things
that other boards can't.

It currently has the following features:
- Works well out of the box and friendly `./settings.txt`
- Thread replying with/without bumps (age/sage)
- Tripcodes (pseudo-registration)
- 4x13 and 0ch themes, with JS styleswitcher
- [spoiler], [code], [yt] (YouTube) BBcode tags
- Backlinking, to keep track of sub-threads
- very weak spam detection
- Permasage, Lock, and Sticky
- Vanilla
- IP logging 
- Atom feeds for recent posts / threads
- Slick NoSQL  

## 2. Screenshots
<a href="https://i.imgur.com/yJztMga.png">
<img src="https://i.imgur.com/yJztMgab.png">
</a><a href="https://i.imgur.com/OTvViMn.png">
<img src="https://i.imgur.com/OTvViMnb.png"></a>
<br><i>Frontpage, in 0ch and 4x13 themes</i><br>

<br><a href="https://i.imgur.com/DxpsOl8.png">
<img src="https://i.imgur.com/DxpsOl8m.png"></a>
<br><i>A thread with no comments, showing off the reply window. "Bump" can 
be unchecked, which preserves the thread's order in the index.</i><br>

<br><a href="https://i.imgur.com/IR5zORs.png">
<img src="https://i.imgur.com/IR5zORsb.png"></a>
<br><i>Ascii art, using [aa][/aa] tags (out for repairs)</i><br>

<br><a href="https://i.imgur.com/8rDMdab.png">
<img src="https://i.imgur.com/8rDMdabm.png"></a>
<br><i>Code, using [code][/code] tags </i><br>

<br><a href="https://i.imgur.com/1yy0OCd.png">
<img src="https://i.imgur.com/1yy0OCdb.png"></a>
<a href="https://i.imgur.com/ktSWd3u.png">
<img src="https://i.imgur.com/ktSWd3ub.png"></a>
<br><a href="https://i.imgur.com/EoyS473.png">
<img src="https://i.imgur.com/EoyS473m.png"></a><br>

Locked, stickied, dead threads. Locked threads cannot be posted in, 
stickied threads always stay at the top of the board, dead threads 
cannot be bumped.

## 3. Installation
Installation couldn't be easier. Just download the repo and give the BBS 
directory and its contents read/write privileges with the web daemon. 
Then, open settings with your favorite text editor, and from there, 
confirm your settings. 

Moderation is currently done by managing text files in a directory; 
the default directory is "./threads/". You need to have at least one 
valid thread on the board to enable posting; if you need to initialize 
the board, create a folder called "./threads/" that's readable/writable 
by the web daemon, and in there create a file called 0.txt. In your iyagi directory, create a file called "list.txt".

    list.txt contents:
    0 >< 0 >< 0 >< 0 >< 0
      
    0.txt contents:
    0
    0 >< 0 >< 0 >< 0
    
Then, try posting another thread from the page to confirm that your board 
works. To get rid of that first thread, remove its entry from list.txt and
remove 0.txt from the thread directory. To edit threads/posts, find a 
thread's filename in your web browser or list.txt, then just modify it in 
a text editor. 

If you want to lock a thread, change the last number in its row, in 
list.txt, to "1". To sticky, "2". To stickylock, "3". To kill, "4". 
Then, open the thread (its\_unix\_time.txt in ./threads/) and add "><",
followed by that same value to the title line. 

Clunky, but it works for now :) 

## 4. Settings / config 
settings.txt
- 0. board name
- 1. board url
- 2. mod username
- 3. mod password (using hash generated from ./tripcode.py)
- 4. theme (unused)
- 5. thread storage (./threads)
- 6. thread list (./list.txt)
- 7. full URL
- 8. time zone
- 9. post IP log (ips.txt)
- 10. thread IP log (ips2.txt)
- 11. show recent - 8
- 12. show replies - 3

index.py
- settings = `./settings.txt`
- bad_words = `["bad", "words", "go", "here"]`

bans.py
```bans = {"ip address":"reason"
"1.2.3.4":"spam",
"2.2.2":"a wildcard for 2.2.2"
".": "ban absolutely everyone from posting"
}
```


## 5. To-do 
Your comments/contributions would be appreciated 

Here's what I'd like to bring to future versions of IYAGI
- More stylesheets
- better refactoring 
- Admin panel, anti-spam filters
- thread / index pagination
- More JS stuff, maybe?

Possible bonus features:
- User storable capcodes
- ?????
