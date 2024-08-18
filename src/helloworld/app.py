import toga
from toga.style import Pack
from toga.style.pack import CENTER, COLUMN, ROW, LEFT, RIGHT, BOTTOM
from helloworld.DB_Manager import criar_db, registrar_usuario, autenticar_usuario

class HelloWorld(toga.App):
    def handle_submit(self, widget):
        # Função chamada quando o botão de envio é pressionado
        name = self.name_input.value
        password = self.password_input.value
        
        # Tente autenticar o usuário
        if autenticar_usuario(name, password,".users"):
            status_label.text = "Login bem-sucedido!"
            self.show_dashboard(None)
        else:
            status_label.text = "Nome de usuário ou senha incorretos."

    def startup(self):
        # Crie a base de dados e a tabela, se necessário
        try:(
            criar_db(".users"),
            registrar_usuario("admin","codefas2024",".users")
        )
        except:
            print("Error 1")

        # Crie a caixa principal que ocupa todo o espaço disponível
        self.main_box = toga.Box(style=Pack(alignment=CENTER, padding=0, flex=1))
        self.sec_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER,))
        self.left_bar = toga.Box(style=Pack(alignment=LEFT, direction=ROW, flex=1,))
        self.right_bar = toga.Box(style=Pack(alignment=RIGHT, direction=ROW, flex=1,))

        # Adicione os botões à barra esquerda
        self.home_button = toga.Button(
            icon=toga.Icon("resources/home-50"),
            on_press=self.show_home,
            style=Pack(padding=10, background_color="white")
        )
        
        # Adicione a caixa secundária à caixa principal
        self.main_box.add(self.left_bar)
        self.main_box.add(self.sec_box)
        self.main_box.add(self.right_bar)
        
        # Exibir a tela inicial
        self.show_home(None)

        # Crie e mostre a janela principal com um título
        self.main_window = toga.MainWindow(title="Hello World")
        self.main_window.content = self.main_box
        self.main_window.show()

    def show_home(self, widget):
        # Remove o conteúdo atual de sec_box
        self.sec_box.clear()
        self.sec_box = self.create_home()
        self.left_bar.remove(self.home_button)
        self.main_box.add(self.left_bar)
        self.main_box.add(self.sec_box)
        self.main_box.add(self.right_bar)

    def create_home(self):
        home_box = toga.Box(style=Pack(direction=ROW, alignment=BOTTOM))
        admin_login_button = toga.Button(
            icon=toga.Icon("resources/user-gear-50"),
            on_press=self.show_admin_login,
            style=Pack(padding=10, background_color="white")
        )
        home_box.add(admin_login_button)
        return home_box
        
    def show_admin_login(self, widget):
        # Remove o conteúdo atual de main_box
        self.main_box.clear()
        self.sec_box = self.create_admin_login()
        
        self.left_bar.add(self.home_button)
        self.main_box.add(self.left_bar)
        self.main_box.add(self.sec_box)
        self.main_box.add(self.right_bar)

    def create_admin_login(self):
        global status_label
        
        admin_login_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER))
        
        # Crie e estilize o rótulo e o campo de entrada do nome
        status_label = toga.Label(
            "",
            style=Pack(padding=(10, 5), font_size=12, font_weight='bold', color='#ff0000', text_align=CENTER)
        )
        
        name_label = toga.Label(
            "Nome:",
            style=Pack(padding=(10, 5), font_size=16, font_weight='bold')
        )
        self.name_input = toga.TextInput(style=Pack(width=300, padding=10, font_size=16))

        # Crie uma caixa para o rótulo e o campo de entrada do nome
        name_box = toga.Box(style=Pack(direction=ROW, padding=10, alignment=CENTER))
        name_box.add(name_label)
        name_box.add(self.name_input)

        # Crie e estilize o rótulo e o campo de entrada de senha
        password_label = toga.Label(
            "Senha:",
            style=Pack(padding=(10, 5), font_size=16, font_weight='bold')
        )
        self.password_input = toga.PasswordInput(style=Pack(width=300, padding=10, font_size=16))

        # Crie uma caixa para o rótulo e o campo de entrada de senha
        password_box = toga.Box(style=Pack(direction=ROW, padding=10, alignment=CENTER))
        password_box.add(password_label)
        password_box.add(self.password_input)

        # Crie um botão de envio e associe uma função
        submit_button = toga.Button(
            'Enviar',
            on_press=self.handle_submit,
            style=Pack(width=300, padding=10, font_size=16, background_color='#007bff', color='white')
        )
        
        admin_login_box.add(status_label)
        admin_login_box.add(name_box)
        admin_login_box.add(password_box)
        admin_login_box.add(submit_button)
        return admin_login_box

    def show_dashboard(self, widget):
        # Remove o conteúdo atual de main_box
        self.main_box.clear()
        self.sec_box = self.create_dashboard()
        self.main_box.add(self.left_bar)
        self.main_box.add(self.sec_box)
        self.main_box.add(self.right_bar)

    def create_dashboard(self):
        dashboard_box = toga.Box(style=Pack(direction=COLUMN, alignment="center"))
        dashboard_label = toga.Label("Dashboard", style=Pack(padding=10))
        dashboard_box.add(dashboard_label)
        return dashboard_box

def main():
    return HelloWorld()

if __name__ == '__main__':
    main().main_loop()
