from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Replace with your Instagram credentials
USERNAME = 'luscasedu'
PASSWORD = '109109Lucas!!'

# Replace with the path to your previous list of followers
PREVIOUS_FOLLOWERS_FILE = 'dados/previous_followers.txt'

# Initialize the Chrome browser and navigate to Instagram
driver = webdriver.Chrome()
driver.get('https://www.instagram.com/')

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

# Wait for the profile page to load
followers_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[@href="/' + USERNAME + '/followers/"]')))
# //*[@id="mount_0_0_yx"]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/header/section/ul/li[2]/a

# Retrieve the current list of followers
time.sleep(5)
followers_button.click()

# get the followers list element
time.sleep(5)
followers_list = driver.find_element(By.CLASS_NAME, '_aano')

# get the initial number of followers in the list
prev_count = len(followers_list.find_elements(By.CLASS_NAME, 'xt0psk2'))

# scroll to the bottom of the list until no more followers are loaded
while True:
    # scroll to the bottom of the list
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', followers_list)
    time.sleep(2) # wait for the next set of followers to load

    # get the new number of followers in the list
    curr_count = len(followers_list.find_elements(By.CLASS_NAME, 'xt0psk2'))
    print(prev_count)
    print(curr_count)

    # break the loop if no more followers are loaded
    if curr_count == prev_count:
        break

    prev_count = curr_count

followers = followers_list.find_elements(By.CLASS_NAME, 'xt0psk2')

current_followers = set()
for follower in followers:
    link = follower.find_element(By.CSS_SELECTOR,'a').get_attribute('href')
    username = link.split('/')[-2]
    current_followers.add(username)

# Compare the current list of followers to the previous list
with open(PREVIOUS_FOLLOWERS_FILE, 'r') as f:
    previous_followers = set(f.read().splitlines())

new_followers = current_followers - previous_followers
unfollowers = previous_followers - current_followers

print(f'New followers: {new_followers}')
print(f'Unfollowers: {unfollowers}')

# Save the current list of followers as the previous list
with open(PREVIOUS_FOLLOWERS_FILE, 'w') as f:
    f.write('\n'.join(current_followers))

# Quit the browser
driver.quit()
