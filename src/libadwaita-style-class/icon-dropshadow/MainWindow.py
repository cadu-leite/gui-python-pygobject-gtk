# -*- coding: utf-8 -*-
"""Python e GTK: PyGObject libadwaita style class icon-dropshadow."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()

TEXT = (
    'Os ícones de aplicativos do GNOME requerem uma sombra para serem legíveis '
    'em um fundo claro. As classes de estilo .icon-dropshadow e .lowres-icon '
    'fornecem isso quando usadas com GtkImage ou qualquer outro widget que '
    'contenha uma imagem.\n'
    '.lowres-icon deve ser usado para ícones de 32×32 ou menores, e '
    '.icon-dropshadow deve ser usado caso contrário.\n'
    'Classes: {}'
)


class ExampleWindow(Gtk.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(
            title='Python e GTK: PyGObject libadwaita style class icon-dropshadow')
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

        self.label = Gtk.Label.new(
            str=TEXT.format("Classes: ['icon-dropshadow']"))
        self.label.set_vexpand(expand=True)
        self.label.set_wrap(wrap=True)
        vbox.append(child=self.label)

        self.image_icon_dropshadow = Gtk.Image.new_from_icon_name(
            icon_name='software-update-urgent-symbolic',
        )
        self.image_icon_dropshadow.set_pixel_size(pixel_size=64)
        self.image_icon_dropshadow.add_css_class(css_class='icon-dropshadow')
        vbox.append(child=self.image_icon_dropshadow)

        button = Gtk.Button.new_with_label(label='Adicionar/remover classe')
        button.set_vexpand(expand=True)
        button.set_valign(align=Gtk.Align.END)
        button.connect('clicked', self.on_button_clicked)
        vbox.append(child=button)

    def on_button_clicked(self, button):
        if 'icon-dropshadow' in self.image_icon_dropshadow.get_css_classes():
            self.image_icon_dropshadow.remove_css_class(
                css_class='icon-dropshadow')
        else:
            self.image_icon_dropshadow.add_css_class(
                css_class='icon-dropshadow')
        self.label.set_text(
            str=TEXT.format(self.image_icon_dropshadow.get_css_classes()),
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
