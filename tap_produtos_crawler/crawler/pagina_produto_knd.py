from bs4 import BeautifulSoup
import re
from .pagina_produto import PaginaProduto


class PaginaProdutoKnd(PaginaProduto):
    pagina_produto: BeautifulSoup

    def __init__(self, pagina: BeautifulSoup):
        self.pagina_produto = pagina
        self.flag_grid = 0
        pass

    # ok
    def disponibilidade(self) -> bool:
        obj = self.pagina_produto.find(
            "button", {"class": "btn btn-success btn-block ml-4"}
        )
        if obj:
            disponivel = True
        else:
            disponivel = False
        return disponivel

    def existe_mais_de_um_sku(self) -> bool:
        obj = self.pagina_produto.find(
            "div", {"class": "options-product mb-2"}
        )
        if obj:
            existe_grade = True
        else:
            existe_grade = False
        return existe_grade

    # há casos de preços diferentes!
    # 100% das vezes que foi verificado o primeiro era 127
    def identificar_grade_selecionada(self) -> str:
        grade_ja_selecionada = ""
        select = self.pagina_produto.find(
            "div", {"class": "options-product mb-2"}
        )
        try:
            options = select.find_all("option")
            grid = options[1].text

            if self.flag_grid == 0:
                if "127" in grid or "110" in grid:
                    grade_ja_selecionada = "110"
                elif "220" in grid:
                    grade_ja_selecionada = "220"
            else:
                grid = options[2].text
                if "127" in grid or "110" in grid:
                    grade_ja_selecionada = "110"
                elif "220" in grid:
                    grade_ja_selecionada = "220"
            self.flag_grid += 1
            return grade_ja_selecionada
        except AttributeError:
            return grade_ja_selecionada

    # ok
    def coletar_preco(self) -> tuple:
        def preco_vista():
            try:
                text = self.pagina_produto.find(
                    "input", {"id": "valor-padrao-prod"}
                )
                text = re.findall("[0-9,]", str(text))
                var_price = "".join(text)
            except AttributeError:
                var_price = 0
            return var_price

        def preco_prazo():
            var_price = ""
            try:
                text = self.pagina_produto.find(
                    "span", {"class": "parcelas"}
                ).text
                if text:
                    digits_price = re.findall("[0-9,x]", str(text))
                    digits_price = "".join(digits_price)
                    digits_price = digits_price.replace(",", ".")
                    split_data = digits_price.split("x")
                    if len(split_data) == 1:
                        var_price = split_data[0]
                    elif len(split_data) == 2:
                        try:
                            valor_parcela = int(float(split_data[1]) * 100)
                            parcela = int(split_data[0])
                            var_price = valor_parcela * parcela / 100
                        except ValueError:
                            print(
                                "Houve um erro ao tentar parsear \
                                    as informações de parcelamento."
                            )
                            var_price = "Houve um erro ao tentar parsear \
                                as informações de parcelamento."
                    else:
                        var_price = "Houve um erro ao tentar parsear \
                            as informações de parcelamento."
            except AttributeError:
                ...
            return var_price

        preco_vista = preco_vista()
        preco_prazo = preco_prazo()
        return preco_vista, preco_prazo
