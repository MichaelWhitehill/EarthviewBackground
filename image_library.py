import json
import requests
import os
import yaml

NEXT_IMAGE_POINTER_KEY = "earthview_pointer"
LOCAL_IMAGES_KEY = "local_paths"
DOWNLOAD_PATH_KEY = "download_path"
class Image_Library():
    def __init__(self, library_config_path: str, image_data_file_path: str) -> None:
        self.config_path = library_config_path
        self.load_config()
        image_data_handler = open(image_data_file_path, encoding="utf-8")
        self.image_data = json.load(image_data_handler)
        image_data_handler.close()

        self.download_path = self.config[DOWNLOAD_PATH_KEY]
    
    def load_config(self) -> None:
        config_file_handler = open(self.config_path)
        self.config = yaml.safe_load(config_file_handler)
        config_file_handler.close()

    def save_config(self) -> None:
        os.remove(self.config_path)
        with open(self.config_path, 'w') as file:
            yaml.dump(self.config, file)


    def next(self) -> str:
        # TODO: make network and io operations async
        # download next image
        # remove current image
        # return local image path
        self.download_image(self.config[NEXT_IMAGE_POINTER_KEY])
        bg = self.image_data[self.config[NEXT_IMAGE_POINTER_KEY]]
        self.config[NEXT_IMAGE_POINTER_KEY] += 1
        return bg["local_path"]

    def cleanup(self) -> str:
        prev_image = self.config[NEXT_IMAGE_POINTER_KEY]

    def download_image(self, index: int):
        img_bytes = requests.get(self.image_data[index]["photoUrl"]).content
        img_name = self.image_data[index]["name"].strip()+".jpg"
        img_path = os.path.join(self.download_path, img_name)
        with open(img_path, 'wb') as handler:
            handler.write(img_bytes)
        self.image_data[index]["local_path"]= img_path

