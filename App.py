import Planilha as Pl
import flet as ft


class Movimentacao(ft.Column):
    def __init__(self, titulo, valor, tipo, edita_saldo, remove_mov, edita_planilha):
        super().__init__()

        # Dados da movimentação.
        self.titulo = titulo
        self.valor = float(valor)
        self.tipo = tipo

        # Métodos da classe FinancasApp.
        self.edita_saldo = edita_saldo
        self.remove_mov = remove_mov
        self.edita_planilha = edita_planilha

        # Elementos expostos para permitir a edição das movimentações.
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
                ft.TextButton(text="Editar", on_click=self.editar_mov),
                ft.TextButton(text="Excluir", on_click=self.remove),
            ],
        )

        # Exibe na página do app.
        self.controls = [self.dados, self.edicao]

    # Permite editar os dados de uma movimentação.
    def editar_mov(self, e):
        self.edita_saldo(self, True)  # Reverte o valor digitado do saldo.
        self.inverte_visibilidade()   # Mostra os controles de edição.

        self.update()

    # Confirma a edição da movimentação.
    def confirma_mudanca(self, e):
        valores_antigos = [self.valor, self.titulo, self.tipo]  # Salva valores antigos para procurar e subtituir na planilha.
        self.atualiza_valores_mov()                             # Troca os valores antigos pelos novos digitados.
        self.edita_planilha(self, valores_antigos)              # Troca os valores editados na planilha.
        self.edita_saldo(self, False)                           # Faz a mudança no saldo total com o novo valor.
        self.atualiza_dados_display()                           # Atualiza os dados da despeza que aparece na tela.
        self.inverte_visibilidade()                             # Esconde os controles de edição.

        self.update()

    # Remove uma movimentação.
    def remove(self, e):
        self.edita_saldo(self, True)        # Descarta a despeza do saldo.
        self.remove_mov(self)           # Chama o método da classe FinancasApp.

    # Troca a visibilidade dos controles de edição.
    # Se tiver visível fica invisível e vice-versa.
    def inverte_visibilidade(self):
        if self.edicao.visible:
            self.edicao.visible = False
        else:
            self.edicao.visible = True

        if self.dados.visible:
            self.dados.visible = False
        else:
            self.dados.visible = True

    # Apenas troca os valores mostrados na tela após uma edição.
    def atualiza_dados_display(self):
        self.dados_display.value = f"{self.titulo} -> {self.tipo} R$ {self.valor:.2f}"

    # Substitui os valores antigos do objeto pelos substituidos.
    def atualiza_valores_mov(self):
        self.titulo = self.edicao_titulo.value
        self.valor = float(self.edicao_valor.value)
        self.tipo = self.edicao_tipo.value


