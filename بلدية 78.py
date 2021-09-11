#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip install webdriver-manager
#!pip install selenium
import re
import csv
from getpass import getpass
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome

def get_tweet_data(cards):
    username = cards.find_element_by_xpath('.//span').text
    handle = cards.find_element_by_xpath('.//span[contains(text(), "@")]').text
    try:
        postdate = cards.find_element_by_xpath('.//time').get_attribute('datetime') 
    except NoSucElementException:
            return
    comment = cards.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
    respooding = cards.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
    text = comment + respooding
    reply_cnt =  cards.find_element_by_xpath('.//div[@data-testid="reply"]').text
    retweet_cnt =  cards.find_element_by_xpath('.//div[@data-testid="retweet"]').text
    like_cnt =cards.find_element_by_xpath('.//div[@data-testid="like"]').text  

        # get a string of all emojis contained in the tweet
    """Emojis are stored as images... so I convert the filename, which is stored as unicode, into 
    the emoji character."""
    emoji_tags = card.find_elements_by_xpath('.//img[contains(@src, "emoji")]')
    emoji_list = []
    for tag in emoji_tags:
        filename = tag.get_attribute('src')
        try:
            emoji = chr(int(re.search(r'svg\/([a-z0-9]+)\.svg', filename).group(1), base=16))
        except AttributeError:
            continue
        if emoji:
            emoji_list.append(emoji)
    emojis = ' '.join(emoji_list)
    
    tweet = (username, handle, postdate, text, emojis, reply_cnt, retweet_cnt, like_cnt)
    return tweet  


# In[ ]:


# application variables
user = input('username: ')
my_password = getpass('Password: ')
search_term = input('search term: ')

# create instance of web driver
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
# navigate to login screen
driver.get('https://www.twitter.com/login')
driver.maximize_window()

username = driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
username.send_keys(user)

password = driver.find_element_by_xpath('//input[@name="session[password]"]')
password.send_keys(my_password)
password.send_keys(Keys.RETURN)
sleep(1)

# find search input and search for term
search_input = driver.find_element_by_xpath('//input[@aria-label="Search query"]')
search_input.send_keys(search_term)
search_input.send_keys(Keys.RETURN)
sleep(1)

# navigate to historical 'latest' tab
driver.find_element_by_link_text('Latest').click()


# In[ ]:


# get all tweets on the page
data = []
tweet_ids = set()
last_position = driver.execute_script("return window.pageYOffset;")
scrolling = True

while scrolling:
    page_cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
    for card in page_cards[-15:]:
        tweet = get_tweet_data(card)
        if tweet:
            tweet_id = ''.join(tweet)
            if tweet_id not in tweet_ids:
                tweet_ids.add(tweet_id)
                data.append(tweet)
            
    scroll_attempt = 0
    while True:
        # check scroll position
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(2)
        curr_position = driver.execute_script("return window.pageYOffset;")
        if last_position == curr_position:
            scroll_attempt += 1
            
            # end of scroll region
            if scroll_attempt >= 3:
                scrolling = False
                break
            else:
                sleep(2) # attempt another scroll
        else:
            last_position = curr_position
            break

# close the web driver
driver.close()


# # Saving the tweet data

# In[ ]:


with open('turkcell14_tweets.csv', 'w', newline='', encoding='utf-8') as f:
    header = ['UserName', 'Handle', 'Timestamp', 'Text', 'Emojis', 'Comments', 'Likes', 'Retweets']
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)


# In[ ]:




