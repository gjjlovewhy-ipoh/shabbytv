import requests
import re

SOURCE_URL = "https://iptv-org.github.io/iptv/index.m3u"

# 扩充最全关键词，保证央视、卫视全部识别
CCTV_KEYS = [
    "CCTV", "中央", "央视", "CCTV-1", "CCTV-2", "CCTV-3", "CCTV-4",
    "CCTV-5", "CCTV-6", "CCTV-7", "CCTV-8", "CCTV-9", "CCTV-10"
]
WEISHI_KEYS = [
    "卫视", "湖南", "浙江", "江苏", "东方", "北京", "广东", "深圳",
    "安徽", "山东", "湖北", "四川", "重庆", "天津", "江西", "福建"
]
DIFANG_KEYS = [
    "都市", "影视", "娱乐", "新闻", "生活", "综合", "文旅",
    "教科", "经视", "城市", "本地", "频道"
]

def has_chinese(text):
    return re.search(r'[\u4e00-\u9fff]', text)

def main():
    resp = requests.get(SOURCE_URL, timeout=30)
    resp.encoding = "utf-8"
    lines = resp.text.splitlines()

    cctv = []
    weishi = []
    difang = []
    other = []

    curr_name = ""

    for line in lines:
        line = line.strip()
        # 解析频道名称
        if line.startswith("#EXTINF"):
            mat = re.search(r',\s*(.+?)\s*$', line)
            if mat:
                curr_name = mat.group(1).strip()
            continue
        
        # 播放地址行
        if line.startswith(("http://", "https://")):
            url = line
            # 过滤无中文频道
            if not has_chinese(curr_name):
                curr_name = ""
                continue

            # 开始分类
            name_low = curr_name
            if any(k in name_low for k in CCTV_KEYS):
                cctv.append(f"{curr_name},{url}")
            elif any(k in name_low for k in WEISHI_KEYS):
                weishi.append(f"{curr_name},{url}")
            elif any(k in name_low for k in DIFANG_KEYS):
                difang.append(f"{curr_name},{url}")
            else:
                other.append(f"{curr_name},{url}")
            curr_name = ""

    # 生成你要的标准格式：分组,#genre# + 每行 频道名,url
    out = []
    out.append("央视,#genre#")
    out.extend(cctv)

    out.append("卫视,#genre#")
    out.extend(weishi)

    out.append("地方,#genre#")
    out.extend(difang)

    out.append("其他,#genre#")
    out.extend(other)

    # 写入文件
    with open("iptv.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    print(f"完成：央视{len(cctv)} 卫视{len(weishi)} 地方{len(difang)} 其他{len(other)}")

if __name__ == "__main__":
    main()
