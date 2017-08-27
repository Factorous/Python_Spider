from queue import Queue
from filter import Filter
from Project import *
from Spider import *
import threading
import time
from Colors import *
import os

#Special Queue class
class CheckableQueue(Queue):
    def __contains__(self, item):
        with self.mutex:
            return item in self.queue


#Handles all the requests/QUEUE/CRAWLED
def Spider():
    global QUEUE , CRAWLED , DONE
    while QUEUE.empty() == False and DONE == False:
        to_visit = QUEUE.get()
        url_data = get_data(to_visit)
        if url_data != False:
            links = detect_links(url_data)

        if url_data == False:
            CRAWLED.append(to_visit)
            QUEUE.task_done()
            continue



        if len(links) == 0: #If we found no links
            QUEUE.task_done()
            CRAWLED.append(to_visit)
            continue
        else:
            links = fix_links(links,get_domain_name(to_visit))  #Fixes the links
            print("Crawled:"+to_visit)

            CRAWLED.append(to_visit)
            TO_FILTER.append(to_visit)
            QUEUE.task_done()
            for link in links:
                if link not in CRAWLED and link not in QUEUE:
                    QUEUE.put(link)







def handle_memory():
    global CRAWLED , QUEUE
    time.sleep(60)
    if len(CRAWLED) > 5000 or QUEUE.qsize() > 10000:
        warning("Queue lenght:{}".format(str(QUEUE.qsize())))
        warning("Crawled lenght:{}".format(str(len(CRAWLED))))
        warning("lists take up too much space! \nSaving them...")
        Good_news("Saving lists...")
        '''
        This part of the script handles the saving of the two lists so the user can resume the spider after
        '''
        write_data_to_file(PROJECT_NAME + "/Crawled.txt", '')
        for url in CRAWLED:
            append_data_to_file(PROJECT_NAME + "/Crawled.txt", url)

        write_data_to_file(PROJECT_NAME + "/Queue.txt", "")
        while QUEUE.empty() == False:
            append_data_to_file(PROJECT_NAME + "/Queue.txt", QUEUE.get_nowait())
        Good_news("Lists saved!")




#Function that handles the filter
def handle_filter():
    global DONE , CRAWLED , QUEUE
    while True:
        try:
            if QUEUE.empty():
                warning("QUEUE IS EMPTY\n")
                warning("PROGRAM WILL STOP\n")
                DONE = True
                exit(0)

                Filter(PROJECT_NAME+"/output.txt",TO_FILTER)
                TO_FILTER[:] = []  #Cleans up the list



        except KeyboardInterrupt:  #if the user exists , [Control+c]

            warning("Saving lists...\nDo not exit the script!")
            DONE = True # To stop the threads
            '''
            This part of the script handles the saving of the two lists so the user can resume the spider after
            '''
            write_data_to_file(PROJECT_NAME + "/Crawled.txt", '')
            for url in CRAWLED:
                append_data_to_file(PROJECT_NAME + "/Crawled.txt", url)

            write_data_to_file(PROJECT_NAME+"/Queue.txt","")
            while QUEUE.empty() == False:
                append_data_to_file(PROJECT_NAME+"/Queue.txt",QUEUE.get_nowait())

            interface()

        except Exception as e:
            warning("An error has occured:{}".format(str(e)))


#Creates the spiders for the script
def create_workers():
    global DONE
    try:
        for _ in range(THREADS):

            info("Created thread:"+str(_))
            #time.sleep(1) #Sleeps two seconds so the Spider can start properly
            worker = threading.Thread(target=Spider)  #Creates a thread
            worker.setDaemon(True)
            '''
            So when the script exists the threads close too. if daemon is False , the threads will continue to work after the main thhread is done
            '''
            worker.start()  #Starts the thread

        #Sets up the memory handler and starts it
        mem_handler = threading.Thread(target=handle_memory)
        mem_handler.setDaemon(True)
        mem_handler.start()
    except KeyboardInterrupt:
        warning("Exiting the script!")
        DONE = True


#Create the prject files
def create_project():
    create_project_folder(PROJECT_NAME)
    create_filter_file(PROJECT_NAME)
    save_into_project_file(PROJECT_NAME, PROJECT_FILES)


def resume():
    try:
        crawled = open(PROJECT_NAME+"/Crawled.txt","r")
    except:
        warning("Could not open {}".format(PROJECT_NAME+"/Crawled.txt"))
        interface()
    crawl = crawled.read().split()
    crawled.close()
    Good_news("Added {} to Crawled.".format(str(len(crawl))))
    for c in crawl:
        CRAWLED.append(c)
    try:
        queue = open(PROJECT_NAME+"/Queue.txt","r")
    except:
        warning("Could not open {}".format(PROJECT_NAME + "/Queue.txt"))
        interface()
    qu = queue.read().split()
    queue.close()
    for q in qu:
        QUEUE.put_nowait(q)



