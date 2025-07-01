class GoogleMapsScraper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.results = []

    def wait_random(self, a=1.5, b=2.5):
        time.sleep(random.uniform(a, b))

    def search(self, query):
        self.driver.get("https://www.google.com/maps")
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "searchboxinput")))
        search_box = self.driver.find_element(By.CLASS_NAME, "searchboxinput")
        search_box.send_keys(query, Keys.ENTER)
        self.wait_random()

    def scroll_results_panel(self, scrolls=10):
        try:
            panel = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@role="feed"]')))
            for _ in range(scrolls):
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", panel)
                self.wait_random()
        except Exception as e:
            print("Error scrolling:", e)

    def get_all_cards(self):
        return self.driver.find_elements(By.CLASS_NAME, 'Nv2PK')

    def click_and_scrape_each(self):
        cards = self.get_all_cards()
        for i, card in enumerate(cards):
            try:
                self.wait_random()
                self.driver.execute_script("arguments[0].click();", card)
                self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'DUwDvf')))
                self.wait_random(2, 3)

                name = self.driver.find_element(By.CLASS_NAME, 'DUwDvf').text
                try:
                    rating = self.driver.find_element(By.XPATH, '//span[@role="img"]').get_attribute("aria-label")
                except:
                    rating = "N/A"

                try:
                    category = self.driver.find_element(By.CLASS_NAME, 'DkEaL').text
                except:
                    category = "N/A"

                try:
                    website = self.driver.find_element(By.XPATH, '//a[contains(@aria-label, "Website")]').get_attribute("href")
                except:
                    website = "N/A"

                try:
                    address = self.driver.find_element(By.XPATH, '//button[contains(@data-item-id,"address")]').text
                except:
                    address = "N/A"

                try:
                    phone = self.driver.find_element(By.XPATH, '//button[contains(@data-item-id,"phone")]').text
                except:
                    phone = "N/A"

                self.results.append({
                    "Name": name,
                    "Rating": rating,
                    "Category": category,
                    "Website": website,
                    "Address": address,
                    "Phone": phone
                })

                self.go_back_to_list()
            except Exception as e:
                print(f"❌ Failed on card {i}: {e}")
                continue

    def go_back_to_list(self):
        try:
            back = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Back"]')))
            back.click()
            self.wait_random()
        except:
            self.driver.back()
            self.wait_random()

    def run(self, query):
        self.search(query)
        self.scroll_results_panel(scrolls=12)
        self.click_and_scrape_each()
        self.driver.quit()
        return self.results
