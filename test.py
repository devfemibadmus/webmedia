from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

edge_options = Options()
edge_options.use_chromium = True
edge_options.add_argument("--headless")
edge_options.add_argument("--disable-gpu")
edge_options.add_argument("--mute-audio")

service = Service('/usr/local/bin/msedgedriver')

driver = webdriver.Edge(service=service, options=edge_options)
driver.get("http://www.google.com")
print(driver.title)
driver.quit()