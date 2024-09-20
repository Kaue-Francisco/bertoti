################################################################################
# Import Libraries

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

################################################################################
class ConfigDriver:
    
    def __init__(self):
        options = Options()
        options.add_argument("--headless")  # Adiciona o modo headless
        options.add_argument("--disable-gpu")  # Necessário para o modo headless funcionar corretamente
        self.service = Service(executable_path="config/msedgedriver.exe")
        self.driver = webdriver.Edge(service=self.service, options=options)

    ################################################################################        
    def get_driver(self):
        return self.driver