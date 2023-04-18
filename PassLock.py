### [== Computer Password Locker ==] ###
# This script uses MD5 hashing, so the 'PassHash' variable should be an MD5 hash value. DO NOT USE ONLINE SITES TO GET AN MD5 HASH, YOU MIGHT LEAK YOUR PASSWORD(S)!
# Instead of using an online converter, use the python script called 'PassEncryption.py'! This will generate an encrypted MD5 hash, Fernet key, and encrypted password file.
# The key file path should be assigned to 'DecryptionKeyPath', the password file path should be assigned to 'PasswordFilePath', and 'UsePasswordFile' should be set to true.
# If you would not like to use a password file, you can simply set 'PassHash' to the MD5 value that was also generated with said script. 'UsePasswordFile' must be set to false!
# For testing purposes, the password can be set to "TestPassword" (without the quotation marks). The hash should be set to: 23fd44228071730e3457dc5de887b3ae

# [===== Imports =====] #
from cryptography.fernet import Fernet
from pywinauto import Desktop
from threading import Thread
import subprocess, hashlib, time, sys, os
import keyboard
import maskpass
import win32gui
import win32con
import pynput
import shutil

# [===== Variables =====] #
ShutdownMessage = "You have entered an incorrect password too many times. The computer will shut down in 10 seconds."
PassHash = "23fd44228071730e3457dc5de887b3ae"
EnteredPassHash = ""
PassHint = "No hint set"
UsePasswordFile = True
ShowHint = True
StopThread = False
CorrectPassword = False
RemainingAttempts = 3
WindowStates = []
Windows = []
TopWindows = []
DecryptionKeyPath = "C:\\ExamplePath\\key.key"
PasswordFilePath = "C:\\ExamplePath\\pass.txt"

# [===== Functions =====] #
# Kill explorer over and over in case the user somehow manages to start it
def KillExplorer():
    while StopThread == False:
        try:
            subprocess.run("taskkill /IM explorer.exe /F", capture_output = True)
        except:
            0+0
            
        time.sleep(0.1)

    # Restart explorer and restore all windows that might've been open
    # This only happens once the correct password has been entered
    if CorrectPassword:
        mouse_listener.stop()
        os.system("start explorer.exe")
        for Window in Desktop(backend="uia").windows():
            SetWindowState(Window.window_text())

# Win32 api stuff for managing windows
def WindowEnumHandler(hwnd, TopWindows):
    TopWindows.append((hwnd, win32gui.GetWindowText(hwnd)))

def SetWindowState(WindowName):
    for Window in TopWindows:
        if WindowName.lower() in Window[1].lower():
            win32gui.ShowWindow(Window[0], WindowStates[Windows.index(WindowName.lower())])
            win32gui.SetForegroundWindow(Window[0])
            break

def PopulateWindowVariables():
    win32gui.EnumWindows(WindowEnumHandler, TopWindows)
    for WindowItem in Desktop(backend="uia").windows():
        for Window in TopWindows:
            if WindowItem.window_text().lower() in Window[1].lower():
                Windows.append(WindowItem.window_text().lower())
                WindowStates.append(win32gui.GetWindowPlacement(Window[0])[1])

def PrintCenter(s):
    print(s.center(shutil.get_terminal_size().columns))

# [===== Main Code =====] #
# If the pre-set password hash is not set, exit
if PassHash == "" or PassHash == None:
    print("There is no password set!")
    sys.exit(-1)

# Determine if we need to decrypt a password file
if UsePasswordFile:
    # Use the fernet key that was generated at a previous date/time
    with open(DecryptionKeyPath, 'rb') as KeyFile:
        Key = KeyFile.read()
        
    fernet = Fernet(Key)
     
    # opening the encrypted file
    with open(PasswordFilePath, 'rb') as EncFile:
        Encrypted = EncFile.read()
     
    # decrypting the file
    PassHash = fernet.decrypt(Encrypted).decode("utf-8")

# Disable the mouse
mouse_listener = pynput.mouse.Listener(suppress = True)
mouse_listener.start()

# Populate the 'WindowStates', 'Windows', and 'TopWindows' tuples
PopulateWindowVariables()

# Clear the screen, minimize all inactive windows, and kill explorer 
os.system("cls")
keyboard.press_and_release("win+home")
Thread(target=KillExplorer).start()

# Lock the computer until the user enters the correct password
print("""╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║               The computer has been locked!               ║
║ Please enter the correct password to unlock the computer. ║
║         Press CTRL to toggle password visibility.         ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝""")
while True:
    # Get the MD5 hash of the entered text
    try:
        if RemainingAttempts > 0:
            EnteredPassHash = str(hashlib.md5(maskpass.advpass(prompt = "Password >> ", mask = "*").encode()).hexdigest())
    except:
        0+0

    # If the hash is equal to a pre-set hash, unlock the computer
    if EnteredPassHash == PassHash:
        os.system("cls")
        print("""╔══════════════════════════╗
║ Correct password entered ║
╚══════════════════════════╝""")
        StopThread = True
        CorrectPassword = True
        sys.exit(0)

    # If the user entered the wrong password, decrement the remaining attempts they have
    RemainingAttempts = RemainingAttempts - 1

    # Determine if we should show a hint
    if ShowHint and PassHint != "" and PassHint != None:
        print("Incorrect password! {0} attempt(s) remaining.\nHint: {1}\n".format(RemainingAttempts, PassHint))
    else:
        print("Incorrect password! {} attempt(s) remaining.\n".format(RemainingAttempts))

    # If there are no more attempts, shut down the computer
    if RemainingAttempts <= 0:
        os.system("cls")
        print("""╔═════════════════════════════╗
║ Incorrect password entered! ║
╚═════════════════════════════╝""")
        os.system("shutdown /s /t 10 /c \"{}\"".format(ShutdownMessage))
        while True:
            keyboard.press_and_release("win+down")
            time.sleep(0.1)
