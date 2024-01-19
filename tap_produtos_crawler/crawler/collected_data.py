from pandas import DataFrame


class SpreadsheetCollectData:

    dataFrameDict = {
        "URL Produto": [],
        "SKU Ferimport": [],
        "Grade Ferimport": [],
        "Grade Concorrente": [],
        "Preço a Vista": [],
        "Preço a Prazo": [],
        "Disponibilidade": [],
        "Observação": [],
    }

    def __init__(self):
        pass

    def add_url_error(
        self, product_url: str, sku_ferimport: int, grade_ferimport: str
    ) -> None:
        error_message = "invalid url"
        self.dataFrameDict["URL Produto"].append(product_url)
        self.dataFrameDict["SKU Ferimport"].append(sku_ferimport)
        self.dataFrameDict["Grade Ferimport"].append(grade_ferimport)
        self.dataFrameDict["Grade Concorrente"].append(error_message)
        self.dataFrameDict["Preço a Vista"].append(error_message)
        self.dataFrameDict["Preço a Prazo"].append(error_message)
        self.dataFrameDict["Disponibilidade"].append(error_message)
        self.dataFrameDict["Observação"].append(error_message)

    def add_price_collect(
        self,
        product_url,
        grade_ferimport,
        grade_concorrente,
        spot_price,
        price,
        disponibility,
        sku_ferimport,
    ):
        self.dataFrameDict["URL Produto"].append(product_url)
        self.dataFrameDict["SKU Ferimport"].append(sku_ferimport)
        self.dataFrameDict["Grade Ferimport"].append(grade_ferimport)
        self.dataFrameDict["Grade Concorrente"].append(grade_concorrente)
        if not str(spot_price).startswith("R$"):
            spot_price = f"R${str(spot_price)}"
        self.dataFrameDict["Preço a Vista"].append(spot_price)
        if not str(price).startswith("R$"):
            price = f"R${str(price)}"
        self.dataFrameDict["Preço a Prazo"].append(price)
        self.dataFrameDict["Disponibilidade"].append(disponibility)
        if grade_ferimport != grade_concorrente and grade_ferimport != " ":
            observacao = "não há grade correspondente"
        else:
            observacao = "ok"
        self.dataFrameDict["Observação"].append(observacao)

    def incrementar_lista_verifica_grade(self, product_url, multiple_grid):
        self.dataFrameDict["URL Produto"].append(product_url)
        self.dataFrameDict["Grade Concorrente"].append(multiple_grid)

    def save_collected_data(self):
        dataFrame = DataFrame.from_dict(self.dataFrameDict)
        df = self.transform_df(dataFrame)
        return df.to_dict("records")

    def transform_df(self, df):
        df.rename(
            columns={
                "URL Produto": "URL",
                "SKU Ferimport": "sku_ferimport",
                "Grade Ferimport": "grade_ferimport",
                "Grade Concorrente": "grade_concorrente",
                "Preço a Vista": "preco_vista",
                "Preço a Prazo": "preco_prazo",
                "Disponibilidade": "disponibilidade",
                "Observação": "observacao",
            },
            inplace=True,
        )

        return df
