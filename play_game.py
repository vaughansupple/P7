import json
import os
import time

def main():
    json_files=[]
    for file in os.listdir():
        if file[-5:]=='.json':
            json_files.append(file)
    if len(json_files)==0:
        print('No adventure files found!')
        return
    print("Which game do you want to play?")
    for i in range(len(json_files)):
        print(str(i+1)+'. '+json_files[i])
    filenumber = input("> ").lower().strip()
    try:
        num = int(filenumber) - 1
        filename = json_files[num]
    except:
        print("I don't understand '{}'...".format(filenumber))
        return
    with open(filename) as fp:
        game = json.load(fp)
    print_instructions()
    print("You are about to play '{}'! Good luck!".format(game['__metadata__']['title']))
    print("")
    play(game)


def play(rooms):
    if not check_all_exits(rooms):
        print("This game board has exits that lead to nowhere!")
    starttime = time.time()
    current_place = rooms['__metadata__']['start']
    stuff = ['Cell Phone; no signal or battery...']

    while True:
        here = rooms[current_place]
        print(here["description"])
        if len(here["items"])!=0:
            for i in here["items"]:
                print("There is a " + i)
        if here.get("ends_game", False):
            break

        usable_exits = find_usable_exits(here, stuff)
        for i, exit in enumerate(usable_exits):
            print("  {}. {}".format(i+1, exit['description']))

        action = input("> ").lower().strip()

        if action in ["quit", "escape", "exit", "q"]:
            print("You quit.")
            break
        
        if action == 'help':
            print_instructions()
            continue
        if action == 'stuff':
            if len(stuff) == 0:
                print('You have nothing.')
            else:
                print("=== Items ===")
                for s in stuff:
                    print(s)
                print("=== Items ===")
            continue
        if action == 'take':
            stuff.extend(here["items"])
            here["items"] = []
            continue
        if action == 'drop':
            print("Which item?")
            for i in range(len(stuff)):
                print(str(i + 1) +'. '+stuff[i])
            whichitem = input("> ").lower().strip()
            try:
                num = int(whichitem) - 1
                here["items"].append(stuff.pop(i))
            except:
                print("I don't understand '{}'...".format(whichitem))
            continue
        if action in ['search','find']:
            print('Searching for hidden exits...')
            for e in here['exits']:
                e['hidden'] = False
            continue

        try:
            num = int(action) - 1
            selected = usable_exits[num]
            if 'required_key' in selected:
                if selected['required_key'] not in stuff:
                    print("You try to open the door, but it's locked!")
                    continue
            current_place = selected['destination']
            print("...")
        except:
            print("I don't understand '{}'...".format(action))
        
    print("")
    print("")
    endtime=time.time()
    elapsedtime = endtime-starttime
    print("It took you " + str(int(elapsedtime//60)) + " minutes and " + str(int(elapsedtime%60)) + "seconds. GAME OVER")

def find_usable_exits(room, stuff):
    """
    Given a room, and the player's stuff, find a list of exits that they can use right now.
    That means the exits must not be hidden, and if they require a key, the player has it.

    RETURNS
     - a list of exits that are visible (not hidden) and don't require a key!
    """
    usable = []
    for exit in room['exits']:
        if exit.get("hidden", False):
            continue
        usable.append(exit)
    return usable
                                                                        
def check_all_exits(rooms):
    for r in rooms:
        if r == '__metadata__':
            continue
        for e in rooms[r]['exits']:
            if e['destination'] not in rooms:
                return False
    return True
    
def print_instructions():
    print("=== Instructions ===")
    print(" - Type a number to select an exit.")
    print(" - Type 'stuff' to see what you're carrying.")
    print(" - Type 'take' to pick up an item.")
    print(" - Type 'quit' to exit the game.")
    print(" - Type 'search' to take a deeper look at a room.")
    print("=== Instructions ===")
    print("")

if __name__ == '__main__':
    main()
