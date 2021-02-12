from random import randint

#def printC(var):
    #if cheese_mode == False:
        #print(var)

## --------     Combat       ---------

def combat(action,choicenum1): #Player attack start
    global monster_stats
    
    if action == "Utok":
        status = attack(choicenum1,"player")
        if status == "death":
            monsters.remove(choicenum1)

def monster_attack(): #Monster attack start
    global monsters, death
    for monster in monsters:
        status = attack("player", monster)
        if status == "death":
            print("! You Died.")
            death = True

def attack(victim, attacker): #Damage being dealt
    victim_position = 0
    attacker_position = 0
    
    x = 0
    for i in monster_stats: #finding the position of the victim and the attacker
        if i == victim:
            victim_position = int(x / 5)
        if i == attacker:
            attacker_position = int(x / 5)
        x = x + 1 

    evasion = evade(victim_position)
    if evasion == "no damage":
        print("- " + victim + " evaded the attack, so no damage was dealt.")
        return "alive"

    damage = round(float(monster_stats[attacker_position * 5 + 1]) - float(monster_stats[attacker_position * 5 + 1]) * (float(monster_stats[victim_position * 5 + 3]) / 100),2)
    monster_stats[victim_position * 5 + 2] = float(monster_stats[victim_position * 5 + 2]) - damage
    remaining = monster_stats[victim_position * 5 + 2]
    if remaining < 0:
        remaining = 0

    print("- " + attacker + " attacked " + victim + " and dealt " + str(damage) + " damage, " + str(remaining) + " remaining.")
    
    if int(monster_stats[victim_position * 5 + 2]) <= 0: #control whether the victim died
        for i in range(5):
            monster_stats.pop(victim_position * 5)
        print("- The "+ victim +" died!")
        return "death"
    else:
        return "alive"

def evade(victim_position): #Did the victim evade?
    evade = randint(1,100)
    if evade <= int(monster_stats[victim_position * 5 + 4]):
        return "no damage"
    else:
        return "damage"

## -------- Input / Room read ---------

def grabItem(room,item):
    global playerInv, world_map
    playerInv.append(item)
    for i in world_map[map_pointer]:
        if i[0] == item:
            world_map[map_pointer].remove(i)
    print('- grabbed {}'.format(item))

def openDoor(door,inventory):
    global roomInx
    if door == "wooden door":
        if "key" in playerInv:
            print("Oops, the key broke. But hey, door's open!")
            roomInx.remove("wooden_door")
            roomInx.append("wooden_door_open")
        else:
            print("Door's locked.")
    else:
        print("Door's open.")
        roomInx.remove("door")
        roomInx.append("door_open")

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
    global world_map, map_pointer, player_health
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

    print('> ',end='')
    inp = input().lower().split() # Basic pre-processing

    if len(inp) != 2: # Check inst length
        if inp[0] == 'cheese':
            print('- cheese')
        else:
            print('? I\'m not sure what you want')
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

    elif inp == ["open","door"]:
        doorType = "door"
    
        if "door" in roomInx or "wooden_door" in roomInx:
            if "door" in roomInx and "wooden_door" in roomInx:
                doorType = input("There's a wooden door and one made out of whatever (just call it a door). Which one do you want to open? ").lower()
            elif "wooden_door" in roomInx:
                doorType = "wooden door"
            openDoor(doorType,playerInv)
        
        else: print("All doors are open. You cannot gaze beyond, but every so often their ambience breaks into a subtle indication of movement.")

    else:
        print('? Sorry, i dont know what you want')

    monster_attack()

    if len(monster_stats) == 5:
        monster_stats[2] = player_health
    
# --------- Global variables ---------

player_health = 15
death = False
world_map = []
map_pointer = 0
monsters = []
monster_stats = ['player','3','15','2','10']
playerInv = []

# ------ init -----
readFile()
find_room('[0,1]')
while death == False:
    console()
