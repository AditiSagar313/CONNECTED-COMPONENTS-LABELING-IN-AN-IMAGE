# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 16:57:05 2021

@author: Aditi
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np
import random
org_img = cv2.imread("image1.jpg")
cv2.imshow("Original Image",org_img)


def No_of_cc(org_img,v_min,v_max,adj):

    gray_img = cv2.cvtColor(org_img,cv2.COLOR_BGR2GRAY)
    
    cc = 0             #initialize number of connected components
    n = 0
    
    map_dict = dict(())
    smart_label = dict(())
    def Rand():
        nonlocal cc
        cc = cc+1                 #Total number of connected components
        r = random.randint(1,255)
        g = random.randint(1,255)
        b = random.randint(1,255)
        bgr = [b,g,r]
        return bgr
    
    
    
    def next_num():
        nonlocal n
        nonlocal smart_label
        n = n+1
        smart_label[n] = n
        return n
    
      
    label = np.zeros((org_img.shape[0],org_img.shape[1]))
    
    def convert(gray_img):
        
        empty_img = np.zeros((org_img.shape[0],org_img.shape[1]))

	 #scan the whole image 
        for i in range(511):
            for j in range(511):

		#assigning label according to threshold value
                if(gray_img[i][j]>=v_min and gray_img[i][j]<=v_max ):
                    empty_img[i][j] = 255
                else:
                    empty_img[i][j] = 0
                    
        cv2.imshow("Empty Image",empty_img)
        return empty_img.astype('uint8')
    
    
    
    def fill( label,i,j,adj):

	#for 4 - adjacency
        if(adj==4):
            global smart_label
            if((i>=1) and (j>=1)):
               #if r and t are same and have value 0
                if((empty_img[i][j]==255) and (empty_img[i][j-1]==0) and (empty_img[i-1][j]==0)):
                    label[i][j] = int(next_num())
                    if label[i][j] not in map_dict:
                        map_dict[int(label[i][j])] = [0]
                    
                #only one of them is high
                elif((empty_img[i][j-1]==0 and empty_img[i-1][j]==255 ) or (empty_img[i][j-1]==255 and empty_img[i-1][j]==0 )):
                    if((empty_img[i][j-1]==0 and empty_img[i-1][j]==255 )):
                        label[i][j] = int(label[i-1][j])
                    else:
                       label[i][j] = int(label[i][j-1])
                #both are high
                elif(empty_img[i][j-1]==255 and empty_img[i-1][j]==255): 
                    #both have same label
                    if(label[i][j-1]==label[i-1][j]):   
                        label[i][j] = int(label[i-1][j])                             
                    #both have different label so have to handle them
                    elif(label[i][j-1]!=label[i-1][j]):   
                        
                        a =int(label[i-1][j])
                        b = int(label[i][j-1])
                        label[i][j]=min(a,b)
                        if(min(a,b)  not in map_dict):
                            map_dict[min(a,b)]=[max(a,b)]
                        else:
                            if max(a,b) not in map_dict[min(a,b)]:
                                map_dict[min(a,b)].append(max(a,b))

	 #for 8 - adjacency 
        elif(adj==8):
            global smart_label
            if((i>=1) and (j>=1)):
               # if all are empty
                if((empty_img[i][j]==255) and (empty_img[i][j-1]==0) and (empty_img[i-1][j]==0) and  (empty_img[i-1][j-1]==0) and (empty_img[i-1][j+1]==0)):
                    label[i][j] = int(next_num())
                    if label[i][j] not in map_dict:
                        map_dict[int(label[i][j])] = [0]
                    
              #only few of them is high
                elif((empty_img[i][j-1]==0 and empty_img[i-1][j]==255 ) or (empty_img[i][j-1]==255 and empty_img[i-1][j]==0 )):
                    if((empty_img[i][j-1]==0 and empty_img[i-1][j]==255 )):
                        label[i][j] = int(label[i-1][j])
                    else:
                       label[i][j] = int(label[i][j-1])
                elif(empty_img[i][j-1]==255 and empty_img[i-1][j]==255 and (empty_img[i-1][j-1]==0) and (empty_img[i-1][j+1]==0) ): 
                    if(label[i][j-1]==label[i-1][j]):   
                        label[i][j] = int(label[i-1][j])                             
                
                    elif(label[i][j-1]!=label[i-1][j]):   
                        
                        a =int(label[i-1][j])
                        b = int(label[i][j-1])
                        label[i][j]=min(a,b)
                        if(min(a,b)  not in map_dict):
                            map_dict[min(a,b)]=[max(a,b)]
                        else:
                            if max(a,b) not in map_dict[min(a,b)]:
                                map_dict[min(a,b)].append(max(a,b))
                else:
                    if((empty_img[i-1][j-1]==255  and  empty_img[i-1][j+1] ==0) or (empty_img[i-1][j-1]==0  and  empty_img[i-1][j+1] ==255)):
                        if (empty_img[i-1][j-1])==255:
                            label[i][j] = int(label[i-1][j-1])
                        else:
                            label[i][j] = int(label[i-1][j+1])
                    elif (empty_img[i-1][j-1]==255  and  empty_img[i-1][j+1] ==255):
                        
                        
                        a =int(label[i-1][j-1])
                        b = int(label[i-1][j+1])
                        label[i][j]=min(a,b)
                        if(min(a,b)  not in map_dict):
                            map_dict[min(a,b)]=[max(a,b)]
                        else:
                            if max(a,b) not in map_dict[min(a,b)]:
                                map_dict[min(a,b)].append(max(a,b))
                    
                    
    
    
                
    empty_img = convert(gray_img)
    col_img = cv2.cvtColor(empty_img,cv2.COLOR_GRAY2BGR) 
    
    
    
    for i in range(512):
        for j in range(512):
            if(empty_img[i][j]==0):
                pass
            else:
                fill(label,i,j,adj)
    
    #creating the dict of the labels
     
    #cannot create a blank list so we intisialize it with 0
    color_list= []
    color_list.append([0,0,0])
    for i in range(1,len(map_dict)+1):
        color_list.insert(i,(0,0,0))
    
    
    for i in range(1,len(map_dict)):
    
        list1 = map_dict[i]
        
        #print("list1",list1)
        if all( x == y for x,y in zip(color_list[i],(0,0,0))):
            color_list[i] = Rand()
            for j in range(1,len(list1)):
                 if all( a == b for a,b in zip(color_list[list1[j]],(0,0,0))):
                        color_list[list1[j]]  = color_list[i]
                        
        else:
            list1 = map_dict[i]
            for j in range(1,len(list1)):
                 if all( a == b for a,b in zip(color_list[list1[j]],(0,0,0))):
                        color_list[list1[j]]  = color_list[i]
            
            
            
                 
    
    for i in range(512):
        for j in range(512):
            if(gray_img[i][j]==0):
                pass
            else:
                col_img[i][j] = color_list[int(label[i][j])]
                
       
            
           
                   
    """
    print(smart_label)
    print(map_dict)
    print(color_list)  
     """   
            


        
    cv2.imshow("Final Image",col_img)
    print("The number of connected component is =>",cc)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

v_min = int(input("v_min : "))
v_max = int(input("v_max : "))
adj = int(input("Enter the adjacency : "))

No_of_cc(org_img,v_min,v_max,adj)