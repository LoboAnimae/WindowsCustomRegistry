from shutil import copy, rmtree
from os import listdir, makedirs, rmdir, system, getcwd, path
from sys import argv
import winreg


targetDirectory = ""
localDirectory = path.dirname(path.join(argv[0]))

try:
    targetDirectory = argv[1]
except:
    targetDirectory = "C:\Windows\CustomIcons"


enterIcons = path.isdir(targetDirectory)
ignoreFile = f"{localDirectory}\\.regignore"
useIgnoreFile = path.isfile(ignoreFile)

if enterIcons:
    print("Icons folder found!")
else:
    print("No icons folder found")

if useIgnoreFile:
    print("Ignore Reg file found. Using.")
else:
    print("No .regignore file found. Skipping...")


try:
    rmtree(f"{localDirectory}\\backup", ignore_errors=True)
    print("Removed old version of backup folder")
except Exception as e:
    print(e)

try:
    makedirs(f"{localDirectory}\\backup")
    print("Created backup folder")
    makedirs(f"{localDirectory}\\backup\\icons")
    print("Created backup\\icons")
    makedirs(f"{localDirectory}\\backup\\regs")
    makedirs(f"{localDirectory}\\backup\\regs\\background")
    makedirs(f"{localDirectory}\\backup\\regs\\surface")
    print("Created backup\\regs")
except:
    pass


if enterIcons:
    for filename in listdir(targetDirectory):
        if filename.endswith(".ico"):
            print(f"Backing up {filename}")
            copy(f"{targetDirectory}\\{filename}",
                 f"{localDirectory}\\backup\icons")


ignored = ""


def backupKeys(rootKey, exportDirectory, exportLocalDirectory):
    names = []
    i = 0
    try:
        while True:
            reg = winreg.EnumKey(rootKey, i)
            if reg not in readFile:
                names.append(reg)
            i = i + 1
    except:
        pass

    for i in names:
        system(
            f"REG EXPORT \"{exportDirectory}\\{i}\" \"{localDirectory}\\{exportLocalDirectory}\\{i}.reg\" /y")
        print(f"Exported {i}")


if useIgnoreFile:
    with open(f"{localDirectory}\\.regignore", "r") as f:
        readFile = f.read().split("\n")

        keyRoot = winreg.ConnectRegistry(
            None, winreg.HKEY_CLASSES_ROOT)

        directoryRootKey = winreg.OpenKey(keyRoot, "Directory")
        backgroundShell = winreg.OpenKey(directoryRootKey, "background")
        backgroundShell = winreg.OpenKey(backgroundShell, "shell")
        backupKeys(backgroundShell,
                   "HKLM\\SOFTWARE\\Classes\\Directory\\background\\shell", "backup\\regs\\background")
        backgroundShell = winreg.OpenKey(directoryRootKey, "shell")
        backupKeys(backgroundShell,
                   "HKLM\\SOFTWARE\\Classes\\Directory\\shell", "backup\\regs\\surface")

    # print(readFile)


input("Press enter to continue...")
