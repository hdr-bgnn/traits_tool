import traits_tool_mini as ttm #import trait_tool_mini.py as module
import json

#Load segmented image to array
fileName,traitsMapAll=ttm.extract_traits_map("/home/bahadir/Desktop/python_projects/Fish_related/segmented_area/INHS_FISH_90766.png")
print(fileName)

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

# A : Standard length / Distance between nose(minX of head) to tail of trunk(xMax of trunk)
head_xMin=ttm.get_trait_edges(traitsMapAll,6,"xMin") #gets xMin of head(trait_index=6)
trunk_xMax=ttm.get_trait_edges(traitsMapAll,11,"xMax") #gets xMax of trunk(trait_index=11)
A=float(abs(trunk_xMax-head_xMin))
print("A :",A," pixels")

# B : eye to head area Ratio
eye_area=ttm.get_trait_area(traitsMapAll,7) #gets area  of eye (trait_index=7)
head_area=ttm.get_trait_area(traitsMapAll,6) #gets area  of head (trait_index=6)
B=float(eye_area/head_area)
print("B :",B)

# C : Length from back of head to caudal fin (distance between xMax of head and xMax of trunk(caudal fin)) ????? C=A-E ????
head_xMax=ttm.get_trait_edges(traitsMapAll,6,"xMax") #gets xMax of head(trait_index=6)
trunk_xMax=ttm.get_trait_edges(traitsMapAll,11,"xMax") #gets xMax of trunk(trait_index=11)
C=float(abs(trunk_xMax-head_xMax))
print("C : ",C," pixels")


# D : Eye diameter (eye width)
D=float(ttm.get_trait_dimensions(traitsMapAll,7,"width")) #gets width of eye (trait_index=7)
print("D : ",D," pixels")

# E : Head length (above midline(horizontal line over centroid of eye or halfpoint of the eye width) of eye)

#if we use centroid
eye_centroid=ttm.get_trait_centroid(traitsMapAll,7) #returns  the (x,y) coordinates of centroid of eye
min,max=ttm.get_trait_minmax_ofPoint(traitsMapAll,6, round(eye_centroid[0],0), 0) 
E=float(float(abs(max-min)))
print("E : ",E," pixels (calculated using centroid)")

#if we use middle point 
eye_edges=ttm.get_trait_edges(traitsMapAll,7,"all")   # returns xMin,xMax,yMin,yMax of eye (trait_index=7)
midX_eye=abs(eye_edges[0]+(eye_edges[1]-eye_edges[0])/2)
min,max=ttm.get_trait_minmax_ofPoint(traitsMapAll,6, round(midX_eye,0), 0)
E=float(abs(max-min))
print("E : ",E," pixels (calculated using midPoint)")

# F: Head depth (head width)
F=float(ttm.get_trait_dimensions(traitsMapAll,6,"width"))
print("F : ",F," pixels")

# G : snout length (distance between xMin of head and xMin of eye )
eye_xMin=ttm.get_trait_edges(traitsMapAll,7,"xMin")
head_xMin=ttm.get_trait_edges(traitsMapAll,6,"xMin")
G=float(abs(head_xMin-eye_xMin))
print("G : ",G," pixels")


#JSON String

output_string={"fileName":fileName, "A": A , "B": B , "C": C , "D": D, "E": E , "F": F , "G": G}
json_string = json.dumps(output_string)

print(json_string) 






