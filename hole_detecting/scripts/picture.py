import cv2
import numpy as np
order = {'left': 0, 'right': 1, 'up': 2, 'down': 3, 'stay': 4}


# 图像处理
def canny(picture):
    blur = cv2.GaussianBlur(picture, (3, 3), 0)
    output = cv2.Canny(blur, 50, 150)
    return output


def dilate(picture):
    # 边缘膨胀
    g = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
    output = cv2.dilate(picture, g)
    return output


# 计算原图中点
def center():
    wid = src.shape[1] / 2
    hei = src.shape[0] / 2
    return wid, hei


# 判断矩形
def judge_rectangle(picture):
    cnt = cv2.findContours(picture, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = cnt[0]
    output = np.ones(src.shape, np.uint8)*255
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.01*peri, True)
        if len(approx) == 4:
            cv2.drawContours(output, c, -1, (0, 255, 0))
            M = cv2.moments(output)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
    return output


def command():
    if cX < width:
        publish(order['right'])
    elif cX > width:
        publish(order['left'])
    else:
        publish(order['stay'])
    if cY < height:
        publish(order['up'])
    elif cY > height:
        publish(order['down'])
    else:
        publish(order['stay'])


def publish():
    pass


# 主函数
src = cv2.imread('hole1.jpg', 0)
edge = canny(src)
dilate = dilate(edge)
final = judge_rectangle(dilate)
width, height = center()
print(cX, cY)
print(width, height)







