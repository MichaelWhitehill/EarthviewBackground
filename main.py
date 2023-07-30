import os
import json
import yaml
import subprocess
from image_library import Image_Library
from earthview_scraper import earthview_scraper



CONFIG_PATH = "config.yaml"

EATHVIEW_DATA_PATH_KEY = "earthview_data_path"
EARTHVIEW_CONFIG_PATH_KEY = "earthview_config_path"
MONITORS_KEY = "monitors"

WALLPAPER_CHANGER_PATH = r"wallpaper_changer\bin\Release\net7.0\publish\DesktopWallpaperSample.exe"

class BackgroundManager():

    def __init__(self) -> None:
        self.config_path = CONFIG_PATH
        self.load_config()

        if not os.path.isfile(self.config[EATHVIEW_DATA_PATH_KEY]):
            print("Earthview data is missing")
            print("Collecting Earthview data")
            locations = earthview_scraper.collect_all_locations()
            earthview_scraper.print_locations_to_file(locations, self.config[EATHVIEW_DATA_PATH_KEY])
        else:
            print("Earthview data is present")
        self.earthview_lib = Image_Library(self.config[EARTHVIEW_CONFIG_PATH_KEY], self.config[EATHVIEW_DATA_PATH_KEY])
        for monitor in self.config[MONITORS_KEY]:
            path = self.earthview_lib.next()
            self.change_background(monitor, path)
    
    def load_config(self) -> None:
        config_file_handler = open(self.config_path)
        self.config = yaml.safe_load(config_file_handler)
        config_file_handler.close()
        if None is self.config.get(MONITORS_KEY, None):
            self.config[MONITORS_KEY] = self.get_monitors()

    def save_config(self) -> None:
        os.remove(CONFIG_PATH)
        with open(CONFIG_PATH, 'w') as file:
            yaml.dump(self.config, file)
        self.earthview_lib.save_config()

    def get_monitors(self) -> list[str]:
        output = subprocess.Popen([WALLPAPER_CHANGER_PATH, "monitors"], stdout=subprocess.PIPE).communicate()[0].decode()
        output = output.strip("[]")
        monitors = output.split(",")
        return monitors

    def change_background(self, monitorId: str, bg_path: str) -> None:
        # TODO Check status
        p = subprocess.Popen([WALLPAPER_CHANGER_PATH, "set", monitorId, bg_path], stdout=subprocess.PIPE)
        status = p.wait()


def main():
    bm = BackgroundManager()
    bm.save_config()


if __name__ == "__main__":
    main()
