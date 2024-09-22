import os

def error(message):
	print(message)
	raise SystemExit

if __name__ == "__main__":
        path = os.path.join(os.path.expanduser('~'), "AppData", "Local", "Packages", "Microsoft.MinecraftUWP_8wekyb3d8bbwe", "LocalState", "games", "com.mojang", "minecraftWorlds")
        if not os.path.isdir(path):
                error("Error: Minecraft directory not found. Have you got Minecraft for Windows installed?")
        worlds = os.listdir(path)
        if not len(worlds):
                error("Error: No worlds detected. Have you started a world?")
        print("Worlds found:")
        for i in range(len(worlds)):
                levelname = os.path.join(path, worlds[i], "levelname.txt")
                with open(levelname) as f:
                        print(str(i + 1) + ".", f.readline())
        selection = int(input("Enter world number > "))
        if selection - 1 not in range(len(worlds)):
                error("Error: Selection not valid")

        data_path = os.path.join(path, worlds[selection - 1], "level.dat")
        with open(data_path, "r+b") as f:
                data = bytearray(f.read())

                pos = data.find(b'\x00GameType')
                data[pos + 9] = 0
                pos = data.find(b'commandsEnabled')
                data[pos + 15] = 0
                pos = data.find(b'hasBeenLoadedInCreative')
                data[pos + 23] = 0
        
                f.seek(0)
                f.write(data)
