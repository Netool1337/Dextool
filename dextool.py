from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import traceback

# Chemin vers le navigateur Chrome
driver_path = r"C:\Users\Hugo\Bureau\chromedriver-win64\chromedriver.exe"

# Configuration de Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--no-first-run")
chrome_options.add_argument("--force-color-profile=srgb")
chrome_options.add_argument("--metrics-recording-only")
chrome_options.add_argument("--password-store=basic")
chrome_options.add_argument("--use-mock-keychain")
chrome_options.add_argument("--export-tagged-pdf")
chrome_options.add_argument("--no-default-browser-check")
chrome_options.add_argument("--disable-background-mode")
chrome_options.add_argument(
    "--enable-features=NetworkService,NetworkServiceInProcess,LoadCryptoTokenExtension,PermuteTLSExtensions")
chrome_options.add_argument("--disable-features=FlashDeprecationWarning,EnablePasswordsAccountStorage")
chrome_options.add_argument("--deny-permission-prompts")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--accept-lang=en-US")
chrome_options.add_argument("--start-maximized")

# Créer une instance de WebDriver
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Lancer le site
    url = "https://www.dextools.io/app/en/solana/hot-pairs"
    print(f"Ouverture de l'url: {url}")
    driver.get(url)

    time.sleep(10)

    print(f"Appuie sur le bouton close")
    # Trouver le bouton Top Trader et cliquer dessus
    bouton1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/ngb-modal-window/div/div/app-video-yt-modal/div[1]/button'))
    )
    bouton1.click()

    time.sleep(10)

    scroll_origin = ScrollOrigin.from_viewport(10, 10)

    ActionChains(driver) \
        .scroll_from_origin(scroll_origin, 0, 600) \
        .perform()

    # Listes pour stocker les noms et adresses
    token_names = []
    token_addresses = []

    # Boucle for de 10 itérations pour récupérer les noms et adresses
    for i in range(1, 11):
        try:
            # Récupérer le nom du token
            token_name_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                f"datatable-row-wrapper.datatable-row-wrapper:nth-child({i}) > datatable-body-row:nth-child(1) > div:nth-child(1) > datatable-body-cell:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > a:nth-child(1) > app-token-name:nth-child(1) > span:nth-child(1) > span:nth-child(1)"))
            )
            token_name = token_name_element.text
            token_names.append(token_name)

            # Récupérer l'adresse du token
            token_link_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR,
                                                f"body > app-root > div > div > main > app-new-home > app-layout > div > div.home-container > app-pairs-dashboard > app-hot-pairs-table > div > ngx-datatable > div > div > datatable-body > datatable-selection > datatable-scroller > datatable-row-wrapper:nth-child({i}) > datatable-body-row > div.datatable-row-group.datatable-row-left.ng-star-inserted > datatable-body-cell:nth-child(2) > div > div > div > a"))
            )
            adresse = token_link_element.get_attribute('href')
            token_addresses.append(adresse)

            print(f"Nom du token récupéré : {token_name}")
            print(f"Adresse récupérée : {adresse}")
        except Exception as e:
            print(f"Erreur lors de la récupération du token {i}: {str(e)}")

    # Boucle pour naviguer vers chaque URL et récupérer les top traders
    for i in range(10):
        try:
            adresse = token_addresses[i]
            token_name = token_names[i]

            # Ouvrir l'URL du token
            print(f"Ouverture de l'URL : {adresse}")
            driver.get(adresse)

            # Attendre que la page se charge complètement
            print("Attente de 20 secondes pour que la page se charge complètement...")
            time.sleep(20)  # Ajuste le délai d'attente si nécessaire

            scroll_origin = ScrollOrigin.from_viewport(10, 10)

            ActionChains(driver) \
                .scroll_from_origin(scroll_origin, 0, 600) \
                .perform()

            # Trouver le bouton Top Trader et cliquer dessus
            bouton = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="tabs-container"]/div/div[1]/app-tabs/ul/li[3]/button'))
            )

            # Vérifier si le texte du bouton est bien "Top Traders"
            if bouton.text.strip() == "Top Traders":
                bouton.click()
                print("Bouton cliqué avec succès!")
            else:
                print("Le texte du bouton ne correspond pas.")

            # Boucle for de 3 itérations pour les top traders
            for j in range(1, 4):
                # Attendre que l'adresse du Top Trader soit présente
                adressetoptrader_element = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR,
                                                    f"datatable-row-wrapper.datatable-row-wrapper:nth-child({j}) > datatable-body-row:nth-child(1) > div:nth-child(2) > datatable-body-cell:nth-child(2) > div:nth-child(1) > app-maker-address:nth-child(1) > div:nth-child(1) > a:nth-child(1)"))
                )

                adressetoptrader = adressetoptrader_element.get_attribute('href')
                print(f"Adresse du Top Trader {j}: {adressetoptrader}")

        except Exception as e:
            print(f"Erreur lors de la navigation pour le token {token_name}: {str(e)}")

except Exception as e:
    print(f"Erreur lors de l'exécution : {str(e)}")
    traceback.print_exc()

finally:
    driver.quit()
