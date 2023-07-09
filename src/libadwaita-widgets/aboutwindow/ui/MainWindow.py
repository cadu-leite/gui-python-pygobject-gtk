# -*- coding: utf-8 -*-
"""Python e GTK: PyGObject libadwaita Adw.AboutWindow() ui file."""

import subprocess
import sys
from pathlib import Path

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()

BASE_DIR = Path(__file__).resolve().parent
APPLICATION_WINDOW = str(BASE_DIR.joinpath('MainWindow.ui'))

# Não utilizar no Gnome Builder. Configurar via meson.
# Tutorial está no blog, acesse o README.md.
# [!] O Compilador Blueprint deve estar instalado [!].
operational_system = sys.platform
if operational_system == 'linux':
    for data in BASE_DIR.iterdir():
        if data.is_file() and data.suffix == '.blp':
            subprocess.run(
                args=['blueprint-compiler', 'compile', f'{data}', '--output',
                      f'{BASE_DIR.joinpath(data.stem)}.ui'],
            )
elif operational_system == 'win32':
    # MSYS2 + MINGW64 terminal.
    BLUEPRINT_COMPILER = 'C:\\msys64\\mingw64\\bin\\blueprint-compiler'
    for data in BASE_DIR.iterdir():
        if data.is_file() and data.suffix == '.blp':
            subprocess.run(
                args=['python3', BLUEPRINT_COMPILER, 'compile', f'{data}', '--output',
                      f'{BASE_DIR.joinpath(data.stem)}.ui'],
            )


@Gtk.Template(filename=APPLICATION_WINDOW)
class ExampleWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'ExampleWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


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
        dialog.set_application_name('Python e GTK')
        dialog.set_version('0.0.1')
        dialog.set_developer_name('Renato Cruz (natorsc)')
        dialog.set_license_type(Gtk.License(Gtk.License.MIT_X11))
        dialog.set_comments('Criando interfaces gráficas com a linguagem de'
                            'programação Python (PyGObject) e o toolkit gráfico Gtk')
        dialog.set_website('https://gtk.justcode.com.br')
        dialog.set_issue_url("https://github.com/natorsc/gui-python-pygobject-gtk/issues")
        dialog.add_credit_section('Contributors', ['Name-01', 'Name-02'])
        dialog.set_translator_credits('Translator')
        dialog.set_copyright('© 2022 Renato Cruz (natorsc)')
        dialog.set_developers(['natorsc https://github.com/natorsc'])
        dialog.set_application_icon('help-about-symbolic')
        dialog.present()

    def exit_app(self, action, param):
        self.quit()

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)


if __name__ == '__main__':
    import sys

    app = ExampleApplication()
    app.run(sys.argv)
