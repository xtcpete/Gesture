import cv2
import os
import numpy as np


def create_secondary_menu(selected_item, image_height, image_width, total = 10): # 创建二级菜单
    item_img = cv2.imread(os.path.join('data', selected_item+'.jpg'))
    secondary_img = np.zeros((image_height, image_width, 3), dtype=np.uint8)

    sub_total = int(total / 2)

    items_ = []
    for i in range(sub_total):
        temp = crete_sub_image(item_img, i, selected_item)
        items_.append(temp)

    items_up = np.concatenate(items_, axis=1)

    items_ = []
    for i in range(5, total):
        temp = crete_sub_image(item_img, i, selected_item)
        items_.append(temp)

    items_down = np.concatenate(items_, axis=1)

    items = np.concatenate([items_up, items_down], axis=0)

    secondary_img[:, :] = (255, 255, 255)
    h_, w_ = items.shape[:2]
    h = image_height
    items = cv2.resize(items, (image_width, h))
    secondary_img[image_height - h:, :image_width, :3] = items

    """cv2.imshow('secondary_img', secondary_img)
    cv2.waitKey(0)"""
    return secondary_img


def crete_sub_image(image, index, selected_item):
    h, w = image.shape[:2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = selected_item + " " + str(index + 1)
    textsize = cv2.getTextSize(text, font, 1, 2)[0]
    sub_height = h + textsize[1] + 20

    textX = int((image.shape[1] - textsize[0]) / 2)

    sub_image = np.zeros((sub_height, w, 3), dtype=np.uint8)
    sub_image[:, :] = (255, 255, 255)
    sub_image[sub_height - h:,:w,:3] = image
    cv2.putText(sub_image, text, (textX, textsize[1]), font, 1, (0, 0, 0), 2)
    return sub_image


create_secondary_menu(selected_item='chicken', image_height=720, image_width=1280)
