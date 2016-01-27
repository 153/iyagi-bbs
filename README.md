# iyagi
Python web board system (textboard, CGI, flatfile)

Inspired by [Kareha](http://wakaba.c3.cx/s/web/wakaba_kareha), 
[Shiichan](https://wakaba.c3.cx/shii/shiichan), [Tablecat BBS](http://tablecat.ipyo.heliohost.org/bbs/), 
and others. 

1. Features
2. Screenshots
3. Installation
4. To-do 

## 1. Features
The script iyagi (이야기,  "chat") is still in a very early beta, but it currently supports the following features:
- Thread posting
- Thread indexing in a list
- Thread replying with/without bumps (age/sage)
- Atom feeds for recent threads / posts
- Tripcodes (pseudo-registration)
 - Admin password is a tripcode (hashed password)
- 4x13 and 0ch themes, with styleswitcher
- [spoiler], [code], [yt], [aa] (ascii art) BBcode tags 
 - [yt] (youtube) is resource efficient through clever JS
- very weak spam detection
- Permasage, Lock, and Sticky, with icons
- Vanilla install

## 2. Screenshots
<a href="https://i.imgur.com/yJztMga.png"><img src="https://i.imgur.com/yJztMgab.png"></a><a href="https://i.imgur.com/OTvViMn.png"><img src="https://i.imgur.com/OTvViMnb.png"></a>
<br><i>Frontpage of 0ch and 4x13 themes</i>

<a href="https://i.imgur.com/DxpsOl8.png"><img src="https://i.imgur.com/DxpsOl8m.png"></a>
<br><i>A thread with no comments, showing off the reply window. "Bump" can be unchecked, which preserves the thread's order in the index.</i>

<a href="https://i.imgur.com/IR5zORs.png"><img src="https://i.imgur.com/IR5zORsb.png"></a>
<br><i>Ascii art, using [aa][/aa] tags</i>

<a href="https://i.imgur.com/8rDMdab.png"><img src="https://i.imgur.com/8rDMdabm.png"></a>
<br><i>Code, using [code][/code] tags </i>

<a href="https://i.imgur.com/tebaE6R.png"><img src="https://i.imgur.com/tebaE6Rm.png"></a>
<br><i>Quotes & replies, using >quote and >>reply </i>

<a href="https://i.imgur.com/P0OUNls.png"><img src="https://i.imgur.com/P0OUNlsm.png"></a>
<br><i>Spoiler (unspoiled), using [spoiler][/spoiler] and Youtube embed [yt][/yt]</i>

<a href="https://i.imgur.com/5YT2QIs.png"><img src="https://i.imgur.com/5YT2QIsm.png"></a>
<br><i>Spoiler (spoiled), using [spoiler][/spoiler] and Youtube embed [yt][/yt]</i>

<a href="https://i.imgur.com/4XXj6IW.png"><img src="https://i.imgur.com/4XXj6IWm.png"></a>
<br><i>Thread limit of (default, 100) reached</i>

<a href="https://i.imgur.com/1yy0OCd.png"><img src="https://i.imgur.com/1yy0OCdb.png"></a><a href="https://i.imgur.com/ktSWd3u.png"><img src="https://i.imgur.com/ktSWd3ub.png"></a><a href="https://i.imgur.com/EoyS473.png"><img src="https://i.imgur.com/EoyS473m.png"></a>

Locked, stickied, dead threads. Locked threads cannot be posted in, stickied threads always stay at the top of the board, dead threads cannot be bumped.

## 3. Installation
Installation couldn't be easier. Just download (at least) index.py3 and the .html and .css files in the top-level directory, then make sure your BBS directory and its contents have read/write privileges by the web daemon. Then, open index.py3 with your favorite text editor, and from there, confirm your settings. 

Moderation is currently done by managing text files in a directory; the default directory is "./threads/". You need to have at least one valid thread on the board to enable posting; if you need to initialize the board, create a folder called "./threads/" that's readable/writable by the web daemon, and in there, a file called "list.txt" and another called "0.txt".

    list.txt contents:
    0 >< 0 >< 0 >< 0 >< 0
      
    0.txt contents:
    0
    0 >< 0 >< 0 >< 0
    
  Then, try posting another thread from the page to confirm that your board works. To get rid of that first thread, remove its entry from list.txt and remove 0.txt from the thread directory. To edit threads/posts, find a thread's filename in your web browser or list.txt, then just modify it in a text editor. 

If you want to lock a thread, change the last number in its row, in list.txt, to "1". To sticky, "2". To stickylock, "3". To kill, "4". Then, open the thread (its_unix_time.txt in ./threads/) and added "[<" followed by that same value to the title line. Clunky, but it works for now :) 

## 4. To-do 
Here's what I'd like to add to bring iyagi to v1.5:
- More stylesheets
- Some kind of markup format - probably markdown derived
- Better admin panel and anti-spam filters (regex spam list, IP-based bans, post deletion, thread mode editting)

Possible bonus features:
- User storable capcodes
- ?????
