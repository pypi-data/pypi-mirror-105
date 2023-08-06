from folders import save_image
import numpy as np

from PIL import Image

import skimage.filters as sk_filters
import skimage.exposure as sk_exposure

def grayscale_filter(np_image, view = False, save = False):
    '''
    Returns a greyscale image from numpy array
    
    Takes RGB numpy image array as argument
    '''
    if not isinstance(np_image, np.ndarray):
        raise ValueError("grayscale_filter(*np_image*) -> Must be a type of numpy array.\n Use image_to_numpy() first   ")

    grayscale = np.dot(np_image[..., :3], [0.2125, 0.7154, 0.0721])
    grayscale_image = Image.fromarray(grayscale)
    if view == True:
        
        grayscale_image.show()
        
    if save == True:
        name= input("*** P L E A S E  E N T E R  A  G R A Y S C A L E  N A M E ****\n")
        newgray = grayscale_image.convert("L")
        save_image(newgray, name)
    return grayscale

def complement_filter (grayscale_image, view = False, save = False):
    '''
    Returns a complement(inverted) greyscale image from numpy array. 
    
    NOTE: Useful for removing the excess white value from the background
    
    Takes GRAYSCALE numpy image array as argument.
    '''
    if not isinstance(grayscale_image, np.ndarray):
        raise ValueError("complement_filter(*grayscale_image*) -> Must be a type of numpy array.\n Use image_to_numpy() first")

    complement = 255-grayscale_image
    
    complement_image = Image.fromarray(complement)
    if view == True:
        
        complement_image.show()
    if save == True:
        name= input("*** P L E A S E  E N T E R   A  C O M P L E M E N T  N A M E ****\n")
        newcomplement = complement_image.convert("L")
        save_image(newcomplement, name)
    
    return complement

def hysterisis_filter(complement_image, view = False, save = False, low_threshold = 50 ,high_threshold=100):
    '''
    Returns a Binary image from a numpy image array based on two level thresholding. 
    
    Takes Complement numpy image array as argument.
    '''
    if not isinstance(complement_image, np.ndarray):
        raise ValueError("hysterisis_filter(*complement_image*) -> Must be a type of numpy array.\n use image_to_numpy() first   ")

    hyst = sk_filters.apply_hysteresis_threshold(complement_image, low_threshold, high_threshold)
    hyst = (255 * hyst).astype("uint8")

    hysterisis_image = Image.fromarray(hyst)

    if view == True:
        
        hysterisis_image.show()
    
    if save == True:
        name= input("*** P L E A S E  E N T E R   A  H Y S T E R I S I S  N A M E ****\n")
        #newcomplement = complement_image.convert("L")
        save_image(hysterisis_image, name)
        
    return hyst

def otsu_filter(complement_image, view = False, save = False):
    '''
    Returns a Binary Otsu threshold image from a numpy image array

        Generates a threshold level based on Complement image returns only the values greater than the threshold

    Takes Complement numpy image array as argument
    '''
    if not isinstance(complement_image, np.ndarray):
        raise ValueError("otsu_filter(*complement_image*) -> Must be a type of numpy array.\n use image_to_numpy() first   ")
    
    otsu_threshold_value = sk_filters.threshold_otsu(complement_image)
    otsu = (complement_image > otsu_threshold_value)
    
    otsu_image = Image.fromarray(otsu)

    if view==True:
        
        otsu_image.show()
    if save == True:
        name= input("*** P L E A S E  E N T E R   A N  O T S U   N A M E ****\n")
        
        save_image(otsu_image, name)
    return otsu

def contrast_stretch(complement_image, view = False, save = False, low=100,high=200):
    '''
    Returns numpy array of image with colour contrast incresed using a minimum and maximum thresehold. 
    Default low = 100, High = 200


    Takes np array of RBG or Grayscale image
    '''
    if not isinstance(complement_image, np.ndarray):
        raise ValueError("contrast_stretch(*complement_image*) -> Must be a type of numpy array.\n use image_to_numpy() first   ")

    low_contrast, high_contrast = np.percentile(complement_image, (low * 100 / 255, high * 100 / 255))
    contrast_stretch = sk_exposure.rescale_intensity(complement_image, in_range=(low_contrast, high_contrast))
    
    contrast_stretch = (contrast_stretch * 255).astype("uint8")
    contrast_image = Image.fromarray(contrast_stretch)
    
    if view == True:
        
        contrast_image.show()

    if save == True:
        name= input("*** P L E A S E  E N T E R  A  C O N T R A S T   N A M E ****\n")
        
        save_image(contrast_image, name)

    return contrast_stretch

def mask_filter (np_image,np_mask, view = False, save = False):
    
    '''
    Returns masked image 

    '''
    if not isinstance(np_image, np.ndarray):
        raise ValueError("mask_filter(*np_image* , np_image) -> Must be a type of numpy array.\n Use image_to_numpy() first   ")

    if not isinstance(np_mask, np.ndarray):
        raise ValueError("mask_filter(np_image , *np_mask*) -> Must be a type of numpy array.\n Use image_to_numpy() first   ")
    
    result = np_image * np.dstack([np_mask, np_mask, np_mask])
    mask_image = Image.fromarray(result)
    if view==True:
        mask_image.show()
    if save == True:
        name= input("*** P L E A S E  E N T E R  A  M A S K   N A M E ****\n")
        
        save_image(mask_image, name)
    return result
