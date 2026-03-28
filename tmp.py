
import html
import os
import json


#apks = [apk for apk in os.listdir("apk")]
apks = set([    
    "tachiyomi-all.ehentai-v1.4.27.apk",
    "tachiyomi-all.hitomi-v1.4.41.apk",
    "tachiyomi-all.nhentai-v1.4.56.apk",
    "tachiyomi-all.pururin-v1.4.10.apk",
    "tachiyomi-en.hentai20-v1.4.39.apk",
    "tachiyomi-en.hentai2read-v1.4.18.apk"
])

index = json.load(open("index.json", "r"))

for i in index:
    if i["apk"] in apks:
        print(i["apk"])
        index.remove(i)
        

        
json.dump(index, open("index.json", "w"), ensure_ascii=False, indent=2)

for item in index:
    for source in item["sources"]:
        source.pop("versionId", None)
        
json.dump(index, open("index.min.json", "w"), ensure_ascii=False, separators=(",", ":"))

with open("index.html", "w", encoding="utf-8") as index_html_file:
    index_html_file.write('<!DOCTYPE html>\n<html>\n<head>\n<meta charset="UTF-8">\n<title>apks</title>\n</head>\n<body>\n<pre>\n')
    for entry in index:
        apk_escaped = 'apk/' + html.escape(entry["apk"])
        name_escaped = html.escape(entry["name"])
        index_html_file.write(f'<a href="{apk_escaped}">{name_escaped}</a>\n')
    index_html_file.write('</pre>\n</body>\n</html>\n')
        