import os

path = os.path.join(os.path.expanduser('~'), "AppData\\Local\\Packages\\Microsoft.MinecraftUWP_8wekyb3d8bbwe\\LocalState\\games\\com.mojang\\minecraftWorlds")
worlds = os.listdir(path)
print("Worlds found:")
levelnames = []
for i in range(len(worlds)):
    levelname = os.path.join(path, worlds[i], "levelname.txt")
    with open(levelname) as f:
        print(str(i + 1) + ".", f.readline())
selection = int(input("Enter world number > "))
data_path = os.path.join(path, worlds[selection - 1], "level.dat")


with open(data_path, "rb") as f:
    data = bytearray(f.read())

pos = data.find(b'\x00GameType')
data[pos + 9] = 0
pos = data.find(b'commandsEnabled')
data[pos + 15] = 0
pos = data.find(b'hasBeenLoadedInCreative')
data[pos + 23] = 0

with open(data_path, "wb") as f:
    f.write(data)
