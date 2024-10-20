import cv2
import numpy as np
from pandas.core.interchange.from_dataframe import primitive_column_to_ndarray

print(cv2.getVersionString())
img = cv2.imread("../../../shot.png")
# for ele in np.ndenumerate(img):
#     print(ele)
# print(img)

black = np.zeros((200,200,3), np.uint8)
cv2.circle(black, (20,20),50,(255,255,255),3,cv2.LINE_AA)
cv2.putText(black, "Hello",(100,100),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2,cv2.LINE_AA)
gray = cv2.cvtColor(black, cv2.COLOR_BGR2GRAY)#颜色模式转化为灰度图
corners = cv2.goodFeaturesToTrack(gray, 500,0.1,10)
print(corners)
print(corners.shape)
for corner in corners:
    x, y = corner.ravel()
    cv2.circle(black, (int(x), int(y)), 3, (0,0,255), -1, cv2.LINE_AA)

cv2.imshow("black",black)
# print(b)
# g = img[:,:,1]
# r = img[:,:,2]
# cv2.imshow("blue",b) #获取整张图像的B通道
# cv2.imshow("green",g)#获取整张图像的G通道
# cv2.imshow("red",r)#获取整张图像的R通道

# grey = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
# cv2.imshow("灰度图",img[200:300,200:1000])
cv2.waitKey(0)