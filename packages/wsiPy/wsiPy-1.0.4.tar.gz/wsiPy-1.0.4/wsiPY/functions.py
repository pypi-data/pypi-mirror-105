import openslide
from openslide import open_slide

from PIL import Image, ImageDraw

import errno
import glob

import math

import skimage.color as sk_color
import numpy as np

from Classes import *
from filters import *
from folders import *
from clusters import *

#TODO: toolkit release, Define and comment


def import_svs(location):
    '''
    Returns OpenSlide object for manipulation.

    Takes string argument for file location e.g. '/Folder/File.svs'
    '''
    if type(location) != str: 
        raise ValueError("\nimport_svs(*location*) -> Location must be a String argmunent  eg '/myfolder/myslide.svs'  ")
    
    check = location.split(".")
    if (check[1]!= "svs"):
        raise ValueError("\nimport_svs(*location*) -> Location must be an svs file  eg '/myfolder/myslide.svs'  ")

    #get_file_name(location)
    
    return openslide.open_slide(location)


def slide_dimensions(slide, details = False):
    '''
    Returns width and height of the Whole Slide Image

    Takes Openslide object (import_slide) as argument. 

    Option details argument. If True will print the slide width and height to screen
    '''
    if type(slide) != openslide.OpenSlide:
        raise ValueError("slide_dimensions(*slide*) -> slide must be an openslide object.  Use import_slide() first")

    slide_width, slide_height = slide.dimensions
    
    if details == True:
        print("\n------ S L I D E  D I M E N S I O N  S U M M A R Y ----\n")
        print(f"Slide is {slide_width:,}px wide by {slide_height:,}px high")
        print("\n--------------------------------------------------------\n")
    return slide_width, slide_height


def scaled_dimensions(width, height, details = False, scale_factor=32):
    '''
    Returns new width and new height of the image at user scale factor (e.g. 32x).

    Recommend scale is 32 but feel free to experiment

    Takes Slide width and Slide height and scale_factor as arguments.
    '''
    
    if (type(width)!= int or type(height) != int):
        raise ValueError("scaled_dimensions(*width* , *height*) -> Width and Height must be integers")
    
    scale_width = math.floor(width/scale_factor)
    scale_height = math.floor(height/scale_factor)

    if details == True:
        print("\n------ S C A L E D  D I M E N S I O N  S U M M A R Y ----\n")
        print(f"Scaled by factor of {scale_factor} from  {width:,}px x {height:,}px to {scale_width:,}px  x {scale_height:,}px")
        print("\n--------------------------------------------------------\n")
    return scale_width , scale_height


def import_slide(slide, scaled_width, scaled_height, level=2, view=False, save = False):
    '''
    Returns image of Slide. 

    Takes slide object, scaled width and scaled height as arguments 

    To view slide set View = True
    '''
    if type(slide) != openslide.OpenSlide:
        raise ValueError("import_slide(*slide* , scaled_width, scaled_height) -> slide must be an openslide object.  Use import_slide() first")

    if (type(scaled_width)!= int or type(scaled_height) != int):
        raise ValueError("import_slide(slide, *scaled_width* , *scaled_height*) -> Scaled Width and Scaled Height must be integers")

    image = slide.read_region((0, 0), level, slide.level_dimensions[level])
    image = image.convert("RGB")
    img = image.resize((scaled_width, scaled_height), Image.BILINEAR)
    
    if view == True:
        img.show()
    if save == True:
        name = get_file_name(slide._filename)
        save_image(img, name)
        
    #save image

    
    return img


def image_to_numpy(image):
    '''
    Returns numpy array of an image

    Takes image as an argument  
    '''
    

    np_image = np.asarray(image)
    return np_image

'''
This if / else is causing distortion
'''

def numpy_to_image(np_image):
    '''
    Returns an image from a numpy array

    Takes numpy array as argument
    '''
    
    if np_image.dtype == 'bool':
        np_image =np_image.astype("uint8") * 255
    
    elif np_image.dtype == "float64":
        np_image = (np_image * 255).astype("uint8")
    image = Image.fromarray(np_image)
    #image.show()
    return image


