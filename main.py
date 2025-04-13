# Import every individual needed instruction
# for the sake of performance, and to save
# some memory in case you have a potato
# device.
from os import remove, mkdir, rmdir
from shutil import copytree, copy2, rmtree
from requests import get
from zipfile import ZipFile
from sys import exception

# Custom paths are not only supported, but mandatory.
# Allows to use different paths without editing any script manually.

# Also, these are not constants, don't get fooled.
# Changed these from constants to normal variables when it was too late.
SD_CARD = "[UNSET]" # SD card
WORKDIR = "./temp/" # Work directory (temp directory)
SPATH = "[UNSET]" # Path to the script to run.

attributes = set()
# instruction that translates paths.
def dir_transl(path: str) -> str:
    path = path.strip()

    if path.upper().startswith("SD:"):
        path = path.replace("SD:", SD_CARD+"/", 1)
    elif path.upper().startswith("WORK:"):
        path = path.replace("WORK:", WORKDIR+"/", 1)
    
    return path

# Some useful definitions.
# they are here in case I need to do a quick fix.
# Or, If I want to modify the behaviour of an
# action I can easily edit the instructions from
# here, rather than change the instruction every
# time it is used.
class instr:
    tryagainflag = False # needed for later

    def copy(fname: str, dest: str) -> None: # copy a file and paste it somewhere else.
        print("Copying", fname, "to", dest)
        #open(dest, "wb").write(open(fname, "rb").read())
        #[ COPY DATA TO DEST  ] [ READ FILE DATA       ]
        copy2(fname, dest)

    def delete(fname: str) -> None: # delete a file.
        print("deleting", fname)
        remove(fname)

    def newdir(dir_: str) -> None: # create a directory.
        print("Creating directory", dir_)
        try:
            mkdir(dir_)
        except:
            print("Directory already exists, ignoring")
        
    def copydir(dir_: str, dest: str) -> None: # copy the contents of a directory from one place to another.
        print("Copying contents of", dir_, "to", dest)
        copytree(dir_, dest)

    def deldir(dir_: str) -> None: # delete a directory.
        print("Deleting", dir_)
        rmdir(dir_)
    
    def rdeldir(dir_: str) -> None:
        print("Recursively deleting", dir_)
        rmtree(dir_)

    def download(url: str, saveas: str) -> None: # download a file and save it.
        print(f"Downloading {url} and saving as {saveas}")
        open(saveas, "wb").write(get(url).content)
       #[ CREATE DEST    ] [ GET AND SAVE DATA   ]

    def extract(fname: str, dest) -> None: # extract the contents of a .zip file
        print(f"Extracting {fname} in {dest}")
        ZipFile(fname, 'r').extractall(dest)
       #[ READ ZIP FILE   ] [ EXTRACT IT   ]
    
    def yninput(ask: str, e_msg: str = "Not valid!") -> str:
        while True:
            res = input(ask).lower()
            if res == "y":
                return True
            elif res == "n":
                return False
            else:
                print(e_msg)
    
    def pause():
        input("Press [RETURN] to continue...")

tryagainflag = 0 # This is important for later

# execute a single instruction of the file.
def run_instr(instr_: str):
    """
     0: successful
    -1: failed, intruction not found
    -2: "selection go back action".
        goes back from the current line being read in the script
        until it finds an instruction that is not NOTICE.
    -3: "selection go back action" with error.
    """

    if instr_.endswith("\n"): # Remove new-line characters ('\n')
        instr_ = instr_[:-1]

    if instr_.startswith("#") or instr_ == "": # comment handling.
        return 0
    else:
        args = instr_.split()
        inst_name = args.pop(0).upper()
        temp0 = instr_.split(maxsplit=1)
        if len(temp0) > 1:
            args_str = temp0[1]
        else:
            args_str = ""
        del temp0

        if inst_name == "NOTICE":
            print("NOTICE: "+args_str)
            instr.pause()
        
        elif inst_name == "LOG":
            print("LOG: "+args_str)

        elif inst_name == "DOWNLOAD": # Download a file from the internet
            instr.download(args[0], dir_transl(args[1]))

        elif inst_name == "COPY": # Copy a file and paste it somewhere else
            instr.copy(dir_transl(args[0]), dir_transl(args[1]))

        elif inst_name == "DELETE": # Delete a file
            for i in args:
                instr.delete(dir_transl(i))
            
        elif inst_name == "NEWDIR": # Make one of more directories
            for i in args:
                instr.newdir(dir_transl(i))
            
        elif inst_name == "COPYDIR": # Copy the contents of a directory in another directory
            instr.copydir(dir_transl(args[0]), dir_transl(args[1]))
            
        elif inst_name == "DELDIR": # Remove a directory (as long as it is empty)
            for i in args:
                instr.deldir(dir_transl(i))
        
        elif inst_name == "RDELDIR":
            for i in args:
                instr.rdeldir(dir_transl(i))
            
        elif inst_name == "EXTRACT":
            instr.extract(dir_transl(args[0]), dir_transl(args[1]))
            
        elif inst_name == "ATTRYN":
            if instr.yninput(f"Add {args} to attributes? (y/n) "):
                for i in args:
                    attributes.add(i)
              
        elif inst_name == "ATTRSEL":
            if instr.tryagainflag:
                print("(Your previous selection was invalid, try again)")
                instr.tryagainflag = False

            selection = -1
            try:
                selection = int(input(f"Insert a number from 1 to {len(args)} and hit [RETURN]:\n? >"))
            except:
                return -3
                
            if selection < 1 or selection > len(args):
                return -3
            else:
                attributes.add(args[selection-1])

        elif inst_name == "ATTRMSEL":
            if instr.tryagainflag:
                print("(Your previous selection was invalid, try again)")
                instr.tryagainflag = False
            try:
                inp = input(f"Insert one or more number from 1 to {len(args)} separated by a comma and then hit [RETURN]:\n? >").split(",")
                for i in range(len(inp)):
                    inp[i] = inp[i].strip()
                    temp0 = int(inp[i])
                    if temp0 < 1 or temp0 > len(args):
                        return -3
                    else:
                        temp0 -= 1
                        attributes.add(args[temp0])
            except:
                return -3

        elif inst_name == "NOTHING":
            pass

        else: return -1

    return 0

