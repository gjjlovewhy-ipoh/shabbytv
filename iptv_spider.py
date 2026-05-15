import requests
import re

SOURCE_URL = "https://iptv-org.github.io/iptv/index.m3u"

# 分组关键词
CCTV_KEYS = {"CCTV","中央","央视"}
WEISHI_KEYS = {"卫视","湖南","浙江","江苏","东方","北京","广东","深圳","安徽","山东","湖北","四川"}
DIFANG_KEYS = {"都市","影视","娱乐","新闻","生活","综合","文旅","教科","经视"}

def main():
    resp = requests.get(SOURCE_URL, timeout=30)
    resp.encoding = "utf-8"
    lines = resp.text.splitlines()

    cctv_list = []
    ws_list = []
    df_list = []
    other_list = []

    name = ""
    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF"):
            # 提取频道名称
            m = re.search(r',(.+)$', line)
            if m:
                name = m.group(1).strip()
            continue
        # 匹配播放地址
        if line.startswith("http"):
            url = line
            # 过滤无中文的频道
            if not re.search(r'[\u4e00-\u9fff]', name):
                name = ""
                continue
            
            # 分类
            if any(k in name for k in CCTV_KEYS):
                cctv_list.append(f"{name},{url}")
            elif any(k in name for k in WEISHI_KEYS):
                ws_list.append(f"{name},{url}")
            elif any(k in name for k in DIFANG_KEYS):
                df_list.append(f"{name},{url}")
            else:
                other_list.append(f"{name},{url}")
            name = ""

    # 组装成你要的 #genre# 格式
    out = []
    out.append("央视,#genre#")
    out.extend([item.split(',')[1] for item in cctv_list])
    
    out.append("卫视,#genre#")
    out.extend([item.split(',')[1] for item in ws_list])
    
    out.append("地方,#genre#")
    out.extend([item.split(',')[1] for item in df_list])
    
    out.append("其他,#genre#")
    out.extend([item.split(',')[1] for item in other_list])

    with open("iptv.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out))

if __name__ == "__main__":
    main()
