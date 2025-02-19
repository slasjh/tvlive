ip_version_priority = "ipv4"

source_urls = [
      "http://156.238.251.122:35455/tv.m3u", #ADDED BY lee from sshh. ON 31/12/2024 
    "https://live.fanmingming.com/tv/m3u/ipv6.m3u", #ADDED BY lee from fanmingming. ON 31/12/2024 
    "https://raw.githubusercontent.com/YanG-1989/m3u/main/Gather.m3u", #ADDED BY lee from https://tv.iill.top/m3u/Gather" ON 31/12/2024 
    "http://175.178.251.183:6689/live.m3u", #ADDED BY lee from yuanlz77" ON 31/12/2024 
    "https://raw.githubusercontent.com/Guovin/TV/gd/output/result.m3u", #ADDED BY lee from Guovin/TV/gd/ (juhe) ON 31/12/2024 
    "https://live.iptv365.org/live.txt", #ADDED BY lee from kimwang1978/collect-tv-txt (juhe) ON 31/12/2024 
    "https://raw.githubusercontent.com/zwc456baby/iptv_alive/master/live.m3u", #ADDED BY lee from zwc456baby cu (juhe) ON 31/12/2024 
    "https://raw.githubusercontent.com/hero1898/tv/refs/heads/main/IPTV.m3u", #ADDED BY lee from hero1898 (juhe) ON 31/12/2024 
    "https://live.zbds.top/tv/iptv6.txt", #ADDED zbds (juhe) ON 31/12/2024 
    "https://live.zbds.top/tv/iptv4.txt", #ADDED zbds (juhe) ON 31/12/2024
    "https://raw.githubusercontent.com/n3rddd/CTVLive/master/live.m3u", #ADDED /n3rddd (juhe) ON 31/12/2024
    "https://raw.githubusercontent.com/xiongjian83/zubo/refs/heads/main/live.txt", #ADDED xiongjian83 (juhe) ON 31/12/2024
    "https://raw.githubusercontent.com/YueChan/Live/main/IPTV.m3u", #ADDED /YueChan(juhe) ON 31/12/2024    
    "http://tv.850930.xyz/kdsb.txt", #ADDED BY LEM ON 28/09/2024
    "http://tv.850930.xyz/kdsb2.txt", #ADDED BY LEM ON 28/09/2024
    "http://tv.850930.xyz/gather.m3u", #ADDED BY LEM ON 29/07/2024
    "https://live.wqwqwq.sbs/tv.m3u", #ADDED BY LEM ON 26/11/2024
    "https://lu.wqwqwq.sbs/tv.m3u", #ADDED BY LEM ON 26/11/2024
    "https://www.mytvsuper.xyz/m3u/Live.m3u", #ADDED BY LEM ON 30/11/2024
    "https://tv.ccsource.us.kg/live.txt", #ADDED BY LEM ON 08/12/2024
    "https://raw.githubusercontent.com/redrainl/iptv/main/speedtest/zubo_fofa.txt", #ADDED BY LEM ON 01/08/2024
    "https://raw.githubusercontent.com/pxiptv/live/main/iptv.txt", #ADDED BY LEM ON 08/08/2024
    "https://raw.githubusercontent.com/n3rddd/MemoryCollection-IPTV/refs/heads/main/hotel.txt", #ADDED BY LEM ON 09/11/2024
    "https://aktv.top/live.m3u", #ADDED BY LEM ON 18/10/2024
    "https://gitcode.net/ygbh66/test/-/raw/master/oh.txt", #ADDED BY LEM ON 10/09/2024
    "https://raw.githubusercontent.com/wwb521/live/main/tv.m3u", #ADDED BY LEM ON 28/09/2024
    "https://raw.githubusercontent.com/kakaxi-1/IPTV/main/iptv.txt", #ADDED BY LEM ON 27/09/2024
    "https://raw.githubusercontent.com/SingerLan/live/refs/heads/main/jiexi.txt", #ADDED BY LEM ON 20/11/2024
    "https://json.doube.eu.org/live/migu/Sub.php", #ADDED BY LEM ON 20/11/2024
    "https://raw.githubusercontent.com/yuanzl77/IPTV/main/直播/央视频道.txt",
    "https://live.zhoujie218.top/tv/iptv6.txt",
    "http://ww.weidonglong.com/dsj.txt",
    "http://xhztv.top/zbc.txt",
    "https://raw.githubusercontent.com/mlvjfchen/TV/main/iptv_list.txt",
    "https://raw.githubusercontent.com/qingwen07/awesome-iptv/main/tvbox_live_all.txt",
    "http://home.jundie.top:81/Cat/tv/live.txt",
    "https://raw.githubusercontent.com/vbskycn/iptv/master/tv/hd.txt",
    "https://cdn.jsdelivr.net/gh/YueChan/live@main/IPTV.m3u",
    "https://raw.githubusercontent.com/cymz6/AutoIPTV-Hotel/main/lives.txt",
    "https://raw.githubusercontent.com/PizazzGY/TVBox_warehouse/main/live.txt",
    "https://fm1077.serv00.net/SmartTV.m3u",
    "https://raw.githubusercontent.com/ssili126/tv/main/itvlist.txt",
    "https://raw.githubusercontent.com/joevess/IPTV/main/iptv.m3u8", #ADDED BY LEM ON 08/09/2024
    "https://raw.githubusercontent.com/kimwang1978/collect-tv-txt/main/merged_output.txt", #ADDED BY LEM ON 29/07/2024
    "https://raw.githubusercontent.com/Supprise0901/TVBox_live/main/live.txt", #ADDED BY LEM ON 29/07/2024
    "https://raw.githubusercontent.com/yoursmile66/TVBox/main/live.txt", #ADDED BY LEM ON 29/07/2024
    "http://kxrj.site:55/lib/kx2024.txt", #ADDED BY LEM ON 22/10/2024
    "https://raw.githubusercontent.com/Kimentanm/aptv/master/m3u/iptv.m3u", #ADDED BY LEM ON 29/07/2024
    "https://raw.githubusercontent.com/Love4vn/love4vn/main/Sport.m3u", #奥运 ON 29/07/2024
    "https://gitlab.com/tvkj/qxitv/-/raw/main/888.txt" #ADDED BY LEM ON 29/07/2024
]

