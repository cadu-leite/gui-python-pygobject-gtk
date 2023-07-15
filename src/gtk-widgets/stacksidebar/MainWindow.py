# -*- coding: utf-8 -*-
"""Python e GTK: PyGObject Gtk.StackSidebar()."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()


class ExampleWindow(Gtk.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title='Python e GTK: PyGObject Gtk.Picture()')
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

        hbox = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        # No GTK 3: set_border_width().
        hbox.set_margin_top(margin=12)
        hbox.set_margin_end(margin=12)
        hbox.set_margin_bottom(margin=12)
        hbox.set_margin_start(margin=12)
        # Adicionando o box na janela principal.
        # No GTK 3: add().
        self.set_child(child=hbox)

        page1 = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        # page1.set_homogeneous(homogeneous=True)
        # Utilizando um laço de repetição para criar alguns botões.
        for n in range(5):
            button = Gtk.Button.new_with_label(label=f'Botão {n}')
            page1.append(child=button)

        page2 = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        for n in range(5):
            label = Gtk.Label.new(str=f'Linha {n}')
            page2.append(child=label)

        stack = Gtk.Stack.new()
        # Definindo o efeito de transição.
        stack.set_transition_type(
            transition=Gtk.StackTransitionType.SLIDE_LEFT_RIGHT
        )
        # Definindo o tempo da transição (1000 = 1 segundo).
        stack.set_transition_duration(duration=1000)
        stack.add_titled(child=page1, name='pagina1', title='Página 1')
        stack.add_titled(child=page2, name='pagina2', title='Página 2')
        hbox.append(child=stack)

        # Criando StackSwitcher Layout.
        # Este container é responsável por realizar as trocas.
        stack_sidebar = Gtk.StackSidebar.new()

        # Adicionando o Stack Layout que contém os
        # widgets (Páginas) No StackSwitcher Layout.
        stack_sidebar.set_stack(stack=stack)

        # Adicionando o StackSwitcher Layout no Box Layout principal.
        hbox.prepend(child=stack_sidebar)


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
