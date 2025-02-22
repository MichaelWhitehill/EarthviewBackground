import json
import requests
import os
from earthview_scraper import earthview_scraper
import shutil

LIB_PATH_KEY = "library_path"
NEXT_IMAGE_KEY = "earthview_image"
LOCAL_IMAGES_KEY = "local_paths"
LIB_DATA_PATH_KEY = "lib_data_path"
DOWNLOAD_PATH_KEY = "download_path"
class ImageLibrary():
    def __init__(self, start_image:int = 0) -> None:
        self.download_path = os.path.join(os.getenv("LOCALAPPDATA"), "bg_changer", "earthview_lib", "downloads")
        self.lib_data_path = os.path.join(os.getenv("LOCALAPPDATA"), "bg_changer", "earthview_lib", "data.json")
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
        img_name = self.image_data[index]["name"].strip()+".jpg"
        img_path = os.path.join(self.download_path, img_name)
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
        with open(img_path, 'wb') as handler:
            handler.write(img_bytes)
        self.image_data[index]["local_path"]= img_path

