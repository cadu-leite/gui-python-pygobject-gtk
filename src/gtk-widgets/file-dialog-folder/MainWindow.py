# -*- coding: utf-8 -*-
"""Python e GTK: PyGObject Gtk.FileDialog() folder."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()


class ExampleWindow(Gtk.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title(
            title='Python e GTK: PyGObject Gtk.FileDialog() folder',
        )
        self.set_default_size(width=int(1366 / 2), height=int(768 / 2))
        self.set_size_request(width=int(1366 / 2), height=int(768 / 2))

        header_bar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=header_bar)

        menu_button_model = Gio.Menu()
        menu_button_model.append(
            label='Preferências',
            detailed_action='app.preferences',
        )

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        header_bar.pack_end(child=menu_button)

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        self.set_child(child=vbox)

        button_select_file = Gtk.Button.new_with_label(
            label='Selecionar pasta',
        )
        button_select_file.connect(
            'clicked',
            self.on_button_select_folder_clicked,
        )
        vbox.append(child=button_select_file)

        button_select_files = Gtk.Button.new_with_label(
            label='Selecionar pastas',
        )
        button_select_files.connect(
            'clicked',
            self.on_button_select_folders_clicked,
        )
        vbox.append(child=button_select_files)

    def on_button_select_folder_clicked(self, widget):
        file_dialog = Gtk.FileDialog.new()
        file_dialog.set_title(title='Selecionar pasta')
        file_dialog.set_modal(modal=True)
        file_dialog.select_folder(
            parent=self,
            callback=self.on_file_dialog_dismissed,
        )

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
