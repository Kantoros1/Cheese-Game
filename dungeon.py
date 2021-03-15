import random
from itertools import chain
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
    save.write("#")
    for i in world_map:
        for n in i:
            save.write("\n")
            for z in n:
                save.write(z)
                if z != n[-1]:
                    save.write(";")
        save.write("\n")
        save.write("#")

    save.write("$")
    save.write(str(monster_stats) + "\n")
    save.write(str(player_health) + "\n")
    save.write(str(playerInv) + "\n")
    save.write(str(map_pointer) + "\n")
    save.write(str(lastroom) + "\n")
    save.write(str(equiped_len) + "\n")
    save.write(str(basic_len))

    save.close()

def load(name):
    global monster_stats, player_health, playerInv, map_pointer, lastroom, name_map, equiped_len, basic_len
    playerInv = []
    x = 0
    y = 0
    monster_stats = []
    load = open("saves/" + name + ".txt", "r")
    info = load.read()
    load.close()
    info_detail = info.split("$")
    info_detail = info_detail[1].split("\n")
    lastroom = info_detail[4]
    equiped_len = [int(i) for i in info_detail[5][1:-1].split(',')]

    info_detail5 = info_detail[2].split(']')
    

    check = False
        ###### splits three dimensional list, so it can be put back together in program
    for info in info_detail[2].split('[['): 
        if info == info_detail[2].split(('[['))[-1]:
            info = info + ','
        info = info.replace("'", '')
        item = []
        for more_info in info.split('['):
            more_info = more_info.replace(']', '').replace(' ','')
            if more_info != '':
                more_info = more_info[:-1].split(',')
                item.append([more_info[0],*[int(i) for i in more_info[1:-1]], more_info[-1]]) 
                check = True
        if check == True:
            playerInv.append(item)
            check = False
    
    x = 0
    #### splits two dimensional list, so it can be put back together in program
    for i in info_detail[0].split(']')[:-2]:
        monster = []
        i = i.replace('[', '').replace("'",'').replace(' ','')
        more = i.split(',')
        if '' in more:
            more.remove('')
        monster = ([more[0],*[int(i) for i in more[1:]]])
        monster = monster
        monster_stats.append(monster)
    
    player_health = int(info_detail[1])
    
    map_pointer = int(info_detail[3])
    
    name_map = ('saves/' + name + ".txt")
    basic_len = int(info_detail[6])
    


    
## --------     Combat       ---------

def monster_attack(): #Monster attack start
    global basic_len
    lowest = monster_stats[0][2]
    victim = monster_stats[0][0]
    victim_position = 0
    x = 0
    for companion in monster_stats[:basic_len]: # finds the opponent with lowest health
        if companion[2] < lowest:
            lowest = companion[2]
            victim = companion[0]
            victim_position = x
        x += 1
        
    for monster in monster_stats[basic_len:]:
        monster = monster[0]
        inx = int(list(chain.from_iterable(monster_stats)).index(monster) / 5)
        status = attack(victim, monster, inx, victim_position)
        if status == "death" and victim == 'player':
            print("! You Died.")
            death = True
            return
        elif status == "death":
            basic_len -= 1
        
def companion_attack():
    global basic_len
    lowest = monster_stats[0][2]
    victim = monster_stats[basic_len][0]
    victim_position = basic_len
    
    x = basic_len
    for monster in monster_stats[basic_len:]: # finds the opponent with the lowest health
        if monster[2] < lowest:
            lowest = monster[2]
            victim = monster[0]
            victim_position = x
        x += 1
        
    for companion in monster_stats[1:basic_len]:
        companion = companion[0]
        inx = int(list(chain.from_iterable(monster_stats)).index(companion) / 5)
        status = attack(victim, companion, inx, victim_position)

        
def attack(victim, attacker, attacker_position, victim_position): #Damage being dealt
    
    evade = random.randint(1,100)
    if evade <= int(monster_stats[victim_position][4]):
        print("! " + victim + " evaded the attack, so no damage was dealt.")
        return 

    damage = round(float(monster_stats[attacker_position][1]) - float(monster_stats[attacker_position][1]) * (float(monster_stats[victim_position][3]) / 100),1)
    monster_stats[victim_position][2] = round(monster_stats[victim_position][2] - damage, 1)
    
    if monster_stats[victim_position][2] < 0:
        monster_stats[victim_position][2] = 0

    print("! " + attacker + " attacked " + victim + " and dealt " + str(damage) + " damage, " + str(monster_stats[victim_position][2]) + " remaining.")
    
    if monster_stats[victim_position][2] == 0: #control whether the victim died
        clear_inventory(victim_position)
        monster_stats.pop(victim_position)      
        print("! The "+ victim +" died!")
        return "death"

