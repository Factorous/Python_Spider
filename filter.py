
from Project import append_data_to_file , insert
import urllib.parse
from Colors import *


#Gets and url and if the url meets the conditions the function  will return True , else it will return False
def parameter_filter(url):
    if url[:7] =='http://'==  True or url[:8] == 'https://':
        if "/?" in url or "&" in url:
            return True
        else:
            return False




#Goes trough the list of urls and saves the urls that meet the conditions in parameter_filter function
def Filter(file,data):  #File has to be syntaxed: Project_name+file
    for url in data:
        if parameter_filter(url):
            Good_news("New url:{}".format(url))


            #Puts the least secure urls on top of the file
            if url[:7] == 'http://':
                if "%" in url:
                    insert(file, urllib.parse.unquote(url))  # Decodes the special chars
                else:
                    insert(file, url)

            else:

                if "%" in url:
                    append_data_to_file(file,urllib.parse.unquote(url))  #Decodes the special chars
                else:
                    append_data_to_file(file,url)








