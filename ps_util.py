import websockets
import requests

# Example: "https://replay.pokemonshowdown.com/search.json?user=anonymous_snorlax&format=gen9vgc2023series1&private"
SIGN_IN_URL = "https://play.pokemonshowdown.com/~~showdown/action.php"
WEB_SOCKET_URL = "ws://sim.smogon.com:8000/showdown/websocket"

BASE_STRING = "https://replay.pokemonshowdown.com/"
SEARCH = "search.json?"
FORMAT = "gen9vgc2023series1"

async def get_challstr() -> list:
    async with websockets.connect(WEB_SOCKET_URL) as websocket:
        while True:
            message = await websocket.recv()
            _, command, *content = message.split('|')
            if command == "challstr":
                return content

def format_challstr(id: str, chall: str) -> str:
    return f'{id}%7C{chall}'

def sign_in(user: str, password: str, challstr_l: list) -> requests.cookies.RequestsCookieJar:
    challstr = format_challstr(challstr_l[0], challstr_l[1])
    r = requests.post(
        SIGN_IN_URL,
        data={
            "act": "login", 
            "name": user,
            "pass": password, 
            "challstr" : challstr
        }
    )

    if r.cookies == requests.cookies.RequestsCookieJar():
        raise Exception("==============================\n" + \
                "Sign-In Failed; text from attempt:\n" + \
                r.text + \
                "\n==============================")

    return r.cookies
