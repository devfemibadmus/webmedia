import os, uuid, time, threading

binList =  [('TikTok/reel.vfx/7357012437419298090_0.jpg', 1721902080.7317343), ('TikTok/reel.vfx/7357012437419298090_1.jpg', 1721902080.7317343), ('TikTok/reel.vfx/7357012437419298090_2.jpg', 1721902080.7317343)]

bin_list =  ['TikTok/reel.vfx/7357012437419298090_0.jpg', 'TikTok/reel.vfx/7357012437419298090_0.jpg', 'TikTok/reel.vfx/7357012437419298090_0.jpg', 'TikTok/reel.vfx/7357012437419298090_0.jpg', 'TikTok/reel.vfx/7357012437419298090_1.jpg', 'TikTok/reel.vfx/7357012437419298090_0.jpg', 'TikTok/reel.vfx/7357012437419298090_0.jpg', 'TikTok/reel.vfx/7357012437419298090_0.jpg', 'TikTok/reel.vfx/7357012437419298090_2.jpg', ]


def add_to_bin_list():
    timestamp = time.time() + 180
    for bin in bin_list:
        if bin not in [b[0] for b in binList]:
            binList.append((bin, timestamp))
    print("binList: ", binList)

add_to_bin_list()
