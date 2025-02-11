# -*- coding: utf-8 -*-
"""Python e GTK: PyGObject libadwaita Adw.PreferencesWindow()."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()


class AdwPreferencesWindow(Adw.PreferencesWindow):
    """Essa classe pode estar em outro arquivo.
    Está tudo junto para facilitar a execução.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title(
            title='Python e GTK: PyGObject libadwaita Adw.PreferencesWindow()')
        self.set_default_size(width=int(1366 / 2), height=int(768 / 2))
        self.set_size_request(width=int(1366 / 2), height=int(768 / 2))

        adw_preferences_page = Adw.PreferencesPage.new()
        self.add(page=adw_preferences_page)

        button_flat = Gtk.Button.new_with_label(label='Sufixo')
        button_flat.set_icon_name(icon_name='list-add-symbolic')
        button_flat.add_css_class(css_class='flat')
        button_flat.connect('clicked', self.on_button_clicked)

        adw_preferences_group = Adw.PreferencesGroup.new()
        adw_preferences_group.set_title(title='AdwPreferencesPage')
        adw_preferences_group.set_description(
            description='AdwPreferencesGroup')
        adw_preferences_group.set_header_suffix(suffix=button_flat)
        adw_preferences_page.add(group=adw_preferences_group)

        switch_01 = Gtk.Switch.new()
        switch_01.set_valign(align=Gtk.Align.CENTER)
        switch_01.connect('notify::active', self.on_switch_button_clicked)

        adw_action_row_01 = Adw.ActionRow.new()
        adw_action_row_01.add_prefix(
            widget=Gtk.Image.new_from_icon_name(
                icon_name='edit-find-symbolic'),
        )
        adw_action_row_01.set_title(title='Libadwaita')
        adw_action_row_01.set_subtitle(subtitle='Adw.ActionRow()')
        adw_action_row_01.add_suffix(widget=switch_01)
        adw_preferences_group.add(child=adw_action_row_01)

        switch_02 = Gtk.Switch.new()
        switch_02.set_valign(align=Gtk.Align.CENTER)
        switch_02.connect('notify::active', self.on_switch_button_clicked)

        adw_action_row_02 = Adw.ActionRow.new()
        adw_action_row_02.add_prefix(
            widget=Gtk.Image.new_from_icon_name(
                icon_name='edit-find-symbolic'),
        )
        adw_action_row_02.set_title(
            title='Libadwaita - Ao clicar na linha widget ativa e desativa'
        )
        adw_action_row_02.set_subtitle(subtitle='Adw.ActionRow()')
        adw_action_row_02.add_suffix(widget=switch_02)
        adw_action_row_02.set_activatable_widget(widget=switch_02)
        adw_preferences_group.add(child=adw_action_row_02)

    def on_button_clicked(self, button):
        print('Botão pressionado.')

    def on_switch_button_clicked(self, switch, GParamBoolean):
        if switch.get_active():
            print('Botão marcado')
        else:
            print('Botão desmarcado')


class ExampleWindow(Gtk.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(
            title='Python e GTK: PyGObject libadwaita Adw.AdwPreferencesPage()')
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

        label = Gtk.Label.new(str='Acesse o menu e clique em preferências.')
        vbox.prepend(child=label)


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
        adw_preferences_window = AdwPreferencesWindow()
        adw_preferences_window.set_transient_for(
            parent=self.get_active_window(),
        )
        adw_preferences_window.set_default_size(
            width=int(1366 / 3),
            height=int(768 / 3),
        )
        adw_preferences_window.set_size_request(
            width=int(1366 / 3),
            height=int(768 / 3),
        )
        adw_preferences_window.present()

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