class FinancasApp(ft.Column):
    def __init__(self):
        super().__init__()

        # Exibirá o saldo.
        self.saldo = 0.00
        self.saldo_txt = ft.Text(value=f"R$ 0.00", size=60)     # Será mostrado na tela do App.

        # Exibe todas as movimentações.
        self.movs = ft.Column(spacing=15, horizontal_alignment=ft.CrossAxisAlignment.START,)

        # Abre a planilha para guardar dados.
        self.planilha = Pl.Planilha()

        # Carrega as movimentações antigas.
        self.carrega_mov()

        # Largura da tela ocupada.
        self.width = 900

        # Filtro de movimentações.
        self.filtro = ft.Tabs(
            scrollable=True,
            animation_duration=300,
            selected_index=0,
            tab_alignment=ft.TabAlignment.CENTER,
            on_change=self.filtro_mudou,
            tabs=[ft.Tab(text="Todas"), ft.Tab(text="Gasto"), ft.Tab(text="Ganho")],
        )

        # Áreas para input dos dados da movimentação.
        self.nome_mov = ft.TextField(hint_text="Título...", width=300)
        self.valor_mov = ft.TextField(hint_text="Valor...", width=300)
        self.botao_add_mov = ft.TextButton("Adicionar", on_click=self.adiciona_mov_nova, opacity=70, width=180, height=70)
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
                self.nome_mov,
                self.valor_mov,
                self.dd,
                self.botao_add_mov,
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
                            self.movs,
                        ],
                    ),
                ],
            ),
        ]

    # Adiciona novas movimentações a página e na planilha.
    def adiciona_mov_nova(self, e):
        if self.valida_entrada():       # Valida se os campos estão preenchidos e corretos.
            self.adiciona_mov(self.valor_mov.value, self.nome_mov.value, self.dd.value)     # Adiciona a nova movimentação.

            self.planilha.adiciona_linha(f"R$ {self.valor_mov.value}", self.nome_mov.value, self.dd.value)      # Adiciona a movimentação na planilha.

            self.limpa_campos()     # Após a criação limpa a área do input para uma nova movimentação ser digitada.

        self.update()

    # Consolida a criação de uma movimentação de dinheiro.
    # Usada tanto para criar uma nova como carregar alguma digitada anteriormente.
    def adiciona_mov(self, valor, titulo, tipo):
        # Cria objeto despeza.
        mov = Movimentacao(titulo, valor, tipo, self.caso_mov_alterada, self.remove_mov, self.edita_planilha)

        self.atualiza_saldo(mov)        # Atualiza o saldo total.

        self.altera_display_saldo()         # Atualiza o valor mostrado na tela.

        self.movs.controls.append(mov)      # Mostra a despeza adicionada na tela.

    # Verifica se os campos de input estão vazios.
    # Caso exista algum campo vazio a movimentação não é criada.
    def valida_entrada(self):
        flag = True

        if self.nome_mov.value == '':
            self.nome_mov.error_text = "Campo vazio."
            flag = False
        if self.valor_mov.value == '' or self.valor_mov.value.__contains__(','):
            self.valor_mov.error_text = "Campo vazio ou formato errado(Use ponto para separar.)."
            flag = False
        if self.dd.value is None:
            self.dd.error_text = "Campo vazio."
            flag = False

        self.nome_mov.focus()

        return flag

    # Limpa a área de inputs de dados.
    def limpa_campos(self):
        self.limpa_input()
        self.limpa_error_text()

    # Retira input anterior.
    def limpa_input(self):
        self.nome_mov.value = ''
        self.valor_mov.value = ''
        self.dd.value = None

    # Retira input error_text.
    def limpa_error_text(self):
        self.dd.error_text = None
        self.valor_mov.error_text = None
        self.nome_mov.error_text = None

    # Deve ser realizado antes de fazer o update da tela.
    # Realiza a filtragem das movimentações pelo tipo.
    def before_update(self):
        status = self.filtro.tabs[self.filtro.selected_index].text

        for mov in self.movs.controls:
            mov.visible = (
                    status == "Todas"
                    or (status == "Gasto" and mov.tipo == status)
                    or (status == "Ganho" and mov.tipo == status)
            )

    # Caso a filtragem tenha sido mudada pelo usuário, atualiza a tela.
    def filtro_mudou(self, e):
        self.update()

    # Altera o saldo de acordo com o tipo de movimentação.
    def atualiza_saldo(self, mov):
        if mov.tipo == "Gasto":
            self.saldo -= mov.valor
        else:
            self.saldo += mov.valor

    # Executado em casos em que o valor da movimentação foi alterado(Editado ou excluido).
    def caso_mov_alterada(self, mov, reverte):
        if reverte:     # Se o reverte for true, o programa deve desfazer a movimentação.
            if mov.tipo == "Gasto":
                self.saldo += mov.valor
            else:
                self.saldo -= mov.valor
        else:       # Senão, ele faz a movimentação normalmente.
            if mov.tipo == "Gasto":
                self.saldo -= mov.valor
            else:
                self.saldo += mov.valor

        self.altera_display_saldo()

        self.update()

    # Remove a movimentação da planilha e tela do app.
    def remove_mov(self, mov):
        self.planilha.remove(mov)
        self.movs.controls.remove(mov)

        self.update()

    # Faz a edição dos dados digitados na planilha.
    def edita_planilha(self, mov, valores_antigos):
        self.planilha.edita(mov, valores_antigos)       # Chama o método da planilha.

    # Atualiza o saldo mostrado na tela.
    def altera_display_saldo(self):
        self.saldo_txt.value = f"R$ {self.saldo:.2f}"

    # Faz a reintrodução dos dados que já foram digitados, salvos na planilha.
    def carrega_mov(self):
        for linha in self.planilha.pagina_movs.iter_rows(min_row=2):        # Percorre todas as linhas da planilha.
            if any(celulas.value is None for celulas in linha[:3]):             # Caso encontre uma linha vazia, para.
                break
            try:
                self.adiciona_mov(linha[0].value[3:], linha[1].value, linha[2].value)   # Caso contrário recria a movimentação.
            except Exception as e:
                print(f"Error processing row {linha}: {e}")


if __name__ == '__main__':
    def main(pagina: ft.Page):
        # Título da página.
        pagina.title = "Gerenciador de gastos"

        # Zera o padding.
        pagina.padding = 0

        # Tamanho da janela.
        pagina.window_height = 900
        pagina.window_width = 1200

        # Cor do app.
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
