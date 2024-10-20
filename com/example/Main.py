import math
from random import random, uniform, randint
from time import sleep
import pyautogui as pag
import numpy as np
import cv2
import requests
from PIL import Image
from PIL.ImageCms import Flags
from selenium import webdriver as wd
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from pytweening import easeInQuad, easeOutQuad, easeOutExpo, easeOutBack


#图像识别部分忽略透明部分，得到遮罩
def get_mask(target):
    alpha = target[:,:,3]
    mask = np.zeros(alpha.shape,np.uint8)
    for idx, v in np.ndenumerate(alpha):
        y, x = idx
        if v != 0:
            mask[y][x] = 255
    return mask

def get_slide_distance(img_target:str,img_template:str):
    target = cv2.imread(img_target)
    template = cv2.imread(img_template,cv2.IMREAD_UNCHANGED)
    mask = get_mask(template)
    template = cv2.cvtColor(template, cv2.COLOR_BGRA2GRAY)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    temp_height, temp_weight = template.shape[0:2]
    # template = template[temp_height - 96:-20, temp_weight - 95:-5]#对图像的裁剪，貌似不需要了
    # print("模板图像大小是",temp_height, temp_weight)
    match = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED,mask=mask)
    # # print(match)
    #
    # 画图方便调试
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
    # cv2.rectangle(target,max_loc,(max_loc[0] + temp_weight,max_loc[1] + temp_height),(255,255,255),2)
    # print("需要的距离是",max_loc[0] + 10)
    # cv2.imshow("template", template)
    # cv2.imshow("target", target)
    # cv2.waitKey(0)
    return max_loc[0] + 10



    #画图方便调试
    # cv2.rectangle(target,max_loc,(max_loc[0] + temp_weight,max_loc[1] + temp_height),(255,255,255),2)
    #假如要得到所有位置那么可以写循环得到
    # locations = np.where(match >= 0.9)
    # print(locations)
    # for pos in zip(*locations):
    #     y, x = pos
    #     cv2.rectangle(target, (x,y), (x+temp_weight,y+temp_height), (0,255,0), 2)

    # cv2.destroyAllWindows()

def download_image(url, save_pos):
    response = requests.get(url)
    with open(save_pos, 'wb') as f:
        f.write(response.content)
    print("图片下载成功！")

def init_img(path_img_template, path_img_target):
    target = Image.open(path_img_target, mode="r")
    target.thumbnail((258, 145))
    target.save(path_img_target, "png")
    template = Image.open(path_img_template, mode="r")
    template.thumbnail((56, 145))
    template.save(path_img_template, "png")
    print("图像大小比例调整完成")

def pag_drag(total_distance):
    total_distance += 5
    x, y= pag.locateCenterOnScreen(image=r"E:\Project\Python\Demo\com\example\res\button.png",confidence=0.5)
    print("滑动按钮在屏幕上的位置是",x, y)
    pag.moveTo(x, y, duration=1)
    pag.mouseDown(button='left')
    pag.moveRel(xOffset=total_distance * 1,yOffset=5,duration=5,tween=easeOutBack)
    pag.moveRel(xOffset=-5 * 1,yOffset=-5,duration=1.5,tween=easeInQuad)
    pag.mouseUp(button='left')


def slow_slide(total_distance, actor:ActionChains,slide_button):
    pag_drag(total_distance)#利用paAutoGui来滑动轨迹
    #一下代码是我尝试用selenium控制元素来实现但是由于对人的行为模仿不够到位导致一直被检测。
    # actor.click_and_hold(slide_button)
    # acceleration = 0.2
    # now_speed = 0
    # have_distance = 0
    # over_distance = 0
    # while have_distance < total_distance:
    #     now_speed = min(now_speed + acceleration, 10)
    #     move_distance = randint(1, max(int(now_speed),2))
    #     have_distance += move_distance
    #     actor.move_by_offset(xoffset=move_distance,yoffset=0).perform()
    #     acceleration += uniform(0.5,1)
    #     print("当前距离是",round(have_distance))
    #     # actor.pause(uniform(0.05, 0.2))
    #     if have_distance > total_distance:
    #         over_distance = total_distance - have_distance
    #         break
    # print("需要滑动",total_distance)
    # print("实际滑动了",have_distance)
    # print("超过了",abs(over_distance))
    #
    # if abs(over_distance) != 0:
    #     avg = round(over_distance / 3)
    #     actor.move_by_offset(xoffset=round(avg),yoffset=0).perform()
    #     actor.move_by_offset(xoffset=round(avg),yoffset=0).perform()
    #     actor.move_by_offset(xoffset=round(avg),yoffset=0).perform()
    # sleep(1)
    # actor.release().perform()

def open_and_slide(url:str):
    driver = wd.Edge(service=Service(r"E:\Lib\Download\edgedriver_win64\edgedriver_win64\msedgedriver.exe"));
    driver.implicitly_wait(10)
    driver.get(url)
    flag = False
    antibot = False
    window_list = driver.window_handles
    for handle in window_list:
        driver.switch_to.window(handle)
        if "访问验证-安居客" in driver.title:
            print("本次未能通过验证码")
            flag = True
            sleep(1)
            break
        if "请输入验证码" in driver.title:
            print("检测到新的验证页面,暂时无法处理")
            flag = True
            return
    if flag == False:
        return
    while flag is True:
        flag = False
        driver.get(url)
        #得到滑动按钮
        slide_button = driver.find_element(By.CSS_SELECTOR,".dvc-slider__handler")
        #得到目标图片
        url_img_temp = driver.find_element(By.CSS_SELECTOR,".dvc-captcha__puzzleImg").get_attribute("src")
        download_image(url_img_temp, r"E:\Project\Python\Demo\com\example\temp\template.png")
        url_img_target = driver.find_element(By.CSS_SELECTOR,".dvc-captcha__bgImg").get_attribute("src")
        download_image(url_img_target, r"E:\Project\Python\Demo\com\example\temp\target.png")
        #图像预处理
        init_img(r"E:\Project\Python\Demo\com\example\temp\template.png",r"E:\Project\Python\Demo\com\example\temp\target.png")
        #得到模板图片
        actor = ActionChains(driver)
        x_offset = get_slide_distance(r"E:\Project\Python\Demo\com\example\temp\target.png",r"E:\Project\Python\Demo\com\example\temp\template.png")
        print("需要滑动",x_offset)
        slow_slide(x_offset, actor, slide_button)
        sleep(3)
        window_list = driver.window_handles
        for handle in window_list:
            driver.switch_to.window(handle)
            if "访问验证-安居客" in driver.title:
                print("本次未能通过验证码")
                flag = True
                sleep(1)
        driver.refresh()
        # input()
    print("验证码已经通过")
if __name__ == "__main__":
    open_and_slide("https://www.anjuke.com/captcha-verify/?history=aHR0cHM6Ly93ZW56aG91LmFuanVrZS5jb20vc2FsZS9wMS8/ZnJvbT1Ib21lUGFnZV9Ub3BCYXI=&namespace=anjuke_ershoufang_pc&serialID=7ed82f7f21afa4b96c8007f578da07ff_996ac1003a5848d6953e4773cd3a051d&callback=shield&from=antispam")
