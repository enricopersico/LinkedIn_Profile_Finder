"""
AUTHOR: ENRICO PERSICO, 2020

HOW TO RUN PROGRAM:
INSTALL PYTHON
GO TO TERMINAL
RUN COMMAND 'pip install pandas'
RUN COMMAND 'pip install selenium'
RUN COMMAND 'pip install webdriver-manager'
CHOOSE YOUR PRESETS - LOOK FOR PRESETS COMMENT BELOW:
    min_value = MINIMUM AMOUNT OF SECONDS BETWEEN LINKEDIN SEARCHES, FEEL FREE TO CHANGE FOR WHATEVER QUICKNESS YOU NEED FROM THIS PROGRAM
    max_value = MAXIMUM AMOUNT OF SECONDS BETWEEN LINKEDIN SEARCHES, FEEL FREE TO CHANGE FOR WHATEVER QUICKNESS YOU NEED FROM THIS PROGRAM
    page_load_time = HOW LONG TO WAIT FOR PAGE TO LOAD BEFORE SCRAPING THE PROFILE, FEEL FREE TO CHANGE FOR WHATEVER QUICKNESS YOU NEED FROM THIS PROGRAM
    username = YOUR LINKEDIN USERNAME
    password = YOUR LINKEDIN PASSWORD
    headless = True IF YOU WANT THE CODE TO RUN SILENTLY, False IF YOU WANT IT TO RUN VISUALLY
    input_name = PATH OF YOUR INPUT CSV, DEFAULT IS 'input/unfiltered_output.csv'
    user_agent = YOUR USER AGENT, IF YOU DON'T KNOW IT SEE 'https://www.whatismybrowser.com/detect/what-is-my-user-agent'
NOW YOU CAN RUN THE PROGRAM!
THE PROGRAM WILL CREATE AN OUTPUT DIRECTORY WITH PROFILES AND RAW HTML ASSOCIATED WITH EACH NAME AND PROFILE
P.S.: YOU CAN SWAP THE DEFAULT INPUT CSV WITH THE OTHER INPUT CSV'S IN THE 'outputs_from_linkFinder' FOLDER

"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time, random, pandas, os
# PRESETS
minValue = 15
maxValue = 30
page_load_time = 3
time_between_clicks = 0.5
username = "USERNAME"
password = "PASSWORD"
headless = False
input_name = "input/unfiltered_output.csv"
user_agent = "USER AGENT"
# web driver configuration
chrome_options = Options()
if headless:
    chrome_options.add_argument('--headless')
else:
    chrome_options.add_argument('--start-maximized')
chrome_options.add_argument(f"user-agent=[{user_agent}]")
driver = webdriver.Chrome(ChromeDriverManager().install())
# logs in to linkedIn
driver.get('https://www.linkedin.com')
sign_in_btn = driver.find_element_by_xpath("//a[text()='Sign in']")
sign_in_btn.click()
username_field = driver.find_element_by_xpath("//input[@id='username']")
password_field = driver.find_element_by_xpath("//input[@id='password']")
submit_btn = driver.find_element_by_xpath("//button[@type='submit']")
time.sleep(time_between_clicks)
username_field.send_keys(username)
time.sleep(time_between_clicks)
password_field.send_keys(password)
time.sleep(time_between_clicks)
submit_btn.click()
# parses csv into a name and link list
dataframe = pandas.read_csv(filepath_or_buffer=input_name, encoding='latin')
name_list = list(dataframe.name)
link_list = list(dataframe.link)
# for each name in the list, it scans the linkedIn profile
for x in range(len(name_list)):
    # generates random interval, then pauses for said interval
    random_interval = random.randint(minValue, maxValue)
    time.sleep(random_interval)
    current_link = link_list[x]
    driver.get(current_link) 
    # waits for page to fully load
    time.sleep(page_load_time)
    # shows all data on page for html collection
    show_more_buttons = driver.find_elements_by_xpath("//button[@class[contains(.,'pv-profile-section__see-more-inline')]]")
    reveal_accomplishments_buttons = driver.find_elements_by_xpath("//button[@aria-label[contains(.,'Expand')]]")
    see_more_buttons = driver.find_elements_by_xpath("//*[text()[contains(.,'see more')]]")
    all_buttons_list = [show_more_buttons, reveal_accomplishments_buttons, see_more_buttons]
    for button_list in all_buttons_list:
        for button in button_list:
            time.sleep(1)
            driver.execute_script("arguments[0].click();", button)
    # gets profile directory from url
    current_profile_directory = current_link.split('/')[-1]
    # adds current name and raw html from profile page to output directory
    current_name = name_list[x]
    new_file_name = f"output/{current_name}/{current_profile_directory}.html"
    try:
        new_file = open(new_file_name, "w", encoding="utf-8")
    except FileNotFoundError:
        os.mkdir(f"output/{current_name}")
        new_file = open(new_file_name, "w", encoding="utf-8")  
    raw_html = driver.page_source
    new_file.write(raw_html)
    new_file.close()
# closes web driver
driver.close()
