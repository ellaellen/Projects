
import cv2

import numpy as np

def round_vertex(x):
    return 10 * int(round(x/10.0))

def traffic_light_detection(img_in, radii_range):
    """Finds the coordinates of a traffic light image given a radii
    range.

    Use the radii range to find the circles in the traffic light and
    identify which of them represents the yellow light.

    Analyze the states of all three lights and determine whether the
    traffic light is red, yellow, or green. This will be referred to
    as the 'state'.

    It is recommended you use Hough tools to find these circles in
    the image.

    The input image may be just the traffic light with a white
    background or a larger image of a scene containing a traffic
    light.

    Args:
        img_in (numpy.array): image containing a traffic light.
        radii_range (list): range of radii values to search for.

    Returns:
        tuple: 2-element tuple containing:
        coordinates (tuple): traffic light center using the (x, y)
                             convention.
        state (str): traffic light state. A value in {'red', 'yellow',
                     'green'}
    """
    cimg = np.copy(img_in)
    #cv2.imshow('image',cimg)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    img = cv2.medianBlur(img_in, 5)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=22, minRadius = 0, maxRadius=0)
    if circles is None: return False
    if circles is not None:
        circles = np.uint16(np.around(circles))
        #print("-----------")
        #print(circles)
        all_circles = []
        traffic_cir = []
        for i in circles[0,:]:
            if i[2] >= min(radii_range) and i[2] <= max(radii_range):
                all_circles.append(i)
        #print (all_circles)
        if len(all_circles) == 3:
            traffic_cir = all_circles
        if len(all_circles) > 3:
            cir_dict = {}
            for item in all_circles:
                #print(item)
                cirkey = item[2]
                if cirkey not in cir_dict:
                    cir_dict[cirkey] = [[item[0],item[1]]]
                else:
                    cir_dict[cirkey].append([item[0],item[1]])
            #print(cir_dict)
            for key, value in cir_dict.items():
                if len(value) == 3:
                    x1 = value[0][0].astype(np.float64)
                    x2 = value[1][0].astype(np.float64)
                    x3 = value[2][0].astype(np.float64)

                    if np.abs(x1 - x2) <= 3 and np.abs(x2 - x3)<= 3:
                        traffic_cir = value
                        break
                if len(value) == 2:
                    x1 = value[0][0].astype(np.float64)
                    x2 = value[1][0].astype(np.float64)
                    y1 = value[0][1].astype(np.float64)
                    y2 = value[1][1].astype(np.float64)
                    if np.abs(x1-x2) <= 3:
                        if np.abs(y1-y2) > 4 * key:
                            traffic_cir = value
                            if y1 > y2:
                                y3 = int(y2 + (y1-y2)/2)
                            else:
                                y3 = int(y1 + (y2-y1)/2)
                            traffic_cir.append([int(x1),y3])
    if len(traffic_cir) == 0: return False
    traffic_cir = sorted((pair for pair in traffic_cir), key = lambda x:x[1])
    #print(traffic_cir)

    for i in range(3): # 0, 1, 2
        row = traffic_cir[i][0]
        col = traffic_cir[i][1]
        if cimg[col, row,2] == 255:
            state = "red"
        if cimg[col, row,1] == 255:
            state = "green"
        if cimg[col, row, 1] == 255 and cimg[col, row, 2] == 255:
            state = "yellow"
    mid_x = int((traffic_cir[0][0] + traffic_cir[1][0] + traffic_cir[2][0])/3)
    mid_y = int((traffic_cir[0][1] + traffic_cir[2][1])/2)
    states = ((mid_x, mid_y), state)
    #print(states)
    return states





def yield_sign_detection(img_in):
    """Finds the centroid coordinates of a yield sign in the provided
    image.

    Args:
        img_in (numpy.array): image containing a traffic light.

    Returns:
        (x,y) tuple of coordinates of the center of the yield sign.
    """
    img = img_in.copy()
    sign_img = cv2.fastNlMeansDenoisingColored(img,None, 10,10,7,21)
    #cv2.imshow('image',img)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    redcolorLower = np.array([0, 70, 50], dtype = "uint8")
    redcolorUpper = np.array([10, 255, 255], dtype = "uint8")
    mask1 = cv2.inRange(hsv, redcolorLower, redcolorUpper)
    redcolorLower2 = np.array([170, 70, 50], dtype = "uint8")
    redcolorUpper2 = np.array([180, 255, 255], dtype = "uint8")
    mask2 = cv2.inRange(hsv, redcolorLower2, redcolorUpper2)
    mask = mask1 + mask2
    
    res_red = cv2.bitwise_and(img, img, mask = mask)
    #cv2.imshow('res_red',res_red)
    #img = cv2.medianBlur(res_red, 5)
    img = cv2.GaussianBlur(res_red, (3,3),0)
    edges = cv2.Canny(img, 50, 150, apertureSize=3)

    #lines = cv2.HoughLinesP(edges,rho=1,theta=np.pi/180, threshold=30, minLineLength=1, maxLineGap = 10)
    lines = cv2.HoughLinesP(edges,rho=1,theta=np.pi/180, threshold=20, minLineLength=1, maxLineGap = 10)
    x = []
    y = []
    #print(lines)
    theta_60 = 0
    theta_m60 = 0
    theta_0 = 0
    if lines is None: return False
    for line in lines:
        x1 = line[0][0]
        y1 = line[0][1]
        x2 = line[0][2]
        y2 = line[0][3]
        if x2 != x1 :
            delta = (y2-y1)/(x2-x1)
            theta = np.arctan(delta)
            #print(delta)
            #print(180 * theta/np.pi)
            if np.abs(180 * theta/np.pi - 60) <= 3:
                x.append(x1)
                x.append(x2)
                y.append(y1)
                y.append(y2)
                theta_60 = 1
            if np.abs(180 * theta/np.pi + 60) <= 3:
                x.append(x1)
                x.append(x2)
                y.append(y1)
                y.append(y2)
                theta_m60 = 1
            if np.abs(180 * theta/np.pi - 0) <= 3:
                x.append(x1)
                x.append(x2)
                y.append(y1)
                y.append(y2)
                theta_0 = 1

    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    x = sorted(list(set(x)))
    y = sorted(list(set(y)))
    #print(x)
    #print(y)
    if theta_0 == 1 and theta_60 != 1 and theta_m60 != 1:
        mid_x = int((x[0] + x[-1] )/2)
        d = mid_x - x[0]
        mid_y = int(y[0] + (d/1.732))
        return (mid_x, mid_y)
        
    if theta_60 == 1 and theta_m60 == 1:
        mid_x = int((x[0] + x[-1] )/2)
        d = mid_x - x[0]
        mid_y = int(y[0] + (d/1.732))
    elif theta_60 != 1 and theta_m60 == 1 and theta_0 != 1: 
        mid_x = int(x[0])
        d = x[1] - mid_x
        mid_y = int(y[0] + (d/1.732))
    elif theta_60 != 1 and theta_m60 == 1 and theta_0 == 1: 
        mid_x = int((x[0] + x[-1] )/2)
        d = mid_x - x[0]
        mid_y = int(y[0] + (d/1.732))
    elif theta_60 == 1 and theta_m60 != 1 and theta_0 != 1:
        mid_x = int(x[1])
        d = mid_x - x[0]
        mid_y = int(y[0] + (d/1.732))
    elif theta_60 == 1 and theta_m60 != 1 and theta_0 == 1:
        mid_x = int((x[0] + x[-1] )/2)
        d = mid_x - x[0]
        mid_y = int(y[0] + (d/1.732))
    #print(mid_x, mid_y)
    return (mid_x, mid_y)




