from random import randint
import os # For file creation

# - Info
# > Input
# ! Important game info
# ? Invalid input/error
# * List

# ----------- saves --------

def save():
    saves = open("saves/save_directory.txt", "a")
    name = input("- Name your savefile:\n> ").replace(' ','_')
    print('- You can now keep playing, or exit the game(end): ')
    saves.write(name + " ")
    saves.close()
    
    save = open("saves/" + name + ".txt", "w")
    for i in world_map:
        save.write("#")
        for n in i:
            save.write("\n")
            for z in n:
                save.write(z)
                if z != n[-1]:
                    save.write(";")
        save.write("\n")

    save.write("$")
    save.write(str(monster_stats) + "\n")
    save.write(str(player_health) + "\n")
    save.write(str(monsters) + "\n")
    save.write(str(playerInv) + "\n")
    save.write(str(map_pointer) + "\n")
    save.write(str(lastroom))

    save.close()

def load(name):
    global monster_stats, player_health, monsters, playerInv, map_pointer, lastroom, name_map
    x = 0
    y = 0
    monster_stats = [[]]
    load = open("saves/" + name + ".txt", "r")
    info = load.read()
    load.close()
    info_detail = info.split("$")
    info_detail = info_detail[1].split("\n")

    for i in info_detail[:-1]:
        info_detail[x] = info_detail[x].replace("]","")
        info_detail[x] = info_detail[x].replace("[","")
        info_detail[x] = info_detail[x].replace("'","")
        x += 1
    x = 0

    info_detail2 = info_detail[0].split(", ")
    
    for i in info_detail2:
        if y == 5:
            x +=1
            y = 0
            monster_stats.append([])
        monster_stats[x].append(i)
        y+=1
    
    player_health = int(info_detail[1])
    
    info_detail2 = info_detail[2].split(", ")
    if info_detail2[0] == "":
        info_detail2.pop()
    monsters = info_detail2

    info_detail2 = info_detail[3].split(", ")
    if info_detail2[0] == "":
        info_detail2.pop()
    playerInv = info_detail2
   
    map_pointer = int(info_detail[4])
    
    lastroom = info_detail[5]

    name_map = ('saves/' + name + ".txt")

    
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
        print("! " + victim + " evaded the attack, so no damage was dealt.")
        return "alive"

    damage = round(float(monster_stats[attacker_position][1]) - float(monster_stats[attacker_position][1]) * (float(monster_stats[victim_position][3]) / 100),2)
    monster_stats[victim_position][2] = float(monster_stats[victim_position][2]) - damage
    remaining = monster_stats[victim_position][2]
    if remaining < 0:
        remaining = 0

    print("! " + attacker + " attacked " + victim + " and dealt " + str(round(damage,1)) + " damage, " + str(round(remaining,1)) + " remaining.")
    
    if remaining == float(0): #control whether the victim died
        monster_stats.pop(victim_position)
        print("! The "+ victim +" died!")
        return "death"
    else:
        return "alive"

def evade(victim_position): #Did the victim evade?
    evade = randint(1,100)
    if evade <= int(monster_stats[victim_position][4]):
        return "no damage"
    else:
        return "damage"

##-------------- Menu -------------

def menu(): # Saving, loading savefiles, introduction
    global monster_stats, player_health, death, classes

    print('- Welcome to the official CheeseGame social experiment!')
    print('- Please take frequent breaks to reduce risk of bad syndrome')

    if not os.path.exists('saves'): # Creates file if it doesn't exist yet
        os.makedirs('saves')
    open("saves/save_directory.txt",'a+') # Creates directory if it doesn't exist yet
    
    dire = open("saves/save_directory.txt").read().split() # Game saves separated by single space

    if len(dire) == 0: # Count available saves, if 0, start new game automatically
        print("- No saves available, creating new game")
        new_game()
    else:
        print('- Saved games:')
        for i in dire:
            print('* ' + i)
        choice = input("- Select game, or create a new one(new):\n> ").lower()
        if choice in ['new','']:
            new_game()
        elif choice in dire:
            load(choice)
        else:
            print("! That save isn't available, starting new game")
            new_game()
            
