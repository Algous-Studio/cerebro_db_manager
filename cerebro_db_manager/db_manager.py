import logging
import settings
from py_cerebro.database import Database as cerebroDB
from py_cerebro import dbtypes, cargador
from cerebro_db_manager.attachment import Attachment

logger = logging.getLogger(__name__)

class CerebroDBManager:
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.db = self._connect_to_database()
        self.cargodor = cargador.Cargador(settings.CARGADOR_HOST,
                                          settings.CARGADOR_XMLRPC_PORT,
                                          settings.CARGADOR_HTTP_PORT)

    def _connect_to_database(self):
        db = cerebroDB(settings.CEREBRO_DB_HOST, settings.CEREBRO_DB_PORT)
        db.connect(self.user, self.password)
        return db

    def _create_report_message(self, task_id, comment, minutes) -> int:
        messages = self.db.task_messages(task_id)
        first_massage = messages[0]
        message_id = first_massage[dbtypes.MESSAGE_DATA_ID]
        report_message_id = self.db.add_report(
            task_id, message_id, comment, minutes=minutes
        )
        return report_message_id

    def _add_attachment(self, message_id, attachment: Attachment):
        self.db.add_attachment(
            message_id=message_id,
            carga=self.cargodor,
            filename=attachment.file_path,
            thumbnails=attachment.thumbnails,
            description=attachment.description,
            as_link=True,
        )

    def _add_attachments(self, message_id, attachments):
        if isinstance(attachments, list):
            for attachment in attachments:
                if isinstance(attachment, Attachment):
                    self._add_attachment(message_id, attachment)
                else:
                    logger.warning(
                        "Один из элементов списка attachments не является экземпляром класса Attachment. Пропуск."
                    )
        elif isinstance(attachments, Attachment):
            self._add_attachment(message_id, attachments)
        else:
            logger.warning(
                "attachments должен быть либо списком объектов Attachment, либо объектом Attachment."
            )

    def add_report(self, task_id, comment, attachments=None, minutes=0):
        report_message_id = self._create_report_message(task_id, comment, minutes)

        if attachments is not None:
            self._add_attachments(report_message_id, attachments)
        return report_message_id
