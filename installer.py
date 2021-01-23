import glob
import os
import platform
import pythoncom
import requests
import shutil
import time
import winshell
import win32api
import win32com.client
import zipfile
from clint.textui import progress
from pathlib import Path

class Variables():
    def __init__(self):
        self.amongusexe = ""
        self.chosen_drv = ""
        self.drives = ""
        self.exepath = ""
        self.extractpath = ""
        self.modlink = ""
        self.modpath = ""
        self.modversion = ""
        self.scriptpath = ""
        self.sheriffpath = ""
        self.steampath= ""
        self.zippath = ""

var = Variables()

def clear():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def copyamongus():
    temppath = var.steampath + "/Among Us"
    var.sheriffpath = var.steampath + "/Among Us Sheriff Mod"
    if glob.glob(var.sheriffpath, recursive=True):
            shutil.rmtree(var.sheriffpath)
            print("Alte Sheriff Mod Version gelöscht.")
            time.sleep(5)
    shutil.copytree(temppath, var.sheriffpath)

def copymod():
    os.chdir(var.zippath)
    files = ['BepInEx', 'mono', 'doorstop_config.ini', 'steam_appid.txt', 'winhttp.dll']
    for f in files:
        shutil.move(f, var.sheriffpath)
    var.exepath = var.sheriffpath + '/Among Us.exe'
    print("Dateien erfolgreich verschoben.")
    time.sleep(5)

def createshortcut():
    desktop = winshell.desktop()

    path = os.path.join(desktop, 'Among Us Sheriff Mod.lnk')
    target = var.exepath
    icon = var.sheriffpath + "/pink.ico"

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.IconLocation = icon
    shortcut.save()


def drive():
    clear()
    var.drives = win32api.GetLogicalDriveStrings()
    var.drives = var.drives.split('\000')[:-1]
    i = 0
    while i < len(var.drives):
        print(str(i) + ": " + '"' +str(var.drives[i]) + '"')
        i += 1
    print('99: Such Steam für mich.')
    var.chosen_drv = input("Auf welcher Festplatte ist Steam: ")
    if var.chosen_drv == "99":
        drive_length = len(var.drives)
        i = 0
        while i < drive_length:
            clear()
            os.chdir(var.drives[i])
            print('Suche auf Festplatte "' + var.drives[i] + '".')
            tmppath = glob.glob('**/common/Among Us/Among Us.exe', recursive=True)
            if "Among Us" in str(tmppath):
                var.chosen_drv = var.drives[i]
                var.steampath = var.chosen_drv + tmppath[0]
                var.steampath = var.steampath.split(r"\A")
                var.steampath = var.steampath[0]
                print('Gefunden auf Festplatte "' + var.drives[i] + '" mit dem Pfad "' + var.steampath + '".')
                i = drive_length
            i += 1
    else:
        clear()
        var.chosen_drv = var.drives[int(var.chosen_drv)]
        os.chdir(var.chosen_drv)
        find()

def find():
    clear()
    var.amongusexe = glob.glob('**/Among Us.exe', recursive=True)
    i = 0
    while i < len(var.amongusexe):
        print(str(i) + ": " + '"' + str(var.amongusexe[i]) + '"')
        i += 1
    temp = input("Welche Exe ist die Richtige: ")
    var.amongusexe = var.amongusexe[int(temp)]
    var.steampath = var.chosen_drv + var.amongusexe
    var.steampath = var.steampath.split(r"\A")
    var.steampath = var.steampath[0]

def getpath():
    var.scriptpath = os.path.realpath(__file__)
    var.scriptpath = var.scriptpath.split(r"\installer")
    var.scriptpath = var.scriptpath[0]

def removetrash():
    os.chdir(var.scriptpath)
    os.rmdir(var.zippath)
    print("Müll entfernt.")
    time.sleep(5)

def zip():
    clear()
    var.modversion = input("Modversion: ")
    var.modlink = "https://github.com/Woodi-dev/Among-Us-Sheriff-Mod/releases/download/v" + var.modversion + "/Among.Us.Sheriff.Mod." + var.modversion + ".zip"
    print("Lädt Sheriff Mod Version " + var.modversion + " von " + var.modlink + " herunter.")
    r = requests.get(var.modlink, allow_redirects=True)
    with open('sheriffmod_v' + var.modversion + ".zip", 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
            if chunk:
                f.write(chunk)
                f.flush()
    print("Heruntergeladen!")
    print("Zip Datei wird entpackt.")
    target = 'sheriffmod_v' + var.modversion + ".zip"
    handle = zipfile.ZipFile(target)
    handle.extractall(var.scriptpath + '\\sheriffmodzip')
    var.zippath = var.scriptpath + '\\sheriffmodzip'
    print("Zip Datei entpackt auf " + var.zippath)
    time.sleep(5)

if __name__ == "__main__":
    getpath()
    zip()
    drive()
    copyamongus()
    copymod()
    removetrash()
    createshortcut()