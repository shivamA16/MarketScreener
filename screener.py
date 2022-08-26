from time import sleep
from tkinter.ttk import Separator
import pync
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import webbrowser
from tkinter import *
from threading import Thread, Lock
import json

global pressed
pressed = False

keepgoing = True

global counter
counter = 0

global stopcounter
stopcounter = 0

def main():  
    while keepgoing:

        lock.acquire()

        loops = 1    

        now = datetime.now() 
        current_time = now.strftime("%H:%M:%S")
        
        time_list = [00, 15, 30, 45]
        
        if int(current_time[3:5]) in time_list:
            loops = 4
        

        links = []
        news = []   
        headlines = []




        for i in range(loops):    

            url_globenewswire = 'https://www.globenewswire.com/search?page=' + str(i + 1)
            url_businesswire = 'https://www.businesswire.com/portal/site/home/template.PAGE/news/?javax.portlet.tpst=ccf123a93466ea4c882a06a9149550fd&javax.portlet.prp_ccf123a93466ea4c882a06a9149550fd_viewID=MY_PORTAL_VIEW&javax.portlet.prp_ccf123a93466ea4c882a06a9149550fd_ndmHsc=v2*A1626606000000*B1629218643383*DgroupByDate*G' + str(i + 1) + '*N1000003&javax.portlet.begCacheTok=com.vignette.cachetoken&javax.portlet.endCacheTok=com.vignette.cachetoken'
            url_accesswire = 'https://www.accesswire.com/newsroom'

            request_globenewswire = requests.get(url_globenewswire)
            request_businesswire = requests.get(url_businesswire)
            request_accesswire = requests.get(url_accesswire)

            soup_globenewswire = BeautifulSoup(request_globenewswire.text, "lxml")
            soup_businesswire = BeautifulSoup(request_businesswire.text, "lxml")
            soup_accesswire = BeautifulSoup(request_accesswire.text, "lxml")

            list_of_a_globenewswire = soup_globenewswire.findAll('a', {'data-autid': 'article-url'})
            list_of_a_businesswire = soup_businesswire.findAll('a', {'class': 'bwTitleLink'})
            
            # list_of_a_accesswire = soup_accesswire.findAll('a', {'data-uw-styling-context': 'true'})
            # print(list_of_a_accesswire)
            
            total_list_of_a = list_of_a_businesswire +  list_of_a_globenewswire 
            # + list_of_a_accesswire
            
                
            for a in list_of_a_globenewswire:
                link = stem_globenewswire + a.get('href')
                links.append(link)
                headlines.append(a.text.lower())
                
            # for a in list_of_a_accesswire:
            #     link = a.get('href')
            #     links.append(link)
            #     print(link)
            #     headlines.append(a.text.lower())
  
                
            for a in list_of_a_businesswire:
                link = stem_businesswire + a.get('href')
                links.append(link)
                headlines.append(a.text.lower())

                
            
            print('scanning...')
        
        
        
        for i, headline in enumerate(headlines):
            if headline not in headlines_shown:

                for word in keywords:
                    if word in headline:
                                
                        show = word + ' - ' + headline

                        pync.notify(show, open=links[i])

                        headlines_shown.append(headline)
                        links_shown.append(links[i])
                        
                
        print('Done')
        print(keywords)
        lock.release()
        sleep(2)
    


def startButton():
    global counter
    if counter==0:
        t1.start()
    else:
        lock.release()

    counter = 1


# def quit():
#     # global pressed
#     # pressed = True
#     lock.acquire()


def stopButton():
    lock.acquire()
    print("Program stopped")


def getinput():
    global keywords
    input = klist.get("1.0", END)
    keywords = input.split(" ")
    keywords[-1] =  keywords[-1][:-1]
    keywords = [x for x in keywords if x]
    print("Keywords Saved")
    print(keywords)


    jsonString = json.dumps(keywords)
    jsonFile = open("data.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()


def loadButton():
    global keywords
    readFile = open("data.json", "r")
    keywords = json.loads(readFile.read())
    print("Keywords Loaded")
    print(keywords)

    klist.delete("1.0","end")
    text = (' ').join(str(word) for word in keywords)
    klist.insert(INSERT, text)



t1 = Thread(target=main)
# t2 = Thread(target=quit)
lock = Lock()


stem_globenewswire = 'https://www.globenewswire.com'
stem_businesswire = 'https://www.businesswire.com'
# stem_accesswire = 'https://www.accesswire.com/'

headlines_shown = []
links_shown = []

global keywords
keywords = ['phase', 'fda', 'treatment', 'patent', 'purchase order', 'topline']

window = Tk()
window.title("News Screener")
window.geometry("600x380")


day = Label(window, text="Stock", font=("Arial", 45))
trading = Label(window, text="Trading", font=("Arial", 45))
news = Label(window, text="News", font=("Arial", 45))
scanner = Label(window, text="Screener", font=("Arial", 45))


day.place(x = 50, y=57)
trading.place(x = 50, y=122)
news.place(x = 50, y=187)
scanner.place(x = 50, y=252)


vertical =Frame(window, bg='#242424', height=280,width=1)
vertical.place(x=300, y=50)

start = Button(window, text="Run Screener", command=startButton, font=('Arial', 13))
start.place(x=330, y=60)

stop = Button(window, text="Stop Screener", command=stopButton, font=('Arial', 13))
stop.place(x=450, y=60)


key_label = Label(window, text="𝘬𝘦𝘺𝘸𝘰𝘳𝘥𝘴:", font=("Arial", 18))

txt = (' ').join(str(word) for word in keywords)

klist = Text(window, font=('Arial', 15), height=5, width=26, fg="purple")
klist.insert(INSERT, txt)
klist.place(x=330, y= 150)

select = Button(window, text="Save keywords", command=getinput, font=('Arial', 13))
select.place(x=330, y=280)

load = Button(window, text="Load keywords", command=loadButton, font=('Arial', 13))
load.place(x=453, y=280)

key_label.place(x=350, y=120)

window.mainloop() 
