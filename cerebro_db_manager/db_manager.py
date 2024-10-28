import os
import logging
import settings
from py_cerebro.database import Database as cerebroDB
from py_cerebro import dbtypes, cargador
from cerebro_db_manager.attachment import Attachment

logger = logging.getLogger(__name__)

_con_db = None
_con_cag = None


class CerebroDBManager: 
    def __init__(self, user = None, password = None):
        global _con_db
        global _con_cag
        if all([user, password]):
            self.user = user
            self.password = password 
            _con_db = self._connect_to_database()
            _con_cag = cargador.Cargador(settings.CARGADOR_HOST,
                                          settings.CARGADOR_XMLRPC_PORT,
                                          settings.CARGADOR_HTTP_PORT)       
        self.cargodor = _con_cag
        self.db = _con_db

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
        self.db.task_set_status(task_id, settings.CHECK_STATUS_ID)
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

    def get_tasks_childrens(self, project_id: int):
        """
        Возвращает список всех детей проекта (включая детей всех уровней).
        """
        task_list = []
        self._get_all_childrens_recursive(project_id, task_list)
        return task_list

    def _get_all_childrens_recursive(self, task_id: int, task_list: list):
        """
        Рекурсивно получает всех детей для задачи и добавляет их в список.

        :param task_id: ID задачи (проекта или подзадачи)
        :param task_list: список, куда будут добавляться все задачи
        """
        children_tasks = self.db.task_children(task_id)

        for task in children_tasks:
            task_dict = {
                "TASK_DATA_MTM": task[dbtypes.TASK_DATA_MTM],
                "TASK_DATA_ID": task[dbtypes.TASK_DATA_ID],
                "TASK_DATA_PARENT_ID": task[dbtypes.TASK_DATA_PARENT_ID],
                "TASK_DATA_PLANNED_DELTA": task[dbtypes.TASK_DATA_PLANNED_DELTA],
                "TASK_DATA_NAME": task[dbtypes.TASK_DATA_NAME],
                "TASK_DATA_PARENT_URL": task[dbtypes.TASK_DATA_PARENT_URL],
                "TASK_DATA_ACTIVITY_NAME": None if task[dbtypes.TASK_DATA_ACTIVITY_NAME] == '' else task[dbtypes.TASK_DATA_ACTIVITY_NAME],
                "TASK_DATA_ACTIVITY_ID": task[dbtypes.TASK_DATA_ACTIVITY_ID],
                "TASK_DATA_SELF_USERS_DECLARED": task[dbtypes.TASK_DATA_SELF_USERS_DECLARED],
                "TASK_DATA_SELF_USERS_APPROVED": task[dbtypes.TASK_DATA_SELF_USERS_APPROVED],
                "TASK_DATA_CREATED": task[dbtypes.TASK_DATA_CREATED],
                "TASK_DATA_PRIORITY": task[dbtypes.TASK_DATA_PRIORITY],
                "TASK_DATA_PROGRESS": task[dbtypes.TASK_DATA_PROGRESS],
                "TASK_DATA_PLANNED": task[dbtypes.TASK_DATA_PLANNED],
                "TASK_DATA_USERS_DECLARED": task[dbtypes.TASK_DATA_USERS_DECLARED],
                "TASK_DATA_USERS_APPROVED": task[dbtypes.TASK_DATA_USERS_APPROVED],
                "TASK_DATA_THUMBS": task[dbtypes.TASK_DATA_THUMBS],
                "TASK_DATA_FLAGS": task[dbtypes.TASK_DATA_FLAGS],
                "TASK_DATA_MODERATOR_ID": task[dbtypes.TASK_DATA_MODERATOR_ID],
                "TASK_DATA_CREATOR_ID": task[dbtypes.TASK_DATA_CREATOR_ID],
                "TASK_DATA_MODIFIED": task[dbtypes.TASK_DATA_MODIFIED],
                "TASK_DATA_ALLOCATED": task[dbtypes.TASK_DATA_ALLOCATED],
                "TASK_DATA_OFFSET": task[dbtypes.TASK_DATA_OFFSET],
                "TASK_DATA_DURATION": task[dbtypes.TASK_DATA_DURATION],
                "TASK_DATA_PROJECT_ID": task[dbtypes.TASK_DATA_PROJECT_ID],
                "TASK_DATA_PRIVILEGE": task[dbtypes.TASK_DATA_PRIVILEGE],
                "TASK_DATA_HUMAN_START": task[dbtypes.TASK_DATA_HUMAN_START],
                "TASK_DATA_HUMAN_FINISH": task[dbtypes.TASK_DATA_HUMAN_FINISH],
                "TASK_DATA_SELF_BUDGET": task[dbtypes.TASK_DATA_SELF_BUDGET],
                "TASK_DATA_SELF_SPENT": task[dbtypes.TASK_DATA_SELF_SPENT],
                "TASK_DATA_BUDGET": task[dbtypes.TASK_DATA_BUDGET],
                "TASK_DATA_SPENT": task[dbtypes.TASK_DATA_SPENT],
                "TASK_DATA_RESOURCE_SELF_DECLARED": task[dbtypes.TASK_DATA_RESOURCE_SELF_DECLARED],
                "TASK_DATA_RESOURCE_SELF_APPROVED": task[dbtypes.TASK_DATA_RESOURCE_SELF_APPROVED],
                "TASK_DATA_RESOURCE_DECLARED": task[dbtypes.TASK_DATA_RESOURCE_DECLARED],
                "TASK_DATA_RESOURCE_APPROVED": task[dbtypes.TASK_DATA_RESOURCE_APPROVED],
                "TASK_DATA_SELF_STATUS": task[dbtypes.TASK_DATA_SELF_STATUS],
                "TASK_DATA_CC_STATUS": task[dbtypes.TASK_DATA_CC_STATUS],
                "TASK_DATA_CC_STATUS_STAT": task[dbtypes.TASK_DATA_CC_STATUS_STAT],
                "TASK_DATA_ORDER": task[dbtypes.TASK_DATA_ORDER],
            }

            task_list.append(task_dict)

            self._get_all_childrens_recursive(task[dbtypes.TASK_DATA_ID], task_list)