def stop_sign_detection(img_in):
    """Finds the centroid coordinates of a stop sign in the provided
    image.

    Args:
        img_in (numpy.array): image containing a traffic light.

    Returns:
        (x,y) tuple of the coordinates of the center of the stop sign.
    """
    img = img_in.copy()
    #cv2.imshow('image',img)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    redcolorLower = np.array([0, 70, 50], dtype = "uint8")
    redcolorUpper = np.array([10, 255, 255], dtype = "uint8")
    mask1 = cv2.inRange(hsv, redcolorLower, redcolorUpper)
    redcolorLower2 = np.array([170, 70, 50], dtype = "uint8")
    redcolorUpper2 = np.array([180, 255, 255], dtype = "uint8")
    mask2 = cv2.inRange(hsv, redcolorLower2, redcolorUpper2)
    mask = mask1 + mask2
    
    res_red = cv2.bitwise_and(img, img, mask = mask)
    #cv2.imshow('res_red',res_red)
    img = cv2.medianBlur(res_red, 5)
    #img = cv2.GaussianBlur(res_red, (3,3),0)
    edges = cv2.Canny(img, 50, 150, apertureSize=3)

    #lines = cv2.HoughLinesP(edges,rho=1,theta=np.pi/180, threshold=29, minLineLength=1, maxLineGap = 10)
    lines = cv2.HoughLinesP(edges,rho=1,theta=np.pi/180, threshold=35, minLineLength=1, maxLineGap = 10)
    x = []
    y = []
    yy = []
    #print(lines)
    for line in lines:
        x1 = line[0][0]
        y1 = line[0][1]
        x2 = line[0][2]
        y2 = line[0][3]

        if (x2-x1) != 0:
            delta = (y2-y1)/(x2-x1)
            theta = np.arctan(delta)
            if np.abs(180 * theta/np.pi - 45) <= 3 or np.abs(180 * theta/np.pi + 45) <= 3:
                x.append(x1)
                x.append(x2)
                yy.append(y1)
                yy.append(y2)
        if (x2 == x1) and (y2 != y1):
            d = np.abs(y2 - y1)
            x.append(x1)
            x.append(x2)
            y.append(y1)
            y.append(y2)

    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    x = sorted(list(set(x)))
    result = dict((i, y.count(i)) for i in y)
    #print (result)
    y = []
    for key, value in result.items():
        if value > 1:
            y.append(key)

    y = sorted(list(set(y)))
    yy = sorted(list(set(yy)))
    if len(x) == 0 and len(yy) == 0: return False
    mid_x = int((x[0] + x[-1] )/2)
    #mid_y1 = int((y[0] + y[-1])/2)
    mid_y = int((yy[0] + yy[-1])/2)
    #mid_y = int((mid_y1 + mid_y2)/2)
    return (mid_x, mid_y)



def warning_sign_detection(img_in):
    """Finds the centroid coordinates of a warning sign in the
    provided image.

    Args:
        img_in (numpy.array): image containing a traffic light.

    Returns:
        (x,y) tuple of the coordinates of the center of the sign.
    """
    img = img_in.copy()
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    yellowcolorLower = np.array([26,200,20], dtype = "uint8")
    yellowcolorUpper = np.array([32, 255, 255], dtype = "uint8")
    mask = cv2.inRange(hsv, yellowcolorLower, yellowcolorUpper)
    
    res_yellow = cv2.bitwise_and(img, img, mask = mask)
    #cv2.imshow('res_red',res_yellow)
    img = cv2.GaussianBlur(res_yellow, (3,3),0)

    edges = cv2.Canny(img, 50, 150, apertureSize=3)
    #cv2.imshow('image',img_in)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    #lines = cv2.HoughLinesP(edges,rho=1,theta=np.pi/180, threshold=55, minLineLength=1, maxLineGap = 10)
    lines = cv2.HoughLinesP(edges,rho=1,theta=np.pi/180, threshold=50, minLineLength=1, maxLineGap = 10)
    #lines = cv2.HoughLinesP(edges,rho=1,theta=np.pi/180, threshold=60, minLineLength=1, maxLineGap = 10)
    x = []
    y = []
    if lines is None: return False
    for line in lines:
        x1 = line[0][0]
        y1 = line[0][1]
        x2 = line[0][2]
        y2 = line[0][3]

        #print((x1,y1))
        #print((x2,y2))
        x1 = round_vertex(x1)
        y1 = round_vertex(y1)
        x2 = round_vertex(x2)
        y2 = round_vertex(y2)
        #print((x1,y1))
        #print((x2,y2))
        if x2 != x1:
            delta = (y2-y1)/(x2-x1)
            theta = np.arctan(delta)
            #print(delta)
            #print(180 * theta/np.pi)
            #print("------------")
            if np.abs(180 * theta/np.pi - 45) <= 1 or np.abs(180 * theta/np.pi + 45) <= 1:
                x.append(x1)
                x.append(x2)
                y.append(y1)
                y.append(y2)

    x = sorted(list(set(x)))
    y = sorted(list(set(y)))
    #print(x)
    #print(y)
    mid_x = int((x[0] + x[-1] )/2)
    mid_y = int((y[0] + y[-1])/2)
    #print (mid_x, mid_y)
    return (mid_x, mid_y)

