import glob,cv2,json,sys,pdb,pickle, os, tqdm
import numpy as np

def load_vid_frames(path):
    op={}
    if os.path.isfile(path):
        vidcap=cv2.VideoCapture(path)
        f=-1
        while (vidcap.isOpened()):
            success,image=vidcap.read()
            if success==True:
                f+=1
                op[f]=image
            else:
                break
    else:
        print(path," doesnt exist")
        sys.exit()
    return op

def find_valid_center(x,y, srch_x, srch_y):
    new_xc = np.random.randint(0+(int(x/2)+1),srch_x-(int(x/2)+1))
    new_yc = np.random.randint(0+(int(y/2)+1),srch_y-(int(y/2)+1))
    return new_xc, new_yc
    
def load_image(f_no, loc,mode, tar_x, tar_y):
    image = dct[f_no]
    if mode == "target":
        op = image[loc[1]:loc[3],loc[0]:loc[2]]
        x_scale_factor = (loc[2]-loc[0])/tar_x
        y_scale_factor = (loc[3]-loc[1])/tar_y
        return [cv2.resize(op,(tar_x,tar_y)),[x_scale_factor,y_scale_factor]]
    elif mode == "search":
        return image

def random_center_search_image(img,loc,sf,pair,srch_x, srch_y):
    # pdb.set_trace()
    loc_1 = loc.copy()
    op = np.zeros((srch_y,srch_x,3))
    width = int(img.shape[1] * sf[0])
    height = int(img.shape[0] * sf[1])
    loc[2] = int(loc[2] * sf[0]) 
    loc[0] = int(loc[0] * sf[0])
    loc[1] = int(loc[1] * sf[1])
    loc[3] = int(loc[3] * sf[1])
    img = cv2.resize(img,(width, height),fx=sf[0],fy=sf[1]) #scaling image to the input scaling factor
    #find the center of scaled image
    x_size = loc[2]-loc[0]
    y_size = loc[3]-loc[1]
    x_c = loc[0] + int(x_size/2)
    y_c = loc[1] + int(y_size/2) 
    
    new_xc , new_yc = find_valid_center(x_size,y_size,srch_x,srch_y)
#     print(new_xc,new_yc,x_size,y_size)
    #padding the image if necessary
    left_pad = 0
    right_pad = 0
    top_pad = 0
    bot_pad = 0
    if y_c-new_yc < 0: #If center cannot accomodate left context.
        left_pad = new_yc-y_c #pad the number of values it is short of
    if y_c+(srch_y-new_yc) > img.shape[0]: #If center cannot accomodate right context.
        right_pad = srch_y-new_yc+y_c-img.shape[0] #pad the number of values it is short of
    if x_c-new_xc < 0:
        top_pad = new_xc-x_c
    if x_c+(srch_x-new_xc) > img.shape[1]:
        bot_pad = srch_x-new_xc+x_c-img.shape[1]
    mean_val = np.mean(img,axis=(0,1))
    try:
        if left_pad or right_pad or top_pad or bot_pad:
    #         print(loc_1)
            if left_pad:
                y1 = 0
            else:
                y1 = y_c-new_yc
            if right_pad:
                y2 = img.shape[0]
            else:
                y2 = y_c+(srch_y-new_yc)
            if top_pad:
                x1 = 0
            else:
                x1 = x_c-new_xc
            if bot_pad:
                x2 = img.shape[1]
            else:
                x2 = x_c+(srch_x-new_xc)
            op_tmp = img[y1:y2,x1:x2]
            op[left_pad:srch_y-right_pad,top_pad:srch_x-bot_pad] = op_tmp
            op[:,:,0][op[:,:,0]==0] = mean_val[0]
            op[:,:,1][op[:,:,1]==0] = mean_val[1]
            op[:,:,2][op[:,:,2]==0] = mean_val[2]
            return op,new_xc,new_yc,int(x_size/2),int(y_size/2),1
        else:
            return img[y_c-new_yc:y_c+(srch_y-new_yc),x_c-new_xc:x_c+(srch_x-new_xc)],new_xc,new_yc,int(x_size/2),int(y_size/2),0
    except:
        pdb.set_trace()


tar_x = 86
tar_y = 46
srch_x = 172
srch_y = 92

root_video_path = "/Volumes/1TB/Text_For_Autonomous_Navigation/Videos/train/"
final_save_path = "/Volumes/1TB/pb_files/train.pb"

folders = ["0","100","200","300","400"]

for fldr in folders:
    Video_Location = root_video_path+fldr+"/"
    with open("prestep/"+fldr+".txt",'rb') as f:
        chk=pickle.load(f)
    final_dump = []
    i=0
    prev_vid_name = Video_Location + str(chk[0][0])+".mp4"
    dct = load_vid_frames(prev_vid_name)
    for pair in tqdm.tqdm(chk):
        vid_name = Video_Location +str(pair[0])+".mp4"
        if vid_name != prev_vid_name:
            dct = load_vid_frames(vid_name)
            prev_vid_name = vid_name
        target_frame_no = pair[1]
        search_frame_no = pair[2]
        target_loc = pair[3]
        search_loc = pair[4]
        try:
            tar_image, sf = load_image(target_frame_no, target_loc,"target", tar_x, tar_y)
            srch_image = load_image(search_frame_no, search_loc,"search", tar_x, tar_y)
            if tar_image.any() and srch_image.any():
                tar_image = cv2.resize(tar_image,(86,46))
                srch_image,xc,yc,x,y = random_center_search_image(srch_image,search_loc,sf,pair)
                final_dump.append([tar_image,srch_image,[xc,yc,x,y]])
                i+=1
                if i>=1000:
                    with open(final_save_path,"ab") as x:
                        pickle.dump(final_dump,x)
                        final_dump = []
                        i=0
        #         cv2.rectangle(srch_image,(xc-x,yc-y), (xc+x,yc+y), (255,0,0), 3)
        #         cv2.imwrite("random.jpg",srch_image)
        #         sys.exit()
            else:
                print("no op",pair)
        except:
            pass
    with open(final_save_path,"ab") as x:
        pickle.dump(final_dump,x)
