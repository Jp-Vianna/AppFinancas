import openpyxl


class Planilha:
    def __init__(self):
        # Abre planilha.
        self.book = openpyxl.load_workbook('PlanilhaDespezas.xlsx')

        # Seleciona página a ser trabalhada.
        self.pagina_despezas = self.book["Despezas"]

    def add(self, valor, titulo, tipo):
        # Adiciona nova linha.
        self.pagina_despezas.append([valor, titulo, tipo])
        # Salva mudanças do arquivo.
        self.book.save('PlanilhaDespezas.xlsx')
