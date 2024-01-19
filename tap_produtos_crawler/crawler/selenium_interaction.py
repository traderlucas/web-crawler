import abc
from bs4 import BeautifulSoup


class SeleniumInteraction(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def alternar_voltagem(self, navegador, url_page) -> int:
        ...

    @staticmethod
    def pegar_html_selenium(navegador) -> BeautifulSoup:
        html = navegador.page_source
        pagina_navegador = BeautifulSoup(html, features="lxml")
        return pagina_navegador
