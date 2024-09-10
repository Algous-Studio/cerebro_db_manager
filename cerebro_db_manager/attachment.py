import os
import logging
from PIL import Image

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
                
                try:
                    with Image.open(thumbnail_path) as img:
                        if img.size != (512, 512):
                            logger.warning(f"Размер изображения {thumbnail_path} не равен 512x512.")
                            break
                except Exception as e:
                    logger.warning(f"Не удалось открыть изображение {thumbnail_path}. Ошибка: {e}")
                    break
                valid_thumbnails.append(thumbnail_path)

            self.thumbnails = valid_thumbnails[:3]