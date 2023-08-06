from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import Search_Tags
import platform
import os
import base64
import ast


if platform.system() == "Windows":
    driver_path = 'chrome_driver/chromedriver.exe'
elif platform.system() == "Darwin":
    driver_path = 'chrome_driver/chromedriver'


class Image:
    def __init__(self, link, source):
        self.link = link
        self.source = source
        self.type = None
        if source == "google":
            try:
                self.data = requests.get(self.link).content
            except requests.exceptions.InvalidSchema:
                self.data = base64.b64decode(self.link.split(",")[-1])
                self.type = self.link.split(",")[0].split("/")[-1].split(";")[0]
            if self.type is None:
                print("defaulted")
                self.type = "jpeg"
        elif source == "bing":
            self.data = requests.get(self.link).content
            self.type = os.path.splitext(self.link)[-1]

    def save(self, filename):
        with open(f"{filename}.{self.type}", "wb") as image_file:
            image_file.write(self.data)


def bing_search_image(search_term: str, number_of_images: int, *tags):
    """Returns a list of images from the search results from bing, supports Gifs and Pngs, you can find search tags in the Search_Tags.py"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    dr = webdriver.Chrome(
        driver_path,
        options=options,

    )
    dr.get(f"https://www.bing.com/images/search?q={search_term}{''.join(tags)}")
    soup = BeautifulSoup(dr.page_source, "html.parser")
    dr.close()
    image_list = soup.find_all("a", class_="iusc")
    return_images = []
    for picture in image_list[:number_of_images]:
        dictionary = picture.get("m")
        return_images.append(Image(ast.literal_eval(dictionary)["murl"], "bing"))

    return return_images


def google_search_image(search_term: str, number_of_images: int, *tags):
    """Returns a list of images from the search results from google, no Pngs or Gifs, still WIP, you can find search tags in the Search_Tags.py"""
    options = webdriver.ChromeOptions()
    options.add_argument('disable-infobars')
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--headless")

    dr = webdriver.Chrome(
        executable_path="chrome_driver/chromedriver",
        options=options,
    )
    dr.get(f"http://www.google.com/search?q={search_term}&tbm=isch{''.join(tags)}")
    soup = BeautifulSoup(dr.page_source, "html.parser")
    dr.close()
    images = soup.find_all("img", class_="rg_i Q4LuWd")
    return_images = []
    for picture in images[:number_of_images]:
        return_images.append(Image(picture.get("src"), "google"))

    return return_images


if __name__ == "__main__":
    # Here is just an example for you to try:
    images = bing_search_image("dog", 10, Search_Tags.Bing_Png)
    for image in images:
        image.save(f"{images.index(image)}")
