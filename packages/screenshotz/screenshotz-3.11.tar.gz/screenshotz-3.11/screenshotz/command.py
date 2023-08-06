import sys
from pathlib import Path
from time import sleep
from typing import List

import yaml

from .code import Screenshotter, crop_element, crop_inwards


def is_logged_in(driver, base_url):
    driver.get(base_url)
    for x in range(3):
        if base_url in driver.current_url:
            return True
        sleep(1.0)
    return False



def run_hook(shotter, hook_name):
    try:
        import hooks  # noqa
    except ImportError:
        print('skipping hook, no hooks module present.')
        return

    method = getattr(hooks, hook_name, None)

    if method:
        print(f'running hook: {hook_name}')
        method(shotter)

    else:
        print(f'skipping hook, no {hook_name} hook defined.')



def run(filename: str):
    p = Path(filename)

    if not p.exists():
        raise ValueError("config file does not exist")

    y = yaml.safe_load(p.read_text())
    print(f"screenshotz: loading file from {p.resolve()}")

    base_url = y["base_url"]
    page_width = y.get("page_width", None)
    page_height = y.get("page_height", None)
    s = Screenshotter(base_url)

    driver = s.driver

    if page_width or page_height:
        page_width = page_width or 800
        page_height = page_height or 800
        print(f"setting window size: ({page_width} x {page_height})")
        driver.set_window_size(page_width, page_height)

    if is_logged_in(driver, base_url):
        print("Already logged in")

        for page in y["pages"]:
            print("taking screenshot for page:")
            print(page)
            path = page.get("path", "/")
            driver.get(base_url + path)
            delay = page.get("delay", 1)
            delay_after = page.get("delay_after", 0)

            sleep(delay)

            fname = page.get("out")

            fullscreen_name = "screenshots/" + fname + ".fullscreen.png"

            #
            inwards = [page.get(x, 0) for x in "top bottom left right".split()]
            crops = [page.get(f"crop_{x}", 0) for x in "top bottom left right".split()]

            xpath = page.get("xpath")

            scroll_down = page.get("scroll_down")

            y_adjust = page.get("y_adjust", 0)

            if scroll_down:
                pix = int(scroll_down)
                print(f"scrolling down {pix} pixels")
                driver.execute_script(f"window.scrollTo(0, {pix})")
                sleep(0.5)
                scroll_y = driver.execute_script("return window.scrollY;")
                print(f"Scroll position: {scroll_y}")

            sleep(delay_after)
            run_hook(s, 'before_shot')
            s.do_shot(fullscreen_name)

            if xpath:
                e = driver.find_element_by_xpath(xpath)

                loc = e.location
                size = e.size

                x, y = loc["x"], loc["y"]
                w, h = size["width"], size["height"]

                y -= scroll_down

                if y_adjust:
                    print(f"Shifting screenshot y dimension by {y_adjust} px")
                    y += y_adjust
                dims = [x, y, w, h]
                print(f"Crop dimensions: {crops}")

                crop_element(fullscreen_name, "screenshots/" + fname, *dims, crops)

            else:
                crop_inwards(fullscreen_name, "screenshots/" + fname, *inwards, crops)

    else:
        print("Not logged in. Please log in.")

        try:
            sleep(300)
        except KeyboardInterrupt:
            print("saving cookies and quitting...")
    s.quit()


def do_command() -> None:  # pragma: no cover
    try:
        args = parse_args(sys.argv[1:])
        # print(args)
        run(args)
    except ValueError:
        # print("Invalid args, please specify exactly two numbers")
        status = 1
        raise
    else:
        status = 0
    sys.exit(status)


def parse_args(args: List[str]) -> str:
    if args:
        return args[0]
    else:
        print("Error:You must spcify a config file.")
        raise ValueError
