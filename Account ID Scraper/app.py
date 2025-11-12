from parsel import Selector
import requests
import json
import time
import json
import json
from datetime import datetime
def get_data(url):
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
        'sec-ch-ua-full-version-list': '"Google Chrome";v="141.0.7390.108", "Not?A_Brand";v="8.0.0.0", "Chromium";v="141.0.7390.108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
    }

    max_try = 3
    err_list = None
    response = None

    for i in range(max_try):
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            if resp.status_code == 200:
                response = resp
                break
            else:
                err_list = Exception(f"Non-200 status code: {resp.status_code}")
        except Exception as e:
            err_list = e
            time.sleep(1)

    if response is None:
        raise err_list if err_list else Exception("Request failed")

    selector = Selector(text=response.text)
    
    scripts = selector.css('script[type="application/json"][data-content-len]::text').getall()
    return scripts


urls = [
    "https://web.facebook.com/groups/547189093584341/",
    "https://www.facebook.com/groups/germtheory.vs.terraintheory/posts/5671657859577842/",
    "https://web.facebook.com/groups/bengaliintellectualsincommentsection",

    
]
import json
results = []
for url in urls:
    print(f"Processing: {url}")
    scripts = get_data(url)


    def contains_best_description(obj):
        """Recursively check if 'best_description' exists anywhere inside a JSON object"""
        if isinstance(obj, dict):
            if "focusCommentID" in obj:
                return True
            return any(contains_best_description(v) for v in obj.values())
        elif isinstance(obj, list):
            return any(contains_best_description(i) for i in obj)
        return False
    data = scripts


    parsed_data = []
    for item in data:
        if isinstance(item, str):
            try:
                parsed_data.append(json.loads(item))
            except json.JSONDecodeError:
                continue
        elif isinstance(item, dict):
            parsed_data.append(item)

    # Step 3: Filter only those that contain "best_description"
    filtered = [item for item in parsed_data if contains_best_description(item)]


    import json

    data = filtered


    def find_value(obj, target_path):
        """Recursive ফাংশন: nested JSON থেকে নির্দিষ্ট path খুঁজে বের করে"""
        if not target_path:
            return None

        key = target_path[0]

 
        if isinstance(obj, dict):
            if key in obj:
                if len(target_path) == 1:
                    return obj[key]
                return find_value(obj[key], target_path[1:])
            # অন্য value গুলোর মধ্যে খুঁজে দেখো
            for v in obj.values():
                result = find_value(v, target_path)
                if result is not None:
                    return result

        elif isinstance(obj, list):
            for item in obj:
                result = find_value(item, target_path)
                if result is not None:
                    return result

        return None


   
    path = [
        "initialRouteInfo",
        "route",
        "upsellConfig",
        "parent_container_id"
    ]

    parent_container_id = find_value(data, path)

    if parent_container_id:
        print(" ID:", parent_container_id)
    else:
        print(" ID not found.")

    # ===========================
    # 🔹 Process all URLs
    
    results.append({"input_url": url,
            "id": parent_container_id if parent_container_id else "Not Found"})

  
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)