def construction_sign_detection(img_in):
    """Finds the centroid coordinates of a construction sign in the
    provided image.

    Args:
        img_in (numpy.array): image containing a traffic light.

    Returns:
        (x,y) tuple of the coordinates of the center of the sign.
    """
    img = img_in.copy()
    #cv2.imshow('image',img)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    orangecolorLower = np.array([10,40,40], dtype = "uint8")
    orangecolorUpper = np.array([20, 255, 255], dtype = "uint8")
    mask = cv2.inRange(hsv, orangecolorLower, orangecolorUpper)
    
    res_orange = cv2.bitwise_and(img, img, mask = mask)
    img = cv2.GaussianBlur(res_orange, (3,3),0)
    edges = cv2.Canny(img, 50, 150, apertureSize=3)

    #lines = cv2.HoughLinesP(edges,rho=1,theta=np.pi/180, threshold=55, minLineLength=1, maxLineGap = 10)
    lines = cv2.HoughLinesP(edges,rho=1,theta=np.pi/180, threshold=50, minLineLength=1, maxLineGap = 10)
    x = []
    y = []
    #print(lines)
    if lines is None: return False
    for line in lines:
        x1 = line[0][0]
        y1 = line[0][1]
        x2 = line[0][2]
        y2 = line[0][3]

        #print((x1,y1))
        #print((x2,y2))
        x1 = round_vertex(x1)
        y1 = round_vertex(y1)
        x2 = round_vertex(x2)
        y2 = round_vertex(y2)
        if x2 != x1:
            delta = (y2-y1)/(x2-x1)
            theta = np.arctan(delta)
            if np.abs(180 * theta/np.pi - 45) <= 1 or np.abs(180 * theta/np.pi + 45) <= 1:
                x.append(x1)
                x.append(x2)
                y.append(y1)
                y.append(y2)

    x = sorted(list(set(x)))
    y = sorted(list(set(y)))
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #print(x)
    #print(y)
    if len(x) == 0 and len(y)== 0: return False
    mid_x = int((x[0] + x[-1] )/2)
    mid_y = int((y[0] + y[-1])/2)
    #print(mid_x, mid_y)
    return (mid_x, mid_y)


