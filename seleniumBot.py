import selenium, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class seleniumBot():

    def __init__(self, email, password):
        self.browser = webdriver.Chrome()
        self.email = email
        self.password = password

    def signIn(self):
        self.browser.get("https://www.instagram.com/accounts/login/")
        time.sleep(2)  # TODO: Change to a wait for element to load
        emailInput = self.browser.find_elements_by_css_selector("form input")[0]
        passwordInput = self.browser.find_elements_by_css_selector("form input")[1]

        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(2)

    def homePage(self):
        self.browser.get("https://www.instagram.com/")

    def goToPage(self, username):
        self.browser.get("https://www.instagram.com/" + username)

    # TODO: Verify the correct account name
    def recordInfo(self, username):
        self.goToPage(username)
        infoElems = self.browser.find_elements_by_class_name("-nal3")  # Class tag for profile info
        profileData = []
        for item in infoElems:  # Add three strings of profile info to profileData list
            profileData.append(item.get_attribute("innerText"))
        return profileData  # Returns a list of 3 items: post count, follower count, following count

    def getUserFollowers(self, username, max):
        followerCount = int(self.recordInfo(username)[1].split()[0])  # Number of followers profile has
        infoElems = self.browser.find_elements_by_class_name("-nal3")  # CSS class tag for profile info
        followersButton = infoElems[1]
        followersButton.click()
        time.sleep(2)

        followerBox = self.browser.find_element_by_css_selector('div[role=\'dialog\'] ul')  # Focuses follower list
        userNames = []

        followerBox.click()
        actionChain = webdriver.ActionChains(self.browser)

        # Fixed scroll bug.
        while len(userNames) < max:  # This is supposed to keep scrolling until all the names are revealed
            followerBox.click()  # Click on the listbox to focus it, in case browser scrolls erratically
            actionChain.key_down(Keys.ARROW_DOWN).key_up(Keys.ARROW_DOWN).perform()  # Press/release down arrow
            userNames = followerBox.find_elements_by_class_name('FPmhX')
            time.sleep(1)
            print(len(userNames))
            if len(userNames) >= (followerCount -1):  # Prevents infinite loop if max is set higher than total follower number
                break                                 # For some reason, list always stops 1 before followerCount, while testing on MR page

        # Blank list bug fixed
        profiles = []  # Will store the actual profile names
        for name in userNames:
            profiles.append(name.get_attribute('innerText'))
        print(len(profiles))
        return profiles

# TODO: The getUserInfo function now works, but the list of names is returned LONGER than the set max (e.g. 48 for 40, 108 for 100).
# TODO: How to stop the list from adding the last 8 names that are loaded?