def extract_tiles(slide,np_img,num_top_tiles):
    '''
    Returns a number of tiles specified by user 
    Can be saved to a folder of users choice
    
    Takes slide, otsu filtered slide, number of tiles
    '''
    print("--------------- E X T R A C T I N G  T I L E S -------------------")
    filename = get_file_name(slide._filename)
    
    is_folder("Extracted Tiles")
    is_folder("Extracted Tiles/"+filename)
    
    tile_sum = score_tiles(slide, np_img)
    
    #generate tiled slide
    all_tiles_slide(tile_sum, np_img)
    #generate top  tiles 
    top_tile_slide(tile_sum, np_img,num_top_tiles, filename, slide._filename)
    print("--------------- E X T R A C T I O N  C O M P L E T E  ------------")
    return tile_sum


def score_tiles(slide,np_image):
    ''' Returns a Slide class object

    '''

    original_width, original_height = slide_dimensions(slide)
    scaled_width = original_width // 32
    scaled_height = original_height // 32

    row_tile_size = round(1024 / 32)  
    col_tile_size = round(1024 / 32)  

    num_row_tiles, num_col_tiles = total_tiles(scaled_height, scaled_width, row_tile_size, col_tile_size)

    slide_sum = Slide(

        orig_w = original_width,
        orig_h = original_height,
        orig_tile_w = 1024,
        orig_tile_h = 1024,
        scaled_w = scaled_width,
        scaled_h = scaled_height,
        scaled_tile_w = col_tile_size,
        scaled_tile_h = row_tile_size,
        tissue_percentage = tissue_percentage(np_image),
        num_col_tiles = num_col_tiles,
        num_row_tiles = num_row_tiles  
    )

    count = 0
    high = 0
    medium = 0
    low = 0
    none = 0

    tile_indices = get_tile_indices(scaled_height, scaled_width, row_tile_size, col_tile_size)

    for t in tile_indices:
        count += 1  
        r_s, r_e, c_s, c_e, r, c = t
        np_tile = np_image[int(r_s):int(r_e), int(c_s):int(c_e)]
        t_p = tissue_percentage_masked(np_tile)
        amount = tissue_quantity(t_p)

        if amount == TissueQuantity.HIGH:
            high += 1
        elif amount == TissueQuantity.MEDIUM:
            medium += 1
        elif amount == TissueQuantity.LOW:
            low += 1
        elif amount == TissueQuantity.NONE:
            none += 1
        o_c_s, o_r_s = small_to_large_mapping((c_s, r_s), (original_width, original_height))
        o_c_e, o_r_e = small_to_large_mapping((c_e, r_e), (original_width, original_height))

        # pixel adjustment in case tile dimension too large (for example, 1025 instead of 1024)
        if (o_c_e - o_c_s) > 1024:
            o_c_e -= 1
        if (o_r_e - o_r_s) > 1024:
            o_r_e -= 1

        score, colour_factor, s_and_v_factor, quantity_factor = score_tile(np_tile, t_p)

        

        tile = Tile(
            
                slide_sum, 
                count, 
                r, 
                c, 
                r_s, 
                r_e, 
                c_s, 
                c_e, 
                o_r_s, 
                o_r_e, 
                o_c_s, 
                o_c_e, 
                t_p, 
                colour_factor, 
                s_and_v_factor,
                quantity_factor,
                score
        )

        slide_sum.tiles.append(tile)

    slide_sum.count = count
    slide_sum.high = high
    slide_sum.medium = medium
    slide_sum.low = low
    slide_sum.none = none
        
    tiles_by_score = slide_sum.tiles_by_score()
    rank = 0
    
    filename = get_file_name(slide._filename)
    
    for t in tiles_by_score:
        rank+=1
        t.rank = rank
    
    slide_sum_percent = ((slide_sum.high + slide_sum.medium + slide_sum.low)/slide_sum.count)*100
    #Document details of original slide to txt file 
    txt = "Total cell coverage : {}%\nTotal Tiles : {} \nHigh Density Tiles : {} \nMedium Density Tiles : {} \nLow Density Tiles : {} \nNo Cells : {}\n "
    f = open ("Extracted Tiles/"+filename+"/"+filename+"_Slide details.txt","w")
    f.write(txt.format (str (int (slide_sum_percent) ), str(slide_sum.count), str(slide_sum.high),str(slide_sum.medium), str(slide_sum.low), str(slide_sum.none)) )
    f.close()

    return slide_sum


