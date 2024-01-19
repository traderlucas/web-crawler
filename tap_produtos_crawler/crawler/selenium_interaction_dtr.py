import selenium
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
from .selenium_interaction import SeleniumInteraction
from typing import Union


class SeleniumDtrInteraction(SeleniumInteraction):
    def alternar_voltagem(
        self, navegador: selenium.webdriver, url_page: str
    ) -> Union[SeleniumInteraction.pegar_html_selenium, int]:
        navegador.get(url_page)
        WebDriverWait(navegador, 14).until(
            ec.presence_of_element_located((By.CLASS_NAME, "variacao-volt"))
        )
        try:
            navegador.find_element(
                By.XPATH,
                "/html/body/div[1]/div/div[7]/div/div[2]/ \
                div/div/div[3]/div[2]/div[3]/div"
                "/div/div[2]/div",
            ).click()
            WebDriverWait(navegador, 14).until(
                ec.presence_of_element_located((By.ID, "colunadireitaS"))
            )
            sleep(2)
            return self.pegar_html_selenium(navegador)
        except (ElementNotInteractableException, NoSuchElementException):
            return 0
