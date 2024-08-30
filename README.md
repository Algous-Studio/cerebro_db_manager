# cerebro_db_manager
CerebroDBManager — это Python-библиотека для управления базой данных Cerebro. Этот репозиторий предоставляет удобные инструменты для подключения, выполнения запросов и обработки данных в базе данных Cerebro. 


## Пример использования

```python
from cerebro_db_manager.db_manager import CerebroDBManager
from cerebro_db_manager.attachment import Attachment

# Инициализация CerebroDBManager с использованием учётных данных
db_manager = CerebroDBManager(user="your_username", password="your_password")

# Создание вложения с эскизами (thumbnails)
attachment = Attachment(
    file_path="path/to/your/file.ext",
    thumbnails=["path/to/thumbnail1.jpg", "path/to/thumbnail2.png"],
    description="Описание вложения"
)

# Добавление отчёта с вложением к задаче
task_id = 123456  # Замените на фактический ID задачи
comment = "Задача выполнена успешно"
minutes = 120  # Время выполнения задачи в минутах

report_message_id = db_manager.add_report(
    task_id=task_id,
    comment=comment,
    attachments=[attachment],
    minutes=minutes
)

print(f"Отчёт добавлен с ID сообщения: {report_message_id}")
```