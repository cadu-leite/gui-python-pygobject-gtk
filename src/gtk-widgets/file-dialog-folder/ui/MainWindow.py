# -*- coding: utf-8 -*-
"""Python e GTK: PyGObject Gtk.FileDialog() (folder) ui file."""

import subprocess
from pathlib import Path

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()

BASE_DIR = Path(__file__).resolve().parent
APPLICATION_WINDOW = str(BASE_DIR.joinpath('MainWindow.ui'))

# Não utilizar no Gnome Builder. Configurar via meson.
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
class ExampleWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'ExampleWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @Gtk.Template.Callback()
    def on_button_select_folder_clicked(self, widget):
        file_dialog = Gtk.FileDialog.new()
        file_dialog.set_title(title='Selecionar pasta')
        file_dialog.set_modal(modal=True)
        file_dialog.select_folder(
            parent=self,
            callback=self.on_file_dialog_dismissed,
        )

    @Gtk.Template.Callback()
    def on_button_select_folders_clicked(self, widget):
        file_dialog = Gtk.FileDialog.new()
        file_dialog.set_title(title='Selecionar pastas')
        file_dialog.set_modal(modal=True)
        file_dialog.select_multiple_folders(
            parent=self,
            callback=self.on_files_dialog_dismissed,
        )

    def on_file_dialog_dismissed(self, file_dialog, gio_task):
        folder = file_dialog.select_folder_finish(gio_task)
        print(f'Nome da pasta: {folder.get_basename()}')
        print(f'Caminho da pasta: {folder.get_path()}')
        print(f'URI da pasta: {folder.get_uri()}\n')

    def on_files_dialog_dismissed(self, file_dialog, gio_task):
        folders = file_dialog.select_multiple_folders_finish(gio_task)
        for folder in folders:
            print(f'Nome da pasta: {folder.get_basename()}')
            print(f'Caminho da pasta: {folder.get_path()}')
            print(f'URI da pasta: {folder.get_uri()}\n')


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
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)


if __name__ == '__main__':
    import sys

    app = ExampleApplication()
    app.run(sys.argv)
