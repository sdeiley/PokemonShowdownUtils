import asyncio
import datetime as dt
import json
import os

import ps_util as ps
import ui_util as ui
import requests

ALL_PUBLIC_REPLAYS = ps.BASE_STRING + ps.SEARCH + "user={username}" + "&format=" + ps.FORMAT
ALL_PRIVATE_REPLAYS = ALL_PUBLIC_REPLAYS + "&private" 
FORMAT = "Gen9VGC2023Series1"
FILENAME = "{format}-{yyyy_mm_dd}-{p1}-{p2}.html"
REPLAY_FOLDER = "replays"

async def main():
    username, password = ui.get_credentials()
   
    challstr_list = await ps.get_challstr()
    cookie = ps.sign_in(username, password, challstr_list)
    get_replay_htmls(cookie, username)


def get_replay_htmls(cookie: requests.cookies.RequestsCookieJar, username: str) -> str:
    pub_replays = requests.get(
        ALL_PUBLIC_REPLAYS.format(username=username))
    private_replays = requests.get(
        ALL_PRIVATE_REPLAYS.format(username=username), 
        cookies=cookie)

    public_json = json.loads(pub_replays.text)
    private_json = json.loads(private_replays.text)


    def process_and_download_replays(text: json, appendix="") -> str:
        html = ""
        for replay in text:
            id = replay["id"]
            upload_epoch = replay["uploadtime"]
            yyyy_mm_dd = dt.datetime.utcfromtimestamp(upload_epoch).strftime("%Y-%m-%d")
            p1 = strip_player(replay["p1"])
            p2 = strip_player(replay["p2"])
            filename = FILENAME.format(
                format=FORMAT,
                yyyy_mm_dd=yyyy_mm_dd,
                p1=p1,
                p2=p2
            )
            
            if not os.path.exists(REPLAY_FOLDER):
                os.makedirs(REPLAY_FOLDER)
            filepath = REPLAY_FOLDER + "/" + filename

            url = ps.BASE_STRING + id + appendix
            with open(filepath, "w+", encoding="utf-8") as f:
                html = requests.get(url)
                f.write(html.text)

    process_and_download_replays(public_json)
    process_and_download_replays(private_json, "pw")
    

def strip_player(p: str):
    if len(p) < 2:
        return p.replace("_", "")
    if p[0] != "!":
        return p.replace("_", "")
    return p[1:].replace("_", "")
    

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
        asyncio.set_event_loop(None)
