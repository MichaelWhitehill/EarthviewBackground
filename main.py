import os
import time
import yaml
from image_libraries.image_library import ImageLibrary
from earthview_scraper import earthview_scraper
from wallpaper_changer.idesktop import IDesktopWallpaper

EARTHVIEW_CONFIG_KEY = "earthview_config"
MONITORS_KEY = "monitors"

class BackgroundManager():

    def __init__(self) -> None:
        self.config_path = os.path.join(os.getenv("LOCALAPPDATA"), "bg_changer", "config.yml")
        self.desktop = IDesktopWallpaper.CoCreateInstance()
        self.earthview_lib = None
        self.load_config()
        self.earthview_lib = ImageLibrary(self.config.get(EARTHVIEW_CONFIG_KEY, {}))

    
    def load_config(self) -> None:
        if not os.path.isfile(self.config_path):
            self.create_config()
        config_file_handler = open(self.config_path)
        self.config = yaml.safe_load(config_file_handler)
        config_file_handler.close()
        if None is self.config.get(MONITORS_KEY, None):
            self.config[MONITORS_KEY] = self.get_monitors()

    def create_config(self) -> None:
        self.config = {}
        self.config[EARTHVIEW_CONFIG_KEY] = None
        if not os.path.isdir(os.path.join(os.getenv("LOCALAPPDATA"), "bg_changer")):
            os.mkdir(os.path.join(os.getenv("LOCALAPPDATA"), "bg_changer"))
        self.save_config()
        

    def save_config(self) -> None:
        if None is not self.earthview_lib:
            self.config[EARTHVIEW_CONFIG_KEY] = self.earthview_lib.get_config()
        else:
            self.config[EARTHVIEW_CONFIG_KEY] = {}
        if os.path.isfile(self.config_path):
            os.remove(self.config_path)
        with open(self.config_path, 'w') as file:
            yaml.dump(self.config, file)

    def get_monitors(self) -> list[str]:
        mon_count = self.desktop.GetMonitorDevicePathCount()
        monitors = []
        for i in range(0, mon_count):
            if self.desktop.GetMonitorDevicePathAt(i) == "":
                continue
            monitors.append(self.desktop.GetMonitorDevicePathAt(i))
        return monitors

    def cycle_monitors(self):
        for monitor in self.config[MONITORS_KEY]:
            background =  self.earthview_lib.next()
            print(f"mon: {monitor} bg: {background}")
            self.change_background(monitor, background)

    def change_background(self, monitorId: str, bg_path: str) -> None:
        self.desktop.SetWallpaper(monitorId=monitorId, wallpaper=bg_path)
        time.sleep(2)
        


def main():
    bm = BackgroundManager()
    bm.cycle_monitors()
    bm.save_config()


if __name__ == "__main__":
    main()
