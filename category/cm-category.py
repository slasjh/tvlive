import urllib.request
from urllib.parse import urlparse
from datetime import datetime, timedelta, timezone
import re
import logging


#读取文本方法
def read_txt_to_array(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
            return lines
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []



def process_url(url):
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 ... Chrome/58.0 ...')
        with urllib.request.urlopen(req) as response:
            text = response.read().decode('utf-8')
            lines = text.split('\n')
            print(f"行数: {len(lines)}")
            is_m3u = any("#EXTINF" in line for line in lines[:15])
            source_type = "m3u" if is_m3u else "txt"
            logging.info(f"url: {url} 获取成功，判断为{source_type}格式")
            
            if is_m3u:
                for line in lines:
                    line = line.strip()
                    if line.startswith("#EXTINF"):
                        match = re.search(r'group-title="(.*?)",(.*)', line)
                        if match:
                            channel_name = match.group(2).strip()
                    elif line and not line.startswith("#"):
                        channel_url = line.strip()
                        all_lines.append(f"{channel_name},{channel_url}")  # 添加由逗号分隔的字符串
                        #all_lines.append((channel_name, channel_url))
            else:
                for line in lines:
                    line = line.strip()
                    if "#genre#" not in line and "," in line and "://" in line:
                        all_lines.append(line)
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




def tiqu_gjz(output_file, feilei, gjz_or_gjzs):
    try:
        # 假设all_lines是从某个地方获取的文本行列表
        # 这里为了示例，我们将其硬编码在函数内部
        #all_lines = [
            #"这是一行测试文本。",
            #"包含chinamobile.com的文本行：http://www.chinamobile.com/something",
            #"另一行包含migu的文本：http://example.com/migu.php",
            #"还有一行包含mg的文本：http://example.com/mg.php",
            #"以及一行不包含目标网址的文本。"
        #]

        # 如果gjz_or_gjzs是字符串，则将其转换为单元素集合以便统一处理
        if isinstance(gjz_or_gjzs, str):
            gjz_set = {gjz_or_gjzs}
        else:
            gjz_set = set(gjz_or_gjzs)

        with open(output_file, 'w', encoding='utf-8') as f:
            # 注意：这里我们不再写入gjz_or_gjzs到文件，因为它可能是多个值
            # 如果您确实需要写入某种标识符，请考虑使用feilei参数
            f.write(f'{feilei},#genre#\n')  # 使用f-string格式化字符串并写入分类信息
            for line in all_lines:
                if any(gjz in line for gjz in gjz_set):
                    f.write(line + '\n')

        print(f"合并后的文本已保存到文件: {output_file}")
        #print("time: {}".format(datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S")))

    except Exception as e:
        print(f"保存文件时发生错误：{e}")
        
def tiqu_gjz_juhe3(output_file, feilei, gjz_or_gjzs1,gjz_or_gjzs2,gjz_or_gjzs3):
    try:
        # 如果gjz_or_gjzs是字符串，则将其转换为单元素集合以便统一处理
        if isinstance(gjz_or_gjzs1, str):
            gjz_set1 = {gjz_or_gjzs1}
        else:
            gjz_set1 = set(gjz_or_gjzs1)
        if isinstance(gjz_or_gjzs2, str):
            gjz_set2 = {gjz_or_gjzs2}
        else:
            gjz_set2 = set(gjz_or_gjzs2)
        if isinstance(gjz_or_gjzs3, str):
            gjz_set3 = {gjz_or_gjzs3}
        else:
            gjz_set3 = set(gjz_or_gjzs3)  

        with open(output_file, 'w', encoding='utf-8') as f:
            # 注意：这里我们不再写入gjz_or_gjzs到文件，因为它可能是多个值
            # 如果您确实需要写入某种标识符，请考虑使用feilei参数
            f.write(f'{feilei},#genre#\n')  # 使用f-string格式化字符串并写入分类信息
            for line in all_lines:
                if any(gjz in line for gjz in gjz_set1):
                    if any(gjz in line for gjz in gjz_set2):    
                        if any(gjz in line for gjz in gjz_set3):    
                            f.write(line + '\n')

        print(f"合并后的文本已保存到文件: {output_file}")
        #print("time: {}".format(datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S")))

    except Exception as e:
        print(f"保存文件时发生错误：{e}")
        
def tiqu_gjz_juhe2(output_file, feilei, gjz_or_gjzs1,gjz_or_gjzs2):
    try:
        # 如果gjz_or_gjzs是字符串，则将其转换为单元素集合以便统一处理
        if isinstance(gjz_or_gjzs1, str):
            gjz_set1 = {gjz_or_gjzs1}
        else:
            gjz_set1 = set(gjz_or_gjzs1)
        if isinstance(gjz_or_gjzs2, str):
            gjz_set2 = {gjz_or_gjzs2}
        else:
            gjz_set2 = set(gjz_or_gjzs2)

        with open(output_file, 'w', encoding='utf-8') as f:
            # 注意：这里我们不再写入gjz_or_gjzs到文件，因为它可能是多个值
            # 如果您确实需要写入某种标识符，请考虑使用feilei参数
            f.write(f'{feilei},#genre#\n')  # 使用f-string格式化字符串并写入分类信息
            for line in all_lines:
                if any(gjz in line for gjz in gjz_set1):
                    if any(gjz in line for gjz in gjz_set2):    
                        f.write(line + '\n')

        print(f"合并后的文本已保存到文件: {output_file}")
        #print("time: {}".format(datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S")))

    except Exception as e:
        print(f"保存文件时发生错误：{e}")
        

all_lines =  []
#读取文本
excudelist_lines=read_txt_to_array('category/ExcludeList.txt') 
# 定义
urls = [

      "https://raw.githubusercontent.com/Guovin/iptv-api/refs/heads/master/output/result.txt",
    "https://raw.githubusercontent.com/xmbjm/IPTV/refs/heads/master/output/user_result.txt",
        "http://156.238.251.122:7000",
    "https://live.zbds.top/tv/iptv4.txt"
    "https://live.zhoujie218.top/tv/iptv4.m3u", #ADDED BY lee  ON 2025/2/19
     "http://156.238.251.122:888/live/live_Lite.txt",
    "https://raw.githubusercontent.com/zwc456baby/iptv_alive/master/live.m3u", 
    "https://raw.githubusercontent.com/hero1898/tv/refs/heads/main/IPTV.m3u"

]
# 处理
for url in urls:
    if url.startswith("http"):        
        # print(f"time: {datetime.now().strftime("%Y%m%d_%H_%M_%S")}")
        print(f"处理URL: {url}")
        process_url(url)
# 分级带#号直播源地址
all_lines=split_url(all_lines)
# 去$
all_lines=clean_url(all_lines)
# 去重
all_lines=remove_duplicates_url(all_lines)
# 将合并后的文本写入文件
output_file1 = "category/cm.txt"
feilei1 = "移动CM"
#gjz1 = ".chinamobile.com"
gjz1 = [".chinamobile.com", "channel-id=bestzb", "channel-id=ystenlive"]  # 使用列表来存储多个关键字

output_file2 = "category/ottrrs.hl.chinamobile.com.txt"
feilei2 = "ottrrs.hl.chinamobile"
gjz2 = ["http://ottrrs.hl.chinamobile.com"]  # 使用列表来存储多个关键字

output_file3 = "category/php.jdshipin.com.txt"
feilei3 = "jdshipin"
gjz3 = ["php.jdshipin.com"]  # 使用列表来存储多个关键字

output_file4 = "category/iptv.666230.xyz.txt"
feilei4 = "666230.xyz"
gjz4 = ["iptv.666230.xyz"]  # 使用列表来存储多个关键字

output_file6 = "category/child.txt"
feilei6 = "少儿分类"
gjz6 = ["儿童", "少儿", "动漫","卡通","动画"]  # 使用列表来存储多个关键字

output_file7 = "category/cctv.txt"
feilei7 = "cctv分类"
gjz7 = ["CCTV", "cctv", "中央电视","央视"]  # 使用列表来存储多个关键字

output_file8 = "category/weishi.txt"
feilei8 = "卫视分类"
gjz8 = ["卫视", "衛視"]  # 使用列表来存储多个关键字

output_file9 = "category/hongkong.txt"
feilei9 = "凤凰分类"
gjz9 = ["凤凰", "翡翠", "TVB","香港"]  # 使用列表来存储多个关键字


output_file21 = "category/cm&cctv.txt"
feilei21 = "cm&cctv分类"
output_file22 = "category/cm&卫士.txt"
feilei22 = "cm&卫士分类"

output_file23 = "category/cm&凤凰.txt"
feilei23 = "cm&凤凰分类"

output_file24 = "category/cm&少儿.txt"
feilei24 = "cm&少儿分类"

# 调用函数示例，注意现在第三个参数对于第二个文件是一个列表
tiqu_gjz(output_file1, feilei1, gjz1)
tiqu_gjz(output_file2, feilei2, gjz2)
tiqu_gjz(output_file3, feilei3, gjz3)
tiqu_gjz(output_file4, feilei4, gjz4)

tiqu_gjz(output_file6, feilei6, gjz6)
tiqu_gjz(output_file7, feilei7, gjz7)
tiqu_gjz(output_file8, feilei8, gjz8)
tiqu_gjz(output_file9, feilei8, gjz9)


tiqu_gjz_juhe2(output_file21, feilei21, gjz1,gjz7) 
tiqu_gjz_juhe2(output_file22, feilei22, gjz1,gjz8) 

tiqu_gjz_juhe2(output_file23, feilei23, gjz1,gjz9) 
tiqu_gjz_juhe2(output_file24, feilei24, gjz1,gjz6) 
 
