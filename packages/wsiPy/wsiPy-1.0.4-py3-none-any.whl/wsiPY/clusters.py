import numpy as np
import skimage.segmentation as sk_segmentation
import skimage.color as sk_color
import skimage.future as sk_future
from PIL import Image
from folders import save_image
#TODO: Progress bar 

def kmeans_segmentation(np_image,view=False, save=False, compactness = 10, n_segments=800 ):
    '''
    Takes numpy image as argument 

    Returns a numpy array
    -- WARNING -- Processor intensive, depending on your machine this could take between 20 seconds and several minutes.

    '''
    if not isinstance(np_image, np.ndarray):
        raise ValueError("kmeans_segmentation(*np_image*) -> Must be a type of numpy array.\n Use image_to_numpy() first   ")

    print("------- K M E A N S  S E G M E N T A T I O N ----- ")
    # com=10 /n=segment= 30
    
    labels = sk_segmentation.slic(np_image, n_segments, compactness)
    
    kmeans = sk_color.label2rgb(labels, np_image, kind='avg')
    
    print()
    print("--------------------------------------------------")
    
    kmeans_image = Image.fromarray((kmeans).astype(np.uint8))
    if view == True:
        
        kmeans_image.show()
    if save == True:
        name= input("*** P L E A S E  E N T E R  A  K-M E A N S   N A M E ****\n")
        
        save_image(kmeans_image, name)
    
    return kmeans

def RAG_segmentation(np_image, view = False, save = False, compactness = 10, n_segments= 800, thresehold= 9):
    '''
   - PROCESSOR INTENSIVE -
    Time to produce a RAG image may vary on your CPU/GPU 

    '''

    if not isinstance(np_image, np.ndarray):
        raise ValueError("RAG_segmentation(*np_image*) -> Must be a type of numpy array.\n Use image_to_numpy() first   ")
    print("------- R A G   S E G M E N T A T I O N ---------- ")
    labels = sk_segmentation.slic(np_image, n_segments, compactness)
    graph = sk_future.graph.rag_mean_color(np_image, labels)
    labels2 = sk_future.graph.cut_threshold(labels, graph, thresehold)
    rag_thresh = sk_color.label2rgb(labels2, np_image, kind='avg')
    
    
    print()
    print("--------------------------------------------------")
    rag_image = Image.fromarray((rag_thresh).astype(np.uint8))
    if view == True:
        
        rag_image.show()
    if save == True:
        name= input("*** P L E A S E  E N T E R  A   R. A. G.  N A M E ****\n")
        
        save_image(rag_image, name)
    return rag_thresh

def kmeans_to_image(np_image):
    '''
    Returns an image from a numpy array after Kmeans modelling

    Takes numpy array as argument
    '''
    image = Image.fromarray((np_image).astype(np.uint8))
    image.show()
    return image