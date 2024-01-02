from tutoring import Tutoring

class Preply(Tutoring):
    pf = 'preply'
    
    def __init__(self, language):
        super().__init__(self.__class__.pf, language)
        self.pagenumber = self.__class__.__get_pagenumber(language)
        
    @classmethod
    def __get_pagenumber(cls, lang):
        if lang == 'english':
            return 1400
        elif lang == 'japanese':
            return 150
        elif lang == 'spanish':
            return 500
        return 0
        
    @classmethod
    def get_countrypath(cls):
        from os.path import join
        from pathlib import Path
        return join(Path.home(), 'jupyter', 'tutoring', cls.pf, 'country.csv')
        
    @classmethod
    def get_historypath(cls):
        from os.path import join
        from pathlib import Path
        return join(Path.home(), 'jupyter', 'tutoring', 'history.txt')
        
    @classmethod
    def load_tutorsdict(cls, jsonpath):
        tutorsdict = dict()
        
        import os.path
        if os.path.exists(jsonpath):
            """
            import json
            f = open(jsonpath, 'r')
            tutorsdict = json.load(f)
            f.close()
            """
            import json
            from json import JSONDecodeError
            f = None
            try:
                f = open(jsonpath, 'r')
                tutorsdict = json.load(f)
            except JSONDecodeError as e:
                print(e)
                raise JSONDecodeError(e)
            except TypeError as e:
                print(e)
                raise TypeError(e)
            finally:
                if f is not None:
                    f.close()
                    
        x = 999.99
        dst = dict()
        for k in tutorsdict.keys():
            if float(tutorsdict[k]['seoPrice']) < x:
                dst[k] = tutorsdict[k]
                    
        """return tutorsdict"""
        return dst
        
    def __get_urliter(self):
        for i in range(1, self.pagenumber):
            url = 'https://preply.com/en/online/'+self.language+'-tutors'
            if i >= 2:
                url += '?page='+str(i)
            yield url
            
    @classmethod
    def __json_tutorsdicttmp(cls, url):
        tutorsdicttmp = dict()
        
        for i in range(10):
            import requests
            response = cls.loopfunc(60, requests.get, url)
            
            if response.status_code == 200:
                from bs4 import BeautifulSoup
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')

                import json
                soupjson = soup.find('script', id='__NEXT_DATA__', type='application/json')
                
                """tutorsdicttmp = dict()"""
                try:
                    tutorsjson = json.loads(soupjson.string)['props']['pageProps']['ssrAllTutors']['tutors']
                    for tutor in tutorsjson:
                        tutorsdicttmp[tutor['id']] = tutor
                except KeyError as err:
                    print(err)
                    from time import sleep
                    sleep(1)
                    continue
                    
                """return tutorsdicttmp"""
                break

            if i == (10-1):
                """print(response.status_code, url)"""
                break

            else:
                from time import sleep
                sleep(1)
                continue
                
        print(response.status_code, url)
        """return dict()"""
        return tutorsdicttmp
        
    def collect(self):
        """
        tutorsorgdict = self.__class__.load_tutorsdict(self.fileindex.get_jsonorgpath())
        """
        import json
        from json import JSONDecodeError
        tutorsorgdict = dict()
        try:
            tutorsorgdict = self.__class__.load_tutorsdict(self.fileindex.get_jsonorgpath())
        except JSONDecodeError as e:
            tutorsorgdict = self.__class__.load_tutorsdict(self.fileindex.get_jsonorgpath()+'.bak')
        except TypeError as e:
            tutorsorgdict = self.__class__.load_tutorsdict(self.fileindex.get_jsonorgpath()+'.bak')
            
        tutorsdict = self.__class__.load_tutorsdict(self.fileindex.get_jsonpath())
            
        try:
            urliter = self.__get_urliter()
            for url in urliter:
                from time import sleep
                sleep(1)

                tutorsorgdicttmp = self.__class__.__json_tutorsdicttmp(url)
                tutorsorgdict.update(tutorsorgdicttmp)
                
                """break"""
        except Exception as err:
            print(err)
        except KeyboardInterrupt as err:
            """print(err)"""
            raise KeyboardInterrupt
        finally:
            """import json"""
            f = open(self.fileindex.get_jsonorgpath(), 'w')
            json.dump(tutorsorgdict, f)
            f.close()
            fbak = open(self.fileindex.get_jsonorgpath()+'.bak', 'w')
            json.dump(tutorsorgdict, fbak)
            fbak.close()

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
                tutorsdict[k]['seoPrice'] = tutorsorgdict[k]['seoPrice']['value']
            except KeyError as e:
                print(e)

        f = open(self.fileindex.get_jsonpath(), 'w')
        json.dump(tutorsdict, f)
        f.close()
        print('len(tutorsdict.keys()):', len(tutorsdict.keys()))

    @classmethod
    def __get_countrydict(cls):
        import csv

        countrydict = {'countryname': dict(), 'timezone': dict()}
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
        
    def remove_log(self):
        """"""
        
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
    """geolocator = Nominatim(user_agent='geoapiExercises')"""
    geolocator = Nominatim(user_agent='preply')

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
    
"""
from history import arrange

prfunc()
find_notexisting()
print(get_tzname('2720881'))
arrange()
"""
