"""
   Консоль парсера Hyprland.
"""

# Импортирование файла
from parser.hyprland import HyprlandParser

# Тестировочный класс парсера(с наследованием из HyprlandParser)
class TestParser:
    def __init__(self):
        self.is_saved = 0
        self.config = None

    def console(self):
        print("Debug Console")
        while True:
            answer = input("> ")
            match answer:
                case "find":
                    self.find_key()
                case "change":
                    self.change_value()
                case "save":
                    self.save_values()
                case "load":
                    self.load_config()
                case "delete":
                    self.delete()
                case "add":
                    self.add()
                case "exit":
                    if self.is_saved == 0:
                        print("Save? (Y/n)")
                        answer = input("(Y/n) > ")
                        answer.lower()
                        if answer == "y":
                            self.save_values()
                            break
                        elif answer == "n":
                            break
                        else:
                            self.save_values()
                            break

    def find_key(self):
        if self.config is None:
            print("Please enter 'load' to command line")
        print("Please enter key value")
        answer = input("> ")
        elements = self.config.config_entries
        for element in elements:
            if answer == element['id']:
                print("-="*10)
                print("Value = '{}'".format(element['value']))
                print("Raw Value = '{}'".format(element['raw_value']))
                print("Id element = '{}'".format(element['id']))
                print("-="*10)
            if answer == element['key']:
                print("-="*10)
                print("Value = '{}'".format(element['value']))
                print("Raw Value = '{}'".format(element['raw_value']))
                print("Id element = '{}'".format(element['id']))
        print("-="*10)

    def change_value(self):
        if self.config is None:
            print("Please enter 'load' to command line")
            return None
        print("Please enter id value")
        id_ = input("> ")
        print("Enter new value")
        value = input("> ")
        change_value = self.config.add_value(value, id_)
        if change_value is True:
            print("Succed changed value!")
            return True
        elif change_value is False:
            print("Failed to change value!")
        else:
            print("Failed to change value!")

    def save_values(self):
        if self.config is None:
            print("Please enter 'load' to command line")
            return None
        print("Save to other config? (Y/n)")
        answer = input("(Y/n) > ")
        answer.lower()
        if answer == "y":
            answer = input("enter file > ")
            self.config.save_config(another_file=answer)
        elif answer == "n":
            self.config.save_config()
        print("Config saved!")

    def load_config(self):
        if self.config:
            print("Config is loaded!")
            return None
        print("Please enter filename your config")
        config_file = input("> ")
        print("Loading file")
        try:
            self.config = HyprlandParser(config_file)
            self.config.load_config()
            print("Loaded!")
        except FileNotFoundError:
            print("File Not Found!")

    def delete(self):
        if self.config is None:
            print("Please enter 'load' to command line")
            return None
        print("Please enter id element to delete")
        answer = input("> ")
        elements = self.config.config_entries
        for index, element in enumerate(elements):
            if element.get('id') == answer:
                print("Found Id!")
                print("Latest Key and Value element is {}, {}"
                      .format(element['key'], element['value']))
                del elements[index]
                print("Element deleted!")
                return True
        print("Not found id!")

    def add(self):
        if self.config is None:
            print("Please enter 'load' to command line")
            return None
        print("Please enter new key and value from space.")
        answer = input("> ")
        answer_listed = answer.split()
        elements = self.config.config_entries
        if len(answer_listed) > 2 or len(answer_listed) < 2:
            print("Entered values more twoes")
        else:
            print("Adding")
            formatting_text = self.config._format_data('', '', answer_listed[0], answer_listed[1], answer_listed[0] + " =")
            elements.append(formatting_text)
            print("Added!")

# Инциализация класса
if __name__ == "__main__":
    cons = TestParser()
    cons.console()