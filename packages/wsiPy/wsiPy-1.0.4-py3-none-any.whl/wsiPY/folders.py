import os
from PIL import Image

def is_folder(name):
    ''' Creates a folder to save images
        Can be defaulted or overwritten by user
    '''
    
    path=os.getcwd()+'/'+name

    if not os.path.exists(path):
        print("\n------ F O L D E R   C R E A T E D -------------\n")
        os.mkdir(path)
        print("----> "+path)
        print("\n----------------------------------------------\n")
    #else:
     #   os.mkdir(path)
      #  print ("------ F O L D E R   C R E A T E D -----------\n")
       # print("----> "+path)
        #print("\n/ \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ /\n")

def save_image(image,name,folder="saved_images"):
    '''
    Saves images in PNG format 

    Name is the name you wish to save your image as
    Folder is the folder that you wish to save it in. Defaults folder name to '/saved_images/' if not specified
    '''
    
    
    is_folder(folder)
    path_name = folder+'/'+name
    image.save(path_name+".png")

def get_file_name(filepath):
    '''
    Returns the filename of the .SVS image
    -> /images/My_SVS.svs
    -> My_SVS

    '''
    filename = os.path.basename(filepath)
    

    name = os.path.splitext(filename)[0]
    
    return name