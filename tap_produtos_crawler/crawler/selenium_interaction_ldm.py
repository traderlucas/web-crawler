import selenium
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
from .selenium_interaction import SeleniumInteraction
from typing import Union


class SeleniumLdmInteraction(SeleniumInteraction):
    def alternar_voltagem(
        self, navegador: selenium.webdriver, url_page: str
    ) -> Union[SeleniumInteraction.pegar_html_selenium, int]:
        navegador.get(url_page)
        WebDriverWait(navegador, 14).until(
            ec.presence_of_element_located((By.ID, "product"))
        )
        try:
            navegador.find_element(By.CLASS_NAME, "btn-secondary").click()
            WebDriverWait(navegador, 14).until(
                ec.presence_of_element_located((By.ID, "product"))
            )
            sleep(2)
            return self.pegar_html_selenium(navegador)
        except ElementNotInteractableException:
            return 0
