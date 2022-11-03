class Preply:
    def __init__(self, language):
        self.language = language
        self.tutorsorgdict = self.__load_tutorsorgdict()
        self.tutorsdict = self.__load_tutorsdict()
        
    @classmethod
    def __get_path(cls, f):
        from os.path import join
        return join('.', 'preply', f)
        
    def __get_jsonorgpath(self):
        return self.__class__.__get_path('preply_'+self.language[0:2]+'org.json')

    def __load_tutorsorgdict(self):
        tutorsdict = dict()
        
        import os.path
        if os.path.exists(self.__get_jsonorgpath()):
            import json
            with open(self.__get_jsonorgpath(), 'r') as f:
                for t in range(100):
                    try:
                        tutorsdict = json.load(f)
                        break
                    except Exception as err:
                        print(err)
                        import time
                        time.sleep(1)
                        tutorsdict = dict()

        notimezoneset = set()
        for tutor in tutorsdict.keys():
            if not isinstance(tutorsdict[tutor]['user']['profile']['timezone'], dict):
                notimezoneset.add(tutor)
                continue
            if 'tzname' not in tutorsdict[tutor]['user']['profile']['timezone'].keys():
                notimezoneset.add(tutor)

        for tutor in notimezoneset:
            del tutorsdict[tutor]

        return tutorsdict
        
    def __get_jsonpath(self):
        return self.__class__.__get_path('preply_'+self.language[0:2]+'.json')

    def __load_tutorsdict(self):
        tutorsdict = dict()
        
        import os.path
        if os.path.exists(self.__get_jsonpath()):
            import json
            with open(self.__get_jsonpath(), 'r') as f:
                for t in range(100):
                    try:
                        tutorsdict = json.load(f)
                        break
                    except Exception as err:
                        print(err)
                        import time
                        time.sleep(1)
                        tutorsdict = dict()
                        
        return tutorsdict
        
    @classmethod
    def __get_countrypath(cls):
        return cls.__get_path('country.csv')
        
    @classmethod
    def __get_countrydict(cls):
        import csv

        countrydict = {'countryname': dict(), 'timezone': dict()}
        with open(cls.__get_countrypath(), 'r') as f:
            reader = list(csv.reader(f))
            for i in range(len(reader)):
                if i == 0:
                    continue
                    
                v = {'countryname': reader[i][1], 'timezone': reader[i][2]}
                for k in ['countryname', 'timezone']:
                    countrydict[k].setdefault(reader[i][0], list())
                    tmp = countrydict[k][reader[i][0]]
                    tmp.append(v[k])
                    countrydict[k][reader[i][0]] = tmp

        return countrydict

    def __get_urliter(self, pagenumber):
        for i in range(1,pagenumber):
            url = 'https://preply.com/en/online/'+self.language+'-tutors'
            if i >= 2:
                url += '?page='+str(i)
            yield url

    @classmethod
    def __json_tutorsdicttmp(cls, url):
        while True:
            try:
                import requests
                response = requests.get(url)
                break
            except Exception as err:
                print(err)
                from time import sleep
                sleep(60)
                
        tutorsdicttmp = dict()
        if response.status_code == 200:
            from bs4 import BeautifulSoup
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            import json
            soupjson = soup.find('script', id='__NEXT_DATA__', type='application/json')
            tutorsjson = json.loads(soupjson.string)['props']['pageProps']['ssrAllTutors']['tutors']
            for tutor in tutorsjson:
                tutorsdicttmp[tutor['id']] = tutor
        else:
            print(response.status_code, url)

        return tutorsdicttmp

    def collect(self, pagenumber, reload=False):
        if reload:
            self.tutorsorgdict = dict()
            self.tutorsdict = dict()
            
        urliter = self.__get_urliter(pagenumber)
        for url in urliter:
            from time import sleep
            sleep(1)

            tutorsorgdicttmp = self.__class__.__json_tutorsdicttmp(url)
            if len(tutorsorgdicttmp) <= 0:
                break
            self.tutorsorgdict.update(tutorsorgdicttmp)

        import json
        
        with open(self.__get_jsonpath(), 'w') as f:
            json.dump(self.tutorsorgdict, f)
            
        for k in self.tutorsorgdict.keys():
            try:
                self.tutorsdict.setdefault(k, dict())
                self.tutorsdict[k]['tzname'] = self.tutorsorgdict[k]['user']['profile']['timezone']['tzname']
                self.tutorsdict[k]['countryOfBirth'] = self.tutorsorgdict[k]['countryOfBirth']['name']
            except TypeError as e:
                print(e)
            except KeyError as e:
                print(e)
                
        with open(self.__get_jsonpath(), 'w') as f:
            json.dump(self.tutorsdict, f)
            print('len(self.tutorsdict.keys()):', len(self.tutorsdict.keys()))
            
    def get_tznameset(self):
        tznameset = set()
        for tutor in self.tutorsdict.keys():
            try:
                """tznameset.add(self.tutorsdict[tutor]['user']['profile']['timezone']['tzname'])"""
                tznameset.add(self.tutorsdict[tutor]['tzname'])
            except KeyError as e:
                print(e)

        return tznameset
        
    def get_urlarray(self, conarrayorg, unseen=False):
        from collections.abc import Iterable

        conarray = list()
        for conorg in conarrayorg:
            from copy import copy
            con = copy(conorg)
            if len(con) == 2:
                con.append(True)
            if isinstance(con[1], str):
                conarray.append(con)
            elif isinstance(con[1], Iterable) and all([isinstance(x, str) for x in con[1]]):
                for x in con[1]:
                    conarray.append([con[0], x, con[2]])
                    
        countrydict = self.__class__.__get_countrydict()
        
        urlarray = list()
        for t in range(100):
            try:
                tutorarray = list()
                for tutor in self.tutorsdict.keys():
                    if 'countryOfBirth' not in self.tutorsdict[tutor]:
                        continue
                    if 'tzname' not in self.tutorsdict[tutor]:
                        continue
                    f = True
                    for con in conarray:
                        if con[0] == 'origin_country_id':
                            """if not((self.tutorsdict[tutor]['countryOfBirth']['name'] in countrydict['countryname'].get(con[1], [])) == con[2]):"""
                            if not((self.tutorsdict[tutor]['countryOfBirth'] in countrydict['countryname'].get(con[1], [])) == con[2]):
                                f = False
                                break
                        if con[0] == 'living_country_id':
                            """if not((self.tutorsdict[tutor]['user']['profile']['timezone']['tzname'] in countrydict['timezone'].get(con[1], [])) == con[2]):"""
                            if not((self.tutorsdict[tutor]['tzname'] in countrydict['timezone'].get(con[1], [])) == con[2]):
                                f = False
                                break
                        if con[0] == 'tzname':
                            """if not((self.tutorsdict[tutor]['user']['profile']['timezone']['tzname'] == con[1]) == con[2]):"""
                            if not((self.tutorsdict[tutor]['tzname'] == con[1]) == con[2]):
                                f = False
                                break
                    if f == True:
                        tutorarray.append(tutor)

                history = list()
                with open('history.txt', 'r') as f:
                    while True:
                        line = f.readline()
                        if len(line) <= 0:
                            break
                        history.append(line.strip().split(' ')[-1])
                        
                for tutor in tutorarray:
                    url = 'https://preply.com/en/tutor/2300258/'.replace('2300258',str(tutor))
                    if unseen == True and url in history:
                        continue
                    else:
                        urlarray.append(url)
                break
            except ValueError as err:
                print(err)
                import time
                time.sleep(1)
                urlarray = list()
                
        return urlarray
                
    def get_tzname(self, tutor):
        """return self.tutorsdict[tutor]['user']['profile']['timezone']['tzname']"""
        return self.tutorsdict[tutor]['tzname']
        
