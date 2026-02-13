from datetime import datetime
ip_version_priority = "ipv4"

source_urls = [
   "https://raw.githubusercontent.com/develop202/migu_video/refs/heads/main/interfaceTXT.txt",
   "https://raw.githubusercontent.com/slasjh/tvlive/refs/heads/main/three.txt",
    "http://156.238.251.122:888/live/fh.txt",
   #"http://156.238.251.122:8089/system/get-favourite-channel?channel_type=all,
    "https://raw.githubusercontent.com/slasjh/tvlive/refs/heads/main/checkspeed/live_Lite.txt",
   "https://raw.githubusercontent.com/slasjh/tvlive/refs/heads/main/checkspeed/whitelist_auto_tv.txt"
    #"http://64.81.114.28:7000/txt"
   
    #"https://gitee.com/mytv-android/iptv-api/raw/master/output/result.m3u"
     #"http://156.238.251.122:888/live/live_Lite.txt",
    #"https://raw.githubusercontent.com/n3rddd/CTVLive/master/live.m3u",
   




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
        "channel": "🤠小土豆直播",
        "entries": [
            #{"name":"free by oneself","url":"","logo":""},
            {"name":"更新日期{placeholder}","url":"http://1.1.1.1","logo":""},
           
        ]
    }
]
# 获取当前日期，并格式化为YYYYMMDD

current_date = datetime.now().strftime('%Y-%m-%d %H:%M')

 

# 替换announcements中的日期占位符

for announcement in announcements:

    for entry in announcement['entries']:

        if '更新日期{placeholder}' in entry['name']:

            entry['name'] = entry['name'].replace('{placeholder}', current_date)
            
epg_urls = [
    "http://epg.51zmt.top:8000/e.xml",
    "http://epg.aptvapp.com/xml",
    "https://epg.pw/xmltv/epg_CN.xml",
    "https://epg.pw/xmltv/epg_HK.xml",
    "https://epg.pw/xmltv/epg_TW.xml"
]
