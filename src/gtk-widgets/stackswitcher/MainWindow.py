# -*- coding: utf-8 -*-
"""Python e GTK: PyGObject Gtk.StackSwitcher()."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()


class ExampleWindow(Gtk.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title='Python e GTK: PyGObject Gtk.StackSwitcher()')
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

        header_bar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=header_bar)

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        self.set_child(child=vbox)

        stack = Gtk.Stack.new()
        # Definindo o efeito de transição.
        stack.set_transition_type(
            transition=Gtk.StackTransitionType.SLIDE_LEFT_RIGHT
        )
        # Definindo o tempo da transição (1000 = 1 segundo).
        stack.set_transition_duration(duration=1000)

        page1 = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        # Adicionando o Box Layout 1 no Stack Layout.
        stack.add_titled(child=page1, name='pagina1', title='Página 1')
        vbox.append(child=stack)

        # Utilizando um laço de repetição para criar alguns botões.
        for n in range(5):
            botao = Gtk.Button.new_with_label(label=f'Botão {n}')
            page1.append(child=botao)

        page2 = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        stack.add_titled(child=page2, name='pagina2', title='Página 2')

        for n in range(5):
            label = Gtk.Label.new(str=f'Linha {n}')
            page2.append(child=label)

        stack_switcher = Gtk.StackSwitcher.new()
        stack_switcher.set_stack(stack=stack)
        header_bar.set_title_widget(title_widget=stack_switcher)


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
