import os, selenium, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class seleniumBot():

    def __init__(self, email, password):
        self.browser = webdriver.Chrome()
        self.email = email
        self.password = password

    def signIn(self):
        self.browser.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)
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

    #TODO: Verify the correct account name
    def recordInfo(self, username):
        self.goToPage(username)
        infoElems = self.browser.find_elements_by_class_name("-nal3")    # Class tag for profile info
        profileData = []
        for item in infoElems:
            profileData.append(item.get_attribute("innerText"))
        return profileData    # Returns a list of three items with descriptions: post count, follower count, following count

    def getUserFollowers(self, username, max):
        followerCount = self.recordInfo(username)[1].split()[0]
        infoElems = self.browser.find_elements_by_class_name("-nal3")  # Class tag for profile info
        followersButton = infoElems[1]
        followersButton.click()
        time.sleep(2)

        # Set up the action chain
        followersList = self.browser.find_element_by_css_selector('div[role=\'dialog\'] ul')
        numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))

        followersList.click()
        actionChain = webdriver.ActionChains(self.browser)

        # TODO: Fix Bug - Scrolling is not updating the number of list items, it is being
        # TODO: returned as 12 every time. Must figure out a way to update this list properly.


        #TODO: POSSIBLE SOLUTION: The page takes a second to load the next set of followers.
        #TODO: Increase sleep timer to allow page load. Or insert some other sort of wait
        #TODO: function.
        
        while (numberOfFollowersInList < max):
            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(1)
            numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
            print(numberOfFollowersInList)

        followers = []
        for user in followersList.find_elements_by_css_selector('li'):
            userLink = user.find_element_by_css_selector('a').get_attribute("innerText")
            print(userLink)
            followers.append(userLink)
            if (len(followers) == max):
                break
        return followers
