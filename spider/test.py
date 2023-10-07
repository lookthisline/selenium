# driver.get(url)
# print(driver.page_source)

# xpath_str = "/html/body/div[@class='flex-img auto mt']/div[@class='item']/a[@class='img']/img[@class='lazy']"

# res = driver.find_element(By.XPATH, "//*").get_attribute("innerHTML") # 获取整个html
# res = driver.find_element(
#     By.XPATH, xpath_str).get_attribute("src")  # 获取获取element的属性
# time.sleep(1)
# images = driver.find_elements(
#     By.XPATH, xpath_str)  # 获取获取element的属性
# for image in images:
#     # print(image.get_attribute("innerHTML"))
#     print(image.get_attribute("data-original"))
