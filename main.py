from selenium import webdriver
from secret import pw
from time import sleep

class InstagramBot:

    def __init__(self, username, pw):
        self.driver = webdriver.Chrome()
        self.username = username
        self.driver.get("https://instagram.com")
        sleep(2)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        sleep(10)
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[3]/button[2]")\
            .click()
            
        sleep(3)

    def _get_names(self):

        sleep(1)    

        check_sugs = self.driver.find_elements_by_xpath("//h4[contains(text(), Suggestions)]")
  

        if check_sugs:
            sugs = self.driver.find_element_by_xpath("//h4[contains(text(), Suggestions)]")
            self.driver.execute_script('arguments[0].scrollIntoView()', sugs)
    

        sleep(2)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")

        last_height, height = 0,1
        while last_height != height:
            last_height = height
            sleep(1)
            ht = self.driver.execute_script("""
            arguments[0].scrollTo(0, arguments[0].scrollHeight); 
            return arguments[0].scrollHeight;
            """, scroll_box)
        

        if check_sugs:

            followers = scroll_box.find_element_by_xpath("/html/body/div[4]/div/div[2]/ul/div")
            links = followers.find_elements_by_tag_name('a')
        else:
            links = scroll_box.find_element_by_tag_name('a')    
        
        
        names = [name.text for name in links if name.text != '']

        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click()

        return names



    def get_unfolowers(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username))\
            .click()
        sleep(3)
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format("followers"))\
            .click()
        followers_list = self._get_names()
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format("following"))\
            .click()
        following_list = self._get_names()

        not_following_back = [user for user in following_list if user not in followers_list]
        print(not_following_back)



mybot = InstagramBot("benchwarmersglobal", pw )
mybot.get_unfolowers()


