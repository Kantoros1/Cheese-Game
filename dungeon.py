from random import randint

## --------     Combat       ---------

def combat(action,choicenum1):
    global monster_stats
    
    if action == "Utok":
        status = attack(choicenum1,"player")
        if status == "death":
            monsters.remove(choicenum1)

    if "player" not in monster_stats:
        return "You died"

def monster_attack():
    global monsters
    for monstrum in monsters:
        status = attack("player", monstrum)
        if status == "death":
            print("! You Died.")

def attack(victim, attacker):
    victim_position = 0
    attacker_position = 0
    
    x = 0
    for i in monster_stats:
        if i == victim:
            victim_position = int(x / 5)
        if i == attacker:
            attacker_position = int(x / 5)
        x = x + 1 

    evasion = evade(victim_position)
    if evasion == "no damage":
        return "alive"

    damage = int(monster_stats[attacker_position * 5 + 1]) - int(monster_stats[attacker_position * 5 + 1]) * (int(monster_stats[victim_position * 5 + 3]) / 100)
    monster_stats[victim_position * 5 + 2] = int(monster_stats[victim_position * 5 + 2]) - damage                       #####Chceme životy v desetinejch číslech?
    remaining = monster_stats[victim_position * 5 + 2]
    if remaining < 0:
        remaining = 0

    print("- " + attacker + " attacked " + victim + " and dealt " + str(damage) + " damage, " + str(remaining) + " remaining.")
    
    if int(monster_stats[victim_position * 5 + 2]) <= 0:
        for i in range(5):
            monster_stats.pop(victim_position * 5)
        print("- The enemy died!")
        return "death"
    else:
        return "alive"

def evade(victim_position):
    evade = randint(1,100)
    if evade <= int(monster_stats[victim_position * 5 + 4]):
        return "no damage"
    else:
        return "damage"

## -------- Input / Room read ---------

def grabItem(room,item): # For will
    print('- grabbed {}'.format(item))

def attackJ(monster): # For jirka
    combat('Utok',monster)
    
def readFile(): # reads the map file and translates into 3D list
    global world_map, map_pointer
    with open('map.txt') as F:
        
        world_map = []
        
        for roomF in F.read().split('#')[1:]: # Split file into rooms
            room = []
            for lineF in roomF.split('\n')[1:-1]: # Split rooms into lines
                room.append(lineF.split(';')[:]) # Split lines into elements
            
            world_map.append(room)

        #print(world_map)

def find_room(pointer): # Searches all rooms until it finds the same index, returns position in 3D list
        i = 0
        for room in world_map: 
            
            if room[0][2] == pointer:
                print('- ' + room[0][1])
                return i
            i += 1        

def console(): # Main class
    global world_map, map_pointer
    roomInx = world_map[map_pointer] # Copy room into buffer RoomInx
    room = [*[x[0] for x in roomInx][1:],'room'] # Creates a list of thing in the room

    # Create monster

    x = 0
    for item in roomInx[1:]:
        x += 1
        if item[3] == '1':
            monster_stats.append(item[0])
            monster_stats.extend(item[4][1:-1].split(',')) # Fixing formatting
            monsters.append(item[0])
            print('! ' + item[1])
            print('- Enemy\'s attack: {0}, Enemy\'s health: {1}, Enemy\'s armor: {2}'.format(monster_stats[-4], monster_stats[-3],monster_stats[-2]))

            del world_map[map_pointer][x]          

    inp = input().lower().split() # Basic pre-processing

    if len(inp) != 2: # Check inst length
        print('? Sorry, i dont know what you want')
    elif inp[1] not in room and inp[1] not in monsters: # Checks second par is valid
        print('? Sorry, that object is not in this room')
        
    elif inp[0] == 'examine': # Examine command
        if inp[1] == 'room': # If specified, will list all items in room
            print('- The room contains: ',end='')
            for i in room[:-1]:
                print(i,end=', ')
            print()
        else: # Prints description of item
            for item in roomInx: # looks through all items until it finds the right one
                if item[0] == inp[1]:
                    print(item[1])

    elif inp[0] == 'grab': # Grab command
        if inp[1] == 'everything': # If specified, will attempt to grab everything
            for item in roomInx:
                if item[2] == '1':
                    grabItem(map_pointer,item[0])
        else: # Grab specified item, if possible
            x = 0
            for item in roomInx:
                if item[0] == inp[1]:
                    if item[2] == '1':
                        grabItem(map_pointer,item[0])
                    else:
                        print('! Cant grab {}'.format(item[0]))
                x += 1
            

    elif inp[0] == 'attack': 
        if inp[1] in monsters:
            attackJ(inp[1])

    elif inp[0] == 'move': # TODO:// Check if door is open. also: implement closed doors
        for item in roomInx:
            if item[0] == inp[1]:
                map_pointer = find_room(item[4])

    else:
        print('? Sorry, i dont know what you want')

    monster_attack()
    
# --------- Global variables ---------

world_map = []
map_pointer = 0
monsters = []
monster_stats = ['player','3','15','2','10']

# ------ init -----
readFile()

find_room('[0,1]')
while True:
    console()
