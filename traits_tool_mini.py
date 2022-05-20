#!/usr/bin/env python
# Tool to extract traits(features) from segmented images
# by @xbahadirx
# bahadiraltintas@gmail.com


import os,sys
import numpy as np
from PIL import Image, ImageFilter
import math
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=np.VisibleDeprecationWarning)
np.set_printoptions(threshold=sys.maxsize)

def create_colorScheme(): #This colorscheme can be modified and applied for different segmentation color shchemes
    colorScheme=[("Dorsal Fin",(254,0,0)),
    ("Adipsos Fin",(0,254,0)),
    ("Caudal Fin",(0,0,254)),
    ("Anal Fin",(254,254,0)),
    ("Pelvic Fin",(0,254,254)),
    ("Pectoral Fin",(254,0,254)),
    ("Head(minus eye)",(254,254,254)),
    ("Eye",(0,254,102)),
    ("Caudal Fin Ray",(254,102,102)),
    ("Alt Fin Ray",(254,102,204)),
    ("Alt Fin Spine",(254,204,102)),
    ("Trunk",(0,124,124))]
    colorScheme=np.array(colorScheme,dtype=object)
    return colorScheme

def getAngle(a, b, c): # calculates the angle between 3 points given x,y coordinates
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang

def rgb2traitName(rgbColor,colorScheme):

    for namesx in colorScheme:

        if namesx[1]==rgbColor:

            return(namesx[0])

def searchArray(arr1,arr2):
    for i in range(len(arr2)):
        if(arr2[i,1]==arr1):
            return True
def get_trait_minmax_ofPoint(traitsMapAll,trait_index, target, index):  #index : 0 for y-axis : 1 for x-axis
    arr=traitsMapAll[trait_index]
    a=np.array([])
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if (arr[i][j] == target):
                a=np.append(a,[target,arr[i,index]])
    a=np.reshape(a,(int(len(a)/2),2))
    return int(min(a[:,1])),int(max(a[:,1]))

def get_trait_names():   #creating headers for treaits csv file or fieldname for json from colorScheme
    colorScheme=create_colorScheme()
    traitNames=colorScheme[:,0]
    return traitNames

def get_trait_edges(traitsMapAll,trait_index,pointName): #gets min and max position of the segmented traits (both for x and y-axis)
    #example: get_feature_edges(traitsMapAll,0,"yMin") -> will return maximum y-coordinate of [0]th  trait(Dorsal Fin) 
    #Trait Index (from colorScheme)
    #[0] Dorsal Fin
    #[1] Adipsos Fin
    #[2] Caudal Fin
    #[3] Anal Fin
    #[4] Pelvic Fin
    #[5] Pectoral Fin
    #[6] Head(minus eye)
    #[7] Eye
    #[8] Caudal Fin Ray
    #[9] Alt Fin Ray
    #[10] Alt Fin Spine
    #[11] Trunk
    #pointname
    #xMin
    #xMax
    #yMin
    #yMax
    if traitsMapAll[trait_index] is not None:
        xMin=min(traitsMapAll[trait_index][:,1])
        xMax=max(traitsMapAll[trait_index][:,1])
        yMin=min(traitsMapAll[trait_index][:,0])
        yMax=max(traitsMapAll[trait_index][:,0])
        if pointName=="xMin":
            return xMin
        elif pointName=="xMax":
            return xMax
        elif pointName=="yMin":
            return yMin
        elif pointName=="yMax":
            return yMax
        elif pointName=="all":
            return xMin,xMax,yMin,yMax
        else:
            print("You should specify proper pointName ('xMin','xMax','yMin','yMax' or 'all')")
            return "NULL"
    else:
        print("The feature you gave does not exist in the image")
        return  "NULL"

def get_trait_area(traitsMapAll,trait_index):
    if traitsMapAll[trait_index] is not None:
       return len(traitsMapAll[trait_index])
    else:
        return "NULL"

def get_trait_centroid(traitsMapAll,trait_index):
    if traitsMapAll[trait_index] is not None:
        centroidX=sum(traitsMapAll[trait_index][:,1])/len(traitsMapAll[trait_index][:,1])
        centroidY=sum(traitsMapAll[trait_index][:,0])/len(traitsMapAll[trait_index][:,0])
        return centroidX,centroidY
    else:
        return "NULL","NULL"

def get_distance(firstPoint,secondPoint): #calculates distance between two given point coordinates
    dist=((((secondPoint[0] - firstPoint[0] )**2) + ((secondPoint[1]-firstPoint[1])**2) )**0.5)
    return dist

def get_trait_dimensions(traitsMapAll,trait_index,dimType): #returns height and width of given trait_index
    xMin,xMax,yMin,yMax=get_trait_edges(traitsMapAll,trait_index,"all")
    width=xMax-xMin
    height=yMax-yMin
    if dimType=="width":
        return width
    elif dimType=="height":
        return height
    elif dimType=="all":
        return height,width
    else:
        print("You should specify proper dimName ('width', 'height' or 'all')")
        return "NULL"

def extract_traits_map(file_name):
    head, tail = os.path.split(file_name)
    traitNames=get_trait_names()
    colorScheme=create_colorScheme()
    ####
    img = Image.open(file_name)
    colors = img.convert('RGB').getcolors() 
    colorx=np.array(colors,dtype=object)
    im = img.convert("RGB")
    na = np.array(im,dtype=object)
    # Median filter to remove outliers
    im = im.filter(ImageFilter.MedianFilter(3))
    cntr=np.array([])
    traitsMap=[]
    numTraits=0
    for x in colorScheme:
    
        if(searchArray(x[1],colorx)):
            numTraits=numTraits+1
            colorMapY, colorMapX = np.where(np.all(na==x[1],axis=2))
            traitsMap.append(np.stack((colorMapY, colorMapX),axis=1))
            cntr=np.append(cntr,[[x[1],"",""]])

    cntr=np.reshape(cntr,(int(len(cntr)/3),3)) 
    traitNamesAvailable=np.array([])
    for f in cntr:
        traitNamesAvailable=np.append(traitNamesAvailable,str(rgb2traitName(f[0],colorScheme)))
    traitsAvailable=np.array([])
    for i in range(np.size(traitNamesAvailable)):
        x = np.where(traitNames == traitNamesAvailable[i])
        traitsAvailable=np.append(traitsAvailable,int(x[0]))
    traitsMapAll=[]
    for i in range(len(colorScheme)):
        if(np.size((np.where(traitsAvailable==i)))>0):
            traitsMapAll.append(traitsMap[int(np.where(traitsAvailable==i)[0])])
        else:
            traitsMapAll.append("NULL")
          
    return tail,traitsMapAll

