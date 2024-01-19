import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from tap_produtos_crawler.crawler.pagina_produto_ldm import PaginaProdutoLdm
from tap_produtos_crawler.crawler.pagina_produto_dtr import PaginaProdutoDtr
from tap_produtos_crawler.crawler.pagina_produto_knd import PaginaProdutoKnd
import tap_produtos_crawler.crawler.planilha_toscrape as planilha_toscrape
import tap_produtos_crawler.crawler.salvar_ajustar.salvar_ajustar as sv
from tap_produtos_crawler.crawler.collected_data import SpreadsheetCollectData
from tap_produtos_crawler.crawler.selenium_interaction_ldm import (
    SeleniumLdmInteraction,
)
from tap_produtos_crawler.crawler.selenium_interaction_dtr import (
    SeleniumDtrInteraction,
)
from tap_produtos_crawler.crawler.selenium_interaction_knd import (
    SeleniumKndInteraction,
)
from typing import Union
from time import sleep
import pandas as pd
from io import StringIO
from webdriver_manager.chrome import ChromeDriverManager
import singer

LOGGER = singer.get_logger()


def iniciar_chrome() -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--verbose")
    chrome_options.add_experimental_option(
        "prefs",
        {
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False,
        },
    )
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), chrome_options=chrome_options
    )

    return driver


def get_spreadsheet_to_scrape():
    planilha_to_scrape = sv.gerar_dataframe(sv.escolher_arquivo())
    planilha_to_scrape = planilha_to_scrape.fillna(" ")
    return planilha_to_scrape


def transform_in_list(planilha_to_scrape):
    try:
        to_scraping = planilha_toscrape.PlanilhaToScrape(
            planilha_to_scrape
        ).transformar_em_lista()
        return to_scraping
    except planilha_toscrape.FormatoPlanilhaErrado:
        print(
            "Houve um problema ao transformar seus dados! \
            Tente verificar o nome de suas colunas"
        )
        exit()


def get_page(url_pagina_produto) -> Union[BeautifulSoup, int]:
    try:
        site = requests.get(url_pagina_produto)  # headers=HEADER optional
        conteudo = site.content
        pagina = BeautifulSoup(
            conteudo.decode("utf-8", "ignore"), features="lxml"
        )
        return pagina
    except requests.exceptions.InvalidURL:
        print("URL INVÁLIDA")
        return 0


def get_model_page(
    page_model_to_scrape: Union[
        PaginaProdutoLdm, PaginaProdutoDtr, PaginaProdutoKnd
    ],
    page: BeautifulSoup(),
):
    return page_model_to_scrape(page)


def get_page_status(
    page_model_to_scrape: Union[
        PaginaProdutoLdm, PaginaProdutoDtr, PaginaProdutoKnd
    ]
) -> tuple:
    return page_model_to_scrape.all_status_product_page()


def check_if_needs_selenium(
    grade_pre_selecionada: str, searched_grid: str, multiplas_grades: bool
) -> bool:
    if (
        grade_pre_selecionada == searched_grid
        or searched_grid not in "110V220V"
        or not multiplas_grades
    ):
        return True
    else:
        return False


def main_extract(tap_stream_id, products):
    products = str(products, "utf-8")
    products = StringIO(products)
    planilha_to_scrape = pd.read_csv(products)

    if tap_stream_id == "ldm":
        iteraction_model: Union[
            SeleniumDtrInteraction,
            SeleniumLdmInteraction,
            SeleniumKndInteraction,
        ] = SeleniumLdmInteraction()

        page_model_to_scrape: Union[
            PaginaProdutoLdm, PaginaProdutoDtr, PaginaProdutoKnd
        ] = PaginaProdutoLdm

    elif tap_stream_id == "dutra":
        iteraction_model: Union[
            SeleniumDtrInteraction,
            SeleniumLdmInteraction,
            SeleniumKndInteraction,
        ] = SeleniumDtrInteraction()

        page_model_to_scrape: Union[
            PaginaProdutoLdm, PaginaProdutoDtr, PaginaProdutoKnd
        ] = PaginaProdutoDtr

    elif tap_stream_id == "knd":
        iteraction_model: Union[
            SeleniumDtrInteraction,
            SeleniumLdmInteraction,
            SeleniumKndInteraction,
        ] = SeleniumKndInteraction()

        page_model_to_scrape: Union[
            PaginaProdutoLdm, PaginaProdutoDtr, PaginaProdutoKnd
        ] = PaginaProdutoKnd
    else:
        raise Exception()

    planilha_to_scrape = planilha_to_scrape.fillna(" ")
    chrome = iniciar_chrome()
    to_scraping = []
    collected_data = SpreadsheetCollectData()
    progress = 0
    to_scraping = transform_in_list(planilha_to_scrape)

    for record_to_collect in to_scraping:
        sleep(1)
        progress += 1
        LOGGER.info(f"Progress: {progress}")
        sku_ferimport = record_to_collect[0]
        url_product = record_to_collect[1]
        searched_grid = str(record_to_collect[2]).upper().replace("V", "")
        page = get_page(url_product)

        if page != 0:
            product_page = get_model_page(page_model_to_scrape, page)
            (
                disponibilidade,
                multiplas_grades,
                selected_grid,
                spot_price,
                price,
            ) = get_page_status(product_page)
            # testing if interaction is necessary
            if check_if_needs_selenium(
                selected_grid, searched_grid, multiplas_grades
            ):
                pass
            elif searched_grid in "110V220V":
                # NEEDS VALIDATION
                page = iteraction_model.alternar_voltagem(chrome, url_product)
                # if it returns 0 is because there is no iterable button
                if page != 0:
                    setattr(product_page, "pagina_produto", page)
                    (
                        disponibilidade,
                        multiplas_grades,
                        selected_grid,
                        spot_price,
                        price,
                    ) = product_page.all_status_product_page()
                else:
                    print("Ocorreu algum erro ao interagir com a página")
            collected_data.add_price_collect(
                url_product,
                searched_grid,
                selected_grid,
                spot_price,
                price,
                disponibilidade,
                sku_ferimport,
            )
        else:
            collected_data.add_url_error(
                url_product, sku_ferimport, searched_grid
            )
    data = collected_data.save_collected_data()

    return data
