################################################################################
# Imports

# Selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Variables
from amazon.definitions import *

################################################################################
class Amazon:
    def __init__(self, driver):
        self.driver = driver
        self.departaments = None

    ################################################################################    
    def get_departaments_offer_of_the_day(self):
        """ Method to get the offer of the day """
        
        self.driver.get(URL_OFFERS_OF_THE_DAY)
        
        # Await until the "See more" button is visible and clickable, then click on it
        see_more_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[aria-labelledby="see-more-departments-label"]'))
        )
        see_more_button.click()

        # Get the div element with the spans and extract the unique texts
        div_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#DealsGridScrollAnchor > div.DesktopRefinements-module__root_bhKhpQRjma_FcGUry8RQ.DesktopDiscountAsinGrid-module__refinements_YB5V1nuIh3E8iHj37aVv > div:nth-child(1) > div'))
        )
        span_elements = div_element.find_elements(By.TAG_NAME, 'span')

        unique_spans = set()

        for span in span_elements:
            unique_spans.add(span.text.strip())

        # Return the unique spans as a string
        self.departaments = "\n".join(unique_spans)
        return self.departaments