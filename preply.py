class Preply:
    class FileIndex:
        def __init__(self, lang):
            self.lang = lang

        @classmethod
        def __get_path(cls, f):
            from os.path import join
            return join('.', 'preply', f)

        def get_jsonorgpath(self):
            return self.__class__.__get_path('preply_'+self.lang+'org.json')

        def get_jsonpath(self):
            return self.__class__.__get_path('preply_'+self.lang+'.json')

        @classmethod
        def get_countrypath(cls):
            return cls.__get_path('country.csv')
            
        @classmethod
        def get_historypath(cls):
            from os.path import join
            return join('.', 'history.txt')

    def __init__(self, language):
        self.language = language
        self.fileindex = self.__class__.FileIndex(self.language[0:2])
        
    @classmethod
    def __load_tutorsdict(cls, jsonpath):
        tutorsdict = dict()

        import os.path
        if os.path.exists(jsonpath):
            import json
            with open(jsonpath, 'r') as f:
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
        
    def __get_urliter(self, pagenumber):
        for i in range(1,pagenumber):
            url = 'https://preply.com/en/online/'+self.language+'-tutors'
            if i >= 2:
                url += '?page='+str(i)
            yield url

    @classmethod
    def __json_tutorsdicttmp(cls, url):
        tutorsdicttmp = dict()

        for i in range(10):
            while True:
                try:
                    import requests
                    response = requests.get(url)
                    break
                except Exception as err:
                    print(err)
                    from time import sleep
                    sleep(60)

            if response.status_code == 200:
                from bs4 import BeautifulSoup
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')

                import json
                soupjson = soup.find('script', id='__NEXT_DATA__', type='application/json')
                tutorsjson = json.loads(soupjson.string)['props']['pageProps']['ssrAllTutors']['tutors']

                for tutor in tutorsjson:
                    tutorsdicttmp[tutor['id']] = tutor

                break

            if i == (10-1):
                print(response.status_code, url)
                break

            else:
                from time import sleep
                sleep(1)
                continue

        return tutorsdicttmp

    """def collect(self, pagenumber, reload=False):"""
    def collect(self, pagenumber):
        tutorsorgdict = self.__class__.__load_tutorsdict(self.fileindex.get_jsonorgpath())
        tutorsdict = self.__class__.__load_tutorsdict(self.fileindex.get_jsonpath())
        
        """
        if reload:
            tutorsorgdict = dict()
            tutorsdict = dict()
        """

        urliter = self.__get_urliter(pagenumber)
        for url in urliter:
            from time import sleep
            sleep(1)

            tutorsorgdicttmp = self.__class__.__json_tutorsdicttmp(url)
            tutorsorgdict.update(tutorsorgdicttmp)

        import json

        """with open(self.fileindex.get_jsonpath(), 'w') as f:"""
        with open(self.fileindex.get_jsonorgpath(), 'w') as f:
            json.dump(tutorsorgdict, f)

        for k in tutorsorgdict.keys():
            try:
                if isinstance(tutorsorgdict[k]['user']['profile']['timezone'], dict):
                    """"""
                else:
                    continue
                    
                if 'tzname' in tutorsorgdict[k]['user']['profile']['timezone'].keys():
                    """"""
                else:
                    continue
                    
                tutorsdict.setdefault(k, dict())
                tutorsdict[k]['tzname'] = tutorsorgdict[k]['user']['profile']['timezone']['tzname']
                tutorsdict[k]['countryOfBirth'] = tutorsorgdict[k]['countryOfBirth']['name']
            except TypeError as e:
                print(e)
            except KeyError as e:
                print(e)

        with open(self.fileindex.get_jsonpath(), 'w') as f:
            json.dump(tutorsdict, f)
            print('len(tutorsdict.keys()):', len(tutorsdict.keys()))

    @classmethod
    def __get_countrydict(cls):
        import csv

        countrydict = {'countryname': dict(), 'timezone': dict()}
        with open(self.fileindex.__class__.get_countrypath(), 'r') as f:
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

        tutorsdict = self.__class__.__load_tutorsdict(self.fileindex.get_jsonpath())
        countrydict = self.__class__.__get_countrydict()

        urlarray = list()
        for t in range(100):
            try:
                tutorarray = list()
                for tutor in tutorsdict.keys():
                    if 'countryOfBirth' not in tutorsdict[tutor]:
                        continue
                    if 'tzname' not in tutorsdict[tutor]:
                        continue
                    f = True
                    for con in conarray:
                        if con[0] == 'origin_country_id':
                            if not((tutorsdict[tutor]['countryOfBirth'] in countrydict['countryname'].get(con[1], [])) == con[2]):
                                f = False
                                break
                        if con[0] == 'living_country_id':
                            if not((tutorsdict[tutor]['tzname'] in countrydict['timezone'].get(con[1], [])) == con[2]):
                                f = False
                                break
                        if con[0] == 'tzname':
                            if not((tutorsdict[tutor]['tzname'] == con[1]) == con[2]):
                                f = False
                                break
                    if f == True:
                        tutorarray.append(tutor)

                history = list()
                """with open('history.txt', 'r') as f:"""
                with open(self.fileindex.__class__.get_historypath(), 'r') as f:
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
        tutorsdict = self.__class__.__load_tutorsdict(self.fileindex.get_jsonpath())
        return tutorsdict[tutor]['tzname']

    def get_tznameset(self):
        tutorsdict = self.__class__.__load_tutorsdict(self.fileindex.get_jsonpath())

        tznameset = set()
        for tutor in tutorsdict.keys():
            try:
                tznameset.add(tutorsdict[tutor]['tzname'])
            except KeyError as e:
                print(e)

        return tznameset

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
    langarray = [['english', 1300], ['japanese', 100], ['spanish', 500]]
    """langarray = [['spanish', 500]]"""
    for lang in langarray:
        pr = Preply(lang[0])
        pr.collect(lang[1])
        
        from git_push import git_push
        git_push([pr.fileindex.get_jsonpath()])
        
    """
    from os.path import join
    parray = list()
    for lang in ['en', 'ja', 'sp']:
        parray.append(join('.', 'preply', 'preply_'+lang+'.json'))
    git_push(parray)
    """
    
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
