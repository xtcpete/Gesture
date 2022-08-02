import numpy as np
import mediapipe as mp
import cv2
from hand_feature import *
from secondary_menu import *

if __name__ == '__main__':
    img = cv2.imread('data/menu.jpg')
    image_height, image_width, c = np.shape(img)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, image_width + 500)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, image_height + 500)
    # 定义手 检测对象
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils
    labels = ['', 'Detected', 'Selecting', 'Cancel', 'Confirmed']
    gesture = 0
    path = []
    items = ['Steak', 'Seafood', 'Bread', 'Chicken'] #菜单上的食品
    selected_item = None
    selected = None
    count = 0
    secondary = False

    while True:

        if secondary:
            img = create_secondary_menu(selected_item, image_height, image_width)
        else:
            img = cv2.imread('data/menu.jpg')
        # 读取一帧图像
        success, _ = cap.read()
        _ = cv2.flip(_, 1)
        if not success:
            continue

        # 转换为RGB
        imgRGB = cv2.cvtColor(_, cv2.COLOR_BGR2RGB)

        # 得到检测结果
        results = hands.process(imgRGB)

        if len(path) > 0:
            points = np.array(path)
            points = points.reshape((-1, 1, 2))
            cv2.polylines(img, [points], False, (0, 255, 255), 8)

        if selected_item != None and not secondary and gesture ==2:
            cv2.putText(img, 'Your selected item is %s' % (selected_item), (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1,
                        cv2.LINE_AA)
        elif selected != None and gesture == 2:
            cv2.putText(img, 'Your selected item is %s' % (selected), (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 1,
                        cv2.LINE_AA)
        elif selected != None and gesture == 4:
            cv2.putText(img, 'Thank you for purchasing %s' % (selected), (30, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]

            mpDraw.draw_landmarks(img, hand, mpHands.HAND_CONNECTIONS)

            # 采集所有关键点的坐标
            list_lms = []
            for i in range(21):
                pos_x = hand.landmark[i].x * image_width
                pos_y = hand.landmark[i].y * image_height
                list_lms.append([int(pos_x), int(pos_y)])

            # 构造凸包点
            list_lms = np.array(list_lms, dtype=np.int32)
            hull_index = [0, 1, 2, 3, 6, 10, 14, 19, 18, 17, 10]

            # 不需要手掌提示的话可以备注掉
            hull = cv2.convexHull(list_lms[hull_index, :])
            # 绘制凸包
            #cv2.polylines(img, [hull], True, (0, 255, 0), 2)

            # 查找外部的点数
            n_fig = -1
            ll = [4, 8, 12, 16, 20]
            up_fingers = []

            for i in ll:
                pt = (int(list_lms[i][0]), int(list_lms[i][1]))
                dist = cv2.pointPolygonTest(hull, pt, False)
                if dist < 1:
                    up_fingers.append(i)

            # print(up_fingers)
            # print(list_lms)
            # print(np.shape(list_lms))
            gesture_ = get_gesture(up_fingers, list_lms)

            if gesture_ == 1:
                count += 1
                if count > 10:
                    gesture = 1
                    count = 0
            elif gesture_ == 2:
                count += 1
                if count > 10:
                    gesture = 2
                    count = 0
            elif gesture_ == 3:
                count += 1
                if count > 10:
                    gesture = 3
                    count = 0
            elif gesture_ == 4:
                count += 1
                if count > 10:
                    gesture = 4
                    count = 0
            else:
                if gesture == 2:
                    gesture = gesture
                else:
                    gesture = 0

            label = labels[gesture]

            # 不需要标识识别到的手势，注释掉就行
            cv2.putText(img, ' %s' % (label), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)

            if gesture == 1:
                pos_x = hand.landmark[8].x * image_width
                pos_y = hand.landmark[8].y * image_height
                # 画点
                cv2.circle(img, (int(pos_x), int(pos_y)), 8, (0, 255, 255), -1)
                if not secondary:
                    selected_item = None
                path = []

            elif gesture == 2:
                pos_x = hand.landmark[8].x * image_width
                pos_y = hand.landmark[8].y * image_height
                path.append((int(pos_x), int(pos_y)))
                points = np.array(path)
                points = points.reshape((-1, 1, 2))
                cv2.polylines(img, [points], False, (0,255,255), 8)
                if not secondary:
                    selected_item = None

                if not secondary:
                    index = get_item(path, image_width, image_height)
                    selected_item = items[index]
                    cv2.putText(img, 'Your selected item is %s' % (selected_item), (30, 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
                else:
                    index = get_item(path, image_width, image_height, total=10,secondary=True)
                    selected = selected_item + " " + str(index + 1)
                    cv2.putText(img, 'Your selected item is %s' % (selected), (30, 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)


            elif gesture == 3:
                path = []
                selected_item = None
                selected = None
                secondary = False

            elif gesture == 4:
                if not secondary:
                    selected = selected
                    secondary = True
                    path = []
                if selected != None and secondary:
                        cv2.putText(img, 'Thank you for purchasing %s' % (selected), (30, 90),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
            elif gesture == 0:
                path = []
                selected = None
        cv2.imshow("hands", img)

        key = cv2.waitKey(1) & 0xFF

        # 按键 "q" 退出
        if key == ord('q'):
            break
    cap.release()