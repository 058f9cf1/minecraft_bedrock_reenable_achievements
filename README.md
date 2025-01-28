# Re-enable Minecraft Bedrock Achievements
A tool for allowing you to earn achievements on a Minecraft Bedrock world that has enabled cheats or used creative mode. After the program is run, cheats will be disabled and the default world game mode will be set to survival. Any players set to creative mode or changed gamerules will remain changed.

> [!IMPORTANT]
> Back up your worlds before using! If any corruption occurs, the worlds can then be restored.

> [!IMPORTANT]
> This is a tool for worlds on 'Minecraft for Windows', not 'Minecraft: Java Edition' or any other Minecraft Bedrock version. After the program has completed, other players on all Bedrock versions will be able to join the world and unlock achievements.

Works on Minecraft Bedrock worlds version 1.21.0 and higher. It may also work on versions below, but this is untested.

## Installation
Download the latest release from the [releases](https://github.com/058f9cf1/minecraft_bedrock_reenable_achievements/releases) section.

## Usage
The program can be run by double-clicking on the executable. This will open the command prompt and search the disk for Minecraft Bedrock worlds. You can select a world by entering the number next to the world name. The program, once completed, can be exited by pressing 'Enter'.

```level.dat``` files can also be dragged and dropped onto the executable in order to do multiple worlds at the same time.

## Running from source

### Dependencies
> Requires ```Python 3``` to be installed. ```git``` is required for the first method only.

### Method 1 (requires git to be installed):
- Open a terminal and run the following commands in order:
```
git clone https://github.com/058f9cf1/minecraft_bedrock_reenable_achievements.git
cd minecraft_bedrock_reenable_achievements
python minecraft_bedrock_reenable_achievements.py
```

### Method 2:
- Download the file 'minecraft_bedrock_reenable_achievements.py' then double-click on the file to run it.

## Executable
The executable can be generated with pyinstaller using the following command:

```
pyinstaller --onefile --console --optimize "2" --icon "icon.ico" "minecraft_bedrock_reenable_achievements.py"