def new_game():
    global monster_stats, player_health, death, classes
    
    print('- Available classes: ') # Print all classes
    for i in classes:
        print('* ' + i)
        
    choice = input('Select your player class:\n> ')
    
    if choice not in classes:
        choice = 'regular' # Default to regular class
        
    monster_stats.append(classes[choice]) # Create player stats

    player_health = monster_stats[0][2] # Set max health

def grabItem(item):
    global playerInv, world_map, map_pointer
    
    for thing in playerInv: # Check if same item not already in inventory. if yes, drop
        if item[4] == thing[4] and item[4].lower() != 'none':
            print(f'- can\'t hold more than one {item[4]} at once')
            dropItem(thing)
            
    playerInv.append([item[0],*[int(i) for i in item[3][1:-1].split(',')], item[4]]) # Add item to inventory
    
    for i in world_map[map_pointer]: # Find item in world map, and delete
        if i[0] == item[0]:
            world_map[map_pointer].remove(i)
    print('- grabbed {}'.format(item[0]))
    
    stats = item[3][1:-1].split(',') # Print which stats increased/decreased
    for i, st in enumerate(zip(stats,['attack','health','evade'])):
        if int(st[0]) != 0:
            dire = 'increased' if int(st[0]) > 0 else 'decreased'
            print('! Player\'s {2} {0} by {1}!'.format(dire,abs(int(st[0])),st[1]))
            monster_stats[0][i+1] += int(st[0])

    #print(monster_stats)

def dropItem(item):
    global playerInv, world_map, map_pointer
    playerInv.remove(item) # Remove item from inventoy
    print('- dropped '+item[0])
    world_map[map_pointer].append([item[0],'Dropped by player','grabable',f'[{item[1]},{item[2]},{item[3]}]',item[4]]) # Add item back to map
    
    for i, st in enumerate(zip(item[1:],['attack','health','evade'])): # Print which stats increased/decreased
        if int(st[0]) != 0:
            dire = 'increased' if int(st[0]) < 0 else 'decreased'
            print('! Player\'s {2} {0} by {1}!'.format(dire,abs(int(st[0])),st[1]))
            monster_stats[0][i+1] -= int(st[0])
    
def readFile(): # reads the map file and translates into 3D list
    global world_map, map_pointer
    with open(name_map) as F:
        
        world_map = []
        
        for roomF in F.read().split('#')[1:]: # Split file into rooms
            room = []
            for lineF in roomF.split('\n')[1:-1]: # Split rooms into lines
                room.append(lineF.split(';')[:]) # Split lines into elements
            
            world_map.append(room)

        #print(world_map)

def find_room(pointer): # Searches all rooms until it finds the same index, returns position in 3D list
        global death
        i = 0
        for room in world_map: 
            if room[0][2] == pointer:
                print('- ' + room[0][1])

                return i
            i += 1
        return
