import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from datetime import datetime
import os
from urllib.parse import urlparse
import socket  #check p3p源 rtp源
import subprocess #check rtmp源
import re

timestart = datetime.now()

BlackHost=["127.0.0.1:8080","live3.lalifeier.eu.org","newcntv.qcloudcdn.com","ottrrs.hl.chinamobile.com","dsm.huarunguoji.top:35455",
           "www.52sw.top:678","gslbservzqhsw.itv.cmvideo.cn","chinamobile.com","hwrr.jx.chinamobile.com:8080",
           "kkk.jjjj.jiduo.me","a21709.tv.netsite.cc","gslbserv.itv.cmvideo.cn","36.251.58.50:6060","47.92.130.115:9000",
           "stream1.freetv.fun","www.freetv.top",
           "[2409:8087:3869:8021:1001::e5]:6610","www.52iptv.vip:35455","dbiptv.sn.chinamobile.com","61.160.112.102:35455"
]

# 读取文件内容
def read_txt_file(file_path):
    skip_strings = ['#genre#']  # 定义需要跳过的字符串数组['#', '@', '#genre#'] 
    required_strings = ['://']  # 定义需要包含的字符串数组['必需字符1', '必需字符2'] 

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [
            line for line in file
            if not any(skip_str in line for skip_str in skip_strings) and all(req_str in line for req_str in required_strings)
        ]
    return lines

# 检测URL是否可访问并记录响应时间
def check_url(url, timeout=6):
    start_time = time.time()
    elapsed_time = None
    success = False

    # 将 URL 中的汉字编码
    encoded_url = urllib.parse.quote(url, safe=':/?&=')
    
    try:
        if get_host_from_url(url) not in BlackHost and not is_ipv6(url) and url.startswith("http") :
            headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            }
            req = urllib.request.Request(encoded_url, headers=headers)
            req.allow_redirects = True  # 允许自动重定向（Python 3.4+）
            with urllib.request.urlopen(req, timeout=timeout) as response:
                if response.status == 200 or response.status == 206:  # 部分内容响应也是成功的:
                    success = True
        elif url.startswith("p3p") or url.startswith("p2p") or url.startswith("rtmp") or url.startswith("rtsp") or url.startswith("rtp"):
            success = False
            print(f"{url}此链接为rtp/p2p/rtmp/rtsp等，舍弃不检测")

        # 如果执行到这一步，没有异常，计算时间
        elapsed_time = (time.time() - start_time) * 1000  # 转换为毫秒

    except Exception as e:
        print(f"Error checking {url}: {e}")
        record_host(get_host_from_url(url))
        # 在发生异常的情况下，将 elapsed_time 设置为 None
        elapsed_time = None

    return elapsed_time, success
           
def is_ipv6(url):
    return re.match(r'^http:\/\/\[[0-9a-fA-F:]+\]', url) is not None
           

# 处理单行文本并检测URL
def process_line(line):
    if "#genre#" in line or "://" not in line :
        return None, None  # 跳过包含“#genre#”的行
    parts = line.split(',')
    if len(parts) == 2:
        name, url = parts
        elapsed_time, is_valid = check_url(url.strip())
        if is_valid:
            return elapsed_time, line.strip()
        else:
            return None, line.strip()
    return None, None

# 多线程处理文本并检测URL
def process_urls_multithreaded(lines, max_workers=15):
    blacklist =  [] 
    successlist = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_line, line): line for line in lines}
        for future in as_completed(futures):
            elapsed_time, result = future.result()
            if result:
                if elapsed_time is not None:
                    successlist.append(f"{elapsed_time:.2f}ms,{result}")
                else:
                    blacklist.append(result)
    return successlist, blacklist

# 写入文件
def write_list(file_path, data_list):
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in data_list:
            file.write(item + '\n')

# 增加外部url到检测清单，同时支持检测m3u格式url
# urls里所有的源都读到这里。
urls_all_lines = []

def get_url_file_extension(url):
    # 解析URL
    parsed_url = urlparse(url)
    # 获取路径部分
    path = parsed_url.path
    # 提取文件扩展名
    extension = os.path.splitext(path)[1]
    return extension

def convert_m3u_to_txt(m3u_content):
    # 分行处理
    lines = m3u_content.split('\n')
    
    # 用于存储结果的列表
    txt_lines = []
    
    # 临时变量用于存储频道名称
    channel_name = ""
    
    for line in lines:
        # 过滤掉 #EXTM3U 开头的行
        if line.startswith("#EXTM3U"):
            continue
        # 处理 #EXTINF 开头的行
        if line.startswith("#EXTINF"):
            # 获取频道名称（假设频道名称在引号后）
            channel_name = line.split(',')[-1].strip()
        # 处理 URL 行
        elif line.startswith("http"):
            txt_lines.append(f"{channel_name},{line.strip()}")
    
    # 将结果合并成一个字符串，以换行符分隔
    # return '\n'.join(txt_lines)
    return txt_lines

url_statistics=[]

