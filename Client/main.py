import contextlib
import sys
import requests
import os
import json
import zipfile
import time

class Colours:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"

    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"
    

@contextlib.contextmanager
def set_argv(args):
    sys._argv = sys.argv[:]
    sys.argv=args
    yield
    sys.argv = sys._argv

def check_internet():
    url='http://www.google.com/'
    timeout=5
    try:
        requests.get(url, timeout=timeout)
        print("Internet Connection: Successful")
    except Exception as e:
        print("Internet Connection: Failed")
        print(e)
        sys.exit(1)

def create_mc_instance():
    with set_argv(["picomc", "--root", "./MinecraftFiles","instance", "create", "default"]):
        from picomc import main
        main()

def set_java_path(java_path):
    with open("./MinecraftFiles/instances/default/config.json", "r") as f:
        config = json.load(f)
    config["java_path"] = java_path
    with open("./MinecraftFiles/instances/default/config.json", "w") as f:
        f.write(json.dumps(config, indent=4))
def launch_mc():
    with set_argv(["picomc", "--root", "./MinecraftFiles","instance", "launch", "default"]):
        from picomc import main
        main()

def write_account_config(username, uuid, client_token):
    config = {
        "default": username,
        "accounts": {
            username: {
                "uuid": uuid,
                "online": False
                }
            },
        "client_token": client_token
        }
    
    with open("./MinecraftFiles/accounts.json", "w") as f:
        f.write(json.dumps(config, indent=4))

#######################################################################
SERVER_URL = "https://testmc.eshark.tk/"
java_path = os.path.abspath("./java/jdk-17.0.8+7/bin/java.exe")
current_user = os.getlogin()


print("\n")
print(Colours.RED, "##########-Minecraft-Custom-Client##########")
print(Colours.RED,"\nDO NOT DISTRUBTE WITHOUT THE OWNER'S PERMISSION!")
print("\n")
time.sleep(1)
check_internet()

# Does the "java" folder exist?
if not os.path.exists("./java"):
    print("Downloading Java...")
    os.mkdir("./java")

    # Download the file from `url` and save it locally under `file_name`:
    url = "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.8%2B7/OpenJDK17U-jdk_x64_windows_hotspot_17.0.8_7.zip"
    r = requests.get(url)
    with open("./java/java.zip", 'wb') as f:
        f.write(r.content)
    print("Extracting Java...")
    with zipfile.ZipFile("./java/java.zip", 'r') as zip_ref:
        zip_ref.extractall("./java")
    os.remove("./java/java.zip")
    print("Java installed.")

try:
    create_mc_instance()
except:
    pass

user_data = requests.get(SERVER_URL + f"/McUser?username={current_user}")
if user_data.status_code == 200:
    user_data = user_data.json()
    if user_data["CanPlayMC"]:
        write_account_config(user_data["MinecraftUsername"], user_data["MinecraftUUID"], user_data["MinecraftClientToken"])
else:
    print("Error: " + str(user_data.status_code))
    sys.exit(1)

set_java_path(java_path)
launch_mc()


