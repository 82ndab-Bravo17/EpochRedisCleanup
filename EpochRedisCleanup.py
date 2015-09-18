import redis
import datetime

keynameai = 'AI:'
keynameitems = 'AI_ITEMS:'
servername = 'NA82:'
_password = 'yourpassword'
_port = 6379
_db = 2
vehicles = {
"C_Offroad_01_EPOCH" : "Offroad",
"C_Quadbike_01_EPOCH" : "Quadbike",
"C_Hatchback_01_EPOCH" : "Hatchback",
"C_Hatchback_02_EPOCH" : "Hatchback",
"C_SUV_01_EPOCH" : "SUV",
"C_Rubberboat_EPOCH" : "Rubberboat",
"C_Rubberboat_02_EPOCH"  : "Rubberboat",
"C_Rubberboat_03_EPOCH"  : "Rubberboat",
"C_Rubberboat_04_EPOCH" : "Rubberboat",
"C_Van_01_box_EPOCH" : "Box Van",
"C_Van_01_transport_EPOCH" : "Transport Van",
"C_Boat_Civil_01_EPOCH" : "Boat",
"C_Boat_Civil_01_police_EPOCH" : "Boat",
"C_Boat_Civil_01_rescue_EPOCH" : "Boat",
"B_Heli_Light_01_EPOCH" :  "MH9",
"B_SDV_01_EPOCH" :  "Sub",
"B_MRAP_01_EPOCH" :  "Hunter",
"B_Truck_01_transport_EPOCH" :  "HEMTT",
"B_Truck_01_covered_EPOCH" :  "HEMTT",
"B_Truck_01_mover_EPOCH" :  "HEMTT",
"B_Truck_01_box_EPOCH" :  "HEMTT",
"O_Truck_02_covered_EPOCH" :  "Zamak",
"O_Truck_02_transport_EPOCH" :  "Zamak",
"O_Truck_03_covered_EPOCH" :  "Tempest",
"O_Truck_02_box_EPOCH" :  "Zamak",
"I_Heli_light_03_unarmed_EPOCH" :  "Hellcat",
"O_Heli_Light_02_unarmed_EPOCH" :  "Orca",
"I_Heli_Transport_02_EPOCH" :  "Mohawk",
"O_Heli_Transport_04_EPOCH" :  "Taru",
"O_Heli_Transport_04_bench_EPOCH" :  "Taru",
"O_Heli_Transport_04_box_EPOCH" :  "Taru",
"O_Heli_Transport_04_covered_EPOCH" :  "Taru",
"B_Heli_Transport_03_unarmed_EPOCH" :  "Huron",
"jetski_epoch" : "Jetski",
"K01" : "Kart",
"K02" : "Kart",
"K03" : "Kart",
"K04" : "Kart",
"ebike_epoch" : "Bike",
"mosquito_epoch" : "Mosquito",
"C_Heli_Light_01_civil_EPOCH" : "Civil MH-9"
}

def getnumitems(ainum, aisitems, finditem):
    items,sep,numbers = aisitems.partition('],[')
    # print ('%s %s' % (items, numbers))
    items = items[2:]
    numbers = numbers.strip(']')
    # print ('%s %s' % (items, numbers))
    items = items.replace('"', '')
    itemslist = items.split(',')
    numberslist = numbers.split(',')
    for i in range(0, len(itemslist)):
        # print ('ai %s has %s %s' % (ainum, itemslist[i], numberslist[i] ))
        if (itemslist[i] == finditem):
            break
    return numberslist[i]

r = redis.StrictRedis(host='localhost', password=_password, port=_port, db=_db)
f = open("databasestats.txt", "a")
timenow = datetime.datetime.now()
f.write ('\n\n\n\nTime is: %s at %s:%s\n\n' % (datetime.date.today(), getattr(timenow, 'hour'), getattr(timenow, 'minute')))
for ainum in range(0,100):
    ainame = str(ainum)
    keyai = keynameai + servername + ainame
    aitype = r.exists(keyai)
    if (aitype):
        keyitems = keynameitems + servername + ainame
        aisitems = r.get(keyitems)
        if aisitems != None:
            for veh in vehicles.keys():
                if veh in aisitems:
                    numveh = getnumitems(ainum, aisitems, veh)
                    if numveh > 0:
                        # print ('ai: %s has %s' % (ainame, vehicles[veh]))
                        f.write('ai: %s has  %s %s \n' % (ainame, numveh, vehicles[veh]))
            if ("ItemRope" not in aisitems) and ("ItemRock" not in aisitems) and ("ItemStick" not in aisitems):
                # print ('ai %s has no rope, rock, or stick, deleting' % ainame)
                f.write ('ai %s has no rope, rock, or stick, deleting\n' % ainame)
                r.delete(keyai)
                r.delete(keyitems)
        else:
            # print ('ai: %s has no itmes, deleting' % ainame)
            f.write ('ai: %s has no itmes, deleting\n' % ainame)
            r.delete(keyai)

            
f.close()




   