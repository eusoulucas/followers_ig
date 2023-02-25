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
driver = webdriver.Firefox()
driver.get('https://www.instagram.com/')

# Log in to Instagram
username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
username_field.send_keys(USERNAME)
password_field.send_keys(PASSWORD)
login_button = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')
login_button.click()

# Wait for the login process to complete
not_now_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Not Now"]')))
not_now_button.click()

try:
    # Wait for the login process to complete
    not_now_button_notifications = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Not Now"]')))
    not_now_button_notifications.click()
except Exception as e:
    print(e)

# Navigate to your profile page
profile_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@href="/' + USERNAME + '/"]')))
profile_button.click()

# Wait for the profile page to load
followers_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//a[@href="/' + USERNAME + '/followers/"]')))

# Retrieve the current list of followers
followers_button.click()

# get the followers list element
followers_list = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, '_aano')))

# get the initial number of followers in the list
prev_count = len(driver.find_elements(By.XPATH, '//*[@id="mount_0_0_Yo"]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]'))

# scroll to the bottom of the list until no more followers are loaded
while True:
    # scroll to the bottom of the list
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', followers_list)
    time.sleep(2) # wait for the next set of followers to load

    # get the new number of followers in the list
    curr_count = len(followers_list.find_elements(By.CSS_SELECTOR, 'li'))
    print(prev_count)
    print(curr_count)

    # break the loop if no more followers are loaded
    if curr_count == prev_count:
        break

    prev_count = curr_count

followers = followers_list.find_elements(By.CSS_SELECTOR,'li')

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
