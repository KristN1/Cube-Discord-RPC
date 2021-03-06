from pypresence import Presence
import time
import os
import json
import psutil
from datetime import datetime

print("Cube RPC started")

appdata = os.getenv('APPDATA')
launcher_data_fullpath = appdata + "\.minecraft\launcher_profiles.json"
logs_fullpath = appdata + "\.minecraft\logs\latest.log"

mc = "javaw.exe"


start_time = None

def checkTime(t):
    if t == None:
        global start_time
        start_time = time.time()
    return t

def getUserName():
    with open(launcher_data_fullpath, 'r') as f:
        launcher_data = json.load(f)

        database = launcher_data['authenticationDatabase']
        profiles = database[list(database.keys())[0]]['profiles']
        profile = profiles[list(profiles.keys())[0]]

        return profile["displayName"]

def getMinigame(logs):
    found = False
    minigames_list = ["Welcome to ||CubeCraft||", "SkyWars is starting", "EggWars is starting", "MinerWare is starting", "Among Slimes is starting", "Tower Defence is starting", "Lucky Islands is starting"]
    for line in logs:
        if found == False:
            for item in minigames_list:
                if item in line:
                    itempos = minigames_list.index(item)

                    if itempos == 0:
                        found = True
                        minigame = "Lobby"

                    elif itempos == 1:
                        found = True
                        minigame = "SkyWars"

                    elif itempos == 2:
                        found = True
                        minigame = "EggWars"

                    elif itempos == 3:
                        found = True
                        minigame = "MinerWare"

                    elif itempos == 4:
                        found = True
                        minigame = "Among Slimes"

                    elif itempos == 5:
                        found = True
                        minigame = "Tower Defence"

                    elif itempos == 6:
                        found = True
                        minigame = "Lucky Islands"   

                    if found == True:
                        return minigame

def checkCube(logs):
    for line in logs:
        if "cubecraft.net., 25565" in line:
            return True

        if "Connecting" in line:
            return False
    return False

def afkCheck(logs):
    current = datetime.now().minute
    for line in logs:
        print(logs)
        print(line)
        minutes = int(line.split(" ")[0].split(":")[1])
        if current < minutes:
            current += 60

        print(f"current - {current}")
        print(f"minutes - {minutes}")
        print(f"counted - {current - 5} should be smaller than {minutes}")

        if current - 5 <= minutes:
            print("true")
            return True
        else:
            print("false")
            return False
            
def updatePresence(logs):
        state = f"Minigame - {getMinigame(logs)}"
        details = f"Username  - {getUserName()}"
        large_image = "cclogo_lq"
        small_image = None
        large_text = "cubecraft.net"
        
        RPC.update(state=state, details=details, large_image=large_image, small_image=small_image, large_text=large_text, start=checkTime(start_time), buttons=[{"label": "Get this presence", "url": "https://github.com/KristN1/Cube-Discord-RPC"}])

client_id = '827982404350115890' 
RPC = Presence(client_id) 
RPC.connect()

while True:
    with open(logs_fullpath,'r') as file:
        logs = reversed(list(file))
        if mc in (p.name() for p in psutil.process_iter()):
            print("mccheck")
            if checkCube(logs) == True:
                print("cubechekc")
                if afkCheck(logs) == False:
                    print("afkcheck")
                    print("AFK")
                    RPC.clear()
                    start_time = None
                else:
                    updatePresence(logs)
                    print("ingame")

            else:
                start_time = None
                RPC.clear()
        
        else:
            start_time = None
            RPC.clear()

    print("-------------")
    time.sleep(15)
