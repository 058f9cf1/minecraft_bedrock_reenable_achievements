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


def find_user_worlds_root():
	"""Find Minecraft Bedrock user folders and let the user choose one"""

	base_path = os.path.join(
		os.path.expanduser('~'),
		"AppData",
		"Roaming",
		"Minecraft Bedrock",
		"Users"
	)

	if not os.path.isdir(base_path):
		finish("Error: Minecraft Bedrock Users directory not found.")

	user_ids = []
	for entry in os.listdir(base_path):
		full_path = os.path.join(base_path, entry)
		worlds_path = os.path.join(full_path, "games", "com.mojang", "minecraftWorlds")
		if os.path.isdir(full_path) and os.path.isdir(worlds_path):
			user_ids.append(entry)

	if not user_ids:
		finish("Error: No valid Minecraft Bedrock users found.")

	user_ids.sort()

	print("User(s) found:")
	for i, user_id in enumerate(user_ids, start=1):
		print(str(i) + '.', user_id)

	selection = get_valid_input("Which user do you want to edit? > ", range(len(user_ids)))
	selected_user_id = user_ids[selection - 1]

	return os.path.join(base_path, selected_user_id, "games", "com.mojang", "minecraftWorlds")


def find_world():
	"""Search the selected user folder for Minecraft Bedrock worlds"""

	path = find_user_worlds_root()

	if not os.path.isdir(path):
		finish("Error: World directory not found for the selected user.")

	worlds = []
	for entry in os.listdir(path):
		world_path = os.path.join(path, entry)
		level_dat_path = os.path.join(world_path, "level.dat")
		if os.path.isdir(world_path) and os.path.isfile(level_dat_path):
			worlds.append(entry)

	if not worlds:
		finish("Error: No worlds detected for the selected user.")

	print()
	print("World(s) found:")
	for i, world in enumerate(worlds, start=1):
		levelname = os.path.join(path, world, "levelname.txt")
		world_name = world

		if os.path.isfile(levelname):
			try:
				with open(levelname, 'r', encoding='utf-8') as f:
					first_line = f.readline().strip()
					if first_line:
						world_name = first_line
			except:
				pass

		print(str(i) + '.', world_name)

	selection = get_valid_input("Enter world number > ", range(len(worlds)))

	return os.path.join(path, worlds[selection - 1], "level.dat")


def write_file(file):
	"""Find the flags and reset their values, then write back to file"""

	flags = [
		b'\x00GameType',
		b'cheatsEnabled',
		b'commandsEnabled',
		b'hasBeenLoadedInCreative',
		b'hasLockedBehaviorPack',
		b'hasLockedResourcePack',
		b'isFromLockedTemplate'
	]

	with open(file, 'r+b') as f:
		data = bytearray(f.read())

		for flag in flags:
			pos = data.find(flag)
			if pos != -1:
				pos += len(flag)
				if pos < len(data):
					data[pos] = 0

		f.seek(0)
		f.write(data)

	print("Written to", file)

	return True


if __name__ == "__main__":
	# Worlds given via args
	if len(argv) > 1:
		written = False
		for file in argv[1:]:

			# Single level.dat file
			if os.path.isfile(file) and os.path.basename(file) == "level.dat":
				written = write_file(file)

			# World directory containing level.dat
			elif os.path.isdir(file) and os.path.isfile(os.path.join(file, "level.dat")):
				written = write_file(os.path.join(file, "level.dat"))

			# Zipped worlds
			elif zipfile.is_zipfile(file):
				tmp_dir = os.path.join(tempfile.gettempdir(), "mcworld")
				if os.path.isdir(tmp_dir):
					shutil.rmtree(tmp_dir)
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

	# Search for a world if on Windows
	elif os.name == 'nt':
		print("No worlds provided, searching disk...")
		file = find_world()
		write_file(file)
	else:
		finish("Error: World must be provided via command-line arguments on Linux/macOS")

	finish("Success!")
