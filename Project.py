import os , shutil


def write_data_to_file(file,data):
    with open(file,"w") as f:
        f.write(data)



def append_data_to_file(file,data):
    with open(file,"a") as f:
        f.write(data+"\n")


def save_into_project_file(project_name,project_file):
    try:
        open(project_file,"x")
        with open(project_file,"w") as f:
            f.write(project_name+"\n")
    except:
        with open(project_file,'a') as f:
            f.write(project_name+"\n")


def create_project_folder(project_name):
    if os.path.exists(project_name)==False:
        os.makedirs(project_name)

    else:
        print("Project already exists!")
        delete = input("Do you want to delete it:(y,n)")
        if  delete in "y Yes YES Y".split():
            shutil.rmtree(project_name)
            os.makedirs(project_name)



def create_filter_file(project_name):
    print("Creating file.")
    try:
        open(project_name+"/output.txt","x")
    except:
        ("File {} already exists!".format(project_name+'/output.txt'))


#Function that allws the program to write a string on top of the file
#Very inefficient , because of the speed
def insert(originalfile,string):
    with open(originalfile,'r') as f:
        with open('newfile.txt','w') as f2:
            f2.write(string+"\n")
            f2.write(f.read())
    os.rename('newfile.txt',originalfile)





