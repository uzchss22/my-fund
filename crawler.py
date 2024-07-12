from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def _string_to_int(input_string):
    cleaned_string = input_string.strip()
    cleaned_string = cleaned_string.replace(',', '')
    result_integer = int(cleaned_string)
    return result_integer    

def crawling_data():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get('fund-url') # insert your fund url

    unprocessed_total_proceeds = driver.find_element(By.XPATH, 'total-preceeds-path').text  # insert XPath
    unprocessed_day_proceeds = driver.find_element(By.XPATH, 'day-proceeds-path').text # insert XPath
    driver.quit()
    total_proceeds = _string_to_int(unprocessed_total_proceeds)
    day_proceeds = _string_to_int(unprocessed_day_proceeds)
    return total_proceeds, day_proceeds


if __name__ == "__main__":
    crawling_data()

