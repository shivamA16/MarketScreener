from win10toast_click import ToastNotifier
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import webbrowser
from tkinter import *


stem_globenewswire = 'https://www.globenewswire.com'
stem_businesswire = 'https://www.businesswire.com'
stem_accesswire = 'https://www.accesswire.com/'


notif = ToastNotifier()

headlines_shown = []
links_shown = []

keywords = ['phase', 'fda', 'treatment', 'patent', 'purchase order', 'topline']


    

while True:

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
        list_of_a_accesswire = soup_accesswire.findAll('a', {'class': 'articlelink'})
        
        total_list_of_a = list_of_a_businesswire +  list_of_a_globenewswire + list_of_a_accesswire
        
            
        for a in list_of_a_globenewswire:
            link = stem_globenewswire + a.get('href')
            links.append(link)
            headlines.append(a.text.lower())
            
        for a in list_of_a_accesswire:
            link = stem_accesswire + a.get('href')
            links.append(link)
            headlines.append(a.text.lower())
            
        for a in list_of_a_businesswire:
            link = stem_businesswire + a.get('href')
            links.append(link)
            headlines.append(a.text.lower())
            
        
        print('scanning...')
    
    
    
    for i, headline in enumerate(headlines):
        if headline not in headlines_shown:
            for word in keywords:
                if word in headline:
                    
                    def action():
                        webbrowser.open(links[i])
                            
                    show = word + ' - ' + headline
                    notif.show_toast(show, "Click to read article", callback_on_click=action)
                    headlines_shown.append(headline)
                    links_shown.append(links[i])
            
    print('Done')
    
    window = Tk()
    window.title("News Screener")
    window.geometry("600x400+10+20")
    window.mainloop()
