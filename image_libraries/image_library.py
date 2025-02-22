import json
import requests
import os
from pathlib import Path
from earthview_scraper import earthview_scraper

EARTHVIEW_DATA_URL = "https://raw.githubusercontent.com/MichaelWhitehill/EarthviewBackground/master/earthview_scraper/earthview_data.json"

class ImageLibrary():
    def __init__(self, start_image:int = 0) -> None:
        self.download_path = os.path.join(os.getenv("LOCALAPPDATA"), "bg_changer", "earthview_lib", "downloads")
        self.lib_data_path = os.path.join(os.getenv("LOCALAPPDATA"), "bg_changer", "earthview_lib", "data.json")
        if not os.path.exists(self.lib_data_path):
            response = requests.get(EARTHVIEW_DATA_URL)
            assert response.status_code == 200
            Path(os.path.dirname(self.lib_data_path)).mkdir(parents=True, exist_ok=True)
            with open(self.lib_data_path, "w") as file:
                json.dump(response.json(), file, indent=4)
        with open(self.lib_data_path, encoding="utf-8") as image_data_handler:
            self.image_data = json.load(image_data_handler)
        self.next_image = start_image

    def next(self) -> str:
        # TODO: make network and io operations async
        # download next image
        # remove current image
        # return local image path
        # os.remove(self.image_data[])
        self.download_image(self.next_image)
        bg = self.image_data[self.next_image]
        self.next_image += 1
        return bg["local_path"]

    def cleanup(self) -> str:
        prev_image = self.config[NEXT_IMAGE_KEY]

    def download_image(self, index: int) -> str:
        img_bytes = requests.get(self.image_data[index]["photoUrl"]).content
        img_name = self.image_data[index]["name"].strip()+str(index)+".jpg"
        img_path = os.path.join(self.download_path, img_name)
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
        with open(img_path, 'wb') as handler:
            handler.write(img_bytes)
        self.image_data[index]["local_path"]= img_path

