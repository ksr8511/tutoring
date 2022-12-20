import json
import pickle

class Italki:
    def __init__(self, language):
        self.language = language
        
    @classmethod
    def __get_tmptecdict(cls, url):
        response = None
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
            tecjson = json.loads(soupjson.string)['props']['pageProps']['teachers']
            tmptecdict = dict()
            for t in tecjson:
                userinfo = t['user_info']
                tmptecdict[userinfo['user_id']] = userinfo
                
            return tmptecdict
        else:
            print(response.status_code, url)
            
        return dict()
        
    @classmethod
    def __get_urlcntyarray(cls, url):
        urlcntyarray = list()
        for i in range(26):
            for j in range(26):
                urlcntyarray.append(url+'?from%5B0%5D='+chr(i+65)+chr(j+65))
                
        return urlcntyarray
        
    @classmethod
    def __get_urllpgrparray(cls, url):
        urllpgrparray = list()
        urllpgrparray.append(url+'&maxPrice=10')
        urllpgrparray.append(url+'&minPrice=11&maxPrice=15')
        urllpgrparray.append(url+'&minPrice=16&maxPrice=20')
        urllpgrparray.append(url+'&minPrice=21&maxPrice=25')
        urllpgrparray.append(url+'&minPrice=25&maxPrice=30')
        urllpgrparray.append(url+'&minPrice=31&maxPrice=35')
        urllpgrparray.append(url+'&minPrice=36&maxPrice=40')
        urllpgrparray.append(url+'&minPrice=41')
        
        return urllpgrparray
        
    @classmethod
    def __get_urllparray(cls, url):
        from copy import copy
        tmpurl = copy(url)
        
        minprice = -1
        if tmpurl.find('minPrice=') >= 0:
            minpricepos = tmpurl.find('minPrice=')+len('minPrice=')
            minprice = int(tmpurl[minpricepos:minpricepos+2])
        else:
            minprice = 6
        maxprice = -1
        if tmpurl.find('maxPrice=') >= 0:
            maxpricepos = tmpurl.find('maxPrice=')+len('maxPrice=')
            maxprice = int(tmpurl[maxpricepos:maxpricepos+2])
        else:
            maxprice = 45
        
        if tmpurl.find('&minPrice=') >= 0:
            tmpurl = tmpurl[:tmpurl.find('&minPrice=')]
        if tmpurl.find('&maxPrice=') >= 0:
            tmpurl = tmpurl[:tmpurl.find('&maxPrice=')]
            
        urllpgrp = list()
        for price in range(minprice, maxprice+1):
            urllpgrp.append(tmpurl+'&minPrice='+str(price)+'&maxPrice='+str(price))
            
        return urllpgrp
        
    @classmethod
    def __get_urlttarray(cls, url):
        ttarray = list()
        ttarray.append(url+'&teacher_type=pro')
        ttarray.append(url+'&teacher_type=tutor')
        
        return ttarray
        
    @classmethod
    def __get_urlkeywordarray(cls, url):
        keywordarray = list()
        for i in range(26):
            keywordarray.append(url+'&keyword='+chr(i+97))
            
        return keywordarray
        
    @classmethod
    def __get_file(cls, f):
        from os.path import join
        return join('.', 'italki', f)
        
    def __get_tecdictorgfile(self):
        return self.__class__.__get_file('italki_'+self.language[0:2]+'org.json')
        
    def __get_tecdictfile(self):
        return self.__class__.__get_file('italki_'+self.language[0:2]+'.json')
        
    def __get_urlpairarrayfile(self):
        return self.__class__.__get_file('log.'+self.language[0:2]+'.pickle')
        
    def collect(self, cont=False):
        tecorgdict = dict()
        baseurl = 'https://www.italki.com/teachers/'+self.language
        log = [[baseurl, '', False]]
        
        from os.path import exists
        if exists(self.__get_tecdictorgfile()):
            with open(self.__get_tecdictorgfile(), 'r') as f:
                tecorgdict = json.load(f)
        if cont and exists(self.__get_urlpairarrayfile()):
            with open(self.__get_urlpairarrayfile(), 'rb') as f:
                log = pickle.load(f)
                
        logiter = iter(log)
        while True:
            entry = next(logiter, None)
            if entry is None:
                break
                
            if entry[2]:
                continue
                
            from time import sleep
            sleep(1)
            
            tmptecdict = self.__class__.__get_tmptecdict(entry[0])
            tecorgdict.update(tmptecdict)
            
            if len(tmptecdict) >= 20:
                if entry[1] == '':
                    urlcntyarray = self.__class__.__get_urlcntyarray(entry[0])
                    log.extend([[urlcnty, 'cnty', False] for urlcnty in urlcntyarray])
                elif entry[1] == 'cnty':
                    urllpgrparray = self.__class__.__get_urllpgrparray(entry[0])
                    log.extend([[urllpgrp, 'lpgrp', False] for urllpgrp in urllpgrparray])
                elif entry[1] == 'lpgrp':
                    urllparray = self.__class__.__get_urllparray(entry[0])
                    log.extend([[urllp, 'lp', False] for urllp in urllparray])
                elif entry[1] == 'lp':
                    urlttarray = self.__class__.__get_urlttarray(entry[0])
                    log.extend([[urltt, 'tt', False] for urltt in urlttarray])
                elif entry[1] == 'tt':
                    urlkeywordarray = self.__class__.__get_urlkeywordarray(entry[0])
                    log.extend([[urlkeyword, 'keyword', False] for urlkeyword in urlkeywordarray])
                    
            entry[2] = True
                    
            while True:
                try:
                    with open(self.__get_tecdictorgfile(), 'w') as f:
                        json.dump(tecorgdict, f)
                    break
                except Exception as err:
                    print(err)
                    from time import sleep
                    sleep(60)
                    
            while True:
                try:
                    with open(self.__get_urlpairarrayfile(), 'wb') as f:
                        pickle.dump(log, f)
                    break
                except Exception as err:
                    print(err)
                    from time import sleep
                    sleep(60)
                
            """entry[2] = True"""
            
        tecdict = dict()
        for k in tecorgdict.keys():
            try:
                tecdict.setdefault(k, dict())
                tecdict[k]['origin_country_id'] = tecorgdict[k]['origin_country_id']
                tecdict[k]['living_country_id'] = tecorgdict[k]['living_country_id']
                tecdict[k]['origin_city_name'] = tecorgdict[k]['origin_city_name']
                tecdict[k]['living_city_name'] = tecorgdict[k]['living_city_name']
                tecdict[k]['timezone'] = tecorgdict[k]['timezone']
            except TypeError as e:
                print(e)
            except KeyError as e:
                print(e)
                
        with open(self.__get_tecdictfile(), 'w') as f:
            json.dump(tecdict, f)
            
    @classmethod
    def __check(cls, tec, conarrayorg):
        from collections.abc import Iterable
        
        conarray = list()
        for con in conarrayorg:
            if isinstance(con[1], str):
                conarray.append(con)
            elif isinstance(con[1], Iterable) and all([isinstance(x, str) for x in con[1]]):
                for x in con[1]:
                    conarray.append([con[0], x, con[2]])
                
        for con in conarray:
            k = con[0]
            v1 = con[1]
            if len(con) == 2:
                v2 = True
            else:
                v2 = con[2]
                
            if not(v2 == (tec[k] == v1)):
                return False
                
        return True
        
    def get_urlarray(self, conarray, unseen=False):
        urlarray = list()
        
        for t1 in range(100):
            try:
                tecdict = dict()
                for t2 in range(100):
                    try:
                        with open(self.__get_tecdictfile(), 'r') as f:
                            tecdict = json.load(f)
                        break
                    except Exception as err:
                        print(err)
                        import time
                        time.sleep(1)
                        tecdict = dict()
                    
                history = list()
                with open('history.txt', 'r') as f:
                    while True:
                        line = f.readline()
                        if len(line) <= 0:
                            break
                        history.append(line.strip().split(' ')[-1])
                        
                for k in tecdict.keys():
                    if self.__class__.__check(tecdict[k], conarray) == True:
                        """url = 'https://www.italki.com/teacher/'+str(tecdict[k]['user_id'])+'/'"""
                        url = 'https://www.italki.com/teacher/'+str(k)+'/'
                        if unseen == True and url in history:
                            continue
                        urlarray.append(url)
                break
            except Exception as err:
                print(err)
                import time
                time.sleep(1)
                urlarray = list()
                
        return urlarray
    
def itfunc(*args, **kwargs):
    """from italki import Italki"""
    
    """"""
    langarray = ['english', 'japanese', 'spanish']
    """langarray = ['english', 'japanese']"""
    """langarray = ['spanish']"""
    for lang in langarray:
        it = Italki(lang)
        it.collect(*args, **kwargs)
    print('Hello, itfunc!')
                    
if __name__ == '__main__':
    """"""
    