url_blacklist = [
    "epg.pw/stream/",
    "103.40.13.71:12390",
    "[2409:8087:1a01:df::4077]/PLTV/",
    "8.210.140.75:68",
    "154.12.50.54",
    "yinhe.live_hls.zte.com",
    "8.137.59.151",
    "[2409:8087:7000:20:1000::22]:6060",
    "histar.zapi.us.kg",
    "www.tfiplaytv.vip",
    "dp.sxtv.top",
    "111.230.30.193",
    "148.135.93.213:81",
    "live.goodiptv.club",
    "iptv.luas.edu.cn"
]

announcements = [
    {
        "channel": "🤠小土豆ipv4直播",
        "entries": [
            {"name":"小土豆ipv4直播","url":"https://cors.isteed.cc/https://raw.githubusercontent.com/n3rddd/N3RD/master/JN/N3RD/W/CTVThemeSong1.mp4","logo":"https://cors.isteed.cc/https://raw.githubusercontent.com/n3rddd/N3RD/master/JN/N3RD/W/ICON1.png"},
            {"name":"free by oneself","url":"https://cors.isteed.cc/https://raw.githubusercontent.com/n3rddd/N3RD/master/JN/N3RD/W/CTVThemeSong2.mp4","logo":"https://cors.isteed.cc/https://raw.githubusercontent.com/n3rddd/N3RD/master/JN/N3RD/W/ICON2.png"},
            {"name":"更新日期","url":"https://cors.isteed.cc/https://raw.githubusercontent.com/n3rddd/N3RD/master/JN/N3RD/W/CRIMETVPV1.mkv","logo":"https://cors.isteed.cc/https://raw.githubusercontent.com/n3rddd/N3RD/master/JN/N3RD/W/ICON3.png"},
            {"name":"20241231","url":"https://cors.isteed.cc/https://raw.githubusercontent.com/n3rddd/N3RD/master/JN/N3RD/W/CRIMETVPV2.mkv","logo":"https://cors.isteed.cc/https://raw.githubusercontent.com/n3rddd/N3RD/master/JN/N3RD/W/ICON4.png"}
        ]
    }
]

epg_urls = [
    "https://live.fanmingming.com/e.xml",
    "http://epg.51zmt.top:8000/e.xml",
    "http://epg.aptvapp.com/xml",
    "https://epg.pw/xmltv/epg_CN.xml",
    "https://epg.pw/xmltv/epg_HK.xml",
    "https://epg.pw/xmltv/epg_TW.xml"
]
