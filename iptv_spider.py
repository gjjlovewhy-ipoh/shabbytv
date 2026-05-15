import requests
import re

# 源地址
SOURCE_URL = "https://iptv-org.github.io/iptv/index.m3u"

# 分组关键词
rule = {
    "央视": ["CCTV", "中央", "央视"],
    "卫视": ["卫视", "湖南", "浙江", "江苏", "东方", "北京", "广东", "深圳"],
    "地方": ["都市", "影视", "娱乐", "睛彩", "移动", "生活", "新闻"]
}

def get_iptv():
    res = requests.get(SOURCE_URL, timeout=20)
    res.encoding = "utf-8"
    lines = res.text.splitlines()

    yangshi = []
    weishi = []
    difang = []
    other = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if not line.startswith("http"):
            continue
        # 只保留含中文的频道
        if not re.search(r"[\u4e00-\u9fff]", line):
            continue

        # 分类
        if any(k in line for k in rule["央视"]):
            yangshi.append(line)
        elif any(k in line for k in rule["卫视"]):
            weishi.append(line)
        elif any(k in line for k in rule["地方"]):
            difang.append(line)
        else:
            other.append(line)

    # 按你要的格式组装
    out = []
    out.append("央视,#genre#")
    out.extend(yangshi)
    out.append("卫视,#genre#")
    out.extend(weishi)
    out.append("地方,#genre#")
    out.extend(other)
    out.append("其他,#genre#")
    out.extend(other)

    # 写入txt
    with open("iptv.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))

if __name__ == "__main__":
    get_iptv()