def runScript(): # Read, prepare and run the whole script.
    print("Reading script...")
    try:
        scriptlines = open(SPATH, "r").readlines()
    except:
        print("Error: Script not found!")
        return None
    
    try:
        instr.newdir(WORKDIR)
    except:
        # The line below is what makes this thing dangerous
        instr.rdeldir(WORKDIR)
        instr.newdir(WORKDIR)
    
    print("Preparing script...")
    i = 0
    for i in range(len(scriptlines)):
        scriptlines[i] = scriptlines[i].strip()
    
    print("Running script...\n")
    i = 0
    while i < len(scriptlines):
        j = scriptlines[i]
        if j.upper().startswith("SECTION "): #BUG: Sections (probably) do not work properly
            if j.strip()[8:].find(" ") != -1:
                print("Error: multiple arguments for a single section declaration are not yet supported!")
                break
            elif j.strip()[8:] not in attributes:
                height = 1
                height_old = 0
                while height != height_old:
                    i += 1
                    j = scriptlines[i]

                    if j.upper().startswith("SECTION "):
                        height += 1
                    elif j.upper().startswith("ENDSECTION"):
                        height -= 1

        elif j.upper().startswith("ENDSECTION"): pass

        else: # Run instruction and handle errors properly
            try: # Run instruction
                result = run_instr(j)
            except: # Exception handling
                print(f"Error on line {i+1}: an exception occoured ({exception()})") # Tell user about exception...
                break # ...And stop execution.
            if result != 0: # Check errors that are not exceptions
                errorlist = {
                    -1: "Unknown command name"
                }
                if result in errorlist.keys():
                    print(f"Error on line {i+1}: {errorlist}")
                    break
                
                elif result == -3 or result == -2:
                    i -= 1
                    while scriptlines[i].upper().startswith("LOG "):
                        i -= 1
                    if result == -3:
                        instr.tryagainflag = True
                else:
                    print(f"Error on line {i+1}: An unknown error occoured ({result})")
                    break
        i += 1
    
    print("# SCRIPT EXECUTION ENDED #")
    instr.pause()
    


# The main loop.
while True:
    titleScreen = f"""
Welcome to the PScrInt!
----+-----------
    |
    +-- 0: Choose the script to run (Quite self-explanatory).
    |      Currently: {SPATH}
    |
    +-- 1: Choose output directory (your SD card, most of the time).
    |      Currently: {SD_CARD}
    |
    +-- 2: Choose work directory (Where temporary files will be stored).
    |      Currently: {WORKDIR}
    |
    |
    +---- R: Run the script!
    |
    +-- Q: Exit
    """
    print(titleScreen)
    chosen = input("You may choose one, then you may hit [RETURN] to confirm:\n? >").strip().upper() # the '.strip().upper()' makes everything more user-friendly

    if chosen == "0":
        SPATH_ = input("\nPlease obtain the full path to the script and paste it here.\nOr, if your system allows it, you can simply drag it and drop it here.\nPlease remember to remove quotes if there are any.\nAfter that, press [RETURN].\nLeave the prompt empty to leave the current selection unchanged.\n\nSCRIPT >").strip()
        if SPATH_ != "":
            SPATH = SPATH_
        del SPATH_

    elif chosen == "1":
        SD_CARD_ = input("\nPlease obtain the full path to the output directory and paste it here.\nThis is your SD card most of the time.\nIf there are any quotes, remove them.\nAfter that, press [RETURN].\nLeave the prompt empty to leave the current selection unchanged.\n\nOUT >").strip()
        if SD_CARD_ != "":
            SD_CARD = SD_CARD_
        del SD_CARD_

    elif chosen == "2":
        WORKDIR_ = input("\nChoose a directory where temporary files will be stored.\nNormally, it is not necessary to edit this.\nAfter that, press [RETURN].\nLeave the prompt empty to leave the current selection unchanged.\n\n? >").strip()
        if WORKDIR_ != "":
            WORKDIR = WORKDIR_
        del WORKDIR_

    elif chosen == "R":
        if SPATH == "[UNSET]":
            print("Please specify the path to the script!")
        elif SD_CARD == "[UNSET]":
            print("Please specify the output directory!")
        else:
            runScript()

    elif chosen == "Q":
        quit()

    elif chosen == "": pass
    else: print(f"Error: '{chosen}' is not a valid option!")
