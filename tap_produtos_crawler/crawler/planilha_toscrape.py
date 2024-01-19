class FormatoPlanilhaErrado(Exception):
    """Verifique o formato da planilha selecionada"""

    pass


class PlanilhaToScrape:
    import pandas as pd

    planilha = pd.DataFrame
    coluna_a: str = "sku"
    coluna_b: str = "url"
    coluna_c: str = "voltagem"
    status_ok: bool = bool

    def __init__(self, planilha: pd.DataFrame):
        self.planilha = planilha
        self.status_ok = self.checar_colunas()

    # body of the constructor

    def checar_colunas(self) -> bool:
        nomes_colunas = self.planilha.columns
        planilha_correta = False
        if (
            (str(nomes_colunas[0]).strip().lower() == self.coluna_a)
            & (str(nomes_colunas[1]).strip().lower() == self.coluna_b)
            & (str(nomes_colunas[2]).strip().lower() == self.coluna_c)
        ):
            planilha_correta = True

        return planilha_correta

    def transformar_em_lista(self) -> list:
        if self.status_ok:
            lista = self.planilha.values.tolist()
            return lista
        else:
            raise FormatoPlanilhaErrado()


if __name__ == "__main__":
    pass
