#!/usr/bin/env python3

import os
from sys import argv
import zipfile
import tempfile
import shutil


def finish(message):
	"""Display a message to the user then exit the program"""

	print(message)
	input("Press Enter to quit.")
	raise SystemExit


def get_valid_input(message, valids):
	"""User selects option from a given list"""

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
	"""Search the disk for Minecraft Bedrock worlds"""

	path = os.path.join(os.path.expanduser('~'), "AppData", "Local", "Packages", "Microsoft.MinecraftUWP_8wekyb3d8bbwe", "LocalState", "games", "com.mojang", "minecraftWorlds")

	#Quit if Minecraft Bedrock isn't installed
	if not os.path.isdir(path):
		finish("Error: Minecraft directory not found. Have you got Minecraft for Windows installed?")

	#Quit if no worlds have been started
	worlds = os.listdir(path)
	if not len(worlds):
		finish("Error: No worlds detected. Have you started a world?")

	#Display all of the worlds found then ask the user for a selection
	print("World(s) found:")
	for i, world in enumerate(worlds, start=1):
		levelname = os.path.join(path, world, "levelname.txt")
		with open(levelname, 'r', encoding='utf-8') as f:
			print(str(i) + '.', f.readline())
	selection = get_valid_input("Enter world number > ", range(len(worlds)))

	return os.path.join(path, worlds[selection - 1], "level.dat")


def write_file(file):
	"""Find the flags and reset their values, then write back to file"""

	flags = [b'\x00GameType', b'cheatsEnabled', b'commandsEnabled', b'hasBeenLoadedInCreative', b'hasLockedBehaviorPack', b'hasLockedResourcePack' ,b'isFromLockedTemplate']
	with open(file, 'r+b') as f:
		data = bytearray(f.read())
		for flag in flags:
			pos = data.find(flag) + len(flag)
			data[pos] = 0
		f.seek(0)
		f.write(data)
	print("Written to", file)

	return True


if __name__ == "__main__":
	#Worlds given via args
	if len(argv) > 1:
		written = False
		for file in argv[1:]:

			#Sinlge level.dat file
			if os.path.isfile(file) and os.path.basename(file) == "level.dat":
				written = write_file(file)

			#World directory containing level.dat
			elif not os.path.isfile(file) and os.path.isfile(os.path.join(file, "level.dat")):
				written = write_file(os.path.join(file, "level.dat"))

			#Zipped worlds
			elif zipfile.is_zipfile(file):
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
					print("Compressed to", file)
				else:
					print(file, "isn't a valid Minecraft Bedrock world archive.")

				shutil.rmtree(tmp_dir)

			else:
				print(file, "isn't a valid Minecraft Bedrock world.")

		if not written:
			finish("Nothing written.")

	#Search for a world if on Windows
	elif os.name == 'nt':
		print("No worlds provided, searching disk...")
		file = find_world()
		write_file(file)
	else:
		finish("Error: World must be provided via command-line arguments on Linux/macOS")

	finish("Sucess!")