#The main function of the program
def main():
    create_workers()  #Creates the spiders
    handle_filter()  #Mainloop



def interface():
    global PROJECT_NAME , QUEUE , CRAWLED ,TO_FILTER , BASE_URL , BASE_URLS , DONE , THREADS
    print("\n\n\r"+Color.bg.red + "\t\t\t\tMENU\t\t\t\t\n" + Color.reset)
    DONE = False
    while True:

        print("\n\n\n------------------------------------\n\n\nYour choices:\n   1)Create a new Project\n   2)Resume an existing Project\n   3)Delete a Project\n   4)Quit the script")
        choices = input("-->")
        if choices == "1":
            PROJECT_NAME = input("Project name:")
            multiple = input("Do you want to load the base urls from a file?:")
            if multiple in "Y YES Yes y".split():
                while True:
                    FILE = input("Filename:")
                    if FILE in "QUIT quit exit EXIT q Q".split():
                        exit(0)
                    try:
                        DATA = open(FILE, "r").read().split()
                        for d in DATA:
                            BASE_URLS.append(d)
                        print("Added {} websites!".format(str(len(DATA))))
                        break
                    except:
                        print("Could not open file!")
                for url in BASE_URLS:
                    QUEUE.put(url)
            else:
                BASE_URL = input("What url do you want to start with:")
                QUEUE.put(BASE_URL)

            while True:
                th = input("How many threads(spiders) do you want to use:")
                try:
                    if int(th) >0:
                        break
                    else:
                        warning("You have to enter a number higher than zero!")

                except:
                    warning("You have to enter a number!")

            THREADS = int(th)
            create_project()

            main()



        elif choices == "2":
            projects = open(PROJECT_FILES, "r").read().split()
            if len(projects) == 0:
                warning("You have no projects!")
            else:
                while True:
                    print("Projects:\n")
                    for pr in projects:
                        print("   {}){}".format(str(projects.index(pr)), pr))
                    resum = input("Which project do you want to resume:")
                    if resum in "Q q Quit quit exit EXIT Exit".split():
                        break
                    try:
                        int(resum)
                    except:
                        print("You have to enter a number! ex:1")
                        continue
                    PROJECT_NAME = projects[int(resum)]
                    resume()
                    while True:
                        th = input("How many threads(spiders) do you want to use:")
                        try:
                            if int(th) >0:
                                break
                            else:
                                warning("You have to enter a number higher than zero!")
                        except:
                            print("You have to enter a number!")
                    THREADS = int(th)
                    main()



        elif choices == "3":

            print(info("You decided to delete a Project."))
            projects = open(PROJECT_FILES,"r").read().split()


            if len(projects) == 0:
                warning("You have no projects!")

            else:
                while True:
                    print("Projects:\n")
                    for pr in projects:
                        print("   {}){}".format(str(projects.index(pr)),pr))
                    delete = input("What project do you want to delete:")
                    if delete in "Q q Quit quit exit EXIT Exit".split():
                        break
                    try:
                        if len(projects) <int(delete):
                            print("The number you choose is out of range!")
                            break
                        else:
                            shutil.rmtree(projects[int(delete)])
                            f  = open(PROJECT_FILES,"r").read().split()
                            for pro in f:
                                if projects[int(delete)] ==pro:
                                    f.remove(pro)
                            n = open(PROJECT_FILES,"w")
                            for p in f:
                                n.write(p)
                            n.close()
                            Good_news("Removed!")
                            break

                    except:
                        print("You have to enter an integer!!!")



        elif choices == "4":
            info("Exiting the script...")
            exit(0)

        else:
            warning("You have to enter a number! ex:1")



#This line makes sure that the program is executed direcly
if __name__ == '__main__':
    '''
    Creating the Global CONSTANTS
    '''

    QUEUE = CheckableQueue()  # Creates the QUEUE and puts in the base url
    PROJECT_NAME = ''#input("Project name:")  #Creates the project
    THREADS = 0#int(input("How many threads(spiders) do you want to use:"))  #Number of threads the program willl use
    BASE_URLS = [] #Used to store the urls in a list
    BASE_URL = '' #The url te script will strat with
    DONE = False
    CRAWLED = list()
    TO_FILTER = CRAWLED
    PROJECT_FILES  = "__PROJECTS__"
    save_into_project_file("",PROJECT_FILES)
    interface()



else:
    import sys
    warning("You have to run the program direcly!\nSyntax: python(3) {}".format(sys.argv[0]))










