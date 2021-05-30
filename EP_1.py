
# pintaaz2.py - 2020
from cv2 import imread,imshow,waitKey,IMREAD_COLOR,TM_CCOEFF_NORMED,matchTemplate,resize,INTER_AREA,imwrite
import numpy as np
import math

def calc_distance(color_a,color_b):
    """[Calculate "distance" between two colors]

    Arguments:
        color_a {[Array]} 
        color_b {[Array]} 

    Returns:
        [float] -- [Distance between colors]
    """
    distance = (color_a[0]-color_b[0])**2+(color_a[1]-color_b[1])**2+(color_a[2]-color_b[2])**2
    distance = distance**0.5
    return distance

def one_color(image,color=[0,0,255]):
    """[Function made to search for one color in the image, returning a black and white result]

    Arguments:
        image {[Array]} -- [Image that you want to change]

    Keyword Arguments:
        color {list} -- [list that contains de RGB format of the image that you want] (default: {[0,0,255]})

    Returns:
        [Array] -- [black and white image ]
    """
    output = image.copy()
    for line in range(len(image)):
        for column in range(len(image[0])):
            distance = calc_distance(color,image[line][column])
            if distance <=150:
                output[line][column]=[255,255,255]
            else:
                output[line][column]=[0,0,0]
    return output

def resize_image(image,scale):
    """[Resize image]

    Arguments:
        image {[Array]} -- [description]
        scale {[Float]} -- [description]

    Returns:
        [Array] -- [Image resized]
    """
    scale_percent = scale # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    image_resized = resize(image.copy(), (width,height), interpolation = INTER_AREA)
    return image_resized

def get_max_point(image):
    """[Get the whitest point of and Black and white image]

    Arguments:
        image {[Array]} -- [Image]

    Returns:
        [array] -- [whitest point]
    """
    max_value= 0
    better_point= None
    for line in range(len(image)):
        for column in range(len(image[0])):
            if image[line][column]>max_value:
                max_value= image[line][column]
                better_point = [line,column]
    return better_point

def paint_square(image,position_x,position_y,square_size,color = [0,0,255]):
    output = image.copy()
    line = int(position_x-square_size/2)
    column = int(position_y-square_size/2)
    while line < position_x+square_size/2:
        column =int(position_y-square_size/2)
        while column < position_y+square_size/2:
            #if line>0 and column>0 and line<len(image)-1 and column<len(image[0])-1:
            output[line,column]=color
            column +=1
        line +=1
    return output

def paint_circle(image,position_x,position_y,size,color = [0,255,0]):
    """[Paint a cicle in a image]

    Arguments:
        image {[Array]} -- [Image]
        position_x {[int]} -- [point x of cicle center]
        position_y {[int]} -- [point y of cicle center]
        size {[float]} -- [circle size]

    Keyword Arguments:
        color {list} -- [description] (default: {[0,255,0]})

    Returns:
        [array] -- [image with circle]
    """
    angles = 360
    step = math.pi/angles *2
    output = image.copy()
    for i in range(angles):
        angle = i*step
        point_x = int(position_x+size*math.cos(angle))
        point_y = int(position_y+size*math.sin(angle))
        if point_x>1 and point_x<len(image)-1 and point_y>1 and point_y<len(image[0])-1:
            output[point_x][point_y]=color
            output[point_x+1][point_y]=color
            output[point_x-1][point_y]=color
            output[point_x][point_y-1]=color
            output[point_x][point_y+1]=color
    return output

#Getting the a reference image to compare ('placa.png')
color = [15,15,225] 
placa = imread('./Reference/am_placa.png',IMREAD_COLOR)
placa_red = one_color(placa,color)

#Getting the image that you want to find the reference
street = imread('./Images/05.jpg',IMREAD_COLOR)

#Resize it and get only the "red part" of the image
factor = 0.3
street_resized = resize_image(street,factor*100)
street_red = one_color(street_resized,color)
imshow('image',street_resized)
waitKey(0) 

#Difine parameters
n_of_matchs = 35  #Number of different reference images to be compared(each iteration the size of it is changed)
step = 100/n_of_matchs
results = []
max_match = 0 
better_scale = 0
for i in range(n_of_matchs):
    scale_percent =10+i*step
    #Form reference that will be compared
    compare = resize_image(placa_red,scale_percent)
    #Getting the match between the new reference and the image
    match=matchTemplate(street_red,compare,TM_CCOEFF_NORMED)

    #Compare results with previous
    if match.max()> max_match:
        max_match= match.max()
        better_scale = scale_percent

#Getting the best match and showing it
print('Better Scale: %.2f'%(better_scale))
compare = resize_image(placa_red,better_scale)
match=matchTemplate(street_red,compare,TM_CCOEFF_NORMED)
max_point = get_max_point(match)
max_point = [max_point[0]+len(compare)/2, max_point[1]+len(compare[0])/2 ]
print('Better match at point: ',max_point)

result_placa = paint_circle(street_resized,max_point[0],max_point[1],len(compare)/2)
imshow('Result',result_placa)
waitKey(0)

#Saving result
x_original = int(max_point[0]*1/factor)
y_original = int(max_point[1]*1/factor)
radius_original =len(compare)/2*1/factor
final_placa = street.copy()

final_placa = paint_circle(final_placa,x_original,y_original,radius_original)
final_placa = paint_circle(final_placa,x_original,y_original,radius_original+1)
final_placa = paint_circle(final_placa,x_original,y_original,radius_original-1)

imwrite('teste.jpg',final_placa)


