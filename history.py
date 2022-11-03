def __has_tzname(vorg):
    from copy import copy
    v = copy(vorg)
    """
    for k in ['user', 'profile', 'timezone', 'tzname']:
        if v[k] is None:
            return False
        v = v[k]
    """
    if 'tzname' not in v.keys():
        return False
        
    return True
    
def arrange():
    import json
    itdict = dict()
    prdict = dict()
    for lang in ['en', 'ja', 'ru']:
        with open('./italki/italki_'+lang+'.json', 'r') as f:
            tmpitdict = json.load(f)
            for k in tmpitdict.keys():
                itdict[k] = tmpitdict[k]['living_country_id']
                
        countrydict = dict()
        import csv
        with open('./preply/country.csv', 'r') as csvfile:
            spamreader = csv.reader(csvfile)
            next(spamreader)
            for row in spamreader:
                countrydict[row[2]] = row[0]
                
        with open('./preply/preply_'+lang+'.json', 'r') as f:
            tmpprdict = json.load(f)
            for k in tmpprdict.keys():
                """if __has_tzname(tmpprdict[k]) and (tmpprdict[k]['user']['profile']['timezone']['tzname'] in countrydict.keys()):"""
                if __has_tzname(tmpprdict[k]) and (tmpprdict[k]['tzname'] in countrydict.keys()):
                    """prdict[k] = countrydict[tmpprdict[k]['user']['profile']['timezone']['tzname']]"""
                    prdict[k] = countrydict[tmpprdict[k]['tzname']]
                else:
                    prdict[k] = '##'
                
    orgarray = list()
    with open('history.txt', 'r') as f:
        while True:
            line = f.readline()
            if len(line) <= 0:
                break
            line = line.strip()
            p = line.find('https://', line.find('https://')+len('https://'))
            tmporgarray = list()
            if p >= 0:
                tmporgarray.append('/'.join(line[:p].split('/')[:-1])+'/')
                tmporgarray.append(line[:p].split('/')[-1]+line[p:])
            else:
                tmporgarray.append(line)
            orgarray += [x.split(' ')[-1].replace('/english', '/').replace('/japanese', '/').replace('/russian', '/') for x in tmporgarray]
    orgarray = list(set(orgarray))
            
    dstarray = list()
    for history in orgarray:
        if not(history[-1] == '/'):
            print(history)
        itpre = 'https://www.italki.com/teacher/'
        prpre = 'https://preply.com/en/tutor/'
        if history.startswith(itpre):
            if history[len(itpre):-1] in itdict.keys():
                dstarray.append([itdict[history[len(itpre):-1]], history])
            else:
                dstarray.append(['**', history])
        if history.startswith(prpre):
            if history[len(prpre):-1] in prdict.keys():
                dstarray.append([prdict[history[len(prpre):-1]], history])
            else:
                dstarray.append(['**', history])
                
    dstarray = sorted(dstarray, key=lambda x: (x[0], x[1]))

    import os
    if os.path.exists('history.txt.backup'):
        os.remove('history.txt.backup')
    os.rename('history.txt', 'history.txt.backup')
    with open('history.txt', 'w') as f:
        for x in dstarray:
            f.write(' '.join(x)+'\n')
            
"""
with open('history.txt.220909', 'r') as f:
    tmparray = list()
    while True:
        line = f.readline()
        if len(line) <= 0:
            break
        for x in line.split(' '):
            if len(x) <= 2 or x.endswith('/'):
                tmparray.append(x)
            else:
                tmparray.append(x[:-2])
                tmparray.append(x[-2:])
                
with open('history.txt', 'w') as f:
    for i in range(len(tmparray)):
        if i % 2 == 0:
            f.write(tmparray[i]+' '+tmparray[i+1]+'\n')
"""
