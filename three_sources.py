import re
import requests
import logging
from collections import OrderedDict, defaultdict
from datetime import datetime
import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.FileHandler("function.log", "w", encoding="utf-8"), logging.StreamHandler()])

def parse_template(template_file):
    template_channels = OrderedDict()
    current_category = None

    with open(template_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                if "#genre#" in line:
                    current_category = line.split(",")[0].strip()
                    template_channels[current_category] = []
                elif current_category:
                    channel_name = line.split(",")[0].strip()
                    template_channels[current_category].append(channel_name)

    return template_channels

def parse_corrections(correction_file):
    corrections = {}

    with open(correction_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                parts = line.split(",")
                unified_name = parts[0].strip()
                for alias in parts[1:]:
                    corrections[alias.strip()] = unified_name

    return corrections

def fetch_channels(url, corrections):
    channels = OrderedDict()
    no_category = "无分类"

    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'utf-8'
        lines = response.text.split("\n")
        current_category = None
        is_m3u = any("#EXTM3U" in line for line in lines[:15]) and any("#EXTINF" in line for line in lines[:15])
        is_txt = any("#genre#" in line for line in lines if line.strip())

        if is_m3u:
            logging.info(f"url: {url} 获取成功，判断为标准的M3U格式")
            for line in lines:
                line = line.strip()
                if line.startswith("#EXTINF"):
                    match = re.search(r'group-title="(.*?)",(.*)', line)
                    if match:
                        current_category = match.group(1).strip()
                        channel_name = match.group(2).strip()
                        channel_name = corrections.get(channel_name, channel_name)
                        if current_category not in channels:
                            channels[current_category] = []
                elif line and not line.startswith("#"):
                    channel_url = line.strip()
                    if current_category and channel_name:
                        channels[current_category].append((channel_name, channel_url))

        if is_txt:
            logging.info(f"url: {url} 获取成功，判断为标准的TXT格式")
            for line in lines:
                line = line.strip()
                if "#genre#" in line:
                    current_category = line.split(",")[0].strip()
                    channels[current_category] = []
                elif current_category:
                    match = re.match(r"^(.*?),(.*?)$", line)
                    if match:
                        channel_name = match.group(1).strip()
                        channel_url = match.group(2).strip()
                        channel_name = corrections.get(channel_name, channel_name)
                        channels[current_category].append((channel_name, channel_url))
                    elif line:
                        channel_name = line.strip()
                        channel_name = corrections.get(channel_name, channel_name)
                        channels[current_category].append((channel_name, ''))
        else:
            logging.info(f"url: {url} 识别为非标准格式，将使用默认分类“{no_category}”")

            for line in lines:
                line = line.strip()
                if line:  # 确保行不为空
                    match = re.match(r"^(.*?),(.*?)$", line)  # 假设每行都是"name, url"格式
                    if match:
                        channel_name = match.group(1).strip()
                        channel_url = match.group(2).strip()
                        channel_name = corrections.get(channel_name, channel_name)
                        if no_category not in channels:
                            channels[no_category] = []
                        channels[no_category].append((channel_name, channel_url))
                    else:
                        logging.warning(f"url: {url} 中有无法解析的行: {line}")

        if channels:
            categories = ", ".join(channels.keys())
            logging.info(f"url: {url} 爬取成功✅，包含频道分类: {categories}")
    except requests.RequestException as e:
        logging.error(f"url: {url} 爬取失败❌, Error: {e}")

    return channels

def match_channels(template_channels, all_channels, url_sources):
    matched_channels = OrderedDict()

    for category, channel_list in template_channels.items():
        matched_channels[category] = OrderedDict()
        for channel_name in channel_list:
            channel_urls = defaultdict(list)  # 存储每个URL的出现次数统计
            
            # 统计每个URL在不同订阅源中的出现情况
            for online_category, online_channel_list in all_channels.items():
                for online_channel_name, online_channel_url in online_channel_list:
                    if channel_name == online_channel_name and online_channel_url:
                        # 记录这个URL来自哪个订阅源
                        channel_urls[online_channel_url].append(online_category)
            
            # 只保留在至少3个订阅源中都出现的URL
            filtered_urls = []
            for url, sources in channel_urls.items():
                # 统计不同来源的数量（去重）
                unique_sources = set(sources)
                if len(unique_sources) >= 3:
                    filtered_urls.append((channel_name, url))
                    logging.info(f"频道 {channel_name} 的URL {url} 在 {len(unique_sources)} 个订阅源中出现: {unique_sources}")
                else:
                    logging.debug(f"频道 {channel_name} 的URL {url} 仅在 {len(unique_sources)} 个订阅源中出现，已过滤")
            
            if filtered_urls:
                matched_channels[category][channel_name] = filtered_urls

    return matched_channels

def filter_source_urls(template_file, correction_file):
    template_channels = parse_template(template_file)
    corrections = parse_corrections(correction_file)
    source_urls = config.source_urls

    all_channels = OrderedDict()
    url_sources = defaultdict(set)  # 记录每个URL来自哪些订阅源
    
    for source_index, url in enumerate(source_urls):
        fetched_channels = fetch_channels(url, corrections)
        for category, channel_list in fetched_channels.items():
            if category in all_channels:
                all_channels[category].extend(channel_list)
            else:
                all_channels[category] = channel_list
            
            # 记录每个URL的来源
            for channel_name, channel_url in channel_list:
                if channel_url:
                    url_sources[(channel_name, channel_url)].add(f"Source_{source_index+1}")

    matched_channels = match_channels(template_channels, all_channels, url_sources)

    # 统计信息
    total_matched = sum(len(channels) for channels in matched_channels.values())
    total_urls = sum(len(urls) for category in matched_channels.values() for urls in category.values())
    logging.info(f"匹配完成✅，共匹配到 {total_matched} 个频道，{total_urls} 个URL（仅保留在至少3个订阅源中都出现的URL）")

    return matched_channels, template_channels

def is_ipv6(url):
    return re.match(r'^http:\/\/\[[0-9a-fA-F:]+\]', url) is not None

def updateChannelUrlsM3U(channels, template_channels):
    written_urls = set()

    current_date = datetime.now().strftime("%Y-%m-%d")
    for group in config.announcements:
        for announcement in group['entries']:
            if announcement['name'] is None:
                announcement['name'] = current_date

    with open("live.m3u", "w", encoding="utf-8") as f_m3u:
        f_m3u.write(f"""#EXTM3U x-tvg-url={",".join(f'"{epg_url}"' for epg_url in config.epg_urls)}\n""")

        with open("live.txt", "w", encoding="utf-8") as f_txt:
            for group in config.announcements:
                f_txt.write(f"{group['channel']},#genre#\n")
                for announcement in group['entries']:
                    f_m3u.write(f"""#EXTINF:-1 tvg-id="1" tvg-name="{announcement['name']}" tvg-logo="{announcement['logo']}" group-title="{group['channel']}",{announcement['name']}\n""")
                    f_m3u.write(f"{announcement['url']}\n")
                    f_txt.write(f"{announcement['name']},{announcement['url']}\n")

            for category, channel_list in template_channels.items():
                f_txt.write(f"{category},#genre#\n")
                if category in channels:
                    for channel_name in channel_list:
                        if channel_name in channels[category]:
                            # 去重逻辑
                            unique_urls = list(OrderedDict.fromkeys([url for _, url in channels[category][channel_name]]))
                            #sorted_urls = sorted(unique_urls, key=lambda url: not is_ipv6(url) if config.ip_version_priority == "ipv6" else is_ipv6(url))
                            sorted_urls = unique_urls       
                            filtered_urls = [url for url in sorted_urls if not is_ipv6(url) and url not in written_urls and not any(blacklist in url for blacklist in config.url_blacklist)]

                            # 保证数字连续
                            index = 1
                            for url in filtered_urls:
                                url_suffix = f"$小土豆•IPV4" if len(filtered_urls) == 1 else f"$小土豆•IPV4『线路{index}』"
                                if '$' in url:
                                    base_url = url.split('$', 1)[0]
                                else:
                                    base_url = url

                                new_url = f"{base_url}{url_suffix}"

                                if base_url not in written_urls:
                                    f_m3u.write(f"#EXTINF:-1 tvg-id=\"{index}\" tvg-name=\"{channel_name}\" tvg-logo=\"https://gitee.com/n3rddd/tvlogos/raw/main/logo/{channel_name}.png\" group-title=\"{category}\",{channel_name}\n")
                                    f_m3u.write(new_url + "\n")
                                    f_txt.write(f"{channel_name},{new_url}\n")
                                    written_urls.add(base_url)
                                    index += 1

            f_txt.write("\n")

if __name__ == "__main__":
    template_file = "demo.txt"
    correction_file = "correction.txt"
    channels, template_channels = filter_source_urls(template_file, correction_file)
    updateChannelUrlsM3U(channels, template_channels)
