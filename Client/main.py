import contextlib
import sys
import requests
import os
import json
import zipfile
import time

class Colours:
    """ANSI Colour codes"""
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
    """Temporarily set sys.argv"""
    sys._argv = sys.argv[:] # Save sys.argv
    sys.argv=args           # Set sys.argv
    yield                   # Execute code
    sys.argv = sys._argv    # Restore sys.argv

def check_internet():
    """Check if the user has an internet connection"""
    try:
        requests.get('http://www.google.com/', timeout=5)
        print(Colours.GREEN + "Internet Connection: Successful" + Colours.RESET)
    except Exception as e:
        print(Colours.RED + "Internet Connection: Failed" + Colours.RESET)
        print(e)
        sys.exit(1)
        
def picomc(args):
    args = args.split(" ")
    args.insert(0, "picomc")
    args.insert(1, "--root")
    args.insert(2, "./MinecraftFiles")
    with set_argv(args):
        from picomc import main
        main()

def create_mc_instance():
    picomc("instance create default")

def set_java_path(java_path):
    picomc("config set java.path " + java_path)
    picomc("instance default config set java.path " + java_path)

def launch_mc():
    picomc("instance launch default")

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
java_path = "./java/jdk-17.0.8+7/bin/java.exe"
current_user = os.getlogin()


print("\n")
print(Colours.RED, "##########-Minecraft-Custom-Client##########" + Colours.RESET)
print(Colours.RED,"\nDO NOT DISTRUBTE WITHOUT THE OWNER'S PERMISSION!" + Colours.RESET)
print("\n")

print(Colours.YELLOW + "Checking for internet connection..." + Colours.RESET)
check_internet()

# Does the "java" folder exist?
print(Colours.YELLOW + "Checking for Java..." + Colours.RESET)
if not os.path.exists("./java"):

    print("Java not found. Downloading Java...")
    os.mkdir("./java") 
    
    # Download the file from `url` and save it 
    url = "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.8%2B7/OpenJDK17U-jdk_x64_windows_hotspot_17.0.8_7.zip"
    r = requests.get(url)
    with open("./java/java.zip", 'wb') as f:
        f.write(r.content)


    print(Colours.YELLOW + "Extracting Java..." + Colours.RESET)
    with zipfile.ZipFile("./java/java.zip", 'r') as zip_ref:
        zip_ref.extractall("./java")
    os.remove("./java/java.zip")
    print(Colours.GREEN + "Java Installed!" + Colours.RESET)
else:
    print(Colours.GREEN + "Java Found!" + Colours.RESET)


# Does the "MinecraftFiles" folder exist?
print(Colours.YELLOW + "Checking if Minecraft folder exists..." + Colours.RESET)
if not os.path.exists("./MinecraftFiles"):
    print("Minecraft folder not found. Creating Minecraft instance...")
    create_mc_instance()
    print(Colours.GREEN + "Minecraft instance created!" + Colours.RESET)
else:
    print(Colours.GREEN + "Minecraft folder found!" + Colours.RESET)


user_data = requests.get(SERVER_URL + f"/McUser?username={current_user}")
if user_data.status_code == 200:
    user_data = user_data.json()
    if user_data["CanPlayMC"]:
        print("You are authorized to play minecraft!")
        write_account_config(user_data["MinecraftUsername"], user_data["MinecraftUUID"], user_data["MinecraftClientToken"])
else:
    print("Error: " + str(user_data.status_code))
    sys.exit(1)

try:
    set_java_path(java_path)
except:
    pass

launch_mc()


