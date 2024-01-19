import abc


class PaginaProduto(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def disponibilidade(self) -> bool:
        ...

    @abc.abstractmethod
    def existe_mais_de_um_sku(self) -> bool:
        ...

    @abc.abstractmethod
    def identificar_grade_selecionada(self) -> str:
        ...

    @abc.abstractmethod
    def coletar_preco(self) -> tuple:
        ...

    def all_status_product_page(self) -> tuple:
        disponibilty = self.disponibilidade()
        multiple_grid = self.existe_mais_de_um_sku()
        selected_grid = self.identificar_grade_selecionada()
        spot_price, price = self.coletar_preco()
        return disponibilty, multiple_grid, selected_grid, spot_price, price
