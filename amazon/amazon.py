################################################################################
# Imports

# Selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

        # Return the unique spans as a list
        self.departaments = list(unique_spans)
        return self.departaments

    ################################################################################
    def is_departament(self, departament):
        """ Method to check if a departament is in the offer of the day """
        return departament.lower() in [d.lower() for d in self.departaments]
        
    ################################################################################
    def get_unique_spans(self):
        """Extract unique spans from the div element."""
        try:
            time.sleep(2)
            div_element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#DealsGridScrollAnchor > div.DesktopRefinements-module__root_bhKhpQRjma_FcGUry8RQ.DesktopDiscountAsinGrid-module__refinements_YB5V1nuIh3E8iHj37aVv > div:nth-child(1) > div'))
            )
            span_elements = div_element.find_elements(By.TAG_NAME, 'span')
            unique_spans = set(span.text.strip() for span in span_elements)
            return unique_spans
        except Exception as e:
            print(f"Error: {e}")
            return set()

    def click_department_label(self, departament):
        """Click on the department label matching the given name."""
        try:
            time.sleep(2)
            department_label = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, f"//label[span/span[text()='{departament}']]"))
            )
            department_label.click()
        except Exception as e:
            print(f"Error: {e}")
            return False
        return True

    def wait_for_products_container(self):
        """Wait for the products container to load."""
        try:
            time.sleep(5)
            products_container = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#DealsGridScrollAnchor div.DesktopDiscountAsinGrid-module__grid_pi4xEmM7RAHNMG9sGVBJ'))
            )
            return products_container
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_product_details(self, products_container):
        """Get product details from the products container."""
        try:
            product_divs = products_container.find_elements(By.CSS_SELECTOR, 'div[data-testid]')
        except Exception as e:
            return []

        products = []
        product_links_set = set()

        for div in product_divs:
            try:
                link_elements = div.find_elements(By.CSS_SELECTOR, 'div > a')
                if not link_elements:
                    continue

                product_link = link_elements[0].get_attribute('href')
                if product_link not in product_links_set:
                    try:
                        product_name = div.find_element(By.CSS_SELECTOR, 'span.a-truncate-cut').text.strip()
                    except Exception:
                        product_name = ""

                    try:
                        product_image = div.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
                    except Exception:
                        product_image = None

                    try:
                        product_discount = div.find_element(By.CSS_SELECTOR, 'span.a-size-mini').text.strip()
                    except Exception:
                        product_discount = ""

                    products.append((product_name, product_link, product_image, product_discount))
                    product_links_set.add(product_link)
            except Exception as e:
                continue
                    
        return products

    def get_products_of_departament(self, departament):
        """Method to get the product links, names, image URLs, and discount percentages of a departament."""
        unique_spans = self.get_unique_spans()
        if not unique_spans:
            return []

        if not self.click_department_label(departament):
            return []

        products_container = self.wait_for_products_container()
        if not products_container:
            return []

        return self.get_product_details(products_container)
    
    ################################################################################
    def get_top_products(self, product_name, max_products=5):
        """Get the top products based on the search query, including name, link, image, and price."""
        self.driver.get('https://www.amazon.com.br/')
        search_box = self.driver.find_element(By.ID, 'twotabsearchtextbox')
        search_box.send_keys(product_name)
        search_box.send_keys(Keys.RETURN)

        try:
            # Wait for the products to load
            products_container = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.s-main-slot.s-result-list'))
            )
            
            # Locate all product divs within the container
            product_divs = products_container.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')

            products = []
            for div in product_divs[:max_products]:
                try:
                    # Extract product link
                    link_element = div.find_element(By.CSS_SELECTOR, 'h2 a')
                    product_link = link_element.get_attribute('href')

                    # Extract product image
                    img_element = div.find_element(By.CSS_SELECTOR, 'img.s-image')
                    product_image = img_element.get_attribute('src')

                    # Extract product name
                    product_name = link_element.text.strip() if link_element.text else "No Name"

                    # Extract product price using adjusted CSS selectors
                    try:
                        # Locate price elements
                        price_whole_element = div.find_element(By.CSS_SELECTOR, 'span.a-price-whole')
                        price_fraction_element = div.find_element(By.CSS_SELECTOR, 'span.a-price-fraction')
                        
                        # Concatenate the whole and fractional parts of the price
                        product_price = f"{price_whole_element.text.strip()},{price_fraction_element.text.strip()}"
                    except Exception as e:
                        print(f"Price not found for {product_name}: {e}")
                        product_price = "Price not available"

                    # Append the product data to the list
                    products.append({
                        'name': product_name,
                        'link': product_link,
                        'image': product_image,
                        'price': product_price
                    })
                except Exception as e:
                    print(f"Error processing product: {e}")
                    return []

            return products

        except Exception as e:
            print(f"Error loading products: {e}")
            return []