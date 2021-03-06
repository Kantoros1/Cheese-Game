'''How to use:

Select: type select [room] to select room.

List: if room selected lists its items. if no room select lists rooms.
List [room]: list specified rooms' items

Edit: if room selected edit its values.
Edit [room]: same as above.
Edit [item]: if room selected edit items' values.

Create: If room selected creates new item. If no room creates new room.
Create room: creates new room.
Create room: if room selected creates new item.

Delete: if room selected deletes room
Delete [room]: deletes room
Delete [item]: delete item in selected room

Save: Adds room to map.txt

Reload: Reloads map from map.txt

CAUTION:
Item name cannot be the same as item type
Do not confuse Object type and item type.
    Object type is preciselly defined (grabable, enemy, door etc.) 
    Item type can be anything (except same as name)
'''

pointer = None # Current room, None means all rooms
typ_format = {'grabable':[['statistics[attack increase, health increase, deflect increase]',3],['item type',1]],
              'door':[['next room[x,y]',2],['state(locked/unlocked)',1]],
              'enemy':[['statistics[attack, health, deflect, block]',4]],
              'none':[]}

def load():
    global Map
    with open('map.txt') as F:
        Map = []
        for roomF in F.read().split('#')[1:]: # Split file into rooms
            room = []
            for lineF in roomF.split('\n')[1:-1]: # Split rooms into lines
                room.append(lineF.split(';')[:]) # Split lines into elements
                
            Map.append(room)
        Map = Map[:-1]

        #print(Map)

print('- Official room creator for Cheese game.')

def IO():
    global pointer, Map
  
    command = input('\n> ').lower().split() # Makes list of arguments
    command += [None] * (2 - len(command)) # Pad to 2

    if command[0] == 'list': # Print all rooms/items available
        if command[1] == 'rooms': # Print all rooms
            pointer = None
            lister(None)
        elif command[1] == 'items': 
            if pointer == None:
                print('! No room selected')
            else:
                lister(pointer)
        elif command[1] == None: # Default to current pointer
            lister(pointer)
        elif command[1] in [x[0][0] for x in Map]: # Specific room
            lister(command[1])
        else:
            print('! Invalid argument')

    elif command[0] in ['select','sel']: # Select room to edit
        rooms = [x[0][0] for x in Map] # Room names list
         
        if command[1] in rooms: # Check for rooms
            print('- Selected ' + command[1])
            pointer = rooms.index(command[1])
            
        else:
            print('! Invalid argument')

    elif command[0] == 'edit':
        if command[1] in [None,'room','all']:
            if pointer == None:
                print('! No room selected')
            else:
                editor(pointer,None)
        elif command[1] in [x[0][0] for x in Map]:
            pointer = [x[0][0] for x in Map].index(command[1])
            editor(pointer,None)
        elif command[1] in [x[0] for x in Map[pointer]]: # Items names list
            editor(pointer,[x[0] for x in Map[pointer]].index(command[1]))
        else:
            print('! Invalid argument')

    elif command[0] == 'save':
        save()
        print('- map saved')

    elif command[0] in ['new','add','create']:
        if command[1] == None:
            if pointer == None:
                Map.append([['Unnamed room','unnamed room','[0,0]']])
                pointer = [x[0][0] for x in Map].index('Unnamed room')
                editor(pointer,None)
            else:
                Map[pointer].append(['Unnamed item','unnamed item','none'])
                editor(pointer,[x[0] for x in Map[pointer]].index('Unnamed item'))
                
        elif command[1] == 'room':
            pointer = None
            Map.append([['Unnamed room','unnamed room','[0,0]']])
            pointer = [x[0][0] for x in Map].index('Unnamed room')
            editor(pointer,None)
            
        elif command[1] == 'item':
            if pointer == None:
                print('! No room selected')
            else:
                Map[pointer].append(['Unnamed item','unnamed item','none'])
                editor(pointer,[x[0] for x in Map[pointer]].index('Unnamed item'))


    elif command[0] in ['delete','del']:
        rooms = [x[0][0] for x in Map]
        if pointer == None: 
            if command[1] in rooms:
                pointer = rooms.index(command[1])
                if input('? Are you sure you want to delete {}?\n> '.format(Map[pointer][0][0])).lower() in ['yes','y']:
                    Map.remove(Map[pointer])
                    print('- room deleted')
                    pointer = None
            else:
                print('! No room selected')
        else:
            items = [x[0] for x in Map[pointer]]
            if command[1] == None:
                if input('? Are you sure you want to delete {}?\n> '.format(Map[pointer][0][0])).lower() in ['yes','y']:
                    Map.remove(Map[pointer])
                    print('- room deleted')
            elif command[1] in rooms:
                pointer = rooms.index(command[1])
                if input('? Are you sure you want to delete {}?\n> '.format(Map[pointer][0][0])).lower() in ['yes','y']:
                    Map.remove(Map[pointer])
                    print('- room deleted')
                    pointer = None
            elif command[1] in items:
                if input('? Are you sure you want to delete {}?\n> '.format(command[1])).lower() in ['yes','y']:
                    Map[pointer].remove(Map[pointer][items.index(command[1])])
                    print('- room deleted')
            else:
                print('! Invalid argument')
                
    elif command[0] == 'reload':
        load()
        print('- map reloaded')
    else:
        print('- Invalid instruction')





