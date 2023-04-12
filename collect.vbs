Set objShell = CreateObject("Shell.Application")
objShell.ShellExecute ".\collect.bat", "/c lodctr.exe /r" , "", "runas", 0
