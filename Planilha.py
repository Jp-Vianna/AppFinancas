import openpyxl


class Planilha:
    def __init__(self):
        self.nome_planilha = "PlanilhaMovs.xlsx"
        self.book = openpyxl.load_workbook(self.nome_planilha)     # Abre planilha.
        self.pagina_movs = self.book["Movimentações"]                # Seleciona página a ser trabalhada.

    def adiciona_linha(self, valor, titulo, tipo):
        self.pagina_movs.append([valor, titulo, tipo])      # Adiciona nova linha.
        self.book.save(self.nome_planilha)                 # Salva mudanças do arquivo.

    # Remove uma linha da planilha.
    def remove(self, mov):
        contador = 1        # Conta as linhas percorridas.
        for linha in self.pagina_movs.iter_rows(min_row=2):     # Percorre todas as linhas do arquivo.
            contador += 1       # Incrementa.

            if self.verifica_vazio(linha):      # Se a linha é vazia, para.
                return

            if self.verifica_igualdade(linha, mov.valor, mov.titulo, mov.tipo):         # Se a linha é a procurada, exclui.
                self.pagina_movs.delete_rows(contador, 1)                             # Exclui a linha do index atual(contador).
                self.book.save(self.nome_planilha)                                        # Salva modificações.

                break

    # Método que procura uma linha para substituir pelos novos valores.
    def edita(self, mov, valores):
        for linha in self.pagina_movs.iter_rows(min_row=2):
            if self.verifica_vazio(linha):
                return

            if self.verifica_igualdade(linha, valores[0], valores[1], valores[2]):      # Se for a linha procurada, substitui.
                linha[0].value = f"R$ {mov.valor:.2f}"                  # Substitui todos os valores.
                linha[1].value = mov.titulo
                linha[2].value = mov.tipo

                self.book.save(self.nome_planilha)

                break

    # Método estático que verifica se a linha da planilha é igual aos dados procurados.
    @staticmethod
    def verifica_igualdade(linha, valor, titulo, tipo):
        return (float(linha[0].value[3:]) == valor) and (linha[1].value == titulo) and (linha[2].value == tipo)

    # Método estático que verifica se alinha está vazia.
    @staticmethod
    def verifica_vazio(linha):
        return any(celulas.value is None for celulas in linha[:3])
