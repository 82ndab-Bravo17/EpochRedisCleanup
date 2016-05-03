import redis
import datetime

keynameai = 'AI:'
keynameitems = 'AI_ITEMS:'
servername = 'NA82:'
_password = '82nd@dmin'
_port = 6379
_db = 2


def getnumitems(ainum, aisitems):
    items,sep,numbers = aisitems.partition('],[')
    items = items[2:]
    numbers = numbers.strip(']')
    items = items.replace('"', '')
    itemslist = items.split(',')
    numberslist = numbers.split(',')
    num = 0
    #for i in range(0, len(itemslist)-1):
    #    f.write ('ai %s has %s %s\n' % (ainum, numberslist[i], itemslist[i]))
    return

def getitemlist(ainum, aisitems):
    items,sep,numbers = aisitems.partition('],[')
    items = items[2:]
    numbers = numbers.strip(']')
    items = items.replace('"', '')
    itemslist = items.split(',')
    numberslist = numbers.split(',')
    return itemslist, numberslist
    
def removeitems(ainum, aisitems):
    itemslist, numberslist = getitemlist(ainum, aisitems)
    #f.write ('Itemslist %s - numberslist %s\n' % (len(itemslist), len(numberslist)))

    for i in range(0, len(itemslist)):
        # f.write ('ai %s has %s %s\n' % (ainum, itemslist[i], numberslist[i] ))
        if (int(numberslist[i]) > 75):
            numberslist[i] = '75'
            f.write ('%s was reduced\n' % itemslist[i])
    itemsdata = '[['
    amountdata = '],['
    for j in range (0, len(itemslist)):
        itemsdata = itemsdata + '"' + itemslist[j] + '",'
        amountdata = amountdata + numberslist[j] + ','
            
    itemsdata = itemsdata[0:len(itemsdata)-1]
    amountdata = amountdata[0:len(amountdata)-1] +  ']]'
    data = itemsdata + amountdata

    return data


r = redis.StrictRedis(host='localhost', password=_password, port=_port, db=_db)
f = open("Refresh_Traders_Stats.txt", "a")
timenow = datetime.datetime.now()
f.write ('\n\n\n\nTime is: %s at %s:%s\n\n' % (datetime.date.today(), getattr(timenow, 'hour'), getattr(timenow, 'minute')))
for ainum in range(0,100):
    ainame = str(ainum)
    keyai = keynameai + servername + ainame
    aitype = r.exists(keyai)
    if ainum < 8:
        aitype = True
    if (aitype):
        aisitems = ''
        keyitems = keynameitems + servername + ainame
        aisitems = r.get(keyitems)
        timelive = r.ttl(keyitems)
        # f.write ('ai %s has items live for %s seconds\n' % (ainum, timelive))
        if aisitems != None:
            f.write('Old data is \n %s \n' % aisitems)
            # getnumitems(ainum, aisitems)
            aisnewitems = removeitems(ainum, aisitems)
            # getnumitems(ainum, aisnewitems)
            f.write('New data is \n %s \n' % aisnewitems)
            f.write ('\n\n')
            r.setex(keyitems, timelive, aisnewitems)


f.close()

  