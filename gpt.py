from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def scraping(categorie):
    prev_count = 0
    curr_count = 0

    # Wait for the profile page to load
    driver.get(url + USERNAME + '/'+ categorie +'/')

    # get the users list element
    time.sleep(5)
    users_list = driver.find_element(By.CLASS_NAME, '_aano')

    # get the initial number of followers in the list
    prev_count = len(users_list.find_elements(By.CLASS_NAME, 'xt0psk2'))

    # scroll to the bottom of the list until no more followers are loaded
    while True:
        try:
            # scroll to the bottom of the list
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', users_list)
            time.sleep(5) # wait for the next set of followers to load

            # get the new number of followers in the list
            curr_count = len(users_list.find_elements(By.CLASS_NAME, 'xt0psk2'))
            
            if curr_count <= prev_count:
                break
            prev_count = curr_count

        except Exception as e:
            print(e)
            break

    users = users_list.find_elements(By.CLASS_NAME, 'xt0psk2')

    current_users = []
    for user in users:
        current_users.append(user.text)
    
    lista_sem_duplicatas = list(set(current_users))

    return lista_sem_duplicatas

# Replace with your Instagram credentials
USERNAME = 'luscasedu'
PASSWORD = '109109Lucas!!'

# Replace with the path to your previous list of followers
PREVIOUS_FOLLOWERS_FILE = 'dados/previous_followers.txt'

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

for i in range(2):
    try:
        # Wait for the login process to complete
        not_now_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Not Now"]')))
        not_now_button.click()

    except Exception as e:
        # Wait for the login process to complete
        not_now_button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Agora não"]')))
        not_now_button.click()


# Navigate to your profile page
profile_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/' + USERNAME + '/"]')))
profile_button.click()

following = scraping('following')
followers = scraping('followers')

print('\n----------------------Followers------------------------')
print(followers)
print('\n----------------------Following------------------------')
print(followers)
print('\n')

for username in following:
    if username not in followers:
        print(username + " is not following you back.")

# Quit the browser
driver.quit()
