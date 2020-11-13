# Data_Creation_Module

This repo is aimed at creating pairs of crops of image around a text object.  
data_prestep.py deals with selecting text tracks that have atleast 5-length (text regions available in 5 consecutive frames), and then outputs
  a.txt file that is to be fed into crop_images.py  
crop_images.py deals takes the text file created in the previous step and then generates search and target images.  
  &emsp;The tagret image contains normalised text centered.  
  &emsp;The search image contains contains a crop from (one of the 5) consecutive frame centered at previous frames text location.  
  &emsp;Random crop is implemented ( Where the text might contain at any place in the search image, not only at the center).  
Inputs have to changed as per requirements in the following variables of each file:  
  &emsp;data_prestep.py:  
    &emsp;&emsp;"video_folder" : This is the folder name of the videos (ex: 0,100,200,300, etc)  
    &emsp;&emsp;"annotation_file_path" : This is the location where the .json file of the corresponding folder is present (ex: //path//0_videos_results.json)  
    &emsp;&emsp;"videos_location" : This is where the videos are located    
  crop_images.py:  
    &emsp;&emsp;"root_video_path" : This is where the videos are located    
&emsp;&emsp;    "final_save_path" : Location where the final output pickle file has to be stored.  
&emsp;&emsp;    "tar_x" : Size of target image in x direction (ex: 256, 127 etc)  
&emsp;&emsp;    "tar_y" : Size of target image in y direction (ex: 256, 127 etc)  
&emsp;&emsp;    "srch_x" : Size of search image in x direction (ex: 256, 127 etc)  
&emsp;&emsp;    "srch_y" : Size of search image in y direction (ex: 256, 127 etc)  
    
