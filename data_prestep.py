import glob,cv2,json,sys,pdb,pickle
import numpy as np


#RoadText-1k Categories:
# (1)   English_Legible
# (2)   Non_English_Legible
# (3)   Illegible

#RoadText Categories:

# (1)   English
# (2)   European
# (3)   Illegible
# (4)   Asian

def load_data(path):
    #Load data from the json file with the text locations and track annotations.
    #json file to be in the format of Scalabel tool output.
    with open(path,"r") as f:
        gt_raw = json.load(f)
    gt={}
    for item in gt_raw:
      if item["videoName"] not in gt.keys():
        gt[item["videoName"]]={}
      if item["index"] not in gt[item["videoName"]].keys():
        gt[item["videoName"]][item["index"]]=[]
      if item["labels"] != None:
        gt[item["videoName"]][item["index"]].append(item["labels"])
    return gt

def check_labels_in_frame(vid,f,s,gt):
    #check if the same text instance is present in the following frames of distance upto s.
    #return a list of items with all the corresponding text locations in the frames.
    tmp_lst=[]
    if f in gt[vid].keys() and s in gt[vid].keys():
        lbls2 = gt[vid][s]
        lbls1 = gt[vid][f]
        for lbl1 in lbls1:
          for lbl2 in lbls2:
            # print(lbl1,lbl1[0])
            # print(lbl2,lbl2[0])
            # sys.exit()
            # print(lbl1["id"],lbl2[0]["id"])
            if (lbl1[0]["id"] == lbl2[0]["id"]) and ((lbl1[0]["category"] == "European" and lbl2[0]["category"] == "European") or (lbl1[0]["category"] == "English" and lbl2[0]["category"] == "English") or (lbl1[0]["category"] == "Asian" and lbl2[0]["category"] == "Asian")):
            # if (lbl1[0]["id"] == lbl2[0]["id"]) and ((lbl1[0]["category"] == "English_Legible" and lbl2[0]["category"] == "English_Legible") or (lbl1[0]["category"] == "Non_English_Legible" and lbl2[0]["category"] == "Non_English_Legible")):
                b1 = [round(lbl1[0]["box2d"]["x1"]),round(lbl1[0]["box2d"]["y1"]),round(lbl1[0]["box2d"]["x2"]),round(lbl1[0]["box2d"]["y2"])]
                b2 = [round(lbl2[0]["box2d"]["x1"]),round(lbl2[0]["box2d"]["y1"]),round(lbl2[0]["box2d"]["x2"]),round(lbl2[0]["box2d"]["y2"])]
                tmp_lst.append([vid,f,s,b1,b2,1])
    return tmp_lst

video_folder = "0"
annotation_file_path = "/Volumes/1TB/Text_For_Autonomous_Navigation/Ground_Truths/Localisation/"+video_folder+"_videos_results.json"
videos_location = "/Volumes/1TB/Text_For_Autonomous_Navigation/Videos/train/"+video_folder+"/*.mp4"

gt = load_data(annotation_file_path)            
vids =glob.glob(videos_location)
lst=[]
# print(vids)


temporal_distance = 5
for v_name in vids:
    print(v_name)
    vid = v_name.split("/")[-1].split(".")[0]
    vidcap=cv2.VideoCapture(v_name)
    frame_no = 0
    while (vidcap.isOpened()):
        success,image=vidcap.read()
        if success==True:
            for i in range(1,6):
                t_lst = check_labels_in_frame(vid,frame_no,frame_no+i,gt)
                if t_lst:
                    lst=lst+t_lst
            frame_no+=1
        else:
            break

with open("prestep/"+folder+".txt",'wb') as f:
    pickle.dump(lst,f)