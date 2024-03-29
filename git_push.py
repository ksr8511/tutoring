def git_push(parray):
    try:
        from git import Repo

        from os.path import join
        from pathlib import Path
        """PATH_OF_GIT_REPO = join('.', '.git')"""
        PATH_OF_GIT_REPO = join(Path.home(), 'jupyter', 'tutoring', '.git')
        COMMIT_MESSAGE = 'tutoring'
        
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(parray)
        repo.index.commit(COMMIT_MESSAGE)
        origin = repo.remote(name='origin')
        origin.push()
    except Exception as e:
        print(e)
        