def __get_alpha_2(countryname):
    import pycountry
    
    for country in pycountry.countries:
        if (country.name).replace(' ', '') == countryname.replace(' ', ''):
            return country.alpha_2
    for country in pycountry.countries:
        if (country.name).replace(' ', '').startswith(countryname.replace(' ', '')):
            return country.alpha_2
    return '**'
    
def __print_country(tzname):
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent='geoapiExercises')
    
    cityname = tzname.split('/')[-1].replace('_', ' ')
    country = geolocator.geocode(cityname, language='en')
    countryname = '##'
    if country is not None:
        countryname = country.address.split(', ')[-1]
    
    print(__get_alpha_2(countryname)+','+countryname+','+tzname)
    
def find_notexisting():
    tznameset = set()
    for p in [Preply('english'), Preply('japanese'), Preply('russian')]:
        tznameset = tznameset.union(p.get_tznameset())

    import csv
    tznameexisting = list()
    
    from os.path import join
    with open(join('.', 'preply', 'country.csv'), 'r') as csvfile:
        spamreader = csv.reader(csvfile)
        next(spamreader)
        for row in spamreader:
            tznameexisting.append(row[2])
            
    for tzname in tznameset:
        if tzname not in tznameexisting:
            if tzname == 'GMT':
                continue
            if tzname.startswith('Etc/'):
                continue
            __print_country(tzname)
            
def prfunc():
    """from preply import Preply"""
    
    """"""
    langarray = [['english', 1200], ['japanese', 100], ['spanish', 500]]
    """langarray = [['english', 1200], ['japanese', 100]]"""
    """langarray = [['spanish', 500]]"""
    for lang in langarray:
        pr = Preply(lang[0])
        pr.collect(lang[1])
    print('Hello, prfunc!')

if __name__ == '__main__':
    """"""
    
"""
xxxarray = list()
with open('history.txt', 'r') as f:
    while True:
        line = f.readline()
        if len(line) <= 0:
            break
        xxxarray.append(line.strip().split(' ')[0]+' '+line.strip().split(' ')[-1].replace('/english','/').replace('/japanese','/').replace('/russian','/'))
        
with open('history.txt.txt', 'w') as f:
    for xxx in xxxarray:
        if xxx[-1] == '/':
            f.write(xxx+'\n')
        else:
            f.write(xxx+'/'+'\n')
"""
"""
with open('history.txt', 'r') as f:
    while True:
        line = f.readline()
        if len(line) <= 0:
            break
        url = line.strip().split(' ')[-1]
        url = url[:-1] if url[-1] == '/' else url
        if 'italki' in url:
            print(url.split('/')[-1])
"""
