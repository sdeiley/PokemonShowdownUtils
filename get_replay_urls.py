import asyncio
import json

import ps_util as ps
import ui_util as ui
import requests

ALL_PUBLIC_REPLAYS = ps.BASE_STRING + ps.SEARCH + "user={username}" + "&format=" + ps.FORMAT
ALL_PRIVATE_REPLAYS = ALL_PUBLIC_REPLAYS + "&private" 

async def main():
    username, password = ui.get_credentials()
   
    challstr_list = await ps.get_challstr()
    cookie = ps.sign_in(username, password, challstr_list)
    replays = get_replay_urls(cookie, username)

    ui.display_results(replays)
    print(replays)

def get_replay_urls(cookie: requests.cookies.RequestsCookieJar, username: str) -> str:
    pub_replays = requests.get(
        ALL_PUBLIC_REPLAYS.format(username=username))
    private_replays = requests.get(
        ALL_PRIVATE_REPLAYS.format(username=username), 
        cookies=cookie)

    public_json = json.loads(pub_replays.text)
    private_json = json.loads(private_replays.text)


    def append_replays(text: json, appendix="") -> str:
        replays = ""
        for replay in text:
            id = replay["id"] + appendix
            replays += ps.BASE_STRING + id + "\n"
        return replays

    replays = ""
    replays += append_replays(public_json)
    replays += append_replays(private_json, "pw")
    
    return replays
    

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()
        asyncio.set_event_loop(None)