def score_tile(np_tile, tissue_percent):
    '''
    Returns score, colour factor, saturation factor and tissue quantity factor

    Takes numpy tile, tissue percentage, row and column
    '''
    
    
    colour_factor = hsv_purple_pink_factor(np_tile)
    s_and_v_factor = hsv_saturation_and_value_factor(np_tile)
    amount = tissue_quantity(tissue_percent)
    quantity_factor = tissue_quantity_factor(amount)
    
    combined_factor = colour_factor * s_and_v_factor * quantity_factor
    
    score = (tissue_percent ** 2) * np.log(1 + combined_factor) / 1000.0
    
    # scale score to between 0 and 1
    score = 1.0 - (10.0 / (10.0 + score))
    return score, colour_factor, s_and_v_factor, quantity_factor


def all_tiles_slide(tile_sum, np_img, view_image=False):
    z = 300
    
    rows = tile_sum.scaled_h
    cols = tile_sum.scaled_w
    row_tile_size = tile_sum.scaled_tile_h
    col_tile_size = tile_sum.scaled_tile_w
    num_row_tiles, num_col_tiles = total_tiles(rows,cols,row_tile_size,col_tile_size)

    summary = create_summary_pil_img(np_img, z, row_tile_size, col_tile_size, num_row_tiles, num_col_tiles)
    draw = ImageDraw.Draw(summary)

    for t in tile_sum.tiles:
        border_colour = tile_border_colour(t.tissue_percentage)
        tile_border(draw, t.r_s, t.r_e,t.c_s, t.c_e, border_colour)
        
    if view_image == True:
        summary.show()
    return summary


def top_tile_slide(tile_sum, np_img,num_top_tiles,filename,filepath):
    #Check if requested number of tiles is too big 
        
    if (num_top_tiles > tile_sum.count):
        flag = True
        
        while (flag == True):
            ask = input("\nThere are only " +str(tile_sum.count)+ " total tiles! \nPlease enter an option. \nAll tiles = A \nHigh Density tiles ["+str(tile_sum.high)+"] = [1]\nHigh and Medium tiles ["+str(tile_sum.high + tile_sum.medium)+"] = [2]\n High,Medium and Low tiles ["+str(tile_sum.high + tile_sum.medium+tile_sum.low)+"] = [3] \nExit = [E]")
            if (ask == "a" or ask =="A"):
                num_top_tiles = tile_sum.count
                flag = False
            elif (ask == "1"):
                num_top_tiles=tile_sum.high
                flag = False
            elif(ask == "2"):
                num_top_tiles = tile_sum.high + tile_sum.medium
                flag = False
            elif (ask == "E" or ask =="e"):
                print("\nExiting.")
                exit()
            else: 
                print("\n -- Invalid response. Please choose an option --")
    
    #check if not enough high tiles
    elif (num_top_tiles > tile_sum.high):
        flag = True
        
        while (flag == True):
            ask = input("\nThere are only " +str(tile_sum.high)+ " high density tiles! Please enter an option. \nHigh Density only = [1]\nHigh and Medium density tiles ["+str(tile_sum.high + tile_sum.medium)+"] = [2]\nHigh,Medium and Low density tiles ["+str(tile_sum.high + tile_sum.medium+tile_sum.low)+"] = [3]\nExit = [E]")
            if (ask == "1"):
                num_top_tiles=tile_sum.high
                flag = False
            elif(ask == "2"):
                num_top_tiles = tile_sum.high + tile_sum.medium
                flag = False
            elif (ask ==3):
                num_top_tiles = tile_sum.low + tile_sum.medium + tile_sum.low
                flag = False
            elif (ask == "E" or ask == "e"):
                print("\nExiting.")
                exit()
            else: 
                print("\n -- Invalid response. Please choose an option -- ")

    z = 300
    rows = tile_sum.scaled_h
    cols = tile_sum.scaled_w
    row_tile_size = tile_sum.scaled_tile_h
    col_tile_size = tile_sum.scaled_tile_w
    num_row_tiles, num_col_tiles = total_tiles(rows,cols,row_tile_size,col_tile_size)
    summary = create_summary_pil_img(np_img, z, row_tile_size, col_tile_size, num_row_tiles, num_col_tiles)
    draw = ImageDraw.Draw(summary)


    #This is where we state how many we want to see
    top_tiles=tile_sum.top_tiles(num_top_tiles)
    f = open("Extracted Tiles/"+filename+"/"+filename+"_Tile Information.txt", "w")
    
    for t in top_tiles:
        
        
        f.write(str(t)+"\n")
        border_colour = tile_border_colour(t.tissue_percentage)
        tile_border(draw, t.r_s, t.r_e,t.c_s, t.c_e, border_colour)

    f.close()
    #shows the original slide with the patch locations 
    
    
    
    rank=1
    for t in top_tiles:
        ### a function if it works
        
        #pass in the correct slide path 
        s = open_slide(filepath)
        x, y = t.o_c_s, t.o_r_s
        w, h = t.o_c_e - t.o_c_s, t.o_r_e - t.o_r_s
        tile_region = s.read_region((x, y), 0, (w, h))
        # RGBA to RGB
        pil_img = tile_region.convert("RGB")
        
        #shows the patches 
        #pil_img.show()
        
        
        pil_img.save("Extracted Tiles/"+filename+"/"+filename+"-"+str(rank)+"-col_"+str(t.r)+"-row_"+str(t.c)+".png")
        rank = rank + 1 
    
    return summary


