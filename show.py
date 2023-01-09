from preply import Preply
from italki import Italki

def __show(urlarray, p=0, w=10, altwindow=False, history=False):
    import pyautogui
    import pyperclip
    
    clipboard = str()
    for i in range(len(urlarray)):
        url = urlarray[i]
        print(i, url)
        if altwindow == True and i == 0:
            pyautogui.hotkey('alt', 'tab')
            pyautogui.press('enter')
        if i >= p and i <= (p+w)-1:
            pyautogui.hotkey('ctrl', 't')
            pyautogui.press('enter')
            pyperclip.copy(url)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            clipboard += str(i)+' '+url+'\n'
    pyperclip.copy(clipboard)
    
    if history:
        """
        with open('history.txt', 'a') as f:
            f.write(clipboard)
        """
        f = open('history.txt', 'a')
        f.write(clipboard)
        f.close()
            
"""
def __loopfunc(t, func, *args, **kwargs):
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
"""
            
def show_country_id(country_idarray, srcarray=[Preply, Italki], langarray=['english', 'japanese', 'spanish']):
    tutoringarray = list()
    for src in srcarray:
        for lang in langarray:
            tutoringarray.append(src(lang))
        
    urlarray = list()
    for country_id in country_idarray:
        for tutoring in tutoringarray:
            if country_id == 'EG':
                """urlarray += tutoring.get_urlarray([['living_country_id', country_id], ['origin_country_id', 'PH', False], ['origin_country_id', 'EG', True], ['origin_country_id', 'ZA', False]], unseen=True)"""
                """urlarray += __loopfunc(1, tutoring.get_urlarray, [['living_country_id', country_id], ['origin_country_id', 'PH', False], ['origin_country_id', 'EG', True], ['origin_country_id', 'ZA', False]], unseen=True)"""
                urlarray += tutoring.get_urlarray([['living_country_id', country_id], ['origin_country_id', 'PH', False], ['origin_country_id', 'EG', True], ['origin_country_id', 'ZA', False]], unseen=True)
            else:
                """urlarray += tutoring.get_urlarray([['living_country_id', country_id], ['origin_country_id', 'PH', False], ['origin_country_id', 'ZA', False]], unseen=True)"""
                """urlarray += __loopfunc(1, tutoring.get_urlarray, [['living_country_id', country_id], ['origin_country_id', 'PH', False], ['origin_country_id', 'ZA', False]], unseen=True)"""
                urlarray += tutoring.get_urlarray([['living_country_id', country_id], ['origin_country_id', 'PH', False], ['origin_country_id', 'ZA', False]], unseen=True)
                
    __show(sorted(set(urlarray)), history=True)
    
def show_city_name(city_namearray, langarray=['english', 'japanese', 'spanish']):
    tutoringarray = list()
    for lang in langarray:
        tutoringarray.append(Italki(lang))
        
    urlarray = list()
    for city_name in city_namearray:
        for tutoring in tutoringarray:
            """urlarray += tutoring.get_urlarray([['living_city_name', city_name]], unseen=True)"""
            """urlarray += __loopfunc(1, tutoring.get_urlarray, [['living_city_name', city_name]], unseen=True)"""
            urlarray += tutoring.get_urlarray([['living_city_name', city_name]], unseen=True)
            
    __show(sorted(set(urlarray)), history=True)

if __name__ == '__main__':
    """"""
    