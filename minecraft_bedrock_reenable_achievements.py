import os
from sys import argv
import zipfile
import shutil

def make_tmpdir():
	if os.name == "posix":
		tmpdir_path = "/tmp/mcworld_temp"
	elif os.name == "nt":
		# Thanks to NT for making the temp folder changable we have to do this
		tmpdir_path = os.path.join(os.environ.get("TEMP", "."), "mcworld_temp")
	else:
		tmpdir_path = -1

	os.makedirs(tmpdir_path, exist_ok=True)
	return tmpdir_path

		

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
	print("Written to", file)

	return True

def zip_folder(folder_path, output_zip):
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, folder_path)
                zipf.write(full_path, rel_path)


if __name__ == "__main__":
	if len(argv) > 1:
		written = False
		for file in argv[1:]:
			if os.path.basename(file) == 'level.dat' and os.path.isfile(file):
				written = write_file(file)
			elif file.endswith('.mcworld') and zipfile.is_zipfile(file):
				print(file, "is an mcworld file. Attempting write but it may fail")
				tempdir = make_tmpdir()
				if tempdir < 0:
					print("Error: Write attempt failed. Either import", file, "into Minecraft or extract the level.dat file directly.")
				with zipfile.ZipFile(file, 'r') as zip_ref:
					zip_ref.extractall(tempdir)

				level_dat_path = os.path.join(tempdir, "level.dat")
				if os.path.isfile(level_dat_path):
					written = write_file(level_dat_path)
				else:
					print("level.dat not found in extracted mcworld.")

				zip_folder(tempdir, file)
				shutil.rmtree(tempdir)
			elif not os.path.isfile(file) and os.path.isfile(f"{file}/level.dat"):
				written = write_file(f"{file}/level.dat")
			else:
				print(file, "isn't a valid Minecraft Bedrock world.")
		if not written:
			finish("Nothing written.")
	else:
		file = find_world()
		write_file(file)

	finish("Sucess!")
