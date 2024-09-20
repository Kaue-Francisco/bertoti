################################################################################
# Imports

# Selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Variables
from amazon.definitions import *

# Dependencies
import time

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

    ################################################################################
    def is_departament(self, departament):
        """ Method to check if a departament is in the offer of the day """
        return departament[0].upper() + departament[1:].lower() in self.departaments
        
    ################################################################################
    def get_products_of_departament(self, departament):
        """ Method to get the product links, names, image URLs, and discount percentages of a departament """

        try:
            # Get the div element with the spans and extract the unique texts
            div_element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#DealsGridScrollAnchor > div.DesktopRefinements-module__root_bhKhpQRjma_FcGUry8RQ.DesktopDiscountAsinGrid-module__refinements_YB5V1nuIh3E8iHj37aVv > div:nth-child(1) > div'))
            )
            span_elements = div_element.find_elements(By.TAG_NAME, 'span')

            unique_spans = set()

            for span in span_elements:
                unique_spans.add(span.text.strip())
        except Exception as e:
            print(f"Error while extracting unique spans: {e}")
            return []

        try:
            # Click on the department matching the given name
            department_label = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, f"//label[span/span[text()='{departament}']]"))
            )
            department_label.click()
        except Exception as e:
            print(f"Error while clicking on department label: {e}")
            return []

        time.sleep(5)

        try:
            # Wait for the products to load
            products_container = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#DealsGridScrollAnchor div.DesktopDiscountAsinGrid-module__grid_pi4xEmM7RAHNMG9sGVBJ'))
            )
        except Exception as e:
            print(f"Error while waiting for products to load: {e}")
            return []

        try:
            # Find all child divs with the data-testid attribute
            product_divs = products_container.find_elements(By.CSS_SELECTOR, 'div[data-testid]')
        except Exception as e:
            print(f"Error while finding product divs: {e}")
            return []

        # List to store product links, names, image URLs, and discount percentages
        products = []
        # Set to store product links to avoid duplicates
        product_links_set = set()

        for div in product_divs:
            try:
                # Find the specific link element with the given selector
                product_link = div.find_element(By.CSS_SELECTOR, 'div > a').get_attribute('href')

                # Check if the product link is already in the set
                if product_link not in product_links_set:
                    # Find the specific span element with the given selector
                    product_name = div.find_element(By.CSS_SELECTOR, 'span.a-truncate-cut').text.strip()
                    # Find the specific img element with the given selector
                    product_image = div.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
                    # Find the specific span element with the given selector for discount
                    product_discount = div.find_element(By.CSS_SELECTOR, 'span.a-size-mini').text.strip()
                    # Store the link, name, image URL, and discount percentage as a tuple
                    products.append((product_name, product_link, product_image, product_discount))
                    # Add the product link to the set
                    product_links_set.add(product_link)
            except Exception as e:
                # If the link, name, image, or discount is not found, continue to the next div
                print(f"Error while processing product div: {e}")
                continue

        return products