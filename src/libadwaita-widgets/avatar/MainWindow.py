# -*- coding: utf-8 -*-
"""Python e GTK: PyGObject libadwaita Adw.Avatar()."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()


class ExampleWindow(Adw.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title='Python e GTK: PyGObject libadwaita Adw.Avatar()')
        self.set_default_size(width=int(1366 / 2), height=int(768 / 2))
        self.set_size_request(width=int(1366 / 2), height=int(768 / 2))

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.set_content(content=vbox)

        header_bar = Gtk.HeaderBar.new()
        vbox.append(child=header_bar)

        menu_button_model = Gio.Menu()
        menu_button_model.append(
            label='Preferências',
            detailed_action='app.preferences',
        )

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        header_bar.pack_end(child=menu_button)

        hbox = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox.set_homogeneous(homogeneous=True)
        vbox.append(child=hbox)

        # Exibindo o ícone padrão.
        avatar_01 = Adw.Avatar.new(
            size=100,
            text='Renato Cruz',
            show_initials=False,
        )
        hbox.append(child=avatar_01)

        # Exibindo as iniciais no lugar do ícone.
        avatar_02 = Adw.Avatar.new(
            size=100,
            text='Renato Cruz',
            show_initials=True,
        )
        hbox.append(child=avatar_02)

        avatar_03 = Adw.Avatar.new(
            size=100,
            text='Renato Cruz',
            show_initials=False,
        )
        avatar_03.set_icon_name('contact-new-symbolic')
        hbox.append(child=avatar_03)


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
