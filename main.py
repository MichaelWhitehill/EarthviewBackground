import os
import time
import yaml
import argparse
from image_libraries.image_library import ImageLibrary
from wallpaper_changer.idesktop import IDesktopWallpaper

EARTHVIEW_CONFIG_KEY = "earthview_config"
MONITORS_KEY = "monitors"

class Monitor():
    def __init__(self, mon_id: str, mon_config: dict) -> None:
        self.id = mon_id
        self.config = mon_config
        self.earthview_lib = ImageLibrary(self.config.get(EARTHVIEW_CONFIG_KEY, {}))
    
    def get_config(self) -> None:
        self.config["id"] = self.id
        self.config[EARTHVIEW_CONFIG_KEY] = self.earthview_lib.get_config()
        return self.config

    def next_bg(self) -> str:
        return self.earthview_lib.next()


class BackgroundManager():

    def __init__(self) -> None:
        """background manager init. Gets the config path, the Idesktop instance for setting the background on monitors
        and loads the config if it exists."""
        self.config_path = os.path.join(os.getenv("LOCALAPPDATA"), "bg_changer", "config.yml")
        self.desktop = IDesktopWallpaper.CoCreateInstance()
        self.load_config()
        self.earthview_lib = ImageLibrary(self.config.get(EARTHVIEW_CONFIG_KEY, {}))
    
    def load_config(self) -> None:
        """Loads the config if it exists. Creates one if it does not exist"""
        if not os.path.isfile(self.config_path):
            self.create_config()
        config_file_handler = open(self.config_path)
        self.config = yaml.safe_load(config_file_handler)
        config_file_handler.close()
        self.monitors = []
        for m in self.config[MONITORS_KEY]:
            self.monitors.append(Monitor(m["id"], m))

    def create_config(self) -> None:
        """Creates a blank config and if the directory for the configs does not exist, it creates one"""
        self.config = {}
        if not os.path.isdir(os.path.join(os.getenv("LOCALAPPDATA"), "bg_changer")):
            os.mkdir(os.path.join(os.getenv("LOCALAPPDATA"), "bg_changer"))
        monitor_ids = self.get_monitors()
        self.monitors = []
        for i, m in enumerate(monitor_ids):
            print(m)
            self.monitors.append(Monitor(m, {EARTHVIEW_CONFIG_KEY: {"earthview_image": i}}))
        self.save_config()


    def save_config(self) -> None:
        """Saves the config as yaml"""
        self.config[MONITORS_KEY] = []
        for m in self.monitors:
            self.config[MONITORS_KEY].append(m.get_config())
        if os.path.isfile(self.config_path):
            os.remove(self.config_path)
        with open(self.config_path, 'w') as file:
            yaml.dump(self.config, file)

    def get_monitors(self) -> list[str]:
        """Only works for Windows. Gets each monitor ID which is uesed for setting its background"""
        mon_count = self.desktop.GetMonitorDevicePathCount()
        monitors = []
        for i in range(0, mon_count):
            if self.desktop.GetMonitorDevicePathAt(i) == "":
                continue
            monitors.append(self.desktop.GetMonitorDevicePathAt(i))
        return monitors

    def cycle_monitors(self):
        for monitor in self.monitors:
            background =  monitor.next_bg()
            print(f"mon: {monitor.id} bg: {background}")
            self.change_background(monitor.id, background)

    def change_background(self, monitorId: str, bg_path: str) -> None:
        self.desktop.SetWallpaper(monitorId=monitorId, wallpaper=bg_path)
        time.sleep(2)
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cycle", default=None)
    args = parser.parse_args()
    bm = BackgroundManager()

    if None is not args.cycle:
        bm.cycle_monitors()
    bm.save_config()


if __name__ == "__main__":
    main()
