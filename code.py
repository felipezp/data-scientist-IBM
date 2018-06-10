
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import requests
from requests.exceptions import ConnectionError

# classes
class Quality_Check:
    def check_broken_link(self,data):
        try:
            url = requests.head(data)
            if url.status_code == 200 or url.status_code == 302 or url.status_code == 301:
                return True
        except requests.exceptions.SSLError as e:
            return False
class Connection_Check:
    def check_broken_conn(self,data):
        try:
            url = requests.get(data)
            if url.status_code == 200 or url.status_code == 302 or url.status_code == 301:
                return True
        except ConnectionError as e:    # This is the correct syntax
            return False

url = input("Enter a website to extract the URL's from: ")

# links treatment 
if url[0:5] == 'http:':
    url = 'https'+url[4:]
elif url[0:5] == 'https':
    url = url
elif url[0:3] == 'www':
    url = 'https://'+ url
else:
    url = 'https://'+ url
if url[-1] == '/':
    url = url
else:
    url = url + '/'
# check broken and not safe links
cc = Connection_Check()
if cc.check_broken_conn(url) == False:
    print('The website you entered is broken or not safe.')
else:
    qc = Quality_Check()
    if qc.check_broken_link(url) == False:
        print('The website you entered is not safe.')
    else:
    
        # put first website on list
        url_list2 = [url]
        j=0
        while j < len(url_list2):
            # test if the link to the website is working
            cc = Connection_Check()
            if cc.check_broken_conn(url_list2[j]):
                #Test if the website is secure:
                qc = Quality_Check()
                if qc.check_broken_link(url_list2[j]):
                    r  = requests.get(url_list2[j], verify=True)
                    
                    data = r.text
                    soup = BeautifulSoup(data,'html5lib')
                    # get root from url
                    url2 = urljoin(url,'/')

                    url_list = []
                    for link in soup.find_all('a'):
                        if link.has_attr('href'):
                            x=link.get('href')
                            # links treatment
                            if len(x)>0:
                                if x[0]!='#':
                                    if (x[0]=='/'):
                                        if len(x)>1:
                                            if (x[1]=='/'):
                                                url_list.append('https:'+x)
                                            else:
                                                url_list.append(url2+x)
                                    elif x[0]=='h':
                                        url_list.append(x)
                    for i in url_list:
                        if i not in url_list2:
                            # put every new link on the list
                            url_list2.append(i)
            # increment counter to cover all the list
            j+=1

