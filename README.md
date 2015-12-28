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
- Thread indexing (subback.html)
- Thread replying with/without bumps (age/sage)
- Tripcodes (pseudo-registration)
- Vanilla install

## 2. Screenshots
<a href="https://i.imgur.com/p00emB2.png"><img src="https://i.imgur.com/p00emB2m.png"></a><br>
1. Frontpage, thread list, thread preview

<a href="https://i.imgur.com/NG91EX1.png"><img src="https://i.imgur.com/NG91EX1m.png"></a><br>
2. Thread preview, replybox

<a href="https://i.imgur.com/ayTsqqD.png"><img src="https://i.imgur.com/ayTsqqDm.png"></a><br>
3. Illustration of long post trunctuation in the index

<a href="https://i.imgur.com/1YUESsM.png"><img src="https://i.imgur.com/1YUESsMm.png"></a><br>
4. Threadpage and replybox 

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

## 3. Installation
Installation couldn't be easier. Just download (at least) index.py3 and the .html and .css files in the top-level directory, then make sure your BBS directory and its contents have read/write privileges by the web daemon. Then, open index.py3 with your favorite text editor, and from there, confirm your settings. 

Moderation is currently done by managing text files in a directory; the default directory is "./threads/". You need to have at least one valid thread on the board to enable posting; if you need to initialize the board, create a folder called "./threads/" that's readable/writable by the web daemon, and in there, a file called "list.txt" and another called "0.txt".

    list.txt contents:
    0 >< 0 >< 0 >< 0 
      
    0.txt contents:
    0
    0 >< 0 >< 0 >< 0
    
  Then, try posting another thread from the page to confirm that your board works. To get rid of that first thread, remove its entry from list.txt and remove 0.txt from the thread directory. To edit threads/posts, find a thread's filename in your web browser or list.txt, then just modify it in a text editor. 

## 4. To-do 
Here's what I'd like to add to bring iyagi to v1.0:
- Themes / Themepicker
- Stickied threads, locked threads, non-bumpable threads
- A proper thread index for the main page
- Some kind of markup format - probably markdown derived
- Admin panel, IP logging, anti-spam filters
- RSS list of threads

Possible bonus features:
- Youtube / Soundcloud embed
- Twitter login as an alternative to tripcodes for identifying posts 
- User storable capcodes
