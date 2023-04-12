def collect(langarray, h):
    from preply import Preply
    from italki import Italki
    
    while True:
        from time import sleep
        sleep(60)
        
        from datetime import datetime
        print(datetime.now().strftime('%H'), h, datetime.now().strftime('%H') == h)
        if datetime.now().strftime('%H') == h:
            for T in [Preply, Italki]:
                for lang in langarray:
                    tutoring = T(lang)

                    """"""
                    tutoring.collect()
                    
                    from git_push import git_push
                    git_push([tutoring.fileindex.get_jsonpath()])
                    
            """
            """
            for T in [Preply, Italki]:
                for lang in langarray:
                    tutoring = T(lang)
                    tutoring.remove_log()
                    
            """break"""
                    
if __name__ == '__main__':
    collect(['english', 'japanese', 'spanish'], '00')
    