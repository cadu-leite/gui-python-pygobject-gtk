# -*- coding: utf-8 -*-
"""Python e GTK: PyGObject libadwaita style class inline."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()

TEXT = (
    'Por predefinição, a GtkSearchBar e a AdwTabBar parecem fazer parte de '
    'uma AdwHeaderBar ou GtkHeaderBar e destinam-se a ser utilizadas '
    'directamente ligadas a uma. Com a classe de estilo .inline, têm fundos '
    'neutros e podem ser utilizados em contextos diferentes.\n'
    'Classes: {}.'
)


class ExampleWindow(Adw.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title='Python e GTK: PyGObject style classe inline')
        self.set_default_size(width=int(1366 / 2), height=int(768 / 2))
        self.set_size_request(width=int(1366 / 2), height=int(768 / 2))

        mbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.set_content(content=mbox)

        header_bar = Gtk.HeaderBar.new()
        mbox.append(child=header_bar)

        menu_button_model = Gio.Menu()
        menu_button_model.append('Preferências', 'app.preferences')

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        header_bar.pack_end(child=menu_button)

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        mbox.append(child=vbox)

        entry = Gtk.Entry.new()
        entry.set_icon_from_icon_name(
            icon_pos=Gtk.EntryIconPosition.PRIMARY,
            icon_name='system-search-symbolic',
        )

        self.search_bar = Gtk.SearchBar.new()
        self.search_bar.set_search_mode(search_mode=True)
        self.search_bar.set_child(child=entry)
        self.search_bar.add_css_class(css_class='inline')
        header_bar.pack_start(child=self.search_bar)

        self.label = Gtk.Label.new(str=TEXT.format("['inline']"))
        self.label.set_vexpand(expand=True)
        self.label.set_wrap(wrap=True)
        vbox.append(child=self.label)

        button = Gtk.Button.new_with_label(label='Adicionar/remover classe')
        button.connect('clicked', self.on_button_clicked)
        vbox.append(child=button)

    def on_button_clicked(self, button):
        if 'inline' in self.search_bar.get_css_classes():
            self.search_bar.remove_css_class(css_class='inline')
        else:
            self.search_bar.add_css_class(css_class='inline')
        self.label.set_text(
            str=TEXT.format(f'{self.search_bar.get_css_classes()}'),
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
