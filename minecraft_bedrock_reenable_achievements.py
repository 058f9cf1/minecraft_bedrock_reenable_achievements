#!/usr/bin/env python3

import os
from sys import argv
import zipfile
import tempfile
import shutil


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
		with open(levelname, 'r', encoding='utf-8') as f:
			print(str(i) + ".", f.readline())
	selection = get_valid_input("Enter world number > ", range(len(worlds)))

	return os.path.join(path, worlds[selection - 1], "level.dat")


def write_file(file):
	with open(file, 'r+b') as f:
		data = bytearray(f.read())
		pos = data.find(b'\x00GameType')
		data[pos + 9] = 0
		pos = data.find(b'cheatsEnabled')
		data[pos + 13] = 0
		pos = data.find(b'commandsEnabled')
		data[pos + 15] = 0
		pos = data.find(b'hasBeenLoadedInCreative')
		data[pos + 23] = 0
		pos = data.find(b'hasLockedBehaviorPack')
		data[pos + 21] = 0
		pos = data.find(b'hasLockedResourcePack')
		data[pos + 21] = 0
		pos = data.find(b'isFromLockedTemplate')
		data[pos + 20] = 0
		f.seek(0)
		f.write(data)

	return True


if __name__ == "__main__":
	if len(argv) > 1:
		written = False
		for file in argv[1:]:
			if os.path.isfile(file) and os.path.basename(file) == 'level.dat':
				written = write_file(file)
				print("Written to", file)
			elif not os.path.isfile(file) and os.path.isfile(os.path.join(file, 'level.dat')):
				written = write_file(os.path.join(file, 'level.dat'))
				print("Written to", os.path.join(file, 'level.dat'))
			elif file.endswith('.mcworld') and zipfile.is_zipfile(file):
				tmp_dir = os.path.join(tempfile.gettempdir(), "mcworld")
				os.makedirs(tmp_dir, exist_ok=True)
				with zipfile.ZipFile(file, 'r') as zip_ref:
					zip_ref.extractall(tmp_dir)

				tmp_level = os.path.join(tmp_dir, "level.dat")
				if os.path.isfile(tmp_level):
					written = write_file(tmp_level)
					shutil.make_archive(file, format='zip', root_dir=tmp_dir)
					os.remove(file)
					os.rename(file + ".zip", file)
					print("Written to", file)
				else:
					print(file, "isn't a valid .mcworld archive")

				shutil.rmtree(tmp_dir)
			else:
				print(file, "isn't a valid Minecraft Bedrock world.")
		if not written:
			finish("Nothing written.")
	else:
		file = find_world()
		write_file(file)
		print("Written to", file)

	finish("Sucess!")
