import Planilha as Pl
import flet as ft


class Despeza(ft.Column):
    def __init__(self, titulo, valor, tipo, edita_saldo, remove_despeza, edita_planilha):
        super().__init__()
        self.titulo = titulo
        self.valor = float(valor)
        self.tipo = tipo
        self.edita_saldo = edita_saldo
        self.remove_despeza = remove_despeza
        self.edita_planilha = edita_planilha

        # Elementos expostos para permitir a edição das despezas.
        self.edicao_titulo = ft.TextField(value=self.titulo)
        self.edicao_valor = ft.TextField(value=self.valor)
        self.edicao_tipo = ft.Dropdown(
            value=self.tipo,
            options=[
                ft.dropdown.Option("Ganho"),
                ft.dropdown.Option("Gasto"),
            ],
        )
        # Combina os elementos de edição em um bloco.
        self.edicao = ft.Column(
            visible=False,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edicao_titulo,
                self.edicao_valor,
                self.edicao_tipo,
                ft.TextButton(text="Confirmar", on_click=self.confirma_mudanca),
            ],
        )

        # Bloco onde é exposto os dados inseridos.
        self.dados_display = ft.Text(value=f"{self.titulo} -> {self.tipo} R$ {self.valor:.2f}", color="white", size=15, width=250)
        self.dados = ft.Row(
            visible=True,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self.dados_display,
                ft.TextButton(text="Editar", on_click=self.editar_despeza),
                ft.TextButton(text="Excluir", on_click=self.remove),
            ],
        )

        # Exibe na página do app.
        self.controls = [self.dados, self.edicao]

    # Permite editar os dados de uma movimentação.
    def editar_despeza(self, e):
        self.edita_saldo(self, True)
        self.inverte_visibilidade()

        self.update()

    # Confirma a edição da movimentação.
    def confirma_mudanca(self, e):
        valores_antigos = [self.valor, self.titulo, self.tipo]
        self.atualiza_valores_despeza()
        self.edita_planilha(self, valores_antigos)
        self.edita_saldo(self, False)
        self.atualiza_dados_display()
        self.inverte_visibilidade()
        self.update()

    def remove(self, e):
        self.edita_saldo(self, True)
        self.remove_despeza(self)

    def inverte_visibilidade(self):
        if self.edicao.visible:
            self.edicao.visible = False
        else:
            self.edicao.visible = True

        if self.dados.visible:
            self.dados.visible = False
        else:
            self.dados.visible = True

    def atualiza_dados_display(self):
        self.dados_display.value = f"{self.titulo} -> {self.tipo} R$ {self.valor:.2f}"

    def atualiza_valores_despeza(self):
        self.titulo = self.edicao_titulo.value
        self.valor = float(self.edicao_valor.value)
        self.tipo = self.edicao_tipo.value


class FinancasApp(ft.Column):
    def __init__(self):
        super().__init__()

        # Exibirá o saldo.
        self.saldo = 0.00
        self.saldo_txt = ft.Text(value=f"R$ 0.00", size=60)

        # Exibe todas as movimentações.
        self.despezas = ft.Column(spacing=15, horizontal_alignment=ft.CrossAxisAlignment.START,)

        # Abre a planilha para guardar dados.
        self.planilha = Pl.Planilha()

        # Carrega as movimentações antigas.
        self.carrega_mov()

        # Largura da tela ocupada.
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
        self.criacao = ft.Column(
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
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                controls=[
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=90,
                        controls=[
                            ft.Text(value=f"Saldo:", size=40),
                            self.saldo_txt,
                            self.criacao,
                        ],
                    ),
                    ft.Column(
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        height=600,
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

            self.planilha.adiciona_linha(f"R$ {self.valor_despeza.value}", self.nome_despeza.value, self.dd.value)

            self.limpa_campos()

        self.update()

    def adiciona_mov(self, valor, titulo, tipo):
        despeza = Despeza(titulo, valor, tipo, self.caso_despeza_alterada, self.remove_despeza, self.edita_planilha)

        self.atualiza_saldo(despeza)

        self.altera_display_saldo()

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

    def filtro_mudou(self, e):
        self.update()

    def atualiza_saldo(self, despeza):
        if despeza.tipo == "Gasto":
            self.saldo -= despeza.valor
        else:
            self.saldo += despeza.valor

    def caso_despeza_alterada(self, despeza, reverte):
        if reverte:
            if despeza.tipo == "Gasto":
                self.saldo += despeza.valor
            else:
                self.saldo -= despeza.valor
        else:
            if despeza.tipo == "Gasto":
                self.saldo -= despeza.valor
            else:
                self.saldo += despeza.valor

        self.altera_display_saldo()
        self.update()

    def remove_despeza(self, despeza):
        self.planilha.remove(despeza)
        self.despezas.controls.remove(despeza)
        self.update()

    def edita_planilha(self, despeza, valores_antigos):
        self.planilha.edita(despeza, valores_antigos)

    def altera_display_saldo(self):
        self.saldo_txt.value = f"R$ {self.saldo:.2f}"

    def carrega_mov(self):
        for linha in self.planilha.pagina_despezas.iter_rows(min_row=2):
            if any(celulas.value is None for celulas in linha[:3]):
                break
            try:
                self.adiciona_mov(linha[0].value[3:], linha[1].value, linha[2].value)
            except Exception as e:
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
