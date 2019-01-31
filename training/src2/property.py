import Tkinter as tk


class Property:

    INTEGER = 1
    STRING = 2

    @classmethod
    def create_integer(cls, title, options):
        return Property(cls.INTEGER, title, options, tk.IntVar())

    @classmethod
    def create_string(cls, title, options):
        return Property(cls.STRING, title, options, tk.StringVar())

    def __init__(self, type, title, options, var):
        self.type = type
        self.title = title
        self.options = options
        self.var = var
        self.var.set(self.options[0])
