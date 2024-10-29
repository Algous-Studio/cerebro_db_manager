import os
import subprocess
import fnmatch


file = "/home/volkov/cerebro_db_manager/2024-10-09_13-31.png"

tumb = '/home/volkov/cerebro_db_manager/11111111111111111.jpeg'
# Создание объекта Attachment
from cerebro_db_manager.attachment import Attachment
at = Attachment(file)

# Добавление отчёта в базу данных
from cerebro_db_manager.db_manager import CerebroDBManager
db = CerebroDBManager('sasha', '1')
task = db.add_report(2814749770945326, "test", at)

print(task)
