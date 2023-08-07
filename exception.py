class ArgumentError(Exception):
    "Класс, обрабатывающий исключения аргументов командной строки"
    def __init__(self, error_type):
        self.error_type = error_type
        self.message = self._get_error_messages()

    def _get_error_messages(self):
        error_messages = {
            "FileIsAbsent": """
                           Не указано название функции распределения, с которой ведётся работа

                            Пожалуйста, укажите название функции распределения.
                       """,
            "FilenameError": """
            указано неверное название функции распределения, пожелуйста, попробуйте ещё раз""",
            "DiapasonError": """
            указан неверный диапазон: конечная граница меньше начальной, попробуйте ещё раз"""

        }