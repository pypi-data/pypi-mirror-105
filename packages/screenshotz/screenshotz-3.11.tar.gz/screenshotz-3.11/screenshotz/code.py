import pickle
from pathlib import Path
from time import sleep

from PIL import Image
from selenium import webdriver


class Screenshotter(object):
    def __init__(
        self,
        base_url
    ):
        self.base_url = base_url
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--user-data-dir=chrome-data")
        self.driver = webdriver.Chrome(options=chrome_options)

    def do_shot(self, filename):
        d = Path("screenshots")
        d.mkdir(exist_ok=True)
        self.driver.save_screenshot(filename)

    def quit(self):
        self.driver.quit()


def crop_inwards(in_name, out_name, top, bottom, left, right, crops):
    img = Image.open(in_name)
    width, height = img.size

    cropped = img.crop((left * 2, top * 2, width - (right * 2), height - (bottom * 2)))
    cropped.save(out_name)


def crop_element(in_name, out_name, left, top, w, h, crops):
    img = Image.open(in_name)
    print(locals())

    t, b, l, r = crops

    cropped = img.crop(
        ((left + l) * 2, (top + t) * 2, (left + w - r) * 2, (top + h - b) * 2)
    )
    cropped.save(out_name)

