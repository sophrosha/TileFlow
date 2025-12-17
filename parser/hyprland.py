"""
    Файл класса обработки конфигурационных
    файлов Hyprland
"""

'''
    Извлечение 2-х значений и возврат 
    их в отдельные переменные
 
    Входные аргументы: строка
    Выходные значения: ключ, значение. Или пустота
'''
def _parse_key_value(line: str):
    line = line.strip()
    if '=' in line:
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip()
        return key, value

'''
    Основной класс для обработки конфигурационных
    файлов оболочки Hyprland
'''
class HyprlandParser:
    def __init__(self, file):
        self.file = file
        self.config_entries = []
        self.block_stack = []
        self.block_depth = 0
        self.next_id = 0

    '''
        Генерация уникального иденфикационного 
        номера для каждой строки.
    
        Входные аргументы: self
        Выходные значения: строка с entry_(индефикационный номер)
    '''
    def _generate_id(self) -> str:
        self.next_id += 1
        return f"entry_{self.next_id}"

    '''
        Возвращение значений ввиде данных об строке, какое у него начало,
        ключ и значение, а так же полное значение с синтаксисом. 
    
        Входные аргументы: self, начало файла, в блоке ли он, ключ
                           значение, полное значение строки.
        Выходные значения: Словарь с теми же значениями, но ввиде названий что за значения
    '''
    def _format_data(self, starts_with: str, block: str,
                     key: str, value: str, raw_value: str) -> dict:
        id_line = self._generate_id()
        return {
                'starts_with': starts_with,
                'block': block,
                'key': key,
                'value': value,
                'raw_value': raw_value,
                'id': id_line
                }

    '''
        Обратная пересборка строк из словаря.
        Если у строки нету ключа и значения то добавляется только
        значение из rawvalue
    
        Входные аргументы: self
        Выходные значения: список с str
    '''
    def _rebuild_config_lines(self) -> list[str]:
        lines = []
        for item in self.config_entries:
            if item['key']:
                lines.append(f"{item['key']} = {item['value']}")
            else:
                lines.append(item['raw_value'])
        return lines

    '''
        Основная функция парсинга строки.
        Определяет какой у него тип через функцию
        и добавляет это значение ввиде отформатированного значения.
        При наличии не тех значений(тоесть не =,{},#,$) то будет выводить
        ошибку парсинга
    
        Входные аргументы: self, строка, номер строки.
        Выходные значения: Отсуствуют
    '''
    def _parse_line(self, value_line, number_line):
        stripped_line = value_line.strip()
        if len(value_line.strip()) == 0:  # Воздух
            formated_data = self._format_data('', '', '', '', stripped_line)
            self.config_entries.append(formated_data)
        elif value_line.strip().startswith('#'):  # Комментарии
            formated_data = self._format_data('#', '', '', '', stripped_line)
            self.config_entries.append(formated_data)
        elif value_line.strip().startswith('$'):  # Переменные
            key, value = _parse_key_value(stripped_line)
            formatted_assignment = key + ' ='
            formated_data = self._format_data('$', '', key, value, formatted_assignment)
            self.config_entries.append(formated_data)
        elif '=' in value_line and self.block_depth == 0:  # Глобальные значения
            key, value = _parse_key_value(stripped_line)
            formatted_assignment = key + ' ='
            formated_data = self._format_data('', '', key, value, formatted_assignment)
            self.config_entries.append(formated_data)
        elif '{' in value_line:  # Открытие блока
            self.block_depth += 1
            block_split = value_line.split()
            self.block_stack.append(block_split[0])
            formated_data = self._format_data('', self.block_stack[0], '', '', stripped_line)
            self.config_entries.append(formated_data)
        elif '}' in value_line:  # Закрытие блока
            self.block_depth -= 1
            formated_data = self._format_data('', '', '', '', stripped_line)
            self.config_entries.append(formated_data)
            self.block_stack.clear()
        elif self.block_depth > 0:  # Блочные значения
            key, value = _parse_key_value(value_line)
            formatted_assignment = key + ' ='
            formated_data = self._format_data('', self.block_stack[0],
                                              key, value, formatted_assignment)
            self.config_entries.append(formated_data)
        else:
            # Ошибка парсинга если строка не парсится
            raise Exception('Invalid line as:', number_line)

    '''
        Дебаг функции выводящие значения словаря или 
        пересобранный конфиг с новыми значениями
    
        Входные аргументы: self
        Выходные значения: Отсуствуют
    '''
    def debug_printf_config_lines(self) -> None:
        rebuild_lines = self._rebuild_config_lines()
        for line in rebuild_lines:
            print(line)

    def debug_print_parser_values(self) -> None:
        for elements in self.config_entries:
            print(elements)

    '''
        Загружает конфиг и обрабатывает его строки через
        основную функцию парсинга
    
        Входные аргументы: self
        Выходные значения: Отсуствуют
    '''
    def load_config(self):
        with open(self.file, 'r') as file:
            file = file.readlines()
            for number_line, value_line in enumerate(file):
                self._parse_line(value_line, number_line+1)

    '''
        Добавляет значения в строку имея его
        индефикационный номер.
    
        Входные аргументы: self, значение, айди строки
        Выходные значения: Булевы значения
    '''
    def add_value(self, value: str, id_: str) -> bool:
        for items in self.config_entries:
            if items['id'] == id_:
                items['value'] = value
                return True
        return False

    '''
        Сохраняет значения в конфигурацию, может так же
        их сохранить в отдельную конфигурацию если нужно
        сохранить прошлую.
        
        Входные аргументы: self, другой файл
        Выходные значения: Булевы значения
    '''
    def save_config(self, another_file=None) -> bool:
        if another_file is None:
            another_file = self.file
        with open(another_file, 'w') as file:
            rebuild_line = self._rebuild_config_lines()
            file.write("\n".join(rebuild_line))
        return True