def save():
    global Map

    save = open("map.txt", "w")
    save.write("#")
    for i in Map:
        for n in i:
            save.write("\n")
            for z in n:
                save.write(z)
                if z != n[-1]:
                    save.write(";")
        save.write("\n")
        save.write("#")
            

def lister(roomP):
    global Map
    
    if roomP == None: # Rooms
        if len(Map) == 0:
            print('- The map is empty')
        for room in Map:
            print('* ' + room[0][0] + '\n  - ' + room[0][1])
    else: # Items
        if len(Map[roomP]) == 1:
            print('- This room is empty')
        for item in Map[roomP][1:]:
            print('* ' + item[0] + '\n  - ' + item[1])

def editor(roomP,itemP):
    global Map
    if itemP == None: # Edit room itself
        item = Map[pointer][0]
        Map[pointer][0] = []
        print('- Current name: ' + item[0])
        inp = input('- New name:\n> ').lower()
        if inp == '':
            inp = item[0]
        Map[roomP][0].append(inp)
        print('- Current description: ' + item[1])
        inp = input('- New description:\n> ').lower()
        if inp == '':
            inp = item[1]
        Map[roomP][0].append(inp)
        print('- Current coordinates: ' + item[2])
        inp = input('- New coordinates:\n> ').lower().replace('[','')\
                .replace(']','').replace(',',' ').strip().split()
        if inp == '':
            inp = item[2]
        inp += [0]*(2 - len(inp))
        inp = inp[:2]
        Map[roomP][0].append('['+str(inp[0])+','+str(inp[1])+']')

        print('- Room editted')
        
    else:
        item = Map[roomP][itemP]
        Map[roomP][itemP] = []
        for i, val in enumerate(['name','description','object type']):    
            print('- Current {}: '.format(val) + item[i])
            inp = input('- New {}:\n> '.format(val)).lower()
            if inp == '':
                inp = item[i]
            Map[roomP][itemP].append(inp)

        try:
            formt = typ_format[Map[roomP][itemP][2]]
        except:
            print('- That is not a valid object type')
        item += ['']*(len(formt)+3-len(item))
        item = item[:len(formt)+3]

        for i, val in enumerate(formt):
            print('- Current {}: '.format(val[0]) + item[i+3])
            inp = input('- New {}:\n> '.format(val[0])).lower()\
                .replace('[','').replace(']','')\
                .replace(',',' ').strip().split()
            if inp in ['',[]]:
                inp = item[i+3].replace('[','').replace(']','')\
                .replace(',',' ').strip().split()
            if val[1] == 1:
                Map[roomP][itemP].append(inp[0])
            else:
                inp += [None] * (val[1] - len(inp))
                inp = inp[:val[1]]
                text = '['
                for i in inp:
                    text += i+','
                text = text[:-1] + ']'
                Map[roomP][itemP].append(text)
        
        print('- Item editted')
    
load()
while True:
    IO()
