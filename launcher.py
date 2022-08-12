from os import system
print("Installing dependencies...")
system("pip install -r requirements.txt --force-reinstall")
system("cls")
print("Done!")
print("Starting up...")
system("py -m bot")