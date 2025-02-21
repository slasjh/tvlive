import requests
import time
import json

def fetch_and_sites_json(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        try:
            return response.json()
        except json.JSONDecodeError:
            raw_text = response.text.replace("'", '"')
            return json.loads(raw_text)
    except Exception as e:
        print(f"此接口 {url}请求JSON数据失败: {str(e)}")
        fail_message = f"此接口 {url}请求JSON数据失败: {str(e)} \n"  # 添加换行符以便每行一个错误信息
        fail_output.append(fail_message)  # 将错误信息添加到列表中
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
        "https://raw.githubusercontent.com/slasjh/18/refs/heads/main/XX/xingfu.json",
        #"http://156.238.251.122:888/jx/parses.json",
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

    with open("x_speed_results.txt", "w", encoding="utf-8") as f:
        f.writelines(output_lines)
  
    print("测速结果已保存到 x_speed_results.txt文件中。")
    fail_output = []
                # 如果所有测试都失败了，可以选择在这里写入文件或返回None
  
    with open("fail_output.txt", "a", encoding="utf-8") as f:
            f.writelines(fail_output)

if __name__ == "__main__":
    main()
