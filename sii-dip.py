from logging import exception
from os import path, getenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

import time

config = load_dotenv(".env")

class PublishedInvoices:
    def __init__(self):
        """ Open and setup driver. """
        driver_path = path.abspath('./chromedriver')
        data_path = path.abspath("./data") 
        # chrome_options 
        options = Options() 
        options.add_argument('--headless')  
        options.add_argument('--disable-gpu')                    # disable gpu.
        options.add_argument('--no-sandbox')                    # disable sandbox.
        options.add_argument('--disable-software-rasterizer')   # disable software rasterizer.
        # preferences
        options.add_experimental_option("prefs", {
            "download.default_directory" : data_path,           # download path.
            "download.prompt_for_download": False,              # don't ask for download.
            "download.directory_upgrade": True,                 # allow to update download path.
            "safebrowsing_for_trusted_sources_enabled": False,  # disable safebrowsing.
            "safebrowsing.enabled": True,                       # disable safebrowsing.
            'profile.default_content_setting_values.automatic_downloads': 2,    # disable auto download.
            'excludeSwitches': ['enable-logging']
        })
        self.driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options) # run the browser.

    def login_sii(self, rut, passwd):
        """ login_sii to Sii """
        url = "https://zeusr.sii.cl/AUT2000/InicioAutenticacion/IngresoRutClave.html?https://www4.sii.cl/publicacionfacturasinternetui/#/descargaArchivo"
        self.driver.get(url)      
        try:
            self.driver.find_element(By.ID, 'rutcntr').send_keys(rut)
            self.driver.find_element(By.ID, 'clave').send_keys(passwd)
            self.driver.find_element(By.ID, 'bt_ingresar').click()   
        except:
            alert = self.driver.find_element(By.XPATH, '//*[@id="alert_placeholder"]/div/span')
            print("-> Login failed.")
            print("-> Msg: ", alert.text)
            self.close()

    def download_invoices(self):
        """ Download invoices file. """
        self.driver.find_element(By.XPATH, '//*[@id="my-wrapper"]/div[2]/div/div/div/div/button').click()
        time.sleep(3) 

    def close(self):
        """ Close the program. """
        self.driver.quit()
        exit(1)

    def run(self):
        """ Run the program. """
        print("# Start app.")
        sii_rut = getenv("SII_RUT")
        sii_pass = getenv("SII_PASSWD")
        print("-> Logging in...")
        self.login_sii(sii_rut, sii_pass)
        print("-> Getting file...")
        self.download_invoices()
        print("-> File downloaded.")
        print("# app finished.")
        self.close()


if __name__ == '__main__':
    pi = PublishedInvoices()
    pi.run()