def process_url(url):
    try:
        # 打开URL并读取内容
        with urllib.request.urlopen(url) as response:
            # 以二进制方式读取数据
            data = response.read()
            # 将二进制数据解码为字符串
            text = data.decode('utf-8')
            if get_url_file_extension(url)==".m3u" or get_url_file_extension(url)==".m3u8":
                m3u_lines=convert_m3u_to_txt(text)
                url_statistics.append(f"{len(m3u_lines)},{url.strip()}")
                urls_all_lines.extend(m3u_lines) # 注意：extend
            elif get_url_file_extension(url)==".txt":
                lines = text.split('\n')
                url_statistics.append(f"{len(lines)},{url.strip()}")
                for line in lines:
                    if  "#genre#" not in line and "," in line and "://" in line:
                        #channel_name=line.split(',')[0].strip()
                        #channel_address=line.split(',')[1].strip()
                        urls_all_lines.append(line.strip())
    
    except Exception as e:
        print(f"处理URL时发生错误：{e}")


# 去重复源 2024-08-06 (检测前剔除重复url，提高检测效率)
def remove_duplicates_url(lines):
    urls =[]
    newlines=[]
    for line in lines:
        if "," in line and "://" in line:
            # channel_name=line.split(',')[0].strip()
            channel_url=line.split(',')[1].strip()
            if channel_url not in urls: # 如果发现当前url不在清单中，则假如newlines
                urls.append(channel_url)
                newlines.append(line)
    return newlines

# 处理带$的URL，把$之后的内容都去掉（包括$也去掉） 【2024-08-08 22:29:11】
#def clean_url(url):
#    last_dollar_index = url.rfind('$')  # 安全起见找最后一个$处理
#    if last_dollar_index != -1:
#        return url[:last_dollar_index]
#    return url
def clean_url(lines):
    urls =[]
    newlines=[]
    for line in lines:
        if "," in line and "://" in line:
            last_dollar_index = line.rfind('$')
            if last_dollar_index != -1:
                line=line[:last_dollar_index]
            newlines.append(line)
    return newlines

# 处理带#的URL  【2024-08-09 23:53:26】
def split_url(lines):
    newlines=[]
    for line in lines:
        # 拆分成频道名和URL部分
        channel_name, channel_address = line.split(',', 1)
        #需要加处理带#号源=予加速源
        if  "#" not in channel_address:
            newlines.append(line)
        elif  "#" in channel_address and "://" in channel_address: 
            # 如果有“#”号，则根据“#”号分隔
            url_list = channel_address.split('#')
            for url in url_list:
                if "://" in url: 
                    newline=f'{channel_name},{url}'
                    newlines.append(line)
    return newlines

# 取得host
def get_host_from_url(url: str) -> str:
    try:
        parsed_url = urlparse(url)
        return parsed_url.netloc
    except Exception as e:
        return f"Error: {str(e)}"

# 使用字典来统计blackhost的记录次数
blacklist_dict = {}
def record_host(host):
    # 如果 host 已经在字典中，计数加 1
    if host in blacklist_dict:
        blacklist_dict[host] += 1
    # 如果 host 不在字典中，加入并初始化计数为 1
    else:
        blacklist_dict[host] = 1