def create_summary_pil_img(np_img, title_area_height, row_tile_size, col_tile_size, num_row_tiles, num_col_tiles):
    r = row_tile_size * num_row_tiles + title_area_height
    c = col_tile_size * num_col_tiles
    
    summary_img = np.zeros([r, c, np_img.shape[2]], dtype = np.uint8)
    #add gray edes so that tile text doesn't get cut off
    summary_img.fill(120)
    # colour title area white
    summary_img[0:title_area_height, 0:summary_img.shape[1]].fill(255)
    #summary_img[title_area_height:np_img.shape[0] - title_area_height, 0:np_img.shape[1]] = np_img
    summary = numpy_to_image(np_img)
    return summary


def hsv_saturation_and_value_factor(np_tile):
    '''
    Returns saturation and value factor 

    Takes RGB numpy
    '''
    hsv = filter_rgb_to_hsv(np_tile)
    saturation = filter_hsv_to_s(hsv)
    value = filter_hsv_to_v(hsv)
    s_std = np.std(saturation)
    v_std = np.std(value)

    if s_std <0.05 and v_std <0.05:
        factor = 0.4
    elif s_std <0.05:
        factor = 0.7
    elif v_std < 0.05:
        factor = 0.7
    else:
        factor = 1

    factor = factor ** 2
    return factor


def filter_hsv_to_s(hsv):
    '''
    Return saturation value as 1-dimensional array

    takes HSV numpy array
    '''
    s = hsv[:, :, 1]
    s = s.flatten()
    return s


def filter_hsv_to_v(hsv):
    '''
    Return value as 1-d array

    Takes HSV numpy 
    '''
    v = hsv[:,:,2]
    v = v.flatten()
    return v


def hsv_purple_pink_factor(np_tile):

    hues = rgb_to_hues(np_tile)
    hues = hues[hues >= 260]  # exclude hues under 260
    hues = hues[hues <= 340]  # exclude hues over 340
    if len(hues) == 0:
        return 0  # if no hues between 260 and 340, then not purple or pink
    purple_dev = hsv_purple_deviation(hues)
    pink_dev = hsv_pink_deviation(hues)
    avg_factor = (340 - np.average(hues)) ** 2

    if purple_dev == 0:  # avoid divide by zero if tile has no tissue
        return 0

    factor = pink_dev / purple_dev * avg_factor
    return factor


def rgb_to_hues(rgb):
  '''
  Convert RGB numpy array to 1-d array of hue values

  Returns 1-D array of hue values
  '''
  hsv = filter_rgb_to_hsv(rgb)
  hue = filter_hsv_to_h(hsv)
  return hue


