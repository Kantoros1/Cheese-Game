from random import randint
        
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
        if i[0] == victim:
            victim_position = x
        if i[0] == attacker:
            attacker_position = x
        x = x + 1 

    evasion = evade(victim_position)
    if evasion == "no damage":
        print("- " + victim + " evaded the attack, so no damage was dealt.")
        return "alive"

    damage = round(float(monster_stats[attacker_position][1]) - float(monster_stats[attacker_position][1]) * (float(monster_stats[victim_position][3]) / 100),2)
    monster_stats[victim_position][2] = float(monster_stats[victim_position][2]) - damage
    remaining = monster_stats[victim_position][2]
    if remaining < 0:
        remaining = 0

    print("- " + attacker + " attacked " + victim + " and dealt " + str(round(damage,1)) + " damage, " + str(round(remaining,1)) + " remaining.")
    
    if int(monster_stats[victim_position][2]) <= 0: #control whether the victim died
        monster_stats.pop(victim_position)
        print("- The "+ victim +" died!")
        return "death"
    else:
        return "alive"

def evade(victim_position): #Did the victim evade?
    evade = randint(1,100)
    if evade <= int(monster_stats[victim_position][4]):
        return "no damage"
    else:
        return "damage"

## -------- Input / Room read ---------

def grabItem(room,item):
    global playerInv, world_map
    playerInv.append(item[0])
    for i in world_map[map_pointer]: # Find item in world map, and delete
        if i[0] == item[0]:
            world_map[map_pointer].remove(i)
    print('- grabbed {}'.format(item[0]))
    stats = item[3][1:-1].split(',')
    for i, st in enumerate(zip(stats,['attack','health','evade'])):
        if int(st[0]) != 0:
            dire = 'increased' if int(st[0]) > 0 else 'decreased'
            print('- Player\'s {2} {0} by {1}!'.format(dire,abs(int(st[0])),st[1]))
            monster_stats[0][i+1] += int(st[0])

def attackJ(monster): # For jirka
    combat('Utok',monster)
    
def readFile(): # reads the map file and translates into 3D list
    global world_map, map_pointer
    with open('map 0.6.txt') as F:
        
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
    global world_map, map_pointer, player_health, cheese_mode
    roomInx = world_map[map_pointer] # Copy room into buffer RoomInx
    room = [*[x[0] for x in roomInx][1:],'room'] # Creates a list of thing in the room

    # Create monster

    x = 0
    for item in roomInx[1:]:
        x += 1
        if item[2] == 'enemy':
            monster_stats.append([item[0],*[int(i) for i in item[3][1:-1].split(',')]]) # Every time i use * i want to stop coding and go live in the woods alone
            monsters.append(item[0])
            print('! ' + item[1])
            print('- Enemy\'s attack: {0}, Enemy\'s health: {1}, Enemy\'s armor: {2}'.format(monster_stats[-1][1], monster_stats[-1][2],monster_stats[-1][3]))

            del world_map[map_pointer][x]          

    print('> ',end='')
    inp = input().lower().split() # Basic pre-processing

    if len(inp) != 2: # Check inst length
        if inp[0] == 'cheese':
            print('- cheese')
            for i in open('cheese.txt').readlines(): print(i,end='')
            

        elif inp[0] == 'help':
            print('- possible commands:\n- help\n- examine [object]\n- grab [object]\n- attack [monster]\n- move [door]\n- cheese')
        else:
            print('? I\'m not sure what you want')
        
    elif inp[0] == 'examine': # Examine command
        if inp[1] == 'room': # If specified, will list all items in room
            print('- The room contains:')
            for i in room[:-1]:
                print('- ' + i)
        else: # prints description of item
            for item in roomInx: # looks through all items until it finds the right one
                if item[0] == inp[1]:
                    print(item[1])
            if inp[1] in monsters:
                inx = 5* (monsters.index(inp[1]) + 1)
                print('- This {0} has {1} attack and {2} health'.format(*monster_stats[inx:inx+3]))

    elif inp[0] == 'grab': # Grab command
        if inp[1] == 'everything': # If specified, will attempt to grab everything
            for item in roomInx:
                if item[2] == 'grabable':
                    grabItem(map_pointer,item)
        else: # Grab specified item, if possible
            x = 0
            for item in roomInx:
                if item[0] == inp[1]:
                    if item[2] == 'grabable':
                        grabItem(map_pointer,item)
                    else:
                        print('! Cant grab {}'.format(item[0]))
                x += 1
            

    elif inp[0] in ['attack',"brutalize"]:
        if inp[1] in monsters:
            attackJ(inp[1])

    elif inp[0] == 'move': # TODO:// Check if door is open. also: implement closed doors
        for item in roomInx:
            if item[0] == inp[1]:
                if item[2] == "door":
                    if item[4] == "unlocked":
                        map_pointer = find_room(item[3])
                    else:
                        if "key" in playerInv:
                            map_pointer = find_room(item[3])
                            playerInv.remove("key")
                            print("- You had to use one of you keys to unlock the door. it broky now")
                        else:
                            print("- Bich you ain' got no damn key in this hoe")
                else:
                    print("- This ain' no damn door, fool")

    else:
        print('? Sorry, i dont know what you want')

    monster_attack()

    if len(monster_stats) == 1:
        monster_stats[0][2] = player_health
    
# --------- Global variables ---------

player_health = 15
death = False
world_map = []
map_pointer = 0
monsters = []
monster_stats = [['player',3,15,2,10]]
playerInv = []
cheese_mode = False

# ------ init -----
readFile()
find_room('[0,1]')

while death == False:
    console()
