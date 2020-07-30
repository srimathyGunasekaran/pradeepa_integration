from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import numpy as np
from datetime import datetime
import logging
from JobPortal_Common_Defs import JobPortal_Common
import Driver_Paths


class IndeedMain:
    job_list = []
    location_list = []
    job_title_list = []
    job_link_list = []
    company_name = ""
    job_title = ""
    job_link = ""
    driver = None
    start_time = datetime.now()
    url = ""
    page = 0
    count = 0
    job_details = {'Job Category': '', 'Date&Time': '', 'Searched Job Title': '', 'Searched Job Location': '',
                   'Job Portal': 'Indeed', 'Job Date Posted': '', 'Job Title': '',
                   'Job Company Name': '', 'Job Location': '', 'Job Phone No.': '', 'Job Email': '', 'Job Link': '',
                   'Job Description': ''}

    def __init__(self, driver, url):
        try:
            print(self.start_time)
            self.driver = driver
            self.url = url
            self.wait = WebDriverWait(self.driver, 20)

            print("######################################################################### \n"
                  "                                                                          \n"
                  "===========================Indeed Job Search=============================\n"
                  "                                                                          \n"
                  "##########################################################################")
            print(url)
        except Exception as e:
            print("Unknown Exception in Indeed class __init__ ", e)
            logging.error("Unknown Exception in Indeed class __init__ ", e)

    '--------------opening website-------'

    def indeed_opening_portal_url(self):
        try:
            self.driver.execute_script("window.open('')")
            self.driver.switch_to.window(self.driver.window_handles[0])
            sleep(1)
            findjobs_button = self.driver.find_element_by_xpath(
                "//button[@class='icl-Button icl-Button--primary icl-Button--md icl-WhatWhere-button']")
            findjobs_button.click()
            self.indeed_alert()
        except Exception as e:
            print("Unknown exception in indeed_opening_portal_url", e)
            logging.error("Unknown exception in indeed_opening_portal_url", e)
            self.driver.get_screenshot_as_file('Screenshots/indeed_opening_portal_url_exception.png')

    def indeed_iterating_job_location(self, job_arr, jp_common):
        try:
            jp_common.get_url(self.driver, self.url)
            self.indeed_opening_portal_url()  
            for title, loc in zip(job_arr[0], job_arr[1]):
                print("checki inside", title)
                key = jp_common.job_categorisation(title)
                self.job_details['Job Category'] = key
                print("key", key)
                print(title, loc)
                job_title = title
                job_loc = loc
                self.job_details['Date&Time'] = datetime.now().strftime("%b-%d-%Y %H:%M:%S")
                self.job_details['Searched Job Title'] = job_title
                self.job_details['Searched Job Location'] = job_loc
                self.indeed_website_search(jp_common, job_title, job_loc)
        except Exception as e:
            print("Unknown exception in indeed_iterating_job_location", e)
            logging.error("Unknown exception in indeed_iterating_job_location", e)
            self.driver.get_screenshot_as_file("Screenshots/indeed_iterating_job_location_exception.png")

    '-----------------alert---------------'

    def indeed_alert(self):
        try:
            WebDriverWait(self.driver, 3)
            self.driver.find_element_by_id("popover-foreground")
            self.driver.find_element_by_id("popover-x").click()
            print("alert found")
        except Exception as e:
            self.driver.get_screenshot_as_file("Screenshots/indeed_alert_exception.png")
            print("Unknown exception in indeed_alert", e)

    def indeed_website_search(self, jp_common, job, location):
        try:
            self.indeed_alert()
            what_label = self.driver.find_element_by_xpath("//input[@id='what']").send_keys(
                str(job) + Keys.TAB + str(location) + Keys.ENTER)
            self.page = 0
            self.count = 0
            self.indeed_alert()
            self.indeed_get_links(jp_common)
            self.indeed_alert()
            what = self.driver.find_element_by_xpath(
                "//input[@id='what']").send_keys(Keys.CONTROL, "a")
        except Exception as e:
            self.driver.get_screenshot_as_file("Screenshots/indeed_website_search_exception.png")
            print("Unknown exception in indeed_website_search", e)
            logging.error("Unknown exception in indeed_website_search", e)

    '------------getting title and link from the website-----------'

    def indeed_get_links(self, jp_common):
        try:
            job_url = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//td[@id='resultsCol']"
                                                                                     "/div/h2/a")))
            for i in job_url:
                self.job_title_list.append(i.get_attribute("title"))
                self.job_link_list.append(i.get_attribute("href"))
            self.page += 1
            print("Page_No", self.page)
            self.indeed_convert_title_link_to_numpy(self.job_title_list, self.job_link_list, jp_common)

        except Exception as e:
            self.driver.get_screenshot_as_file("Screenshots/indeed_get_links_exception.png")
            print("Unknown exception in indeed_get_links", e)
            logging.error("Unknown exception in indeed_get_links", e)

    '-----converting the job_title and job_link list to numpy------'

    def indeed_convert_title_link_to_numpy(self, _job_title, _job_link, jp_common):
        job_link = np.array(_job_link).tolist()
        job_title = np.array(_job_title).tolist()
        self.driver.switch_to.window(self.driver.window_handles[-1])
        for jobtitles, joblinks in np.nditer([job_title, job_link]):
            stri_joblinks = np.array_str(joblinks)
            self.job_details['Job Link'] = stri_joblinks
            self.job_details['Job Title'] = jobtitles
            self.driver.get(stri_joblinks)

            self.indeed_job_title_link(jobtitles, joblinks, jp_common)
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.indeed_next_page(jp_common)
        return None

    '--------checking for dismiss---------'

    def indeed_check_dismiss(self):
        try:
            dismiss = self.driver.find_element_by_xpath("//div[@class='icl-LegalConsentBanner-action']/button")
            dismiss.click()
        except Exception as e:
            self.driver.get_screenshot_as_file("Screenshots/indeed_check_dismiss_exception.png")
            print("Unknown exception in indeed_check_dismiss", e)
            logging.error("Unknown exception in indeed_check_dismiss", e)

    def indeed_next_page(self, jp_common):
        try:
            self.indeed_check_dismiss()
            self.indeed_alert()
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            sleep(1)
            nextpage = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH,
                                                                                           "//a[@aria-label='Next']")))
            nextpage.click()
            sleep(1)
            self.job_link_list.clear()
            self.job_title_list.clear()
            self.indeed_get_links(jp_common)
        except Exception as e:
            print("Unknown exception in indeed_next_page", e)
            logging.error("Unknown exception in indeed_next_page", e)
            self.driver.get_screenshot_as_file("Screenshots/indeed_next_page_exception.png")

    '----------extract job_title and job_link------'

    def indeed_job_title_link(self, jobtitle, joblink, jp_common):
        self.job_title = jobtitle
        self.job_link = joblink
        self.count += 1
        print(self.page, self.count, self.job_title, '\n', self.job_link)
        self.indeed_extract_companyname(jp_common)

        '----------extract company_name------'

    def indeed_extract_companyname(self, jp_common):
        try:
            self.company_name = WebDriverWait(self.driver, 1).until(EC.presence_of_element_located(
                (By.XPATH, "//div[@class='jobsearch-InlineCompanyRating icl-u-xs-mt--xs  jobsearch"
                           "-DesktopStickyContainer-companyrating']/div[1]"))).text
            print("company Name:", self.company_name)
            self.job_details['Job Company Name'] = self.company_name
        except Exception as e:
            print("Unknown exception in indeed_extract_companyname", e)
            logging.error("Unknown exception in indeed_extract_companyname", e)
            self.driver.get_screenshot_as_file("Screenshots/indeed_extract_companyname_exception.png")

        self.indeed_extract_job_location(jp_common)

    '----------extract joblocation--------'

    def indeed_extract_job_location(self, jp_common):
        try:
            location = self.driver.find_elements_by_xpath("//div[@class='icl-u-lg-mr--sm icl-u-xs-mr--xs']/"
                                                          "following-sibling::div")
            print("job location", location[-1].text)
            self.job_details['Job Location'] = location[-1].text
        except Exception as e:
            print("Unknown exception in indeed_extract_job_location", e)
            logging.error("Unknown exception in indeed_extract_job_location", e)
            self.driver.get_screenshot_as_file("Screenshots/indeed_extract_job_location_exception.png")
        self.indeed_extract_email_date_posted_phone(jp_common)

    '-----------extract email, phonenumber, dateposted--------------'

    def indeed_extract_email_date_posted_phone(self, jp_common):
        try:
            description = self.driver.find_element_by_xpath("//div[@id='jobDescriptionText']").text
            self.job_details['Job Description'] = description
            dateposted = self.driver.find_element_by_xpath("//div[@class='jobsearch-JobMetadataFooter']").text
            self.job_details['Job Email'] = jp_common.get_Email_desc(description)
            print(self.job_details['Job Email'])
            self.job_details['Job Phone No.'] = jp_common.get_Phno_desc(description)
            print(self.job_details['Job Phone No.'])
            dateposted = jp_common.datePosted(dateposted)
            self.job_details['Job Date Posted'] = dateposted
            print(dateposted)

            jp_common.get_all_phno()
            jp_common.get_all_email()
            jp_common.write_to_csv(self.job_details)
        except Exception as e:
            print("Unknown exception in indeed_extract_email_date_posted_phone", e)
            logging.error("Unknown exception in indeed_extract_email_date_posted_phone", e)
            self.driver.get_screenshot_as_file("Screenshots/indeed_extract_email_date_posted_phone_exception.png")


#job_search=["SDET","SDET","DS","Franklin-TN","Oregon","Oregon"]
#job_search=["SDET","Java Developer","Java","Chicago","Seattle","Atlanta"]
#job_search=["SDET","Franklin-TN"]
# job_search=["SDET","Remote"]
#
# print(job_search)
# job_arr = np.array(job_search).reshape(2, int(len(job_search) / 2))
# jp_common = JobPortal_Common()
# driver = jp_common.driver_creation("chrome")
# indeed_obj = Indeedmain(driver, Driver_Paths.indeed_url)
# indeed_obj.indeed_iterating_job_location(job_arr, jp_common)























