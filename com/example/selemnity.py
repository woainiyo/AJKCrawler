from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.select import Select

driver = webdriver.Edge(service=Service(r"E:\Dev\edgedriver_win64\msedgedriver.exe"))
driver.get("http://localhost:63342/Demo/com/HH.html?_ijt=osmat7ac3eadterdfb5cccqsod&_ij_reload=RELOAD_ON_SAVE")
man_window = driver.current_window_handle

driver.implicitly_wait(10)
print(driver.title)
s1 = Select(driver.find_element(By.CSS_SELECTOR, "#fw"))
s1.select_by_value("ningbo")
sleep(1)
s1.select_by_visible_text("wenzhou")
sleep(1)
s1.select_by_visible_text("hanzhou")

l1 = s1.all_selected_options
print(l1)
ac = ActionChains(driver)

while True:
    if input() == "1":
        print(driver.title)
    else:
        driver.switch_to.window(man_window)