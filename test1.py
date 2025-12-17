import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class FlowBoxButtonWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Кнопка с FlowBox")
        self.set_border_width(10)
        self.set_default_size(400, 300)

        # Создаем основную разметку
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # Создаем кнопку, которая будет открывать FlowBox
        self.button = Gtk.Button(label="Открыть FlowBox")
        self.button.connect("clicked", self.on_button_clicked)
        vbox.pack_start(self.button, False, False, 0)

        # Создаем FlowBox и добавляем в него элементы
        self.flowbox = Gtk.FlowBox(
            selection_mode=Gtk.SelectionMode.NONE,
            valign=Gtk.Align.START,
            max_children_per_line=4,
            row_spacing=10,
            column_spacing=10,
        )
        for i in range(1, 10):
            button_child = Gtk.Button(label=f"Элемент {i}")
            self.flowbox.add(button_child)

        # Создаем всплывающее окно (Popover)
        self.popover = Gtk.Popover()
        self.popover.add(self.flowbox)

    def on_button_clicked(self, button):
        """Обработчик нажатия кнопки."""
        # Устанавливаем привязку Popover к кнопке
        self.popover.set_relative_to(button)
        # Показываем или скрываем Popover
        if self.popover.get_visible():
            self.popover.hide()
        else:
            self.popover.show_all()


if __name__ == "__main__":
    win = FlowBoxButtonWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
