# -*- coding: utf-8 -*-
"""Python e GTK: PyGObject libadwaita Adw.Toast()."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()


class ExampleWindow(Gtk.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title='Python e GTK: PyGObject libadwaita Adw.Toast()')
        self.set_default_size(width=int(1366 / 2), height=int(768 / 2))
        self.set_size_request(width=int(1366 / 2), height=int(768 / 2))

        header_bar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=header_bar)

        menu_button_model = Gio.Menu()
        menu_button_model.append('Preferências', 'app.preferences')

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        header_bar.pack_end(child=menu_button)

        self.toast_overlay = Adw.ToastOverlay.new()
        self.toast_overlay.set_margin_top(margin=12)
        self.toast_overlay.set_margin_end(margin=12)
        self.toast_overlay.set_margin_bottom(margin=12)
        self.toast_overlay.set_margin_start(margin=12)
        self.set_child(child=self.toast_overlay)

        self.button = Gtk.Button.new_with_label(label='Clique aqui')
        self.button.set_valign(align=Gtk.Align.CENTER)
        self.button.set_vexpand(expand=True)
        self.button.connect('clicked', self.on_button_clicked)
        self.toast_overlay.set_child(child=self.button)

        self.toast = Adw.Toast.new(title='')
        self.toast.connect('dismissed', self.on_toast_dismissed)

    def on_button_clicked(self, button):
        button.set_sensitive(sensitive=False)
        self.toast.set_title(title='Mensagem do toast')
        self.toast_overlay.add_toast(self.toast)

    def on_toast_dismissed(self, toast):
        print('O toast foi fechado')
        self.button.set_sensitive(sensitive=True)


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