def clear_inventory(victim_position):
    ### drops all the items the dead entity held
    for i in range(len(playerInv[victim_position])):
        for item in playerInv[victim_position]:
            dropItem(item, victim_position)
    playerInv.pop(victim_position)
    equiped_len.pop(victim_position)
    print('- All items the monster held are now lying all over the room.')



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

def grabItem(item, inventory):
    global playerInv, world_map, map_pointer
    
    playerInv[0].append([item[0],*[int(i) for i in item[3][1:-1].split(',')], item[4]]) # Add item to inventory
    
    for i in world_map[map_pointer]: # Find item in world map, and delete
        if i[0] == item[0]:
            world_map[map_pointer].remove(i)
    print('- grabbed {}'.format(item[0]))

def equipItem(item, inventory):
    global playerInv, world_map, map_pointer, equiped_len
    
    playerInv[inventory].remove(item)
    
    for thing in playerInv[inventory][:equiped_len[inventory]]: # Check if same item is not already equiped. if yes, unequip
        if item[4] == thing[4] and item[4].lower() != 'none':
            print(f'- can\'t hold more than one {item[4]} at once')
            unequipItem(thing, inventory)

    playerInv[inventory].insert(0, item)        
    stats = item[1:-1] # Print which stats increased/decreased
    for i, st in enumerate(zip(stats,['attack','health','evade'])):
        if int(st[0]) != 0:
            dire = 'increased' if int(st[0]) > 0 else 'decreased'
            if monster == False:               
                print('! {3}\'s {2} {0} by {1}!'.format(dire,abs(int(st[0])),st[1], monster_stats[inventory][0]))
            monster_stats[inventory][i+1] += int(st[0])
    if monster == False:    
        equiped_len[inventory] += 1

def dropItem(item, inventory):
    global playerInv, world_map, map_pointer, equiped_len

    if (playerInv[inventory].index(item)+1) <= equiped_len[inventory]: #check if the item is equiped, if so unequip it
        unequipItem(item, inventory)
        
    playerInv[inventory].remove(item) # Remove item from inventory
    print('- dropped '+item[0])
    world_map[map_pointer].append([item[0],'Dropped by player','grabable',f'[{item[1]},{item[2]},{item[3]}]',item[4]]) # Add item back to map
    
def unequipItem(item, inventory):
    global playerInv, world_map, map_pointer, equiped_len
    
    playerInv[inventory].remove(item)
    playerInv[inventory].append(item)
    equiped_len[inventory] -= 1

    for i, st in enumerate(zip(item[1:],['attack','health','evade'])): # Print which stats increased/decreased
        if int(st[0]) != 0:
            dire = 'increased' if int(st[0]) < 0 else 'decreased'
            print('! {3}\'s {2} {0} by {1}!'.format(dire,abs(int(st[0])),st[1], monster_stats[inventory][0]))
            monster_stats[inventory][i+1] = int(monster_stats[inventory][i+1])
            monster_stats[inventory][i+1] -= int(st[0])

def playerInvsetup(item):
    global monster
    z = 0
    playerInv.append([])
    if [i for i in item[4][2:-2].split(',')] != ['']:  # check if after split, the list is not empty (if the entity has any objects)
        for y in range(len([i for i in item[4][2:-2].split('[')])): # goes through the lenght of the list, if split
            playerInv[int(len(monster_stats)) -1].append([i for i in item[4][2:-2].replace('[','').replace(' ','').split(']')[z].split(',')])
            if z > 0:
                playerInv[int(len(monster_stats))-1][z].remove(playerInv[int(len(monster_stats)) + 1][z][0])
            z+=1
    equiped_len.append(int(item[5]))


    if int(item[5]) > 0: # checks if there are any equiped items
        monster = True
        for i in range(equiped_len[-1]): # adds the value of equiped items to stats
            equipItem(playerInv[-1][i],-1)
    monster = False

