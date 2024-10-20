import cv2
import numpy as np

target = cv2.imread("./squre.jpg")
template = cv2.imread("./temp.jpg")

dup = target.copy()

target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
match = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
# locations = np.where(match)
# print(match.shape)

th, tw = template.shape[0:2]

locations = np.where(match >= 0.9)#一个元素
for pos in zip(*locations):
    y1,x1 = pos
    cv2.rectangle(dup,(x1,y1),(x1 + th, y1 + tw),(255,0,0),1)

cv2.imshow("sum",dup)
cv2.waitKey(0)