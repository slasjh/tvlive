import requests
import time
import json
import re
import os
from datetime import datetime

fail_output = []

def remove_single_line_comments(json_str):

    # 使用正则表达式匹配并移除以 //  开头单行注释

    cleaned_json_str = re.sub(r'//.*', '', json_str, flags=re.MULTILINE)

    return cleaned_json_str


def fetch_and_sites_json(url):

    try:

        response = requests.get(url, timeout=10)

        response.raise_for_status()

        try:

            # 尝试直接解析JSON

            return response.json()

        except json.JSONDecodeError:

            # 如果解析失败，尝试移除注释后重新解析

            cleaned_text = remove_single_line_comments(response.text)

            try:

                return json.loads(cleaned_text)

            except json.JSONDecodeError as e:

                # 如果移除注释后仍然无法解析，抛出异常或进行其他处理

                print(f"移除注释后仍然无法解析JSON: {e}")

                raise  # 可以选择重新抛出异常，或者返回None等其他处理方式

    except Exception as e:

        print(f"此接口 {url} 请求JSON数据失败: {str(e)}")

        fail_message = f"此接口 {url} 请求JSON数据失败: {str(e)} \n"

        fail_output.append(fail_message)

        return None

def extract_sites_urls(json_data, source_url):
    urls = []
    if "sites" in json_data:
        for site in json_data["sites"]:
            url = site.get("api", "")
            if url.startswith(("http://", "https://")):
                urls.append({"source": source_url, "url": url})
    return urls

def speed_test(url, test_times=3):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    total_time = 0
    success_count = 0
    
    for _ in range(test_times):
        try:
            # 构造测试URL（附加测试视频地址）
            test_url = url 
            start = time.time()
            response = requests.head(
                test_url, 
                headers=headers, 
                timeout=5, 
                allow_redirects=True
            )
            latency = (time.time() - start) * 1000  # 毫秒
            if response.status_code in [200, 302, 301]:
                total_time += latency
                success_count += 1
        except Exception as e:
            print(f"测速失败 {url}: {str(e)}")
            fail_message = f"测速失败 {url}: {str(e)}\n"  # 添加换行符以便每行一个错误信息
            fail_output.append(fail_message)  # 将错误信息添加到列表中
    
    if success_count == 0:

        return None
    
    return {
        "url": url,
        "avg_latency": round(total_time / success_count, 2),
        "success_rate": round(success_count / test_times * 100, 1)
    }

def main():
    json_urls = [
        #"https://raw.githubusercontent.com/slasjh/18/refs/heads/main/XX/xingfu.json",
        "http://116.62.139.149:3000/slasjh/xingfu/raw/branch/main/xingfu.json",
        # 可以添加更多JSON URL
    ]

    sites_urls = []

    for json_url in json_urls:
        json_data = fetch_and_sites_json(json_url)
        if json_data:
           sites_urls.extend(extract_sites_urls(json_data, json_url))

    if not sites_urls:
        print("未找到有效的url")
        return

    print("\n开始测速...")
    results = []
    for item in sites_urls:
        source_url, url = item["source"], item["url"]
        print(f"正在测试 {url}（来自 {source_url}）...")
        result = speed_test(url)
        if result:
            result["source"] = source_url  # 记录来源
            results.append(result)

    # 准备写入文件的内容
    output_lines = []
    output_lines.append(f"找到 {len(sites_urls)} 个解析地址:\n")
    for idx, item in enumerate(sites_urls, 1):
        source_url, url = item["source"], item["url"]
        output_lines.append(f"{idx}. {url}（来自 {source_url}）\n")

    output_lines.append("\n测速结果（按延迟排序）：\n")
    for idx, res in enumerate(sorted(results, key=lambda x: x["avg_latency"]), 1):
        output_lines.append(f"{idx}. {res['url']}（来自 {res['source']}）\n")
        output_lines.append(f"  平均延迟: {res['avg_latency']}ms | 成功率: {res['success_rate']}%\n")
        output_lines.append("-" * 50 + "\n")
       # 获取当前脚本所在的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 获取上一层目录
    parent_dir = os.path.dirname(current_dir)
    # 获取再上一层目录
    #parent2_dir = os.path.dirname(parent_dir)
    # # 获取根目录
    # root_dir = os.path.abspath(os.sep)  

    x_results = os.path.join(current_dir, 'x_results.txt')  # 输入文件路径1
    fail_result = os.path.join(current_dir, f"{datetime.now().strftime('%Y%m%d_%H_%M_%S')}_fail_result.txt.txt")  # 输入文件路径1
    with open(x_results, "w", encoding="utf-8") as f:
        f.writelines(output_lines)
  
    print("测速结果已保存到 x_results.txt文件中。")
    # 如果所有测试都失败了，可以选择在这里写入文件或返回None
    with open(fail_result, "a", encoding="utf-8") as f:
            f.writelines(fail_output)
    print("fail结果已保存到 fail_result.txt文件中。")

if __name__ == "__main__":
    main()

