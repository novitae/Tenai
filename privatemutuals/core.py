import requests
from json import dump, load
from argparse import ArgumentParser
from os.path import dirname, join
from pysimpleig import A1, sessionid_to_ios_auth, Login, exceptions

AUTHS_PATH = join(dirname(__file__), "auths.json")
HEADERS = {
    "Host": "i.instagram.com",
    "Connection": "keep-alive",
    "Accept": "*/*",
    "X-IG-App-ID": "124024574287414",
    "User-Agent": "Instagram 224.1.0.15.115 (iPhone7,2; iOS 12_5_5; fr_FR; fr-FR; scale=2.00; 750x1334; 353721074) AppleWebKit/420+",
    "Accept-Language": "fr-FR;q=1.0",
    "Accept-Encoding": "gzip, deflate",
}

class InstaPrivateMutuals:
    def __init__(self, session_id:str = None) -> None:     
        with open(AUTHS_PATH, "r") as stored_auth_file:
            stored_auth = load(stored_auth_file)["ssid"]

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

        self.userinfo = A1(cookies=self.cookies)
        self.headers = HEADERS
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

    result = InstaPrivateMutuals(
        session_id=args.get("session_id")
    ).get_data(
        username=username
    )
    print("[*] InstaPrivateMutuals by @novitae")
    if result["status"] == "fail":
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