def console(): # Main class
    global world_map, map_pointer, player_health, cheese_mode, death, lastroom
    roomInx = world_map[map_pointer] # Copy room into buffer RoomInx
    room = [*[x[0] for x in roomInx][1:],'room'] # Creates a list of thing in the room

    # Create monster
    x = 0 # Current index
    for item in roomInx[1:]:
        x += 1 
        if item[2] == 'enemy': # Test type
            monster_stats.append([item[0],*[int(i) for i in item[3][1:-1].split(',')]]) # Every time i use * i want to stop coding and go live in the woods alone
            monsters.append(item[0]) # Move monster to special monster list
            print('! ' + item[1])
            print('- {3}\'s attack: {0}, {3}\'s health: {1}, {3}\'s armor: {2}'.format(monster_stats[-1][1], monster_stats[-1][2],monster_stats[-1][3],monster_stats[-1][0]))
            del world_map[map_pointer][x] # Delete monster from map
            x -= 1 # Compensate for deleted monster

    print('> ',end='')
    inp = input().lower().split() # Basic pre-processing

    if len(inp) == 0:
        print('- You do nothing...')

    elif inp[0] == 'cheese':
        print('- cheese')
        try:
            for i in open('cheese.txt').readlines(): print(i,end='')
        except:
            print('- chesse')

    elif inp[0] == 'help':
            print('- possible commands:\n* help\n* examine [object]\n* grab [object]\n* drop[object]\n* attack [monster]\n* move [door]\n* cheese')
    elif inp[0] == 'end':
            death = True
            return
    elif inp[0] == 'save':
            save()
        
    elif inp[0] in ['examine','look']: # Examine command
        if inp[1] in ['room','all','everything']: # If specified, will list all items in room
            print('- The room contains:')
            for i in room[:-1]:
                print('* ' + i)

        elif inp[1] in ['self','me','myself']:
            print('* You have {0} attack and {1} health'.format(*monster_stats[0][1:3]))
        else: # prints description of item
            for item in roomInx: # looks through all items until it finds the right one
                if item[0] == inp[1]:
                    print('- ' + item[1])
                    break
            else:
                print('? There is no object like that visible')
                
            if inp[1] in monsters:
                inx = 5* (monsters.index(inp[1]) + 1)
                print('* This {0} has {1} attack and {2} health'.format(*monster_stats[inx:inx+3]))

    elif inp[0] in ['grab','take']: # Grab command
        if inp[1] == 'everything': # If specified, will attempt to grab everything
            for item in roomInx:
                if item[2] == 'grabable':
                    grabItem(item)

        else: # Grab specified item, if possible
            for item in roomInx:
                if item[0] == inp[1]:
                    if item[2] == 'grabable':
                        grabItem(item)
                    else:
                        print('? Cant grab {}'.format(item[0]))
                    break
            else:
                print('? There is no object like that')
                
    elif inp[0] in ['drop','leave']:
        for item in playerInv:
            if item[0] == inp[1]:
                dropItem(item)
                break
        else:
            print('? No such item in inventory')

    elif inp[0] in ['attack',"brutalize"]:
        if inp[1] in monsters:
            combat('Utok',inp[1])
        else:
            print('? You can\'t attack that right now')

    elif inp[0] in ['move','open']: # TODO:// Check if door is open. also: implement closed doors
        for i, item in enumerate(roomInx):
            if item[0] == inp[1]:
                if item[2] == "door":
                    if item[4] == "unlocked":
                        map_pointer = find_room(item[3])
                        lastroom = item[3]
                    else:
                        for thing in playerInv: # Check if player even has a key
                            if thing[0] == 'key':
                                print("- The door has been unlocked, but your key got stuck in the lock")
                                world_map[map_pointer][i][4] = 'unlocked' # Unlock door in world_map for later
                                map_pointer = find_room(item[3]) # Change room
                                lastroom = item[3]
                                playerInv.remove(thing)
                            break

                        else:
                            print("? You need a key to open this door")
                else:
                    print("? You can't go through this object")

    else:
        print('? You cant do that right now')

    monster_attack()

    if len(monster_stats) == 1:
        monster_stats[0][2] = player_health
    
# --------- Global variables ---------

player_health = 10 # Health limit, not current value
death = False
name_map = 'map.txt' # Map file
lastroom = '[0,1]' # Coordinates of last room in [x,y]
world_map = [] # Entire game map as a 3D list
map_pointer = 0 # Index of current room in world_map
monsters = [] # Monsters currently attacking. 2D list // CONFLICT
monster_stats = [] # Monsters currently attacking with stats // CONFLICT
playerInv = [] # Player inventory with stats. 2D list
classes = {'regular':['player',3,10,12,5],'tank':['player',2,15,10,2],'rogue':['player',4,7,15,10]}

# ------ init -----
menu()
readFile()
find_room(lastroom)

while death == False:
    console()
