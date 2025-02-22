import os
import time
import pickle
import argparse
from image_libraries.image_library import ImageLibrary
from desktop_interface import desktop

EARTHVIEW_CONFIG_KEY = "earthview_config"
MONITORS_KEY = "monitors"

class Monitor():
    def __init__(self, mon_id: str, mon_index: int) -> None:
        self.id = mon_id
        self.monitor_index = mon_index
        self.earthview_lib = ImageLibrary(mon_index)

    def next_bg(self):
        self.current_background =  self.earthview_lib.next()
        desktop.set_background(self.id, self.current_background)
        print(f"mon: {self.id} bg: {self.current_background}")
        time.sleep(2)


class BackgroundManager():

    def __init__(self) -> None:
        """background manager init. Gets the config path, the Idesktop instance for setting the background on monitors
        and loads the config if it exists."""
        monitor_ids = desktop.get_monitors()
        self.monitors = []
        for i, m in enumerate(monitor_ids):
            self.monitors.append(Monitor(m, i))


    def cycle_monitors(self):
        for monitor in self.monitors:
            monitor.next_bg()

        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cycle", default=None)
    args = parser.parse_args()

    if os.path.isfile(os.path.join(os.getenv("LOCALAPPDATA"), "bg_changer", "state.pkl")):
        bm = pickle.load(open(os.path.join(os.getenv("LOCALAPPDATA"), "bg_changer", "state.pkl"), "rb"))
    else:
        bm = BackgroundManager()

    if None is not args.cycle:
        bm.cycle_monitors()

    
    with open(os.path.join(os.getenv("LOCALAPPDATA"), "bg_changer", "state.pkl"), "wb") as f:
        pickle.dump(bm, f)


if __name__ == "__main__":
    main()
