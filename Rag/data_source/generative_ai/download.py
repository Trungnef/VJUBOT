
file_links = [
    {
        "title" : " ",
        "url"  : " "
    },
    {
        "title" : " ",
        "url"  : " "
    },
    {
        "title" : " ",
        "url"  : " "
    },
    {
        "title" : " ",
        "url"  : " "
    },
]

import os
import wget

def is_exist(file_link):
    return os.path.exists(f"./{file_link["title"]}.pdf")

for file_link in file_links:
    if not is_exist[file_link]:
        wget.download(file_link["url"], out = f"./{file_link["title"]}.pdf")
