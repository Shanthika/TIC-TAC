# Import the required modules
import dlib
import cv2
import argparse as ap 
import numpy as np
import time as t

def draw_o(img,i,j):
    img[80+(i*100):120+(i*100),80+(j*100):120+(j*100)]=255
    return img

def draw_x(img,i,j):
    img[60+(i*100):140+(i*100),100+(j*100)]=255
    img[100+(i*100),60+(j*100):140+(j*100)]=255
    return img

def evaluate(mat):
    sum_arr=[]
    sum_val=0
    for i in range(3):
        for j in range(3):
            sum_val+=mat[i][j]
        sum_arr.append(sum_val)
    count1=sum_arr.count(9)
    count2=sum_arr.count(12)
    if(count1>0):
        return 1
    if(count2>0):
        return 2
    else:
        return 0


def interface(val,flag,img):
    count=0
    
    l={1:(0,0),2:(0,1),3:(0,2),4:(1,0),5:(1,1),6:(1,2),7:(2,0),8:(2,1),9:(2,2) }
 
    mat=[[0,0,0],[0,0,0],[0,0,0]]
 
    i,j=l[val] 
    if(flag==1):
        img=draw_o(img,i*2,j*2)
        flag=2
        count+=1
        mat[i][j]=3

    elif(flag==2):
        img=draw_x(img,i*2,j*2)
        flag=1
        count+=1
        mat[i][j]=4
    
    val=evaluate(mat)

    return img,val
    
      

def run(dispLoc=False):
    # Create the VideoCapture object
    cam = cv2.VideoCapture(1)

    # If Camera Device is not opened, exit the program
    if not cam.isOpened():
        print("Video device or file couldn't be opened")
        exit()
    
    count=0
    m,n=600,600
    #interface display matrix
    mat_img=np.zeros([m,n])
    mat_img[190:210,:]=255
    mat_img[390:410,:]=255
    mat_img[:,190:210]=255
    mat_img[:,390:410]=255
    
    flag=1 
    count_val=[]
    print("Press key `p` to pause the video to start tracking")
    while(True):
        if(count%150000==0):
            count = 0
            # Retrieve an image and Display it.
            retval, img = cam.read()
            if not retval:
                print("Cannot capture frame device")
                exit()
            av = []

            #box coordinates (x1,x2) and(y1,y2) of all 9 boxes obtained using box_detecion
            l= {1:(30,221,261,435),2:(228,406,262,435),3:(409,589,266,431),4:(61,228,118,249),5:(236,394,119,253),6:(399,564,119,254),7:(87,238,0,108),8:(243,385,7,108),9:(390,540,11,110)}
           
            mapping={3:1,2:2,1:3,6:4,5:5,4:6,9:7,8:8,7:9}
            
            for con in range(1,10):
                x1,x2,y1,y2 = l[con]

                av.append(np.mean(img[y1:y2, x1:x2]))

            #threshold value to detect a person standing in the box
            thresh = 115

            indexes = []
            for i in range(len(av)):
                if av[i]<thresh:
                    indexes.append(i) 
            if(len(indexes)>0):
                final_val=min(indexes)+1
                print("You are standing in box number ",final_val)
                
                if(flag==1 and final_val not in count_val):
                    mat_img,val=interface(mapping[final_val],flag,mat_img)
                    flag=2
                elif(flag==2 and final_val not in count_val):
                    mat_img,val=interface(mapping[final_val],flag,mat_img)
                    flag=1
                count_val.append(final_val)
                if(val==1):
                    print('player1')
                    
                elif(val==2):
                    print('player2')

            cv2.imshow("Image", img)
            cv2.imshow('original',mat_img)  
            if(cv2.waitKey(1)==ord('p')):
                cv2.destroyAllWindow()
                break
        count+=1
        print(count)    
    

if __name__ == "__main__":
    run()
