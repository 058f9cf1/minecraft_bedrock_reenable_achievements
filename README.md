# Re-enable Minecraft Bedrock Achievements
A tool for allowing you to earn achievements on a Minecraft Bedrock world that has enabled cheats or used creative mode. After the program is run, cheats will be disabled and the default world game mode will be set to survival. Any players set to creative mode or changed gamerules will remain changed.

> [!IMPORTANT]
> Back up your worlds before using! If any corruption occurs, the worlds can then be restored.

> [!IMPORTANT]
> This is a tool for worlds on 'Minecraft for Windows', not 'Minecraft: Java Edition' or any other Minecraft Bedrock version. After the program has completed, other players on all Bedrock versions will be able to join the world and unlock achievements.

Works on Minecraft Bedrock worlds version 1.21.0 and higher. It may also work on versions below, but this is untested.


## Installation
Download the latest stable release from the [releases](https://github.com/058f9cf1/minecraft_bedrock_reenable_achievements/releases) section.

### Latest development version
Clone the repository with ```git clone https://github.com/058f9cf1/minecraft_bedrock_reenable_achievements.git```.


## Running

### Python file (Recommended method)
Ensure Python 3 is installed then either double-click on the file or run ```python minecraft_bedrock_reenable_achievements.py``` in a terminal from the directory containing the file.

### Standalone executable (Windows only)
Either double-click on the executable or run ```.\minecraft_bedrock_reenable_achievements.exe``` in a terminal from the directory containing the executable.


## Usage
When the program is run by itself on Windows, it will search the disk for Minecraft Bedrock worlds that can currently be played. You can select a world from the list of worlds found by entering the number next to the world name.

On any operating system, worlds can be done individually or multiple at once by either providing them as arguments when running the program or, on Windows, dragging-and-dropping them on to the standalone executable. The following world formats are accepted:
- World directories
- ```level.dat``` files
- Zipped world directories
- .mcworld files

The program, once completed, can be exited by pressing 'Enter'.


## Executable
The standalone executable can be generated with pyinstaller using the following command:

```
pyinstaller --onefile --console --optimize "2" --icon "icon.ico" "minecraft_bedrock_reenable_achievements.py"
