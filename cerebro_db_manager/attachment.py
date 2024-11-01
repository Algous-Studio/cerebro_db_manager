import os
import logging
import subprocess
import fnmatch
from PIL import Image
import settings

logger = logging.getLogger(__name__)

class Attachment:
    def __init__(self, file_path: str, thumbnails: list = None, description: str = ""):
        if not isinstance(file_path, str) or not os.path.isfile(file_path):
            raise ValueError("file_path должен быть строкой и указывать на существующий файл.")
        self.file_path = file_path
        
        self.description = description
        self.thumbnails = []

        if thumbnails:
            if not isinstance(thumbnails, list):
                raise ValueError("thumbnails должен быть списком путей.")
            
            valid_thumbnails = []

            for thumbnail_path in thumbnails:
                if len(valid_thumbnails) >= 3:
                    break

                if not os.path.isfile(thumbnail_path):
                    logger.warning(f"Файл {thumbnail_path} не существует.")
                    break
                if not thumbnail_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                    logger.warning(f"Файл {thumbnail_path} должен быть в формате JPG или PNG.")
                    break
                
                # try:
                #     with Image.open(thumbnail_path) as img:
                #         if img.size != (512, 512):
                #             logger.warning(f"Размер изображения {thumbnail_path} не равен 512x512.")
                #             break
                # except Exception as e:
                #     logger.warning(f"Не удалось открыть изображение {thumbnail_path}. Ошибка: {e}")
                #     break
                valid_thumbnails.append(thumbnail_path)

            self.thumbnails = valid_thumbnails[:3]

def generate_thumbnails(thumbnail_dir, file_path):   
    res_code = subprocess.call([settings.MIRADA_PATH, '--mode', 'thumb', file_path, '--temp', thumbnail_dir])
    if res_code != 0:
        raise Exception("Mirada returned a non-zero exit status.\n" + settings.MIRADA_PATH)
    
    thumbnails = []
    for f in os.listdir(thumbnail_dir):
        if fnmatch.fnmatch(f, os.path.basename(file_path) + '.thumb--3-*.jpg'):
            thumbnails.append(os.path.join(thumbnail_dir, f))
    
    thumbnails.sort()
    return thumbnails
