from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from random import randint
import pandas as pd
from notify_run import Notify

# sign in to instagram
driver = webdriver.Chrome(
    '../../Downloads/chrome_driver/chromedriver')
time.sleep(2)  # 2 sec delay
# logs in for you
driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
time.sleep(3)  # 3 sec delay

# enter username and password into input fields
username = driver.find_element_by_name('username')
username.send_keys('rainy.study')
password = driver.find_element_by_name('password')
password.send_keys('raynili12')
password.submit()  # hit enter on password field will submit form

time.sleep(3)

# Begin to follow, like and comment
# stationery #backtoschool #schoolsupplies #schoolessentials #studygram #studyblr #lettering #handlettering #whitelinespaper #whitelines #notestagram #artlinestix #zebrapen #aestheticnotes #notes #whitelineslink #study #school #studying #handlettering #zebramildliner #mildliners #studyinspo #studyinspiration #studygrammer
hashtags = ['notetaking']

old_followed_users = []

# old_followed_users = pd.read_csv(
# '20200511-225156_user_list.csv', delimiter=', ').iloc[0:, 1:2]  # useful to build a user log
# old_followed_users = list(old_followed_users['0'])

new_followed = []
followed = 0
liked = 0
commented = 0

for i in range(len(hashtags)):
    driver.get('https://www.instagram.com/explore/tags/' + hashtags[i] + '/')
    print(i)
    time.sleep(5)

    # click the first picture
    first_pic = driver.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div/div[2]')
    first_pic.click()

    time.sleep(randint(1, 2))

    try:
        # for the next 151 pictures
        for j in range(1, 151):
            print(j)
            # check if already following or not
            # get the username
            user_name = driver.find_element_by_xpath(
                '/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/a').text

            # check if in old_followed_users list
            if user_name not in old_followed_users:

                # check if already follow them
                if driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').text == 'Follow':

                    # follow user
                    driver.find_element_by_xpath(
                        '/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()
                    followed += 1
                    new_followed.append(user_name)

                    # like their post
                    driver.find_element_by_xpath(
                        '/html/body/div[4]/div[2]/div/article/div[2]/section[1]/span[1]/button').click()
                    liked += 1

                    # 2 / 5 chance will write a comment
                    # if (randint(1, 5) > 3):
                    # make a randomly generated comment
                    comments = ['Love it', 'Looks good!',
                                'Nicee', 'I like it!']
                    commented += 1

                    driver.find_element_by_xpath(
                        '/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form').click()
                    comment_bar = driver.find_element_by_xpath(
                        '/html/body/div[4]/div[2]/div/article/div[2]/section[3]/div/form/textarea')

                    comment_bar.send_keys(
                        comments[randint(0, 3)])  # inclusive 0-2
                    time.sleep(1)

                    comment_bar.submit()
                    time.sleep(randint(17, 20))

                # next picture
                driver.find_element_by_link_text('Next').click()
                time.sleep(randint(17, 20))

            else:
                # skip to next picture
                driver.find_element_by_link_text('Next').click()
                time.sleep(randint(13, 15))

    except:
        continue

for new in new_followed:
    old_followed_users.append(new)

df = pd.DataFrame(old_followed_users)
df.to_csv('{}_user_list.csv'.format(time.strftime("%Y%m%d-%H%M%S")))

notify = Notify()
notify.send('Your script is done running.')
