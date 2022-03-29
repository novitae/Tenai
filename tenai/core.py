import requests
from json import dump, load
from argparse import ArgumentParser
from os.path import dirname, join
from pysimpleig import A1, sessionid_to_ios_auth, Login, exceptions
from random import choice, randint

IOS = ['15_0', '15_1', '15_0_1', '15_0_2', '15_2', '15_1_1', '15_3', '15_2_1', '15_4', '15_3_1']
VER = ['211.0.0.21.118', '210.0.0.16.67', '212.1.0.25.118', '212.1.0.25.118', '213.0.0.19.117', '213.0.0.19.117', '212.1.0.25.118', '213.0.0.19.117', '213.0.0.19.117', '213.0.0.19.117', '208.0.0.26.131', '208.0.0.26.131', '213.0.0.19.117', '213.0.0.19.117', '213.0.0.19.117', '213.0.0.19.117']
REF = [
    ("10,1", "750x1334"),
    ('10,2', "1080x1920"),
    ('10,3', "1125x2436"),
    ("10,4", "750x1334"),
    ('10,5', "1080x1920"),
    ('10,6', "1125x2436"),
    ('11,2', "1125x2436"),
    ('11,4', "1242x2688"),
    ('11,6', "1242x2688"),
    ('11,8', "828x1792"),
    ('12,1', "828x1792"),
    ('12,3', "1125x2436"),
    ('12,5', "1242x2688"),
    ('12,8', "750x1334"),
    ('13,1', "1080x2340"),
    ('13,2', "1170x2532"),
    ('13,3', "1170x2532"),
    ('13,4', "1284x2778"),
    ('14,2', "1170x2532"),
    ('14,3', "1284x2778"),
    ('14,4', "1080x2340"),
    ('14,5', "1170x2532")
    ] # https://gist.github.com/adamawolf/3048717
MODEL = choice(REF)

AUTHS_PATH = join(dirname(__file__), "auths.json")
HEADERS = {
    "Host": "i.instagram.com",
    "Connection": "keep-alive",
    "Accept": "*/*",
    "X-IG-App-ID": "124024574287414",
    "User-Agent": f'''Instagram {choice(VER)} (iPhone{MODEL[0]}; iOS {choice(IOS)}; fr_FR; fr-FR; scale=2.00; {MODEL[1]}; {"".join([str(randint(0,9)) for x in range(9)])}) AppleWebKit/420+''',
    "Accept-Language": "fr-FR;q=1.0",
    "Accept-Encoding": "gzip, deflate",
}

class PrivateInstaChaining:
    def __init__(self, session_id:str = None) -> None:
        try:
            with open(AUTHS_PATH, "r") as stored_auth_file:
                stored_auth = load(stored_auth_file)["ssid"]
        except FileNotFoundError:
            stored_auth = ""
            with open(AUTHS_PATH, "w") as make_stored_auth_file:
                stored_auth = dump({"ssid":stored_auth}, make_stored_auth_file, indent=4)

        ssid = session_id if session_id else stored_auth

        if not ssid:
            exit("[!] Please login with sessionid. This will save it locally so you don't have to log with again.")

        logger = Login()
        try:
            self.cookies = logger.session_id(session_id=ssid)
        except exceptions.NotConnectedAccount:
            exit(f'[!] "{ssid}" is not connected to any account')
        if not logger.check_login(cookies=self.cookies):
            raise exceptions.NotLoggedInError(f'"{ssid}" has not logged in the program')

        if session_id and not stored_auth:
            with open(AUTHS_PATH, "w") as storing_auth_file:
                stored_auth = dump({"ssid":ssid}, storing_auth_file, indent=4)

        self.ssid = ssid
        self.userinfo = A1(cookies=self.cookies)
        self.headers = HEADERS
        print(HEADERS)
        self.headers.update(sessionid_to_ios_auth(session_id=ssid))

    def get_data(self, username: str) -> dict:
        try:
            user_id = self.userinfo.infos(username=username)
            if user_id["is_private"] and user_id["followed_by_viewer"]:
                exit("[!] You have access to this target.")
            user_id = user_id["id"]
        except exceptions.UserNotFoundError:
            exit(f"[!] {username} is not an existing instagram account")
        return requests.get(f"https://i.instagram.com/api/v1/fbsearch/accounts_recs/?surface=profile_view&target_user_id={user_id}", headers=self.headers).json() # &include_friendship_status=true

def main() -> None:
    parser = ArgumentParser(
        epilog="" # afficher l'article de mon blog
    )
    parser.add_argument("-u", "--username", type=str, help="the target's username", required=True)
    parser.add_argument("-s", "--session-id", type=str, help="the sessionid of an empty account")
    parser.add_argument("-e", "--export", action="store_true", help="will export the json result")
    args = vars(parser.parse_args())
    
    username=args["username"]

    result = PrivateInstaChaining(
        session_id=args.get("session_id")
    ).get_data(
        username=username
    )
    print('[*] "Tenai" by @novitae')
    if result["status"] == "fail":
        print(result)
        exit(f"[!] {username} is not eligible for chaining.")

    output = []
    for user in result["users"]:
        if user["chaining_info"]["sources"] == "[11]":
            output.append(user)
    
    if not output:
        exit("[!] The result list contains only suggestions for you.")
    print("[+] Results:")
    for user in output:
        print(f""" -  {user["username"]}""")

    if args['export']:
        name = f"{username}_private_mutuals.json"
        with open(name,"w") as exp:
            dump({"users":output}, exp, indent=4)
        print(f'[e] Exported under "{name}"')

if __name__ == "__main__":
    main()