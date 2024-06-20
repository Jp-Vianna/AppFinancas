import openpyxl


class Planilha:
    def __init__(self):
        # Abre planilha.
        self.book = openpyxl.load_workbook('PlanilhaDespezas.xlsx')

        # Seleciona página a ser trabalhada.
        self.pagina_despezas = self.book["Despezas"]

    def adiciona_linha(self, valor, titulo, tipo):
        # Adiciona nova linha.
        self.pagina_despezas.append([valor, titulo, tipo])
        # Salva mudanças do arquivo.
        self.book.save('PlanilhaDespezas.xlsx')

    # for linha in self.planilha.pagina_despezas.iter_rows(min_row=2):
    #     if any(celulas.value is None for celulas in linha[:3]):
    #         break

    def remove(self, despeza):
        contador = 1
        for linha in self.pagina_despezas.iter_rows(min_row=2):
            contador += 1

            if self.verifica_vazio(linha):
                return

            if self.verifica_igualdade(linha, despeza.valor, despeza.titulo, despeza.tipo):
                self.pagina_despezas.delete_rows(contador, 1)
                self.book.save("PlanilhaDespezas.xlsx")
                break

    def edita(self, despeza, valores):
        for linha in self.pagina_despezas.iter_rows(min_row=2):
            print(self.verifica_vazio(linha))
            if self.verifica_vazio(linha):
                return

            print(self.verifica_igualdade(linha, valores[0], valores[1], valores[2]))
            if self.verifica_igualdade(linha, valores[0], valores[1], valores[2]):
                linha[0].value = f"R$ {despeza.valor:.2f}"
                linha[1].value = despeza.titulo
                linha[2].value = despeza.tipo
                self.book.save("PlanilhaDespezas.xlsx")
                break

    @staticmethod
    def verifica_igualdade(linha, valor, titulo, tipo):
        return (float(linha[0].value[3:]) == valor) and (linha[1].value == titulo) and (linha[2].value == tipo)

    @staticmethod
    def verifica_vazio(linha):
        return any(celulas.value is None for celulas in linha[:3])


