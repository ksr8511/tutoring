class Italki:
    class FileIndex:
        def __init__(self, language):
            self.language = language
            
        @classmethod
        def __get_file(cls, f):
            from os.path import join
            return join('.', 'italki', f)
            
        def get_tecdictorgfile(self):
            return self.__class__.__get_file('italki_'+self.language[0:2]+'org.json')
            
        def get_tecdictfile(self):
            return self.__class__.__get_file('italki_'+self.language[0:2]+'.json')
            
        def get_logfile(self):
            return self.__class__.__get_file('log.'+self.language[0:2]+'.pickle')
            
    def __init__(self, language):
        self.language = language
        self.fileindex = self.__class__.FileIndex(self.language[0:2])
        
    @classmethod
    def __loopfunc(cls, t, func, *args, **kwargs):
        y = None
        while True:
            try:
                y = func(*args, **kwargs)
                break
            except Exception as err:
                print(err)
                from time import sleep
                sleep(t)
                
        return y
        
    @classmethod
    def __get_tecdicttmp(cls, url):
        import requests
        response = cls.__loopfunc(60, requests.get, url)
                
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
        
    def collect(self):
        """
        def dump(file, mode, module, obj):
            with open(file, mode) as f:
                module.dump(obj, f)
        """
                
        tecdictorg = dict()
        baseurl = 'https://www.italki.com/teachers/'+self.language
        log = [[baseurl, '', False]]
        
        import json
        import pickle
        
        from os.path import exists
        if exists(self.fileindex.get_tecdictorgfile()):
            """
            with open(self.fileindex.get_tecdictorgfile(), 'r') as f:
                tecdictorg = json.load(f)
            """
            f = open(self.fileindex.get_tecdictorgfile(), 'r')
            tecdictorg = json.load(f)
            f.close()
        if exists(self.fileindex.get_logfile()):
            """
            with open(self.fileindex.get_logfile(), 'rb') as f:
                log = pickle.load(f)
            """
            f = open(self.fileindex.get_logfile(), 'rb')
            log = pickle.load(f)
            f.close()
            
        jsonfile = open(self.fileindex.get_tecdictorgfile(), 'w')
        logfile = open(self.fileindex.get_logfile(), 'wb')
        
        logiter = iter(log)
        while True:
            entry = next(logiter, None)
            if entry is None:
                break
                
            if entry[2]:
                continue
                
            from time import sleep
            sleep(1)
            
            tecdicttmp = self.__class__.__get_tecdicttmp(entry[0])
            tecdictorg.update(tecdicttmp)
            
            if len(tecdicttmp) >= 20:
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
                    
            """
            self.__class__.__loopfunc(1, dump, self.fileindex.get_tecdictorgfile(), 'w', json, tecdictorg)
            """
            """jsonfile = open(self.fileindex.get_tecdictorgfile(), 'w')"""
            """self.__class__.__loopfunc(1, json.dump, tecdictorg, jsonfile)"""
            json.dump(tecdictorg, jsonfile)
            """jsonfile.close()"""
            """self.__class__.__loopfunc(1, dump, self.fileindex.get_logfile(), 'wb', pickle, log)"""
            """logfile = open(self.fileindex.get_logfile(), 'wb')"""
            """self.__class__.__loopfunc(1, pickle.dump, log, logfile)"""
            pickle.dump(log, logfile)
            """logfile.close()"""
            
        jsonfile.close()
        logfile.close()
            
        tecdict = dict()
        for k in tecdictorg.keys():
            try:
                tecdict.setdefault(k, dict())
                tecdict[k]['origin_country_id'] = tecdictorg[k]['origin_country_id']
                tecdict[k]['living_country_id'] = tecdictorg[k]['living_country_id']
                tecdict[k]['origin_city_name'] = tecdictorg[k]['origin_city_name']
                tecdict[k]['living_city_name'] = tecdictorg[k]['living_city_name']
                tecdict[k]['timezone'] = tecdictorg[k]['timezone']
            except KeyError as e:
                print(e)
            """
            except TypeError as e:
                print(e)
            """
                
        """self.__class__.__loopfunc(1, dump, self.fileindex.get_tecdictfile(), 'w', json, tecdict)"""
        tecdictfile = open(self.fileindex.get_tecdictfile(), 'w')
        """self.__class__.__loopfunc(1, json.dump, tecdict, tecdictfile)"""
        json.dump(tecdict, tecdictfile)
        tecdictfile.close()
        
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
        
    """def __get_urlarray(self, conarray, unseen):"""
    def get_urlarray(self, conarray, unseen):
        """
        tecdict = dict()
        with open(self.fileindex.get_tecdictfile(), 'r') as f:
            import json
            tecdict = json.load(f)
        """
        import json
        f = open(self.fileindex.get_tecdictfile(), 'r')
        tecdict = json.load(f)
        f.close()
        
        """
        history = list()
        with open('history.txt', 'r') as f:
            while True:
                line = f.readline()
                if len(line) <= 0:
                    break
                history.append(line.strip().split(' ')[-1])
        """
        f = open('history.txt', 'r')
        while True:
            line = f.readline()
            if len(line) <= 0:
                break
            history.append(line.strip().split(' ')[-1])
        f.close()
        
        urlarray = list()
        for k in tecdict.keys():
            if self.__class__.__check(tecdict[k], conarray) == True:
                url = 'https://www.italki.com/teacher/'+str(k)+'/'
                if unseen == True and url in history:
                    continue
                urlarray.append(url)
                
        return urlarray
    
    """
    def get_urlarray(self, conarray, unseen=False):
        urlarray = self.__class__.__loopfunc(1, self.__get_urlarray, conarray, unseen)
        return urlarray
    """
        
def itfunc():
    langarray = ['english', 'japanese', 'spanish']
    
    for lang in langarray:
        it = Italki(lang)
        
        it.collect()
        
        from git_push import git_push
        git_push([it.fileindex.get_tecdictfile()])
        
    for lang in langarray:
        it = Italki(lang)
        
        from os.path import exists
        from os import remove
        if exists(it.fileindex.get_logfile()):
            remove(it.fileindex.get_logfile())
            
if __name__ == '__main__':
    """
    itfunc()
    """
    