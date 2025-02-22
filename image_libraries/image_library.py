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
    def __init__(self, lib_config: dict) -> None:
        self.config = lib_config
        self.load_config()
        image_data_handler = open(self.config[LIB_DATA_PATH_KEY], encoding="utf-8")
        self.image_data = json.load(image_data_handler)
        image_data_handler.close()
        self.download_path = self.config[DOWNLOAD_PATH_KEY]
    
    def load_config(self):
        if None is self.config.get(LIB_PATH_KEY, None):
            self.config[LIB_PATH_KEY] = os.path.join(os.getenv("LOCALAPPDATA"), "bg_changer", "earthview_lib")
        if None is self.config.get(DOWNLOAD_PATH_KEY, None):
            self.config[DOWNLOAD_PATH_KEY] = os.path.join(self.config[LIB_PATH_KEY], "downloads")
        if None is self.config.get(LIB_DATA_PATH_KEY, None):
            self.config[LIB_DATA_PATH_KEY] = os.path.join(self.config[LIB_PATH_KEY], "data.json")
        if None is self.config.get(NEXT_IMAGE_KEY, None):
            self.config[NEXT_IMAGE_KEY] = 0
        # check that paths and files exist
        if not os.path.isdir(self.config[LIB_PATH_KEY]):
            os.mkdir(self.config[LIB_PATH_KEY])
        if not os.path.isfile(self.config[LIB_DATA_PATH_KEY]):
            print("Earthview data is missing")
            will_fetch = input("Would you like to use the prebuilt earthview library index? (y/n)")
            if "y" == will_fetch:
                # copy relative path to earthview results to data path
                shutil.copy(r"earthview_scraper\earthview_data.json", self.config[LIB_DATA_PATH_KEY])
            else:
                print("Collecting Earthview data")
                locations = earthview_scraper.collect_all_locations()
                earthview_scraper.print_locations_to_file(locations, self.config[LIB_DATA_PATH_KEY])
                print("earthview data collected")
    
    def get_config(self):
        return self.config


    def next(self) -> str:
        # TODO: make network and io operations async
        # download next image
        # remove current image
        # return local image path
        # os.remove(self.image_data[])
        self.download_image(self.config[NEXT_IMAGE_KEY])
        bg = self.image_data[self.config[NEXT_IMAGE_KEY]]
        self.config[NEXT_IMAGE_KEY] += 1
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

