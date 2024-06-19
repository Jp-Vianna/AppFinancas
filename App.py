import Planilha as Pl
import flet as ft


class Despeza(ft.Column):
    def __init__(self, titulo, valor, tipo):
        super().__init__()
        self.titulo = titulo
        self.valor = float(valor)
        self.tipo = tipo

        self.dados = ft.Row(
            [ft.Text(value=f"{self.titulo}  |  {self.valor}".upper(), color="white", size=20)],
            alignment=ft.MainAxisAlignment.CENTER
        )

        self.controls = [self.dados]


class FinancasApp(ft.Column):
    def __init__(self):
        super().__init__()

        # Exibirá o saldo.
        self.saldo = 0.00
        self.saldo_txt = ft.Text(value=f"R$ 0.00", size=60)

        # Todas as movimentações.
        self.despezas = ft.Column(spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER,)

        # Carrega a planilha para guardar dados.
        self.planilha = Pl.Planilha()

        # Atualiza dados que já estavam guardados.
        self.carrega_mov()

        # Largura das informações.
        self.width = 900

        # Filtro de despezas.
        self.filtro = ft.Tabs(
            scrollable=True,
            animation_duration=300,
            selected_index=0,
            tab_alignment=ft.TabAlignment.CENTER,
            on_change=self.filtro_mudou,
            tabs=[ft.Tab(text="Todas"), ft.Tab(text="Gasto"), ft.Tab(text="Ganho")],
        )

        # GUI para escrever dados da movimentação.
        self.nome_despeza = ft.TextField(hint_text="Título...", width=300)
        self.valor_despeza = ft.TextField(hint_text="Valor...", width=300)
        self.botao_add_movimentacao = ft.TextButton("Adicionar", on_click=self.adiciona_mov_nova, opacity=70, width=180, height=70)
        self.dd = ft.Dropdown(
            width=200,
            options=[
                ft.dropdown.Option("Ganho"),
                ft.dropdown.Option("Gasto"),
            ],
        )

        # Junta os elementos.
        self.visivel_criacao = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            controls=[
                self.nome_despeza,
                self.valor_despeza,
                self.dd,
                self.botao_add_movimentacao,
            ],
        )

        # Adiciona na página.
        self.controls = [
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                spacing=300,
                controls=[
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=90,
                        controls=[
                            ft.Text(value=f"Saldo:", size=40),
                            self.saldo_txt,
                            self.visivel_criacao,
                        ],
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self.filtro,
                            self.despezas,
                        ],
                    ),
                ],
            ),
        ]

    # Adiciona novas despezas a página e na planilha.
    def adiciona_mov_nova(self, e):
        if self.valida_entrada():
            self.adiciona_mov(self.valor_despeza.value, self.nome_despeza.value, self.dd.value)

            self.atualiza_planilha(f"R$ {self.valor_despeza.value}", self.nome_despeza.value, self.dd.value)

            self.limpa_campos()

        self.update()

    def adiciona_mov(self, valor, titulo, tipo):
        despeza = Despeza(titulo, valor, tipo)

        if despeza.tipo == "Gasto":
            self.saldo -= despeza.valor
        else:
            self.saldo += despeza.valor

        self.saldo_txt.value = f"R$ {round(self.saldo, 2)}"

        self.despezas.controls.append(despeza)

    def valida_entrada(self):
        flag = True

        if self.nome_despeza.value == '':
            self.nome_despeza.error_text = "Campo vazio."
            flag = False
        if self.valor_despeza.value == '' or self.valor_despeza.value.__contains__(','):
            self.valor_despeza.error_text = "Campo vazio ou formato errado(Use ponto para separar.)."
            flag = False
        if self.dd.value is None:
            self.dd.error_text = "Campo vazio."
            flag = False

        self.nome_despeza.focus()

        return flag

    def limpa_campos(self):
        self.nome_despeza.value = ''
        self.valor_despeza.value = ''
        self.dd.value = None
        self.dd.error_text = None
        self.valor_despeza.error_text = None
        self.nome_despeza.error_text = None

    def before_update(self):
        status = self.filtro.tabs[self.filtro.selected_index].text

        for despeza in self.despezas.controls:
            despeza.visible = (
                    status == "Todas"
                    or (status == "Gasto" and despeza.tipo == status)
                    or (status == "Ganho" and despeza.tipo == status)
            )

    def atualiza_planilha(self, valor, titulo, tipo):
        self.planilha.add(valor, titulo, tipo)

    def filtro_mudou(self, e):
        self.update()

    def carrega_mov(self):
        for linha in self.planilha.pagina_despezas.iter_rows(min_row=2):
            if any(celulas.value is None for celulas in linha[:3]):
                break
            try:
                valor = linha[0].value[3:]
                titulo = linha[1].value
                tipo = linha[2].value
                self.adiciona_mov(valor, titulo, tipo)
            except Exception as e:
                # Log the error if needed, for now, just print
                print(f"Error processing row {linha}: {e}")


if __name__ == '__main__':
    def main(pagina: ft.Page):
        # Título da página.
        pagina.title = "Gerenciador de gastos"

        # Zera o padding.
        pagina.padding = 0

        # Tamanho da janela.
        pagina.window_height = 700
        pagina.window_width = 900

        pagina.theme = ft.Theme(color_scheme_seed="green")

        # Inicia o app.
        financas_app = FinancasApp()

        # Mostra a GUI.
        pagina.add(financas_app)

        # Adiciona scroll na página.
        pagina.scroll = "ALWAYS"
        # Atualiza a página.
        pagina.update()

    ft.app(target=main)
