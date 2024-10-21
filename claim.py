import requests
import time

# 读取代理列表
def load_proxies(file_path):
    with open(file_path, 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies

# 解析代理字符串
def parse_proxy(proxy_string):
    try:
        parts = proxy_string.split(':')
        if len(parts) == 4:
            server, port, username, password = parts
            return f"http://{username}:{password}@{server}:{port}"
        else:
            raise ValueError("Invalid proxy format")
    except Exception as e:
        print(f"Failed to parse proxy: {proxy_string} - {e}")
        return None

# 发送请求领取测试币
def request_test_coins(proxy, recipient_address):
    url = "https://faucet.testnet.sui.io/v1/gas"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,fr;q=0.7",
        "content-type": "application/json",
        "origin": "https://faucet.blockbolt.io",
        "referer": "https://faucet.blockbolt.io/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }
    payload = {
        "FixedAmountRequest": {
            "recipient": recipient_address
        }
    }
    parsed_proxy = parse_proxy(proxy)
    if not parsed_proxy:
        return

    proxies = {
        "http": parsed_proxy,
        "https": parsed_proxy
    }
    try:
        response = requests.post(url, json=payload, headers=headers, proxies=proxies)
        if response.status_code == 202:
            print(f"Success: {proxy} - Test coins received for {recipient_address}")
        else:
            print(f"Failed: {proxy} - Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error with proxy {proxy}: {e}")

# 主函数
def main():
    recipient_address = "0x6ba6f04a2564b48047ab27d88ccdf4097acf1147f6f3503xxxxxxxxxxxxxxxxxx"
    
    # 读取代理列表
    proxies = load_proxies("proxies.txt")
    
    # 使用每个代理请求测试币
    for proxy in proxies:
        request_test_coins(proxy, recipient_address)
        # time.sleep(1)  # 添加1秒延时

if __name__ == "__main__":
    main()
