import requests
from .version import version


def update(where):
    try:
        res = requests.get("https://api.github.com/repos/websploit/websploit/releases/latest", timeout=2)
        if res.status_code == 200:
            response = res.json()
            git_version = response['tag_name']
            # check for new version
            if version != git_version:
                print(f"New version available: {git_version}")
                print(f"Download Link : https://api.github.com/repos/websploit/websploit/zipball/{git_version}")
            else:
                if where == "update_command":
                    print("You are using the latest version of websploit.")
                elif where == "main_menu":
                    pass

        else:
            if where == "main_menu":
                pass
            elif where == "update_command":
                print("Error while updating! Check your internet connection!")
    except:
        pass