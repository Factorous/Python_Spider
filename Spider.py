try:
    from bs4 import BeautifulSoup
    import requests
except ImportError:
    print("Warning : Missing modules! \nPlease install [bs4] and [requests] modules to run this script!\nYou can install them with pip: pip install bs4/pip install requests")
    exit(0)


import urllib.parse
import UA_Forger
from Colors import warning , info


def fix_links(links,domain_name):

    for link in links:
        try:
            if link[0] == "#" or link[0] == ".":
                links.remove(link)




            if link[0] == "/":

                try:
                    if link[1]=="/"==False:
                        links.remove(link)
                        info("[Replacing:" + domain_name + link + "]")
                        links.append(domain_name+link)
                except:
                    links.remove(link)
        except:
            links.remove(link)

    return links



def detect_links(url_data):

    founded = []
    soup = BeautifulSoup(url_data,"html.parser")
    Content = soup.findAll("a")
    #print(len(Content))
    for content in Content:
        #if "href=" in content:
        try:
            if len(content) > 0:
                founded.append(content["href"])
        except:
            pass
    return founded


def get_data(url):
    headers = requests.utils.default_headers()
    try:
        headers.update({'User-Agent':UA_Forger.get_random_ua()})
        resp = requests.get(url).content
        return resp
    except Exception as e:
        warning("Error:"+str(e))
        return False



def get_domain_name(url):
    fragment = urllib.parse.urlparse(url)
    return fragment.scheme+"://"+fragment.netloc

def get_scheme(url):
    return urllib.parse.urlparse(url).scheme