def filter_rgb_to_hsv(np_img):
    '''
    Returns image as numpy array in HSV representation

    Filter RGB channels to Hue, saturation, value

    takes Numpy array 
    '''
    hsv = sk_color.rgb2hsv(np_img)
    return hsv


def filter_hsv_to_h(hsv):
    '''
    Returns Hue values as 1-d array.

    Takes HSV numpy array
    '''

    h = hsv[:, :, 0]
    h = h.flatten()
    h *= 360
    h = h.astype("int")
    return h


def hsv_purple_deviation(hsv_hues):

    '''
    Returns HSV purple deviation
    
    Takes HUE numpy 
    '''
    purple_deviation = np.sqrt(np.mean(np.abs(hsv_hues - 270) ** 2))
    return purple_deviation


def hsv_pink_deviation(hsv_hues):
    '''
    Returns HSV pink deviation

    Takes HSV numpy array
    '''
    pink_deviation = np.sqrt(np.mean(np.abs(hsv_hues - 330) ** 2))
    return pink_deviation    


def tissue_quantity(tissue_percentage):
    if tissue_percentage >= 80:
        return TissueQuantity.HIGH
    elif (tissue_percentage >= 10) and (tissue_percentage < 80):
        return TissueQuantity.MEDIUM
    elif (tissue_percentage > 0) and (tissue_percentage < 10):
        return TissueQuantity.LOW
    else:
        return TissueQuantity.NONE


def tissue_quantity_factor(amount):
    '''
    Returns scoring factor base on tile tissue quality

    Takes tissue amount as enum value

    '''
    if amount == TissueQuantity.HIGH:
        quantity_factor = 1.0
    elif amount == TissueQuantity.MEDIUM:
        quantity_factor = 0.2
    elif amount == TissueQuantity.LOW:
        quantity_factor = 0.1
    else: 
        quantity_factor = 0.0
    return quantity_factor


def tissue_percentage(np_img):
    return 100 - mask_percent(np_img)


def tile_border_colour(tissue_percent):
    '''
    Returns RGB code for colour 
    
    Suitable colours for colour blindness?

    '''

    if tissue_percent >= 80:
        border_colour = (0, 255, 0)
    elif (tissue_percent >= 15) and (tissue_percent <80):
        border_colour =  (255, 230, 0)
    elif (tissue_percent > 0) and (tissue_percent <15):
        border_colour = (255, 125, 52)
    else:
        border_colour = (22,23,26)
    
    return border_colour


def tile_border(draw, r_s, r_e, c_s, c_e, colour, border_size = 2 ):
    '''
    Draws the tiles and colours them in across the image. 

    '''
    for i in range(0, border_size):
        draw.rectangle([(c_s + i, r_s + i), (c_e - 1 - i, r_e - 1 - i)], outline = colour)


def get_tile_indices(rows, cols, row_tile_size, col_tile_size):
    
    indices = list()
    
    num_row_tiles, num_col_tiles = total_tiles(rows, cols, row_tile_size, col_tile_size)
    
    for r in range(0, num_row_tiles):
        start_r = r * row_tile_size
        end_r = ((r + 1) * row_tile_size) if (r < num_row_tiles - 1) else rows
    
        for c in range(0, num_col_tiles):
            start_c = c * col_tile_size
            end_c = ((c + 1) * col_tile_size) if (c < num_col_tiles - 1) else cols
            indices.append((start_r, end_r, start_c, end_c, r + 1, c + 1))
  
    return indices


def total_tiles(rows, cols, row_tile_size, col_tile_size):
    '''
    Returns array containing number of vertical tiles and horizontal tiles the image can be divided into

    Takes Rows, Columns, Tile Row Size and Tile Column Size
    '''
    num_row_tiles = math.ceil(rows / row_tile_size)
    num_col_tiles = math.ceil(cols / col_tile_size)
    return num_row_tiles, num_col_tiles


