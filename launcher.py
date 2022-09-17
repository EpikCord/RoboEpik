from os import system
from sys import platform


print("Installing dependencies...")
system("pip install -r requirements.txt --force-reinstall")
if platform.startswith("linux"):
    system("clear")
    print("Done!")
    print("Starting up...")
    system("python3 -m bot")
else:
    system("cls")
    print("Done!")
    print("Starting up...")
    system("py -m bot")
