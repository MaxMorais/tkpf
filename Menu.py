import tkinter as tk
from . import Directive


class Menu(Directive.Structural):
    """ Translates the XML hierarchy into proper method calls when constructing a menu """

    def create(self, parent):
        menu = tk.Menu(parent)
        if not isinstance(parent, tk.Menu):
            parent.winfo_toplevel().config(menu=menu)
        return menu

    def add_child(self, parent, classname, attrib, text=None):
        name = attrib.pop('name', None)
        if text:
            attrib['label'] = text
        if classname == 'Menu':
            directive, widget = super().inflate(parent, classname)
            widget.config(tearoff=0)
            self.root_widget.add_cascade(menu=widget, **self.resolve_bindings(widget, attrib))
            self.named_widgets[name] = directive or widget
            return directive, widget
        else:
            self.root_widget.add(classname.lower(), **self.resolve_bindings(None, attrib))
            return None, self.root_widget

    @property
    def named_widgets(self):
        return self.parent_directive.named_widgets
