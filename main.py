from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm

def listar_seguidores(n):
    accounts = []

    account = str(username)
    print('Followers of the "{}" account'.format(account))
    follower_css = "div._ab9-:nth-child({})"
    for group in tqdm(range(1, n, 12)):  # Scrape 100 followers in groups of 10
        for follower_index in range(group, group + 12):
            try:
                # Scroll to the last follower in the group
                last_follower = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, follower_css.format(follower_index))))
                
                driver.execute_script("arguments[0].scrollIntoView();", last_follower)
                accounts.append(last_follower.text)

            except Exception as e:
                print(e)
                accounts.append(last_follower.text)
    return accounts


def get_first_element(string):
    return string.split("\n")[0]
            

followers_list = []
following_list = []

# Prompt the user to enter their Instagram username and password
username = input("Enter your Instagram username: ")
password = input("Enter your Instagram password: ")

# Set up the Firefox webdriver and navigate to Instagram login page
driver = webdriver.Firefox()
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(10)

'''
try:
    #Closing popup
    cookies_bt = driver.find_elements(By.XPATH, "//button[text()='Permitir apenas cookies essenciais']")
    #print(cookies_bt)
    cookies_bt[0].click()
    time.sleep(5)
except Exception as e:
    print(e)
'''

# Enter the user's Instagram username and password
username_field = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
password_field = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
username_field.send_keys(username)
password_field.send_keys(password)
password_field.send_keys(Keys.ENTER)
time.sleep(10)

# Navigate to the user's profile and get their followers
driver.get(f"https://www.instagram.com/{username}")
time.sleep(10)

count = driver.find_elements(By.CLASS_NAME, '_ac2a')
n_follower = int(count[1].text.replace('.',''))
n_following = int(count[2].text.replace('.',''))
time.sleep(5)

follows = driver.find_elements(By.XPATH, '//a[@href="/{}/followers/"]'.format(username))
print(follows[0])
follows[0].click()
time.sleep(5)

followers_list = listar_seguidores(n_follower)

# Navigate to the user's following and get the list of users they're following
driver.get(f"https://www.instagram.com/{username}/following/")
time.sleep(2)

following_list = listar_seguidores(n_following)

followers_list_clean = [get_first_element(s) for s in followers_list]
following_list_clean = [get_first_element(s) for s in following_list]

# Identify the users the user is following that are not following them back
not_following_back = [user for user in following_list_clean if user not in followers_list_clean]

# Print the list of users the user is following that are not following them back
print("Users you're following that are not following you back:")
for people in not_following_back:
    print(people)

# Close the Firefox webdriver
driver.quit()
