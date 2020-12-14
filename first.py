from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv


username = ""
password = ""


class Twitter:
     def __init__(self, username, password):
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.browser = webdriver.Chrome('chromedriver.exe', chrome_options=self.browserProfile)
        self.username = username
        self.password = password


     def singIn(self):
         self.browser.get("https://twitter.com/login")
         time.sleep(2)

         usernameInput = self.browser.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div[1]/form/div/div[1]/label/div/div[2]/div/input")
         passwordInput = self.browser.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div[1]/form/div/div[2]/label/div/div[2]/div/input")

         usernameInput.send_keys(self.username)
         passwordInput.send_keys(self.password)

         btnSubmit = self.browser.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div[1]/form/div/div[3]/div/div")
         btnSubmit.click()

         time.sleep(2)
         
       
         
     def auth(self):
         time.sleep(2)
         authInput = self.browser.find_element_by_xpath("//*[@id='challenge_response']")
         authInput.send_keys("hawmns@gmail.com")
         btnAuth = self.browser.find_element_by_xpath("//*[@id='email_challenge_submit']")
         btnAuth.click()


     def get_tweet_data(self, card):
         time.sleep(2)
         name = card.find_element_by_xpath('.//span').text
         try:
             username = card.find_element_by_xpath('.//span[contains(text(),"@")]').text
         except NoSuchElementException:
             return

         try:
             postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
         except NoSuchElementException:
             return


         tweet = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
         reply_cnt = card.find_element_by_xpath('.//div[@data-testid="reply"]').text
         retweet_cnt = card.find_element_by_xpath('.//div[@data-testid="retweet"]').text
         like_cnt = card.find_element_by_xpath('.//div[@data-testid="like"]').text



         

         time.sleep(2)



         tweet = (name, username, postdate, tweet, reply_cnt,retweet_cnt,like_cnt)
         
         return tweet           


                 
         




     def search(self, key):
         time.sleep(5)
         searchInput = self.browser.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div[2]/input")
         searchInput.send_keys(key)
         time.sleep(2)
         searchInput.send_keys(Keys.ENTER)
         time.sleep(2)
         lastInput = self.browser.find_element_by_xpath("//*[@id='react-root']/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[2]/nav/div/div[2]/div/div[2]/a")
         lastInput.send_keys(Keys.ENTER)
         time.sleep(2)

         data = []
         tweet_ids = set()
         last_position = self.browser.execute_script("return window.pageYOffset;")
         scrolling = True

         while scrolling:
             page_cards = self.browser.find_elements_by_xpath('//div[@data-testid="tweet"]')
             for card in page_cards[-15:]:
                 tweet = twitter.get_tweet_data(card)
                 if tweet:
                     tweet_id = ''.join(tweet)
                     if tweet_id not in tweet_ids:
                         tweet_ids.add(tweet_id)
                         data.append(tweet)
             scroll_attempt = 0
             while True:
                 self.browser.execute_script('window.scrollTo(0,document.body.scrollHeight);')
                 time.sleep(2)
                 curr_position = self.browser.execute_script("return window.pageYOffset;")
                 if last_position == curr_position:
                     scroll_attempt += 1

                     if scroll_attempt >= 3:
                         scrolling = False
                         break
                     else:
                         time.sleep(2)

                 else:
                     last_position = curr_position
                     break


             time.sleep(2)

             with open('save.csv', 'w', newline='', encoding='utf-8') as f:
                 header = ['Name', 'Username', 'Time', 'Tweet', 'Comments Count', 'Likes Count', 'Retweets Count']
                 writer = csv.writer(f)
                 writer.writerow(header)
                 writer.writerows(data)

                               

         
         

         
         
         
             

     


         

    
         






    
    
twitter = Twitter(username, password)
    
twitter.singIn()

twitter.search('"request for startup"')







