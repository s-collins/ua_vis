import Tkinter as tk
from view import View
from property import Property


class Controller:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Training Examples')
        self.view = View(self.root, self)

        # TODO: This should probably not be hard-coded...
        self.view.edit_tab.property_editor.add_property(Property.create_string('Name', ('Sean', 'Venkata')))
        self.view.edit_tab.property_editor.add_property(Property.create_integer('Number', (1, 2, 3)))

        self.view.grid()

    def run(self):
        self.root.mainloop()


Controller().run()
