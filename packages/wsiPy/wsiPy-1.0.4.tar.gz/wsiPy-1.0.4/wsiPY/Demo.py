from functions import *

#svs object
slide = import_svs('Slides/TCGA2.svs')

w,h = slide_dimensions(slide, details=True)
s_w, s_h = scaled_dimensions(w,h, details=True)


slide_img=import_slide(slide,s_w,s_h)
#Numpy array
np_slide=image_to_numpy(slide_img)


 
gray_np=grayscale_filter(np_slide, view=True)
complement_np = complement_filter(gray_np,view=True)
#hysterisis_filter(complement_np,view=True)
otsu = otsu_filter(complement_np)
contrast_stretch(complement_np,save=True, low=50,high=255)
#kmeans_segmentation(np_slide, )
#RAG_segmentation(np_slide,view_image=True)
#otsu_mask = mask_filter(np_slide,otsu)
#RAG_segmentation(otsu_mask)


#extract_tiles(slide, otsu_mask, 13)
#extractor("Slides/TCGA2.svs", 13)
#batch_extractor(12, 4)
