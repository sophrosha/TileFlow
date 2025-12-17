'''
    Оболочка программы MPSTWM
'''
import gi
import sys
from parser.hyprland import HyprlandParser

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gtk

test_translate = [
    ["monitor", "Monitor Settings"],
    ["env", "Environment"],
    ["border_size", "Border size"],
    ["test", "Test option"],
    ["user", "User"],
    ["rounding", "Rounding corners"],
    ["enabled", "Enabled"],
]
PROGRAM_TITLE = [
    "Mpstwm Version 0.1",
    "Mpstwm: Menu parser"
]
PROGRAM_ID = "ru.sophron.mpstwm"

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs, title=PROGRAM_TITLE[0])
        
        # Инициализация виджетов
        self.create_main_window()
        self.header_button_modules()
        self.header_button_about()
        self.stack_starter_text()   

    # Создание окна
    def create_main_window(self):        
        self.set_default_size(700, 500)
        self.stack = Gtk.Stack()
        self.set_child(self.stack)
        self.header_bar = Gtk.HeaderBar()
        self.set_titlebar(self.header_bar)  
    
    # Кнопки модулей
    def header_button_modules(self):
        button_new = Gtk.Button(icon_name="document-open")
        button_new.connect("clicked", self.button_new_clicked)
        self.header_bar.pack_start(button_new)
        widget_modules = Gtk.FlowBox(
            selection_mode=Gtk.SelectionMode.NONE,
            valign=Gtk.Align.START,
            row_spacing=10,
            column_spacing=10,
        )
        # [Название модуля, функция модуля]
        elements = [
            ["Hyprland", self.test_func],
            ["Waybar", self.test_func],
            ["BSPWM", self.test_func],
            ["I3", self.test_func],
            ["Polybar", self.test_func],
        ]
        for element in elements:
            button_module = Gtk.Button(label=element[0])
            button_module.connect("clicked", element[1])
            widget_modules.append(button_module)
        self.popover = Gtk.Popover()
        self.popover.set_child(widget_modules)

    # Об программе
    def header_button_about(self):
        button_credits = Gtk.Button(icon_name="help-about")
        button_credits.connect("clicked", self.on_about_clicked)
        self.header_bar.pack_end(button_credits)

    # Стартовый текст в стэке
    def stack_starter_text(self):
        starter_text = Gtk.Label()
        starter_text.set_markup(
            "<big>Press the top left button to select the configurator</big>"
        )
        self.stack.add_titled(starter_text, "label", "A label")
    
    # Функция не реализованна
    def error_credit(self, _button):
        print("Function didn't created")
    
    # Нажатие кнопки модули
    def button_new_clicked(self, _button):
        self.popover.set_parent(_button)
        self.popover.popup()
    
    # Тестовая кнопка работы элементов
    def test_func(self, _button):
        print("button is clicked")

    # Диалог "об программе"
    def on_about_clicked(self, button):
        dialog = Adw.AboutWindow(
            transient_for=self,
            application_name="MPSTWM",
            application_icon="preferences-desktop",
            version="0.1",
            developer_name="Sophron Ragozin",
            website="https://git.sophron.ru/sophron/itc_projects",
            comments="Панель настройки тайлинговых оконных менеджеров"
        )
        dialog.present()

        
# Активирую окно и представляю его
def activate(app):
    window = MainWindow(application=app)
    window.present()

# Инициализирую программу через библиотеку libadwaita
# После ее активирую через функцию activate
def main():
    app = Adw.Application(application_id=PROGRAM_ID)
    app.connect("activate", activate)
    app.run(None)


class ModuleParserHyprland(Gtk.ApplicationWindow):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs, title=PROGRAM_TITLE[1])
        self.set_default_size(700, 500)
        self.list_parsed = self.init_parser("example_hyprland.conf")

        # Скроллинг
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_vexpand(True) 

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.scroll.set_child(self.box)
        self.header_bar = Gtk.HeaderBar()
        self.set_titlebar(self.header_bar)
        
        self.generate_elements()

    @staticmethod
    def init_parser(file):
        config = HyprlandParser(file)
        config.load_config()
        return config.config_entries
    
    def bool_value(key):
        if key == "True":
            return False
        else:
            return True
    
    @staticmethod
    def convert_to_text(key):
        for element in test_translate:
            if element[0] == key:
                return str(element[1])
            else:
                return str(key)

    def is_index(self, ind):
        print(f"Button is a {ind}")

    def generate_elements(self):
        for index, element in enumerate(self.list_parsed):

            # Вытаскиваю значения в элементе под отдельные переменные
            starts_with = element['starts_with']
            block = element['block']
            key = element['key']
            value = element['value']
            raw_value = element['raw_value']
            id_ = element['id']

            # Убираю из обработки итерации элементы (#, {, })
            if starts_with.startswith('#'):
                continue
            elif '{' in raw_value:
                continue
            elif '}' in raw_value:
                continue
            elif len(raw_value) == 0:
                continue
            else:
                element_container = Gtk.Box()
                self.box.append(element_container)
                if value.lower() == "true" or value.lower() == "false":
                    label = Gtk.Label(label=self.convert_to_text(key))
                    button = Gtk.Button()
                    button.connect("clicked", lambda widget, i=index: self.is_index(self.list_parsed[i]['id']))
                    element_container.append(label)
                    element_container.append(button)
                else:
                    label = Gtk.Label(label=self.convert_to_text(key))
                    element_text = Gtk.Entry()
                    element_container.append(label)
                    element_container.append(element_text)
        self.set_child(self.scroll)

def activatemodule(app):
    window = ModuleParserHyprland(application=app)  
    window.present()

def main_hyprland_module():
    app = Adw.Application(application_id=PROGRAM_ID)
    app.connect("activate", activatemodule)
    app.run(None)

if __name__ == "__main__":
    main_hyprland_module()