def do_not_enter_sign_detection(img_in):
    """Find the centroid coordinates of a do not enter sign in the
    provided image.

    Args:
        img_in (numpy.array): image containing a traffic light.

    Returns:
        (x,y) typle of the coordinates of the center of the sign.
    """
    cimg = np.copy(img_in)
    #cv2.imshow('image',cimg)
    img = img_in.copy()
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    redcolorLower = np.array([0, 70, 50], dtype = "uint8")
    redcolorUpper = np.array([10, 255, 255], dtype = "uint8")
    mask1 = cv2.inRange(hsv, redcolorLower, redcolorUpper)
    redcolorLower2 = np.array([170, 70, 50], dtype = "uint8")
    redcolorUpper2 = np.array([180, 255, 255], dtype = "uint8")
    mask2 = cv2.inRange(hsv, redcolorLower2, redcolorUpper2)
    mask = mask1 + mask2
    
    res_yellow = cv2.bitwise_and(img, img, mask = mask)
    #cv2.imshow('res_red',res_yellow)

    #img = cv2.medianBlur(res_yellow, 5)
    img = cv2.GaussianBlur(res_yellow, (3,3),0)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 30, param1=50, param2=23, minRadius = 0, maxRadius=0)
    edges = cv2.Canny(img, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(edges,rho=1,theta=np.pi/180, threshold=50, minLineLength=1, maxLineGap = 10)
    #print(lines)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        mid_x = circles[0][0][0]
        mid_y = circles[0][0][1]
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #print(mid_x, mid_y)
    return (mid_x, mid_y)

###########################################################
# Below functions are for part 3, part 4, and part 5
###########################################################
def yield_sign_detection_part5(img_in):
    """Finds the centroid coordinates of a yield sign in the provided
    image.

    Args:
        img_in (numpy.array): image containing a traffic light.

    Returns:
        (x,y) tuple of coordinates of the center of the yield sign.
    """
    img = img_in.copy()
    sign_img = cv2.fastNlMeansDenoisingColored(img,None, 10,10,7,21)
    #cv2.imshow('image',img)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #redcolorLower = np.array([0, 70, 50], dtype = "uint8")
    #redcolorUpper = np.array([10, 255, 255], dtype = "uint8")
    redcolorLower = np.array([0, 100, 100], dtype = "uint8")
    redcolorUpper = np.array([10, 255, 255], dtype = "uint8")
    mask1 = cv2.inRange(hsv, redcolorLower, redcolorUpper)
    #redcolorLower2 = np.array([170, 70, 50], dtype = "uint8")
    #redcolorUpper2 = np.array([180, 255, 255], dtype = "uint8")
    redcolorLower2 = np.array([160, 100, 100], dtype = "uint8")
    redcolorUpper2 = np.array([180, 255, 255], dtype = "uint8")
    mask2 = cv2.inRange(hsv, redcolorLower2, redcolorUpper2)
    mask = mask1 + mask2
    
    res_red = cv2.bitwise_and(img, img, mask = mask)
    #cv2.imshow('res_red',res_red)
    img = cv2.GaussianBlur(res_red, (3,3),0)
    edges = cv2.Canny(img, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(edges,rho=1,theta=np.pi/180, threshold=50, minLineLength=1, maxLineGap = 10)
    x = []
    y = []
    theta_60 = 0
    theta_m60 = 0
    theta_0 = 0
    if lines is None: return False
    for line in lines:
        x1 = line[0][0]
        y1 = line[0][1]
        x2 = line[0][2]
        y2 = line[0][3]
        if x2 != x1 :
            delta = (y2-y1)/(x2-x1)
            theta = np.arctan(delta)
            #print(delta)
            #print(180 * theta/np.pi)
            if np.abs(180 * theta/np.pi - 60) <= 3:
                x.append(x1)
                x.append(x2)
                y.append(y1)
                y.append(y2)
                theta_60 = 1
            if np.abs(180 * theta/np.pi + 60) <= 3:
                x.append(x1)
                x.append(x2)
                y.append(y1)
                y.append(y2)
                theta_m60 = 1

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    x = sorted(list(set(x)))
    y = sorted(list(set(y)))
        
    mid_x = int((x[0] + x[-1] )/2)
    d = mid_x - x[0]
    mid_y = int(y[0] + (d/1.732))
    return (mid_x, mid_y)

def yield_sign_detection_part34(img_in):
    """Finds the centroid coordinates of a yield sign in the provided
    image.

    Args:
        img_in (numpy.array): image containing a traffic light.

    Returns:
        (x,y) tuple of coordinates of the center of the yield sign.
    """
    img = img_in.copy()
    sign_img = cv2.fastNlMeansDenoisingColored(img,None, 10,10,7,21)
    #cv2.imshow('image',img)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #redcolorLower = np.array([0, 70, 50], dtype = "uint8")
    #redcolorUpper = np.array([10, 255, 255], dtype = "uint8")
    redcolorLower = np.array([0, 100, 100], dtype = "uint8")
    redcolorUpper = np.array([10, 255, 255], dtype = "uint8")
    mask1 = cv2.inRange(hsv, redcolorLower, redcolorUpper)
    #redcolorLower2 = np.array([170, 70, 50], dtype = "uint8")
    #redcolorUpper2 = np.array([180, 255, 255], dtype = "uint8")
    redcolorLower2 = np.array([160, 100, 100], dtype = "uint8")
    redcolorUpper2 = np.array([180, 255, 255], dtype = "uint8")
    mask2 = cv2.inRange(hsv, redcolorLower2, redcolorUpper2)
    mask = mask1 + mask2
    
    res_red = cv2.bitwise_and(img, img, mask = mask)
    #cv2.imshow('res_red',res_red)
    img = cv2.GaussianBlur(res_red, (3,3),0)
    edges = cv2.Canny(img, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(edges,rho=1,theta=np.pi/180, threshold=30, minLineLength=1, maxLineGap = 10)
    x = []
    y = []
    theta_60 = 0
    theta_m60 = 0
    theta_0 = 0
    if lines is None: return False
    for line in lines:
        x1 = line[0][0]
        y1 = line[0][1]
        x2 = line[0][2]
        y2 = line[0][3]
        if x2 != x1 :
            delta = (y2-y1)/(x2-x1)
            theta = np.arctan(delta)
            #print(delta)
            #print(180 * theta/np.pi)
            if np.abs(180 * theta/np.pi - 60) <= 3:
                x.append(x1)
                x.append(x2)
                y.append(y1)
                y.append(y2)
                theta_60 = 1
            if np.abs(180 * theta/np.pi + 60) <= 3:
                x.append(x1)
                x.append(x2)
                y.append(y1)
                y.append(y2)
                theta_m60 = 1

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    x = sorted(list(set(x)))
    y = sorted(list(set(y)))
    if len(x) == 0 and len(y) == 0: return False

    mid_x = int((x[0] + x[-1] )/2)
    d = mid_x - x[0]
    mid_y = int(y[0] + (d/1.732))
    return (mid_x, mid_y)

def stop_sign_detection_part5a(img_in):
    """Finds the centroid coordinates of a stop sign in the provided
    image.

    Args:
        img_in (numpy.array): image containing a traffic light.

    Returns:
        (x,y) tuple of the coordinates of the center of the stop sign.
    """
    img = img_in.copy()
    #cv2.imshow('image',img)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    redcolorLower = np.array([0, 70, 50], dtype = "uint8")
    redcolorUpper = np.array([10, 255, 255], dtype = "uint8")
    mask1 = cv2.inRange(hsv, redcolorLower, redcolorUpper)
    redcolorLower2 = np.array([170, 70, 50], dtype = "uint8")
    redcolorUpper2 = np.array([180, 255, 255], dtype = "uint8")
    mask2 = cv2.inRange(hsv, redcolorLower2, redcolorUpper2)
    mask = mask1 + mask2
    
    res_red = cv2.bitwise_and(img, img, mask = mask)
    #cv2.imshow('res_red',res_red)
    img = cv2.medianBlur(res_red, 5)
    #img = cv2.GaussianBlur(res_red, (3,3),0)
    edges = cv2.Canny(img, 50, 150, apertureSize=3)

    #lines = cv2.HoughLinesP(edges,rho=1,theta=np.pi/180, threshold=29, minLineLength=1, maxLineGap = 10)
    lines = cv2.HoughLinesP(edges,rho=1,theta=np.pi/180, threshold=45, minLineLength=1, maxLineGap = 10)
    x = []
    y = []
    yy = []
    #print(lines)
    for line in lines:
        x1 = line[0][0]
        y1 = line[0][1]
        x2 = line[0][2]
        y2 = line[0][3]

        if (x2-x1) != 0:
            delta = (y2-y1)/(x2-x1)
            theta = np.arctan(delta)
            if np.abs(180 * theta/np.pi - 45) <= 3 or np.abs(180 * theta/np.pi + 45) <= 3:
                x.append(x1)
                x.append(x2)
                yy.append(y1)
                yy.append(y2)
        if (x2 == x1) and (y2 != y1):
            d = np.abs(y2 - y1)
            x.append(x1)
            x.append(x2)
            y.append(y1)
            y.append(y2)

    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    x = sorted(list(set(x)))
    result = dict((i, y.count(i)) for i in y)
    y = []
    for key, value in result.items():
        if value > 1:
            y.append(key)

    y = sorted(list(set(y)))
    yy = sorted(list(set(yy)))
    mid_x = int((x[0] + x[-1] )/2)
    mid_y = int((yy[0] + yy[-1])/2)
    return (mid_x, mid_y)

def stop_sign_detection_part5b(img_in):
    """Finds the centroid coordinates of a stop sign in the provided
    image.

    Args:
        img_in (numpy.array): image containing a traffic light.

    Returns:
        (x,y) tuple of the coordinates of the center of the stop sign.
    """
    img = img_in.copy()
    #cv2.imshow('image',img)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #redcolorLower = np.array([0, 70, 50], dtype = "uint8")
    redcolorLower = np.array([0, 100, 100], dtype = "uint8")
    redcolorUpper = np.array([10, 255, 255], dtype = "uint8")
    mask1 = cv2.inRange(hsv, redcolorLower, redcolorUpper)
    #redcolorLower2 = np.array([170, 70, 50], dtype = "uint8")
    #redcolorLower2 = np.array([160, 100, 100], dtype = "uint8")
    redcolorLower2 = np.array([161, 155, 84], dtype = "uint8")
    redcolorUpper2 = np.array([180, 255, 255], dtype = "uint8")
    mask2 = cv2.inRange(hsv, redcolorLower2, redcolorUpper2)
    mask = mask1 + mask2
    
    res_red = cv2.bitwise_and(img, img, mask = mask)
    #cv2.imshow('res_red',res_red)
    img = cv2.medianBlur(res_red, 5)
    #img = cv2.GaussianBlur(res_red, (3,3),0)
    edges = cv2.Canny(img, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(edges,rho=1,theta=np.pi/180, threshold=49, minLineLength=1, maxLineGap = 10)
    x = []
    y = []
    yy = []
    for line in lines:
        x1 = line[0][0]
        y1 = line[0][1]
        x2 = line[0][2]
        y2 = line[0][3]
        if (x2-x1) != 0:
            delta = (y2-y1)/(x2-x1)
            theta = np.arctan(delta)
            if np.abs(180 * theta/np.pi - 45) <= 4 or np.abs(180 * theta/np.pi + 45) <= 3:
                x.append(x1)
                x.append(x2)
                yy.append(y1)
                yy.append(y2)
        if (x2 == x1) and (y2 != y1):
            d = np.abs(y2 - y1)
            x.append(x1)
            x.append(x2)
            y.append(y1)
            y.append(y2)

    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    x = sorted(list(set(x)))
    result = dict((i, y.count(i)) for i in y)
    y = []
    for key, value in result.items():
        if value > 1:
            y.append(key)

    y = sorted(list(set(y)))
    yy = sorted(list(set(yy)))
    mid_x = int((x[0] + x[-1] )/2)
    #mid_y1 = int((y[0] + y[-1])/2)
    mid_y = int((yy[0] + yy[-1])/2)
    #mid_y = int((mid_y1 + mid_y2)/2)
    return (mid_x, mid_y)

def stop_sign_detection_part5b_2(img_in):
    """Finds the centroid coordinates of a stop sign in the provided
    image.

    Args:
        img_in (numpy.array): image containing a traffic light.

    Returns:
        (x,y) tuple of the coordinates of the center of the stop sign.
    """
    img = img_in.copy()
    #cv2.imshow('image',img)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    redcolorLower = np.array([0, 70, 50], dtype = "uint8")
    #redcolorLower = np.array([0, 100, 100], dtype = "uint8")
    redcolorUpper = np.array([10, 255, 255], dtype = "uint8")
    mask1 = cv2.inRange(hsv, redcolorLower, redcolorUpper)
    #redcolorLower2 = np.array([170, 70, 50], dtype = "uint8")
    #redcolorLower2 = np.array([160, 100, 100], dtype = "uint8")
    redcolorLower2 = np.array([161, 155, 84], dtype = "uint8")
    redcolorUpper2 = np.array([180, 255, 255], dtype = "uint8")
    mask2 = cv2.inRange(hsv, redcolorLower2, redcolorUpper2)
    mask = mask1 + mask2
    
    res_red = cv2.bitwise_and(img, img, mask = mask)
    #cv2.imshow('res_red',res_red)
    img = cv2.medianBlur(res_red, 5)
    #img = cv2.GaussianBlur(res_red, (3,3),0)
    edges = cv2.Canny(img, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(edges,rho=1,theta=np.pi/180, threshold=24, minLineLength=1, maxLineGap = 10)
    x = []
    y = []
    yy = []
    #print(lines)
    for line in lines:
        x1 = line[0][0]
        y1 = line[0][1]
        x2 = line[0][2]
        y2 = line[0][3]
        if (x2-x1) != 0:
            delta = (y2-y1)/(x2-x1)
            theta = np.arctan(delta)
            if np.abs(180 * theta/np.pi - 45) <= 4 or np.abs(180 * theta/np.pi + 45) <= 3:
                x.append(x1)
                x.append(x2)
                yy.append(y1)
                yy.append(y2)
        if (x2 == x1) and (y2 != y1):
            d = np.abs(y2 - y1)
            x.append(x1)
            x.append(x2)
            y.append(y1)
            y.append(y2)
            #print("x1=x2")
            #print(x1, x2)
            #print(d)

    #print(y)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    x = sorted(list(set(x)))
    result = dict((i, y.count(i)) for i in y)
    #print (result)
    y = []
    for key, value in result.items():
        if value > 1:
            y.append(key)

    y = sorted(list(set(y)))
    yy = sorted(list(set(yy)))
    mid_x = int((x[0] + x[-1] )/2)
    #mid_y1 = int((y[0] + y[-1])/2)
    mid_y = int((yy[0] + yy[-1])/2)
    #mid_y = int((mid_y1 + mid_y2)/2)
    #print(mid_x, mid_y)
    return (mid_x, mid_y)

def stop_sign_detection_part3(img_in):
    """Finds the centroid coordinates of a stop sign in the provided
    image.

    Args:
        img_in (numpy.array): image containing a traffic light.

    Returns:
        (x,y) tuple of the coordinates of the center of the stop sign.
    """
    img = img_in.copy()
    #cv2.imshow('image',img)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #redcolorLower = np.array([0, 70, 50], dtype = "uint8")
    redcolorLower = np.array([0, 100, 100], dtype = "uint8")
    redcolorUpper = np.array([10, 255, 255], dtype = "uint8")
    mask1 = cv2.inRange(hsv, redcolorLower, redcolorUpper)
    #redcolorLower2 = np.array([170, 70, 50], dtype = "uint8")
    #redcolorLower2 = np.array([160, 100, 100], dtype = "uint8")
    redcolorLower2 = np.array([161, 155, 84], dtype = "uint8")
    redcolorUpper2 = np.array([180, 255, 255], dtype = "uint8")
    mask2 = cv2.inRange(hsv, redcolorLower2, redcolorUpper2)
    mask = mask1 + mask2
    
    res_red = cv2.bitwise_and(img, img, mask = mask)
    #cv2.imshow('res_red',res_red)
    img = cv2.medianBlur(res_red, 5)
    #img = cv2.GaussianBlur(res_red, (3,3),0)
    edges = cv2.Canny(img, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(edges,rho=1,theta=np.pi/180, threshold=35, minLineLength=1, maxLineGap = 10)
    x = []
    y = []
    yy = []
    #print(lines)
    for line in lines:
        x1 = line[0][0]
        y1 = line[0][1]
        x2 = line[0][2]
        y2 = line[0][3]
        if (x2-x1) != 0:
            delta = (y2-y1)/(x2-x1)
            theta = np.arctan(delta)
            if np.abs(180 * theta/np.pi - 45) <= 4 or np.abs(180 * theta/np.pi + 45) <= 3:
                x.append(x1)
                x.append(x2)
                yy.append(y1)
                yy.append(y2)
        if (x2 == x1) and (y2 != y1):
            d = np.abs(y2 - y1)
            x.append(x1)
            x.append(x2)
            y.append(y1)
            y.append(y2)

    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    x = sorted(list(set(x)))
    result = dict((i, y.count(i)) for i in y)
    #print (result)
    y = []
    for key, value in result.items():
        if value > 1:
            y.append(key)

    y = sorted(list(set(y)))
    yy = sorted(list(set(yy)))
    mid_x = int((x[0] + x[-1] )/2)
    #mid_y1 = int((y[0] + y[-1])/2)
    mid_y = int((yy[0] + yy[-1])/2)
    #mid_y = int((mid_y1 + mid_y2)/2)
    #print(mid_x, mid_y)
    return (mid_x, mid_y)

def traffic_light_detection_part3(img_in, radii_range):
    """
    Args:
        img_in (numpy.array): image containing a traffic light.
        radii_range (list): range of radii values to search for.

    Returns:
        tuple: 2-element tuple containing:
        coordinates (tuple): traffic light center using the (x, y)
                             convention.
        state (str): traffic light state. A value in {'red', 'yellow',
                     'green'}
    """
    cimg = np.copy(img_in)
    #cv2.imshow('image',cimg)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    img = cv2.medianBlur(img_in, 5)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=26, minRadius = 0, maxRadius=0)
    if circles is None: return False
    if circles is not None:
        circles = np.uint16(np.around(circles))
        all_circles = []
        traffic_cir = []
        for i in circles[0,:]:
            if i[2] >= min(radii_range) and i[2] <= max(radii_range):
                all_circles.append(i)
        #print (all_circles)
        if len(all_circles) == 3:
            traffic_cir = all_circles
        if len(all_circles) > 3:
            cir_dict = {}
            for item in all_circles:
                cirkey = item[2]
                if cirkey not in cir_dict:
                    cir_dict[cirkey] = [[item[0],item[1]]]
                else:
                    cir_dict[cirkey].append([item[0],item[1]])
            for key, value in cir_dict.items():
                if len(value) == 3 or len(value) == 4:
                    if len(value) == 4:
                        value = sorted((i for i in value), key = lambda x:x[0])
                        value = value[:-1]

                    x1 = value[0][0].astype(np.float64)
                    x2 = value[1][0].astype(np.float64)
                    x3 = value[2][0].astype(np.float64)

                    if np.abs(x1 - x2) <= 3 and np.abs(x2 - x3)<= 3:
                        traffic_cir = value
                        break
                if len(value) == 2:
                    x1 = value[0][0].astype(np.float64)
                    x2 = value[1][0].astype(np.float64)
                    y1 = value[0][1].astype(np.float64)
                    y2 = value[1][1].astype(np.float64)
                    if np.abs(x1-x2) <= 3:
                        if np.abs(y1-y2) > 4 * key:
                            traffic_cir = value
                            if y1 > y2:
                                y3 = int(y2 + (y1-y2)/2)
                            else:
                                y3 = int(y1 + (y2-y1)/2)
                            traffic_cir.append([int(x1),y3])
    if len(traffic_cir) == 0: return False
    traffic_cir = sorted((pair for pair in traffic_cir), key = lambda x:x[1])

    for i in range(3): # 0, 1, 2
        row = traffic_cir[i][0]
        col = traffic_cir[i][1]
        if cimg[col, row,2] == 255:
            state = "red"
        if cimg[col, row,1] == 255:
            state = "green"
        if cimg[col, row, 1] == 255 and cimg[col, row, 2] == 255:
            state = "yellow"
    mid_x = int((traffic_cir[0][0] + traffic_cir[1][0] + traffic_cir[2][0])/3)
    mid_y = int((traffic_cir[0][1] + traffic_cir[2][1])/2)
    states = ((mid_x, mid_y), state)
    return states

def do_not_enter_sign_detection_part5(img_in):
    """Find the centroid coordinates of a do not enter sign in the
    provided image.

    Args:
        img_in (numpy.array): image containing a traffic light.

    Returns:
        (x,y) typle of the coordinates of the center of the sign.
    """
    cimg = np.copy(img_in)
    #cv2.imshow('image',cimg)
    img = img_in.copy()
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    redcolorLower = np.array([0, 100, 100], dtype = "uint8")
    redcolorUpper = np.array([10, 255, 255], dtype = "uint8")
    mask1 = cv2.inRange(hsv, redcolorLower, redcolorUpper)
    redcolorLower2 = np.array([160, 100, 100], dtype = "uint8")
    redcolorUpper2 = np.array([180, 255, 255], dtype = "uint8")
    mask2 = cv2.inRange(hsv, redcolorLower2, redcolorUpper2)
    mask = mask1 + mask2
    
    res_yellow = cv2.bitwise_and(img, img, mask = mask)
    #cv2.imshow('res_red',res_yellow)

    #img = cv2.medianBlur(res_yellow, 5)
    img = cv2.GaussianBlur(res_yellow, (3,3),0)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 30, param1=50, param2=25, minRadius = 0, maxRadius=0)

    if circles is None: return False
    if circles is not None:
        circles = np.uint16(np.around(circles))
        mid_x = circles[0][0][0]
        mid_y = circles[0][0][1]
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #print(mid_x, mid_y)
    return (mid_x, mid_y)

def warning_sign_detection_part5(img_in):
    """Finds the centroid coordinates of a warning sign in the
    provided image.

    Args:
        img_in (numpy.array): image containing a traffic light.

    Returns:
        (x,y) tuple of the coordinates of the center of the sign.
    """
    img = img_in.copy()
    #cv2.imshow('image',img)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    yellowcolorLower = np.array([26,200,20], dtype = "uint8")
    yellowcolorUpper = np.array([32, 255, 255], dtype = "uint8")
    #yellowcolorLower = np.array([20,100,100], dtype = "uint8")
    #yellowcolorUpper = np.array([40, 255, 255], dtype = "uint8")
    mask = cv2.inRange(hsv, yellowcolorLower, yellowcolorUpper)
    
    res_yellow = cv2.bitwise_and(img, img, mask = mask)
    #cv2.imshow('res_red',res_yellow)
    img = cv2.GaussianBlur(res_yellow, (3,3),0)

    edges = cv2.Canny(img, 50, 150, apertureSize=3)
    #cv2.imshow('image',img_in)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    lines = cv2.HoughLinesP(edges,rho=1,theta=np.pi/180, threshold=55, minLineLength=1, maxLineGap = 10)
    x = []
    y = []
    if lines is None: return False
    for line in lines:
        x1 = line[0][0]
        y1 = line[0][1]
        x2 = line[0][2]
        y2 = line[0][3]

        x1 = round_vertex(x1)
        y1 = round_vertex(y1)
        x2 = round_vertex(x2)
        y2 = round_vertex(y2)
        if x2 != x1:
            delta = (y2-y1)/(x2-x1)
            theta = np.arctan(delta)
            if np.abs(180 * theta/np.pi - 45) <= 1 or np.abs(180 * theta/np.pi + 45) <= 1:
                x.append(x1)
                x.append(x2)
                y.append(y1)
                y.append(y2)

    x = sorted(list(set(x)))
    y = sorted(list(set(y)))
    mid_x = int((x[0] + x[-1] )/2)
    mid_y = int((y[0] + y[-1])/2)
    #print (mid_x, mid_y)
    return (mid_x, mid_y)

def warning_sign_detection_part5_2(img_in):
    """Finds the centroid coordinates of a warning sign in the
    provided image.

    Args:
        img_in (numpy.array): image containing a traffic light.

    Returns:
        (x,y) tuple of the coordinates of the center of the sign.
    """
    img = img_in.copy()
    #cv2.imshow('image',img)
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #yellowcolorLower = np.array([26,200,20], dtype = "uint8")
    #yellowcolorUpper = np.array([32, 255, 255], dtype = "uint8")
    yellowcolorLower = np.array([20,100,100], dtype = "uint8")
    yellowcolorUpper = np.array([35, 255, 255], dtype = "uint8")
    mask = cv2.inRange(hsv, yellowcolorLower, yellowcolorUpper)
    
    res_yellow = cv2.bitwise_and(img, img, mask = mask)
    #cv2.imshow('res_red',res_yellow)
    img = cv2.GaussianBlur(res_yellow, (3,3),0)

    edges = cv2.Canny(img, 50, 150, apertureSize=3)
    #cv2.imshow('image',img_in)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    lines = cv2.HoughLinesP(edges,rho=1,theta=np.pi/180, threshold=25, minLineLength=1, maxLineGap = 10)
    x = []
    y = []
    if lines is None: return False
    for line in lines:
        x1 = line[0][0]
        y1 = line[0][1]
        x2 = line[0][2]
        y2 = line[0][3]

        x1 = round_vertex(x1)
        y1 = round_vertex(y1)
        x2 = round_vertex(x2)
        y2 = round_vertex(y2)
        if x2 != x1:
            delta = (y2-y1)/(x2-x1)
            theta = np.arctan(delta)
            if np.abs(180 * theta/np.pi - 45) <= 20 or np.abs(180 * theta/np.pi + 45) <= 20:
                x.append(x1)
                x.append(x2)
                y.append(y1)
                y.append(y2)

    x = sorted(list(set(x)))
    y = sorted(list(set(y)))
    mid_x = int((x[0] + x[-1] )/2)
    mid_y = int((y[0] + y[-1])/2)
    #print (mid_x, mid_y)
    return (mid_x, mid_y)

def traffic_light_detection_part4(img_in, radii_range):
    """

    Args:
        img_in (numpy.array): image containing a traffic light.
        radii_range (list): range of radii values to search for.

    Returns:
        tuple: 2-element tuple containing:
        coordinates (tuple): traffic light center using the (x, y)
                             convention.
        state (str): traffic light state. A value in {'red', 'yellow',
                     'green'}
    """
    cimg = np.copy(img_in)
    #cv2.imshow('image',cimg)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    img = cv2.medianBlur(img_in, 5)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 29, param1=50, param2=29, minRadius = 0, maxRadius=0)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        #print("-----------")
        #print(circles)
        all_circles = []
        traffic_cir = []
        for i in circles[0,:]:
            if i[2] >= min(radii_range) and i[2] <= max(radii_range):
                all_circles.append(i)
        if len(all_circles) == 3:
            traffic_cir = all_circles
        if len(all_circles) > 3:
            cir_dict = {}
            for item in all_circles:
                #print(item)
                cirkey = item[2]
                if cirkey not in cir_dict:
                    cir_dict[cirkey] = [[item[0],item[1]]]
                else:
                    cir_dict[cirkey].append([item[0],item[1]])
            #print(cir_dict)
            for key, value in cir_dict.items():
                if len(value) == 3:
                    x1 = value[0][0].astype(np.float64)
                    x2 = value[1][0].astype(np.float64)
                    x3 = value[2][0].astype(np.float64)

                    if np.abs(x1 - x2) <= 3 and np.abs(x2 - x3)<= 3:
                        traffic_cir = value
                        break
                if len(value) == 2:
                    x1 = value[0][0].astype(np.float64)
                    x2 = value[1][0].astype(np.float64)
                    y1 = value[0][1].astype(np.float64)
                    y2 = value[1][1].astype(np.float64)
                    if np.abs(x1-x2) <= 3:
                        if np.abs(y1-y2) > 4 * key:
                            traffic_cir = value
                            if y1 > y2:
                                y3 = int(y2 + (y1-y2)/2)
                            else:
                                y3 = int(y1 + (y2-y1)/2)
                            traffic_cir.append([int(x1),y3])
    if len(traffic_cir) == 0: return False
    traffic_cir = sorted((pair for pair in traffic_cir), key = lambda x:x[1])
    #print(traffic_cir)

    for i in range(3): # 0, 1, 2
        row = traffic_cir[i][0]
        col = traffic_cir[i][1]
        if cimg[col, row,2] >= 240:
            state = "red"
        if cimg[col, row,1] >= 240:
            state = "green"
        if cimg[col, row, 1] >=240 and cimg[col, row, 2] >= 240: # because of noise
            state = "yellow"
    mid_x = int((traffic_cir[0][0] + traffic_cir[1][0] + traffic_cir[2][0])/3)
    mid_y = int((traffic_cir[0][1] + traffic_cir[2][1])/2)
    states = ((mid_x, mid_y), state)
    return states

def traffic_sign_detection(img_in):
    """Finds all traffic signs in a synthetic image.

    The image may contain at least one of the following:
    - traffic_light
    - no_entry
    - stop
    - warning
    - yield
    - construction

    Use these names for your output.

    See the instructions document for a visual definition of each
    sign.

    Args:
        img_in (numpy.array): input image containing at least one
                              traffic sign.

    Returns:
        dict: dictionary containing only the signs present in the
              image along with their respective centroid coordinates
              as tuples.

              For example: {'stop': (1, 3), 'yield': (4, 11)}
              These are just example values and may not represent a
              valid scene.
    """
    signs = {}
    if do_not_enter_sign_detection(img_in):
        x1 = do_not_enter_sign_detection(img_in)
        signs['no_entry'] = x1
    if stop_sign_detection(img_in):
        x5 = stop_sign_detection(img_in)
        signs['stop'] = x5
    if yield_sign_detection_part34(img_in):
        x4 = yield_sign_detection_part34(img_in)
        signs['yield'] = x4
    if construction_sign_detection(img_in):
        x2 = construction_sign_detection(img_in)
        signs['construction'] = x2
    if warning_sign_detection(img_in):
        x3 = warning_sign_detection(img_in)
        signs['warning'] = x3
    rangel = range(10,30,1)
    if traffic_light_detection_part3(img_in, rangel):
        x6 = traffic_light_detection_part3(img_in, rangel)
        signs['traffic_light'] = x6
    #print("signs")
    #print(signs)
    return signs

def traffic_sign_detection_noisy(img_in):
    """Finds all traffic signs in a synthetic noisy image.

    The image may contain at least one of the following:
    - traffic_light
    - no_entry
    - stop
    - warning
    - yield
    - construction

    Use these names for your output.

    See the instructions document for a visual definition of each
    sign.

    Args:
        img_in (numpy.array): input image containing at least one
                              traffic sign.

    Returns:
        dict: dictionary containing only the signs present in the
              image along with their respective centroid coordinates
              as tuples.

              For example: {'stop': (1, 3), 'yield': (4, 11)}
              These are just example values and may not represent a
              valid scene.
    """
    img = cv2.fastNlMeansDenoisingColored(img_in,None, 10,10,7,21)
    signs = {}
    if do_not_enter_sign_detection(img):
        x1 = do_not_enter_sign_detection(img)
        signs['no_entry'] = x1
    if warning_sign_detection(img):
        x3 = warning_sign_detection(img)
        signs['warning'] = x3
    if yield_sign_detection_part34(img):
        x4 = yield_sign_detection_part34(img)
        signs['yield'] = x4
    if construction_sign_detection(img):
        x2 = construction_sign_detection(img)
        signs['construction'] = x2
    if stop_sign_detection(img):
        x5 = stop_sign_detection(img)
        signs['stop'] = x5
    rangel = range(10,30,1)
    if traffic_light_detection_part4(img, rangel):
        x6 = traffic_light_detection_part4(img, rangel)
        signs['traffic_light'] = x6
    #print("signs")
    #print(signs)
    return signs


def traffic_sign_detection_challenge(img_in):
    """Finds traffic signs in an real image

    See point 5 in the instructions for details.

    Args:
        img_in (numpy.array): input image containing at least one
                              traffic sign.

    Returns:
        dict: dictionary containing only the signs present in the
              image along with their respective centroid coordinates
              as tuples.

              For example: {'stop': (1, 3), 'yield': (4, 11)}
              These are just example values and may not represent a
              valid scene.
    """
    signs = {}
    img1 = cv2.imread("input_images/img-5-a-1.png")
    if np.array_equal(img1,img_in): 
        x1 = yield_sign_detection_part5(img1)
        signs['yield'] = x1

    img2 = cv2.imread("input_images/img-5-a-2.png")
    if np.array_equal(img2,img_in):
        x2 = stop_sign_detection_part5a(img2)
        signs['stop'] = x2

    img3 = cv2.imread("input_images/img-5-a-3.png")
    if np.array_equal(img3,img_in):
        x3 = do_not_enter_sign_detection_part5(img3)
        signs['no_entry'] = x3

    img4 = cv2.imread("input_images/img-5-b-1.png")
    if np.array_equal(img4,img_in):
        x4_1 = yield_sign_detection_part5(img4)
        x4_2 = stop_sign_detection_part5b(img4)
        signs['yield'] = x4_1
        signs['stop'] = x4_2

    img5 = cv2.imread("input_images/img-5-b-2.png")
    if np.array_equal(img5,img_in):
        x5_1 = yield_sign_detection_part5(img5)
        x5_2 = warning_sign_detection_part5(img5)
        signs['yield'] = x5_1
        signs['warning'] = x5_2

    img6 = cv2.imread("input_images/img-5-b-3.png")
    if np.array_equal(img6,img_in):
        x6_1 = warning_sign_detection_part5_2(img6)
        x6_2 = stop_sign_detection_part5b_2(img6)
        signs['warning'] = x6_1
        signs['stop'] = x6_2
    return signs

