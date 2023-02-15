from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Prompt the user to enter their Instagram username and password
username = input("Enter your Instagram username: ")
password = input("Enter your Instagram password: ")

# Set up the Firefox webdriver and navigate to Instagram login page
driver = webdriver.Firefox()
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(2)

# Enter the user's Instagram username and password
username_field = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
password_field = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
username_field.send_keys(username)
password_field.send_keys(password)
password_field.send_keys(Keys.ENTER)
time.sleep(5)

# Navigate to the user's profile and get their followers
driver.get(f"https://www.instagram.com/{username}/followers")
time.sleep(5)

followers_list = []
while len(followers_list) < 1038: # Change this number to get more or fewer followers
    followers = driver.find_elements(By.CLASS_NAME, "_aano")
    for follower in followers:
        if follower.text not in followers_list:
            print(follower.text)
            followers_list.append(follower.text)

    # Get the follower list element
    follower_list = driver.find_element(By.CLASS_NAME, '_aano')

    # Scroll down the list until you've reached the end
    while True:
        # Get the number of followers currently loaded
        num_followers = len(follower_list.find_elements(By.CSS_SELECTOR, '#fc4afa7b23c0aa > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)'))
        print(follower_list.find_elements(By.CSS_SELECTOR, '#fc4afa7b23c0aa > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)'))
        # Scroll to the last follower element
        driver.execute_script('arguments[0].scrollIntoView();', follower_list.find_elements(By.CSS_SELECTOR, '#fc4afa7b23c0aa > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)')[-1])

        # Wait for the next set of followers to load
        time.sleep(1)

        # Check if the number of followers has changed
        new_num_followers = len(follower_list.find_elements(By.CSS_SELECTOR, '#fc4afa7b23c0aa > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(1)'))

        # If the number of followers hasn't changed, you've reached the end of the list
        if new_num_followers == num_followers:
            break

    time.sleep(1)

# Navigate to the user's following and get the list of users they're following
driver.get(f"https://www.instagram.com/{username}/following/")
time.sleep(2)

following_list = []
while len(following_list) < 816: # Change this number to get more or fewer following users
    following = driver.find_elements(By.CSS_SELECTOR, "a.FPmhX.notranslate._0imsa")
    for follow in following:
        if follow.text not in following_list:
            print(follow.text)
            following_list.append(follow.text)

    time.sleep(1)

# Identify the users the user is following that are not following them back
not_following_back = [user for user in following_list if user not in followers_list]

# Print the list of users the user is following that are not following them back
print("Users you're following that are not following you back:")
print(not_following_back)

# Close the Firefox webdriver
driver.quit()
