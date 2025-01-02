import os
from sys import argv


def finish(message):
	print(message)
	input("Press Enter to quit.")
	raise SystemExit


def get_valid_input(message, valids):
	print()
	selection = 0
	while selection - 1 not in valids:
		try:
			selection = int(input(message))
		except:
			print("Error: Selection is not an integer. ", end='')
		else:
			if selection - 1 not in valids:
				print("Error: Selection is not in range. ", end='')

	return selection


def find_world():
	path = os.path.join(os.path.expanduser('~'), "AppData", "Local", "Packages", "Microsoft.MinecraftUWP_8wekyb3d8bbwe", "LocalState", "games", "com.mojang", "minecraftWorlds")
	if not os.path.isdir(path):
		finish("Error: Minecraft directory not found. Have you got Minecraft for Windows installed?")
	worlds = os.listdir(path)
	if not len(worlds):
		finish("Error: No worlds detected. Have you started a world?")

	print("World(s) found:")
	for i, world in enumerate(worlds, start=1):
		levelname = os.path.join(path, world, "levelname.txt")
		with open(levelname) as f:
			print(str(i) + ".", f.readline())
	selection = get_valid_input("Enter world number > ", range(len(worlds)))

	return os.path.join(path, worlds[selection - 1], "level.dat")


def write_file(file):
	with open(file, "r+b") as f:
		data = bytearray(f.read())
		pos = data.find(b'\x00GameType')
		data[pos + 9] = 0
		pos = data.find(b'commandsEnabled')
		data[pos + 15] = 0
		pos = data.find(b'hasBeenLoadedInCreative')
		data[pos + 23] = 0
		f.seek(0)
		f.write(data)
	print("Written to", file)


if __name__ == "__main__":
	if len(argv) > 1:
		written = False
		for file in argv[1:]:
			if file.endswith('.dat') and os.path.isfile(file):
				write_file(file)
				written = True
			else:
				print(file, "isn't a valid Minecraft Bedrock world.")
		if written:
			finish("Sucess!")
		else:
			finish("Nothing written.")
	else:
		file = find_world()
		write_file(file)
		finish("Sucess!")
