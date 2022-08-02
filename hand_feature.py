import numpy as np


def get_angle(v1,v2):
    angle = np.dot(v1,v2)/(np.sqrt(np.sum(v1*v1))*np.sqrt(np.sum(v2*v2)))
    angle = np.arccos(angle)/3.14*180
    
    return angle
    
    
def get_gesture(up_fingers, list_lms): # 1 = 识别手指， 2 = 开始选择，记录轨迹， 3 = 取消， 4 = 确认
    
    if len(up_fingers) <= 2 and 8 in up_fingers and 12 not in up_fingers:
        v1 = list_lms[8] - list_lms[7]
        v2 = list_lms[6] - list_lms[7]
        angle = get_angle(v1, v2)

        if angle > 150:
            gesture = 1
        else:
            gesture = 0

    elif len(up_fingers) <= 2 and 4 in up_fingers:
        v1 = list_lms[2] - list_lms[3]
        v2 = list_lms[4] - list_lms[3]
        angle = get_angle(v1, v2)
        if angle > 150:
            gesture = 4
        elif 8 in up_fingers and angle < 150:
            gesture = 1
        else:
            gesture = 0

    elif len(up_fingers) < 4 and 8 in up_fingers and 12 in up_fingers:
        v1 = list_lms[8]
        v2 = list_lms[12]
        dist = np.linalg.norm(v1-v2)

        v3 = list_lms[8] - list_lms[7]
        v4 = list_lms[6] - list_lms[7]
        angle = get_angle(v3, v4)

        if angle > 150 and dist < 60:
            gesture = 2
        else:
            gesture = 0
    
    elif len(up_fingers) == 5:
        v1 = list_lms[8]
        v2 = list_lms[12]
        dist = np.linalg.norm(v1 - v2)
        if dist > 60:
            gesture = 3
        else:
            gesture = 2
    
    else:
        gesture = 0
        
    return gesture
       
    
def get_item(path, width, height, total=4, height_percent = 0.85, secondary = False):
    """
    :param path:  all points for selecting gesture
    :param width: width of menu image
    :param height: height of menu image
    :return: index of the item
    """
    idxs = []
    for point in path:
        x = point[0]
        y = point[1]
        if not secondary:
            item_width = int(width/total)
            item_height = int(height*height_percent)
            index = None
            if y < item_height:
                for i in range(1,total+1):
                    if x <= item_width*i:
                        index = i - 1
                        idxs.append(index)
                        break
            else:
                index = None
        else:
            item_width = int(width / int(total/2))
            item_height = int(height / 2)
            index = None
            if y < item_height:
                for i in range(1, int(total/2) + 1):
                    if x <= item_width * i:
                        index = i - 1
                        idxs.append(index)
                        break
            else:
                for i in range(1, int(total/2) + 1):
                    if x <= item_width * i:
                        index = i - 1
                        idxs.append(index+5)
                        break

    item = max(set(idxs), key=idxs.count)

    return item