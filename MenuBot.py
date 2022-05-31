from telebot import types


class Menu:
    hash = {}
    cur_menu = None

    def __init__(self, name, buttons=None, parent=None, action=None):
        self.parent = parent
        self.name = name
        self.buttons = buttons
        self.action = action

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
        markup.add(*buttons)
        self.markup = markup

        self.__class__.hash[name] = self

    @classmethod
    def getMenu(cls, name):
        menu = cls.hash.get(name)
        if menu is not None:
            cls.cur_menu = menu
        return menu


m_main = Menu("Главное меню", buttons=["Развлечения", "Помощь"])
m_fun = Menu("Развлечения", buttons=["Погода", "Да или Нет", "Выход"], parent=m_main)
