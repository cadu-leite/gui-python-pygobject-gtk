# -*- coding: utf-8 -*-
"""Python e GTK: PyGObject Gtk.MenuButton()."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()


class ExampleWindow(Gtk.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title(title='Python e GTK: PyGObject Gtk.MenuButton()')
        self.set_default_size(width=int(1366 / 2), height=int(768 / 2))
        self.set_size_request(width=int(1366 / 2), height=int(768 / 2))

        header_bar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=header_bar)

        menu_model = Gio.Menu()
        menu_model.append('Preferências', 'app.preferences')

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_model)
        header_bar.pack_end(child=menu_button)

        popover = menu_button.get_popover()
        # popover.set_position(position=Gtk.PositionType.BOTTOM)
        # popover.set_has_arrow(has_arrow=False)
        popover.set_offset(x_offset=-50, y_offset=0)
        print(popover)

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_homogeneous(homogeneous=True)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        self.set_child(child=vbox)

        # Criando uma seção.
        section = Gio.Menu.new()
        section.append(label='Item 01', detailed_action='win.item1')
        section.append(label='Item 02', detailed_action='win.item2')
        menu_model.append_section(label='Título da seção',section=section)
        self.create_win_action(
            name='item1', callback=self.on_menu_item_clicked)
        self.create_win_action(
            name='item2', callback=self.on_menu_item_clicked)

        # Criando um submenu.
        submenu = Gio.Menu.new()
        submenu.append(label='Item 03', detailed_action=f'win.item3')
        submenu.append(label='Item 04', detailed_action=f'win.item4')
        menu_model.append_submenu(label='Título do submenu',submenu=submenu)
        self.create_win_action(
            name='item3', callback=self.on_menu_item_clicked)
        self.create_win_action(
            name='item4', callback=self.on_menu_item_clicked)

    def on_menu_item_clicked(self, action, param):
        print(action.get_name())

    def create_win_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name=name, parameter_type=None)
        action.connect('activate', callback)
        self.add_action(action=action)
        if shortcuts:
            self.set_accels_for_action(
                detailed_action_name=f'win.{name}',
                accels=shortcuts,
            )


class ExampleApplication(Gtk.Application):

    def __init__(self):
        super().__init__(application_id='br.com.justcode.Example',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        self.create_action('quit', self.exit_app, ['<primary>q'])
        self.create_action('preferences', self.on_preferences_action)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = ExampleWindow(application=self)
        win.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

    def on_preferences_action(self, action, param):
        print('Ação app.preferences foi ativa.')

    def exit_app(self, action, param):
        self.quit()

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name=name, parameter_type=None)
        action.connect('activate', callback)
        self.add_action(action=action)
        if shortcuts:
            self.set_accels_for_action(
                detailed_action_name=f'app.{name}',
                accels=shortcuts,
            )


if __name__ == '__main__':
    import sys

    app = ExampleApplication()
    app.run(sys.argv)
