from tutoring import Tutoring

class Preply(Tutoring):
    """"""
    pf = 'preply'
    
    """def __init__(self, language, pagenumber):"""
    def __init__(self, language):
        self.language = language
        self.pagenumber = self.__class__.__get_pagenumber(language)
        """self.fileindex = self.__class__.FileIndex(self.language[0:2])"""
        """self.fileindex = self.__class__.FileIndex(self.language)"""
        """self.fileindex = self.__class__.FileIndex('preply', self.language)"""
        """"""
        self.fileindex = self.__class__.FileIndex(self.__class__.pf, self.language)
        """self.fileindex = self.__class__.FileIndex(self.__class__.__get_pf(), self.language)"""
        
    """
    @classmethod
    def __get_pf(cls):
        return 'preply'
    """
    
    @classmethod
    def __get_pagenumber(cls, lang):
        if lang == 'english':
            return 1300
        elif lang == 'japanese':
            return 100
        elif lang == 'spanish':
            return 500
        return 0
        
    @classmethod
    def get_countrypath(cls):
        """return cls.__get_path('country.csv')"""
        from os.path import join
        """return join('.', 'preply', 'country.csv')"""
        """"""
        return join('.', cls.pf, 'country.csv')
        """return join('.', cls.__get_pf(), 'country.csv')"""
        
    @classmethod
    def get_historypath(cls):
        from os.path import join
        return join('.', 'history.txt')
        
    @classmethod
    def load_tutorsdict(cls, jsonpath):
        import os.path
        if os.path.exists(jsonpath):
            """
            with open(jsonpath, 'r') as f:
                import json
                tutorsdict = cls.loopfunc(1, json.load, f)
                return tutorsdict
            """
            import json
            f = open(jsonpath, 'r')
            """tutorsdict = cls.loopfunc(1, json.load, f)"""
            tutorsdict = json.load(f)
            f.close()
            
            return tutorsdict
                
        return dict()
        
    """def __get_urliter(self, pagenumber):"""
    def __get_urliter(self):
        for i in range(1, self.pagenumber):
            url = 'https://preply.com/en/online/'+self.language+'-tutors'
            if i >= 2:
                url += '?page='+str(i)
            yield url
            
    @classmethod
    def __json_tutorsdicttmp(cls, url):
        """tutorsdicttmp = dict()"""

        for i in range(10):
            """

            """
            import requests
            response = cls.loopfunc(60, requests.get, url)
            """response = cls.get_response(url)"""
            
            if response.status_code == 200:
                from bs4 import BeautifulSoup
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')

                import json
                soupjson = soup.find('script', id='__NEXT_DATA__', type='application/json')
                
                tutorsdicttmp = dict()
                try:
                    tutorsjson = json.loads(soupjson.string)['props']['pageProps']['ssrAllTutors']['tutors']
                    for tutor in tutorsjson:
                        tutorsdicttmp[tutor['id']] = tutor
                except KeyError as err:
                    print(err)
                    from time import sleep
                    sleep(1)
                    continue

                """break"""
                return tutorsdicttmp

            if i == (10-1):
                print(response.status_code, url)
                break

            else:
                from time import sleep
                sleep(1)
                continue

        """return tutorsdicttmp"""
        return dict()
        
    """def collect(self, pagenumber):"""
    def collect(self):
        tutorsorgdict = self.__class__.load_tutorsdict(self.fileindex.get_jsonorgpath())
        tutorsdict = self.__class__.load_tutorsdict(self.fileindex.get_jsonpath())
        
        """urliter = self.__get_urliter(pagenumber)"""
        urliter = self.__get_urliter()
        for url in urliter:
            from time import sleep
            sleep(1)

            tutorsorgdicttmp = self.__class__.__json_tutorsdicttmp(url)
            tutorsorgdict.update(tutorsorgdicttmp)

        import json
        """
        with open(self.fileindex.get_jsonorgpath(), 'w') as f:
            json.dump(tutorsorgdict, f)
        """
        f = open(self.fileindex.get_jsonorgpath(), 'w')
        json.dump(tutorsorgdict, f)
        f.close()

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
            except KeyError as e:
                print(e)
            """
            except TypeError as e:
                print(e)
            """

        """
        with open(self.fileindex.get_jsonpath(), 'w') as f:
            json.dump(tutorsdict, f)
            print('len(tutorsdict.keys()):', len(tutorsdict.keys()))
        """
        f = open(self.fileindex.get_jsonpath(), 'w')
        json.dump(tutorsdict, f)
        f.close()
        print('len(tutorsdict.keys()):', len(tutorsdict.keys()))

    @classmethod
    def __get_countrydict(cls):
        import csv

        countrydict = {'countryname': dict(), 'timezone': dict()}
        """
        with open(cls.get_countrypath(), 'r') as f:
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
        """
        f = open(cls.get_countrypath(), 'r')
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
        f.close()
        
        return countrydict
        
    """def __get_urlarray(self, conarrayorg, unseen):"""
    def get_urlarray(self, conarrayorg, unseen):
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

        tutorsdict = self.__class__.load_tutorsdict(self.fileindex.get_jsonpath())
        countrydict = self.__class__.__get_countrydict()
        
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
        """
        with open(self.__class__.get_historypath(), 'r') as f:
            while True:
                line = f.readline()
                if len(line) <= 0:
                    break
                history.append(line.strip().split(' ')[-1])
        """
        f = open(self.__class__.get_historypath(), 'r')
        while True:
            line = f.readline()
            if len(line) <= 0:
                break
            history.append(line.strip().split(' ')[-1])
        f.close()
        
        urlarray = list()
        for tutor in tutorarray:
            url = 'https://preply.com/en/tutor/2300258/'.replace('2300258',str(tutor))
            if unseen == True and url in history:
                continue
            else:
                urlarray.append(url)
                
        return urlarray

    """
    def get_urlarray(self, conarrayorg, unseen=False):
        urlarray = self.__class__.loopfunc(1, self.__get_urlarray, conarrayorg, unseen)
        return urlarray
    """
        
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
    for p in [Preply('english'), Preply('japanese'), Preply('spanish')]:
        tutorsdict = p.__class__.load_tutorsdict(p.fileindex.get_jsonpath())
        for tutor in tutorsdict.keys():
            try:
                tznameset.add(tutorsdict[tutor]['tzname'])
            except KeyError as e:
                print(e)

    import csv
    tznameexisting = list()

    from os.path import join
    """
    with open(join('.', 'preply', 'country.csv'), 'r') as csvfile:
        spamreader = csv.reader(csvfile)
        next(spamreader)
        for row in spamreader:
            tznameexisting.append(row[2])
    """
    """csvfile = open(join('.', 'preply', 'country.csv'), 'r')"""
    csvfile = open(Preply.get_countrypath(), 'r')
    spamreader = csv.reader(csvfile)
    next(spamreader)
    for row in spamreader:
        tznameexisting.append(row[2])
    csvfile.close()
    
    for tzname in tznameset:
        if tzname not in tznameexisting:
            if tzname == 'GMT':
                continue
            if tzname.startswith('Etc/'):
                continue
            __print_country(tzname)
            
def get_tzname(tutor):
    tzname = None
    for p in [Preply('english'), Preply('japanese'), Preply('spanish')]:
        tutorsdict = p.__class__.load_tutorsdict(p.fileindex.get_jsonpath())
        if tutor in tutorsdict.keys() and 'tzname' in tutorsdict[tutor].keys():
            tzname = tutorsdict[tutor]['tzname']
            break
            
    return tzname
    
def prfunc():
    """langarray = [['english', 1300], ['japanese', 100], ['spanish', 500]]"""
    langarray = ['english', 'japanese', 'spanish']
    for lang in langarray:
        """
        pr = Preply(lang[0])
        pr.collect(lang[1])
        """
        """pr = Preply(lang[0], lang[1])"""
        pr = Preply(lang)
        pr.collect()
        
        from git_push import git_push
        git_push([pr.fileindex.get_jsonpath()])
        
if __name__ == '__main__':
    """
    from history import arrange
    
    prfunc()
    find_notexisting()
    print(get_tzname('2720881'))
    arrange()
    """
    