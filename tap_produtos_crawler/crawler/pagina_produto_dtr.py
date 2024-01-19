from bs4 import BeautifulSoup
from .pagina_produto import PaginaProduto


class PaginaProdutoDtr(PaginaProduto):
    pagina_produto: BeautifulSoup

    def __init__(self, pagina: BeautifulSoup):
        self.pagina_produto = pagina
        pass

    def disponibilidade(self) -> bool:
        try:
            text = self.pagina_produto.find(
                "div", {"class": "btn_aviseme interna"}
            ).get_text()
            disponivel = False if text else True
        except AttributeError:
            disponivel = True
        return disponivel

    # OK
    def existe_mais_de_um_sku(self) -> bool:
        existe_mais_de_uma_grade = False
        try:
            text_list = self.pagina_produto.find(
                "div", class_="produtoSelect"
            ).text.split(" ")
            text = "".join(text_list).replace("\n", "").replace("V", "")
            existe_mais_de_uma_grade = True if text == "110220" else False
        except AttributeError:
            existe_mais_de_uma_grade = False
        finally:
            return existe_mais_de_uma_grade

    def identificar_grade_selecionada(self) -> str:
        try:
            grade_ja_selecionada = (
                self.pagina_produto.find("span", "variacao-volt active")
                .text.split()[0]
                .upper()
                .replace("V", "")
            )
        except AttributeError:
            grade_ja_selecionada = "Não há"
        return grade_ja_selecionada

    # OK
    def coletar_preco(self) -> tuple:
        try:
            preco_vista = self.pagina_produto.find(
                "span", {"data-locale": "pt_BR"}
            ).text.replace(".", ",")
        except AttributeError:
            preco_vista = ""

        try:
            preco_prazo_phrase = (
                self.pagina_produto.find("div", class_="ou-sem-juros")
                .text.replace("&nbsp", " ")
                .split()
            )
            preco_prazo = (
                preco_vista
                if preco_prazo_phrase[2].isalpha()
                else preco_prazo_phrase[2]
            )
        except AttributeError:
            preco_prazo = ""
        return preco_vista, preco_prazo
