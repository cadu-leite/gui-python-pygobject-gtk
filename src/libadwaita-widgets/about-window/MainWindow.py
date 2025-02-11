# -*- coding: utf-8 -*-
"""Python e GTK: PyGObject libadwaita Adw.AboutWindow()."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()


class ExampleWindow(Adw.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(
            title='Python e GTK: PyGObject libadwaita Adw.AboutWindow()')
        self.set_default_size(width=int(1366 / 2), height=int(768 / 2))
        self.set_size_request(width=int(1366 / 2), height=int(768 / 2))

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_content(content=vbox)

        header_bar = Gtk.HeaderBar.new()
        vbox.append(child=header_bar)

        menu_button_model = Gio.Menu()
        menu_button_model.append(
            label='Preferências',
            detailed_action='app.preferences',
        )
        menu_button_model.append('Sobre', 'app.about')

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        header_bar.pack_end(child=menu_button)

        label = Gtk.Label.new()
        label.set_label(str='Clique no menu e selecione sobre')
        label.set_vexpand(expand=True)
        vbox.append(child=label)


class ExampleApplication(Gtk.Application):

    def __init__(self):
        super().__init__(application_id='br.com.justcode.Example',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        self.create_action('quit', self.exit_app, ['<primary>q'])
        self.create_action('preferences', self.on_preferences_action)
        self.create_action('about', self.on_about_action)

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

    def on_about_action(self, action, param):
        dialog = Adw.AboutWindow.new()
        dialog.set_transient_for(parent=self.get_active_window())
        dialog.set_application_name('Python e GTK 4')
        dialog.set_version('0.0.1')
        dialog.set_developer_name('Renato Cruz (natorsc)')
        dialog.set_license_type(Gtk.License(Gtk.License.MIT_X11))
        dialog.set_comments('Criando interfaces gráficas com a linguagem de'
                            'programação Python (PyGObject) e o toolkit gráfico Gtk 4')
        dialog.set_website('https://gtk.justcode.com.br')
        dialog.set_issue_url(
            "https://github.com/natorsc/gui-python-pygobject-gtk4/issues")
        dialog.add_credit_section('Contributors', ['Name-01', 'Name-02'])
        dialog.set_translator_credits('Translator')
        dialog.set_copyright('© 2022 Renato Cruz (natorsc)')
        dialog.set_developers(['natorsc https://github.com/natorsc'])
        dialog.set_application_icon('help-about-symbolic')
        dialog.present()

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
