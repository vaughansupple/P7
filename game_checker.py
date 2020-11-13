import json
import os

def main():
    print("Choose a game to check.")
    json_files = []
    for file in os.listdir():
        if file[-5:]=='.json':
            json_files.append(file)
    if len(json_files)==0:
        print('No adventure files found!')
        return
    print("Which game should be checked?")
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
    print("Checking game '{}'".format(game['__metadata__']['title']))
    print("")
    check(game)
    
def check(rooms):
    if not check_all_exits(rooms):
        print("This game board has exits that lead nowhere")
    current_place = rooms['__metadata__']['start']
    here = rooms[current_place]
    if check_for_exits(rooms, here):
        print('An exit exists')
    else:
        print('No exit exists')
        
def check_for_exits(rooms, room, visited = []):
    if room.get('ends_game', False):
        return True
    for e in room.get('exits',[]):
        if e['destination'] not in visited:
            new_visited = visited.copy()
            new_visited.append(room['name'])
            if check_for_exits(rooms, rooms[e['destination']], new_visited):
                return True
    return False

def check_all_exits(rooms):
    for r in rooms:
        if r == '__metadata__':
            continue
        for e in rooms[r]['exits']:
            if e ['destination'] not in rooms:
                return False
    return True

if __name__ == '__main__':
    main()