def readFile(): # reads the map file and translates into 3D list
    global world_map, map_pointer
    with open(name_map) as F:
        
        world_map = []
        
        for roomF in F.read().split('#')[1:]: # Split file into rooms
            room = []
            for lineF in roomF.split('\n')[1:-1]: # Split rooms into lines
                room.append(lineF.split(';')[:]) # Split lines into elements
            
            world_map.append(room)
            
        world_map = world_map[:-1]
        #print(world_map)

def find_room(pointer): # Searches all rooms until it finds the same index, returns position in 3D list
        i = 0
        for room in world_map:
            if room[0][2] == pointer:
                print('- ' + room[0][1])

                return i
            i += 1
        return
    
def console(inp = None): # Main class
    global world_map, map_pointer, player_health, cheese_mode, death, lastroom, basic_len, equiped_len, playerInv
    roomInx = world_map[map_pointer] # Copy room into buffer RoomInx

    # Create monster
    x = 0 # Current index
    for item in roomInx[1:]:
        x += 1
        
        if item[2] == 'enemy': # Test type
            monster_stats.append([item[0],*[int(i) for i in item[3][1:-1].split(',')]]) # Every time i use * i want to stop coding and go live in the woods alone
            playerInvsetup(item)
            print('! ' + item[1])
            print('- {3}\'s attack: {0}, {3}\'s health: {1}, {3}\'s armor: {2}'.format(monster_stats[-1][1], monster_stats[-1][2],monster_stats[-1][3],monster_stats[-1][0]))
            del world_map[map_pointer][x] # Delete monster from map
            x -= 1 # Compensate for deleted monster

        elif item[2] == 'end':
            death = True
            print("\n\
#####  #   #  #### \n\
#      ##  #  #  ##\n\
###    # # #  #   #\n\
#      #  ##  #  ##\n\
#####  #   #  ####")

    print('> ',end='')
    if inp == None:
        inp = input().lower().split() # Basic pre-processing
    else:
        inp = inp.lower().split()
    inp += [None] * (3 - len(inp)) # Pad to 3 arguments in list

    if inp[0] == None:
        print('- You do nothing...')
    elif inp[0] == 'cheese':
        print('- cheese')
        try:
            for i in open('cheese.txt').readlines(): print(i,end='')
        except:
            print('- chesse')

    elif inp[0] == 'help':
            print("- Possible commands:\n\
* Help - List all commands\n\
* Examine/look [object] - Examine object or person\n\
* Grab/Take [item] - Grab item and put it in your inventory\n\
* Drop/leave [item] - Drop an item from your inventory on the ground\n\
* Equip [item] - Equip an item from your inventory\n\
* Unequip [item] - See above in reverse\n\
* Move/Open [path/chest] - Open a chest or go down a path\n\
* Attack [monster] - attack a monster\n\
* Ask/Join [companion] - Convince an npc to help fight with you\n\
* Give [companion] [item] - Give an item to your companion\n\
* Equip/Unequip/Drop [companion] [item] - See above but for companion\n\
* Buy [item] - buy an item from a seller NPC")
            
    elif inp[0] == 'end':
            death = True
            return
    elif inp[0] == 'save':
            save()
        
    elif inp[0] in ['examine','look']: # Examine command
        if inp[1] in ['room','all','everything',None]: # If specified, will list all items in room
            print('- The room contains:')
            for item in roomInx[1:]:
                print('* ' + item[0] + ' - '+ item[2])

        elif inp[1] in ['self','me','myself']:
            print('* You have {0} attack and {1} health'.format(*monster_stats[0][1:3]))
            
        elif inp[1] in list(chain.from_iterable(monster_stats)):
                inx = int(list(chain.from_iterable(monster_stats)).index(inp[1]) / 5)
                print('* {0} has {1} attack and {2} health'.format(*monster_stats[inx][0:3]))
        else: # prints description of item
            for item in roomInx: # looks through all items until it finds the right one
                if item[0] == inp[1]:
                    print('- ' + item[1])
                    
                    if item[2] == "npc":
                        stuff = item[4].split("_")
                        if item[3] == "vendor":
                            print("- " + item[0] + " is a vendor. You buy stuff from him for money.")
                            print("- Here's " + item[0] + "'s stuff:")
                            print("* you can trade " + stuff[0] + ' for ' + item[5])
                                
                        if item[3] == "chatter":
                            print('- ' + random.choice(stuff))
                    
                    break
            else:
                print('? There is no object like that visible')
                            
    elif inp[0] in ['grab','take']: # Grab command
        if inp[1] == 'everything': # If specified, will attempt to grab everything
            for item in roomInx:
                if item[2] == 'grabable':
                    grabItem(item, 0)

        else: # Grab specified item, if possible
            for item in roomInx:
                if item[0] == inp[1]:
                    if item[2] == 'grabable':
                        grabItem(item, 0)
                    else:
                        print('? Cant grab {}'.format(item[0]))
                    break
            else:
                print('? There is no object like that')
                
    elif inp[0] in ['drop','leave']: # Drop command - item is returned to the room
        check_2 = False
        if inp[1] in [i[0] for i in monster_stats[1:basic_len]]: # Drop someone's item --- check if input[1] je v monster listu (jen player a companioni)
            inventory = [i[0] for i in monster_stats].index(inp[1]) # where in monster_stats is the person whose item is being dropped
            if inp[2] in [i[0] for i in playerInv[inventory]]: # check if called item is in inventory
                item = playerInv[inventory][int(list(chain.from_iterable(playerInv[inventory])).index(inp[2]) / 5)] # the searched item in inventory
                dropItem(item, inventory)
                check_2 = True
            else:
                print('? {0} has no such item in their inventory'.format(inp[1]))
                check_2 = True

        elif check_2 == False:
            for item in playerInv[0]:
                if item[0] == inp[1]:
                    dropItem(item, 0)
                    check_2 = True
                    break
        if check_2 == False: #happens if no item was dropped
            print('? No such item in inventory')

    elif inp[0] == 'equip': # Equip command - item's stats are used from now
        check_2 = False
        if inp[1] in [i[0] for i in monster_stats[1:]]: # same as in drop
            inventory = [i[0] for i in monster_stats].index(inp[1]) # same as in drop
            if inp[2] in [i[0] for i in playerInv[inventory]]: # same as in drop
                 item = playerInv[inventory][int(list(chain.from_iterable(playerInv[inventory])).index(inp[2]) / 5)] # same as in drop
                 equipItem(item, inventory)
                 check_2 = True
                 
        elif check_2 == False:
            for item in playerInv[0]:
                if item[0] == inp[1]:
                    equipItem(item, 0)
                    check_2 = True
                    break
                
        if check_2 == False: #same as in drop
            print('? There is no such equipable item in your inventory')

    elif inp[0] == 'unequip': #same as in drop
        check_2 = False
        if inp[1] in [i[0] for i in monster_stats[1:basic_len]]: #same as in drop
            inventory = [i[0] for i in monster_stats].index(inp[1]) #same as in drop
            if inp[2] in [i[0] for i in playerInv[inventory]]: #same as in drop
                item = playerInv[inventory][int(list(chain.from_iterable(playerInv[inventory])).index(inp[2]) / 5)] #same as in drop
                unequipItem(item, inventory)
                check_2 = True
                
        elif check_2 == False:
            for item in playerInv[0]:
                if item[0] == inp[1]:
                    unequipItem(item, 0)
                    check_2 = True
                    break
        if check_2 == False: #same as in drop
            print('? You aren\'t equiped with that object')

    elif inp[0] in ['attack',"brutalize"]:
        if inp[1] in list(chain.from_iterable(monster_stats)):
            inx = int(list(chain.from_iterable(monster_stats)).index(inp[1]) / 5)
            attack(inp[1],monster_stats[0][0], 0, inx)
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
                        for thing in playerInv[0]: # Check if player even has a key
                            if thing[0] == 'key':
                                print("- The door has been unlocked, but your key got stuck in the lock")
                                world_map[map_pointer][i][4] = 'unlocked' # Unlock door in world_map for later
                                map_pointer = find_room(item[3]) # Change room
                                lastroom = item[3]
                                playerInv[0].remove(thing)
                                break

                        else:
                            print("? You need a key to open this door")
                else:
                    print("? You can't go through this object")

    elif inp[0] in ['ask', 'join']: #is command join or ask
        x = 0 # Current index
        check = False
        for item in roomInx[1:]: #searches through the rooms to find the companion
            x += 1
            if item[2] == 'companion':
                check = True
                if inp[1] == item[0]: #check if its the right companion
                    monster_stats.insert(basic_len, [item[0],*[int(i) for i in item[3][1:-1].split(',')]]) #make the companion active

                    playerInvsetup(item) 
                
                    print('! ' + item[1])
                    print('- {3}\'s attack: {0}, {3}\'s health: {1}, {3}\'s armor: {2}'.format(monster_stats[basic_len][1], monster_stats[basic_len][2],monster_stats[basic_len][3],monster_stats[basic_len][0]))
                    del world_map[map_pointer][x]
                    basic_len +=1
                    x -=1
                    break
            
            elif item == roomInx[-1] and check == True:
                print('? The companion in this room has a different name')
                break
        else:
            print('? There is no companion in this room')

    elif inp[0] == 'give': # give command
        if inp[1] in [i[0] for i in monster_stats[1:]]: # same as drop
            if inp[2] in [i[0] for i in playerInv[0][equiped_len[0]:]]: #checks if item is in your inventory 
                item = playerInv[0][int(list(chain.from_iterable(playerInv[0])).index(inp[2]) / 5)] #finds item in your inventory
                inventory = [i[0] for i in monster_stats].index(inp[1])
                playerInv[inventory].append(item)
                print('- {0} received {1}'.format(inp[1],inp[2]))
                playerInv[0].remove(item)

    elif inp[0] == "buy":
        for item in roomInx[1:]:
            if len(item) > 4:
                if item[4].split('_')[0] == inp[1]:
                    sell = item[4].split('_')
                    if item[5] in list(chain.from_iterable(playerInv[0])):
                        playerInv[0].append([sell[0],*[int(i) for i in sell[1][1:-1].split(',')], sell[2]])
                        playerInv[0].remove(playerInv[0][int(list(chain.from_iterable(playerInv[0])).index(item[5]) / 5)])
                        print('- You just bought ' + sell[0])
                        break
        else:
            print("? Nobody got that.")
            
            
    else:
        print('? You cant do that right now')



    if len(monster_stats) == basic_len:
        monster_stats[0][2] = player_health
    else:
        monster_attack()
        if death == False:
            companion_attack()
    