if __name__ == "__main__":
    # 定义要访问的多个URL
    urls = [
        "http://156.238.251.122:888/live/live_Lite.txt",
            "https://raw.githubusercontent.com/xmbjm/IPTV/refs/heads/master/output/user_result.txt",
    "https://raw.githubusercontent.com/Guovin/iptv-api/refs/heads/master/output/result.txt",
        "http://156.238.251.122:7000", 
   
    "https://156.238.251.122:888/live/dalao/iptv-Kimentanm.m3u",
    "https://gitee.com/mytv-android/iptv-api/raw/master/output/result.m3u", 
    "https://raw.githubusercontent.com/n3rddd/CTVLive/master/live.m3u",
    "https://raw.githubusercontent.com/zwc456baby/iptv_alive/master/live.m3u", 
    "https://raw.githubusercontent.com/hero1898/tv/refs/heads/main/IPTV.m3u"

 
    ]
    for url in urls:
        print(f"处理URL: {url}")
        process_url(url)   #读取上面url清单中直播源存入urls_all_lines

    # 获取当前脚本所在的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 获取上一层目录
    parent_dir = os.path.dirname(current_dir)
    # 获取再上一层目录
    #parent2_dir = os.path.dirname(parent_dir)
    # # 获取根目录
    # root_dir = os.path.abspath(os.sep)  

    #input_file1 = os.path.join(parent_dir, 'live.txt')  # 输入文件路径1
    input_file1 = os.path.join(current_dir, 'live.txt')  # 输入文件路径1
    input_file2 = os.path.join(current_dir, 'blacklist_auto.txt')  # 输入文件路径2
    #input_file2 = os.path.join(current_dir, 'live_test.txt')  # 输入文件路径2 
    success_file = os.path.join(current_dir, 'whitelist_auto.txt')  # 成功清单文件路径
    success_file_tv = os.path.join(current_dir, 'whitelist_auto_tv.txt')  # 成功清单文件路径（另存一份直接引用源）
    blacklist_file = os.path.join(current_dir, 'blacklist_auto.txt')  # 黑名单文件路径

    # 读取输入文件内容
    lines1 = read_txt_file(input_file1)
    lines2 = read_txt_file(input_file2)
    lines=urls_all_lines + lines1 + lines2 # 从list变成集合提供检索效率⇒发现用了set后加#合并多行url，故去掉
    #lines=urls_all_lines  # Test
    
    # 计算合并后合计个数
    urls_hj_before = len(lines)

    # 分级带#号直播源地址
    lines=split_url(lines)
    urls_hj_before2 = len(lines)

    # 去$
    lines=clean_url(lines)
    urls_hj_before3 = len(lines)

    # 去重
    lines=remove_duplicates_url(lines)
    urls_hj = len(lines)

    # 处理URL并生成成功清单和黑名单
    successlist, blacklist = process_urls_multithreaded(lines)
    
    # 给successlist, blacklist排序
    # 定义排序函数
    def successlist_sort_key(item):
        time_str = item.split(',')[0].replace('ms', '')
        return float(time_str)
    
    successlist=sorted(successlist, key=successlist_sort_key)
    blacklist=sorted(blacklist)

    # 计算check后ok和ng个数
    urls_ok = len(successlist)
    urls_ng = len(blacklist)

    # 把successlist整理一下，生成一个可以直接引用的源，方便用zyplayer手动check
    def remove_prefix_from_lines(lines):
        result = []
        for line in lines:
            if  "#genre#" not in line and "," in line and "://" in line:
                parts = line.split(",")
                result.append(",".join(parts[1:]))
        return result


    # 加时间戳等
    version=datetime.now().strftime("%Y%m%d-%H-%M-%S")+",url"
    successlist_tv = ["更新时间,#genre#"] +[version] + ['\n'] +\
                  ["whitelist,#genre#"] + remove_prefix_from_lines(successlist)
    successlist = ["更新时间,#genre#"] +[version] + ['\n'] +\
                  ["RespoTime,whitelist,#genre#"] + successlist
    blacklist = ["更新时间,#genre#"] +[version] + ['\n'] +\
                ["blacklist,#genre#"]  + blacklist

    # 写入成功清单文件
    write_list(success_file, successlist)
    write_list(success_file_tv, successlist_tv)

    # 写入黑名单文件
    write_list(blacklist_file, blacklist)

    print(f"成功清单文件已生成: {success_file}")
    print(f"成功清单文件已生成(tv): {success_file_tv}")
    print(f"黑名单文件已生成: {blacklist_file}")

    # 写入history
    timenow=datetime.now().strftime("%Y%m%d_%H_%M_%S")
    history_success_file = f'history/blacklist/{timenow}_whitelist_auto.txt'
    history_blacklist_file = f'history/blacklist/{timenow}_blacklist_auto.txt'
    write_list(history_success_file, successlist)
    write_list(history_blacklist_file, blacklist)
    print(f"history成功清单文件已生成: {history_success_file}")
    print(f"history黑名单文件已生成: {history_blacklist_file}")

    # 执行的代码
    timeend = datetime.now()

    # 计算时间差
    elapsed_time = timeend - timestart
    total_seconds = elapsed_time.total_seconds()

    # 转换为分钟和秒
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)

    # 格式化开始和结束时间
    timestart_str = timestart.strftime("%Y%m%d_%H_%M_%S")
    timeend_str = timeend.strftime("%Y%m%d_%H_%M_%S")

    print(f"开始时间: {timestart_str}")
    print(f"结束时间: {timeend_str}")
    print(f"执行时间: {minutes} 分 {seconds} 秒")
    print(f"urls_hj最初: {urls_hj_before} ")
    print(f"urls_hj分解井号源后: {urls_hj_before2} ")
    print(f"urls_hj去$后: {urls_hj_before3} ")
    print(f"urls_hj去重后: {urls_hj} ")
    print(f"  urls_ok: {urls_ok} ")
    print(f"  urls_ng: {urls_ng} ")


# 确保路径存在
blackhost_dir = os.path.join(current_dir, "blackhost")
os.makedirs(blackhost_dir, exist_ok=True)

# 构造文件名
blackhost_filename = os.path.join(
    blackhost_dir,
    f"{datetime.now().strftime('%Y%m%d_%H_%M_%S')}_blackhost_count.txt"
)

# 将结果保存为 txt 文件 
def save_blackhost_to_txt(filename=blackhost_filename):
    with open(filename, "w") as file:
        for host, count in blacklist_dict.items():
            file.write(f"{host}失败次数是 {count}\n")
    print(f"结果已保存到 {filename}")

save_blackhost_to_txt()
            
for statistics in url_statistics: #查看各个url的量有多少 2024-08-19
    print(statistics)
    
