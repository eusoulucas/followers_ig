import winsound
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from selenium.webdriver.common.keys import Keys

def human_typing(frase, onde_digitar):
    for letra in frase:
        onde_digitar.send_keys(letra)
        time.sleep(random.randint(3, 10) / 40)

# Replace with your Instagram credentials
USERNAME = str(input('Digite o usuário:'))
PASSWORD = str(input("Digite a senha:"))

# Initialize the Chrome browser and navigate to Instagram
driver = webdriver.Chrome()
url = 'https://www.instagram.com/'
driver.get(url)

# Creating a waiter
wait = WebDriverWait(driver, 10)

# Log in to Instagram
username_field = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
password_field = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
username_field.send_keys(USERNAME)
password_field.send_keys(PASSWORD)
login_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')))
login_button.click()
time.sleep(5)

driver.get('https://www.instagram.com/reel/Cq830ikJkEh/?igshid=YmMyMTA2M2Y%3D')
time.sleep(3)

for i in range(0, 10000):
    time.sleep(random.randint(10, 27))
    
    # Encontrar o elemento com o XPath específico e comentar
    comentario = "#DESAFIOTOMAESSA"

    approaches = ['textarea.x1i0vuye', 'textarea.x112ta8', 'textarea.x76ihet']

    for approach in approaches:
        try:
            textarea = driver.find_element(By.CSS_SELECTOR, approach)
            human_typing(comentario, textarea) # Replace with the text you want to input
            time.sleep(3)            
            textarea.send_keys(Keys.ENTER)
            break # Break out of the loop if textarea is found and filled successfully
        except Exception as e:
            print(e)# Handle exception if element is not found using the current approach
            continue
    
    # List of different approaches to locate the textarea element
    approaches = [
        'textarea[aria-label="Add a comment…"][placeholder="Add a comment…"]',
        'textarea.x1i0vuye.xvbhtw8.x76ihet.xwmqs3e.x112ta8.xxxdfa6.x5n08af.x78zum5.x1iyjqo2.x1qlqyl8.x1d6elog.xlk1fp6.x1a2a7pz.xexx8yu.x4uap5.x18d9i69.xkhd6sd.xtt52l0.xnalus7.x1bq4at4.xaqnwrm.xs3hnx8'
                    ]
    
    try:
        element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and text()="Post"]')))
        # Click on the element
        element.click()
        time.sleep(5)
    except Exception as e:
        print(e)
        time.sleep(40)

# Play a beep sound when code finishes running
winsound.Beep(1000, 500)  # 1000 Hz frequency, 500 milliseconds duration

# Fechar o navegador
driver.quit()