# --------- Global variables ---------

player_health = 10 # Health limit, not current value
death = False
monster = False
name_map = 'map.txt' # Map file
lastroom = '[0,0]' # Coordinates of last room in [x,y]
world_map = [] # Entire game map as a 3D list
map_pointer = 0 # Index of current room in world_map
monster_stats = [] # Monsters currently attacking with stats
playerInv = [[]] # Player inventory with stats. 2D list
basic_len = 1
equiped_len = [0]
classes = {'regular':['player',3,10,12,5],'tank':['player',2,15,10,2],'rogue':['player',4,7,15,10]}
commands = ['grab money','buy cheese','equip cheese', 'move home', 'move chest', 'grab dagger', 'equip dagger', 'move back', 'move outside', 'move forest', 'move forward', 'move entrance', 'move hallway', 'move forward', 'attack wasp_1', 'attack wasp_2', 'attack wasp_3', 'move door', 'move chest', 'grab key', 'grab iron_sword', 'equip iron_sword', 'move back', 'move back', 'move back', 'move back', 'move left', 'attack goblin', 'grab sleeve', 'equip sleeve', 'move metal_door', 'move forward', 'move left', 'grab bucket', 'equip bucket', 'move left', 'attack goblin', 'grab can', 'equip can', 'move right', 'move down', 'grab ring', 'equip ring', 'move forward', 'move left', 'attack large_goblin', 'move chest', 'grab shield', 'move back', 'move back', 'move right', 'move door', 'grab rock', 'move back', 'move forward', 'move jump', 'move back', 'move back', 'move right', 'move forward', 'move person', 'buy key', 'move back', 'move right', 'ask rat', 'move back', 'move back', 'move hallway', 'move metal_door']

# ------ init -----
menu()
readFile()
find_room(lastroom)
i = 0

#for i in range(len(commands)):
    #console(commands[i])
while death == False:
    console()
    
