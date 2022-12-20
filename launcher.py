from os import system
from sys import platform


print("Installing dependencies...")

system("pip install -r requirements.txt --force-reinstall")

if platform.startswith("linux"):
    system("clear")
else:
    system("cls")

print("Starting up...")
system("py -m bot")