def mask_percent(np_img):
    if (len(np_img.shape) == 3) and (np_img.shape[2] == 3):
        np_sum = np_img[:, :, 0] + np_img[:, :, 1] + np_img[:, :, 2]
        mask_percentage = 100 - np.count_nonzero(np_sum) / np_sum.size * 100
    else:
        mask_percentage = 100 - np.count_nonzero(np_img) / np_img.size * 100
    
    return mask_percentage


def small_to_large_mapping(small_pixel, large_dimensions):
    ''' 
    Returns tuple consisting of scaled up width and height

    Takes scaled down width and height, original width and height

    '''

    small_x, small_y = small_pixel
    large_w, large_h = large_dimensions
    large_x = round((large_w / 32) / math.floor(large_w / 32) * (32 * small_x))
    large_y = round((large_h / 32) / math.floor(large_h / 32) * (32 * small_y))

    return large_x, large_y


def tissue_percentage_masked(np_image):
    return 100 - mask_percent(np_image)


def extractor(filepath,num_top_tiles):
    '''
    | Returns: n number of tiles from an unfiltered svs slide, a slide.txt file and a tile.txt file 
       
    Files are saved in a folder system for clarity
    
    -> /Extracted Tiles/ -> /"Filename"/ -> Filename1.png
    
    | args: 
        filepath =  'folder/image.svs'
        
        Integer number of expected tiles
    '''

    if type(filepath) != str: 
        raise ValueError("\nbatch_extractor(*folder* , num) -> Folder name must be a String argmunent  eg '/myfolder/'  ")

    if type(num_top_tiles)!= int:
        raise ValueError("\nbatch_extractor(folder , *num*) - > Num must be an integer")

    if num_top_tiles <= 0:
        raise ValueError("batch_extractor(folder , *num*) - > Num must be greater than 0")

    print("--------------- E X T R A C T I N G  T I L E S -------------------\n")
    filename = get_file_name(filepath)
    slide = import_svs(filepath)
    width,height = slide_dimensions(slide)
    s_w, s_h = scaled_dimensions(width, height)
    slide_img = import_slide(slide, s_w, s_h)
    np_slide=image_to_numpy(slide_img)
    gray_np=grayscale_filter(np_slide)
    complement_np = complement_filter(gray_np)
    otsu = otsu_filter(complement_np)
    otsu_mask = mask_filter(np_slide,otsu)
    
    is_folder("Extracted Tiles")
    is_folder("Extracted Tiles/"+filename)
    
    tile_sum = score_tiles(slide, otsu_mask)
    tile_slide = all_tiles_slide(tile_sum, otsu_mask)
    top_slide = top_tile_slide(tile_sum, otsu_mask,num_top_tiles, filename, filepath)
    
    save_image(tile_slide, "Tiled_"+filename, "Extracted Tiles/"+filename)
    save_image(top_slide, "Top_Tiles_"+filename, "Extracted Tiles/"+filename)
    
    print("--------------- E X T R A C T I O N  C O M P L E T E  ------------\n")


def batch_extractor(folder, num):
    '''
    | Returns: n number of tiles from an unfiltered svs slide from a folder, a slide.txt file and a tile.txt file 
       
    Files are saved in a folder system for clarity
    
    -> /Extracted Tiles/ -> /"Filename"/ -> Filename1.png
    
    *Make sure source folder is within the project folder*

    | args: 
        folder =  'folder/'
        
        Integer number of expected tiles
    '''
    if type(folder) != str: 
        raise ValueError("\nbatch_extractor(*folder* , num) -> Folder name must be a String argmunent  eg '/myfolder/'  ")

    if type(num)!= int:
        raise ValueError("\nbatch_extractor(folder , *num*) - > Num must be an integer")

    if num <= 0:
        raise ValueError("batch_extractor(folder , *num*) - > Num must be greater than 0")
    #Check if folder exists
    if os.path.exists("./"+folder):
        
        #get all svs files from path
        files = glob.glob("./"+folder+"*.svs")
        
        #no svs files found
        if not files: 
            print("no files in "+folder)
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), "/"+folder)
        #
        for file in files:
            #Have to slice off ./ at start because of formatting of the argument slide
            file = file[2:]
            extractor(file,num)
    else:
        print("No such folder")