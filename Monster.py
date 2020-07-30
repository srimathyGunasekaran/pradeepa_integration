import datetime
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import logging
from selenium.webdriver.support.ui import WebDriverWait


class Monster:
    try:
        monster_job_email = []
        monster_job_phoneNo = []
        driver = None
        start_time = datetime.now()
        url = ""
        wait = ''
        link_count = 0
        job_count = []
        #logging.basicConfig(filename='monster.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',level=logging.INFO)
        #logger = logging.getLogger(__name__)
        job_details = {'Job Category': '', 'Date&Time': '', 'Searched Job Title': '', 'Searched Job Location': '',
                       'Job Portal': 'Monster', 'Job Date Posted': '', 'Job Title': '',
                       'Job Company Name': '', 'Job Location': '', 'Job Phone No.': '', 'Job Email': '', 'Job Link': '',
                       'Job Description': ''}

        def __init__(self, driver, url):
            try:
                print(self.start_time)
                self.driver = driver
                self.url = url
                self.wait = WebDriverWait(self.driver, 30)
                # logging.basicConfig(filename='monster.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',
                #                    level=logging.INFO)

                print("######################################################################### \n"
                      "                                                                          \n"
                      "===========================Monster Job Search=============================\n"
                      "                                                                          \n"
                      "##########################################################################")
                print(url)
            except Exception as e:
                print("Unknown Exception in Monster class __init__ ",e)
                logging.error("Unknown Exception in Monster class __init__ ",e)

        # search jobs
        def monster_search_jobs(self, jp_common, job_title, job_location):
            try:
                logging.info("In monster_search_jobs")
                print("In monster_search_jobs")

                # Finding Job Title Textbox element and sending text.
                job_title_web_element = jp_common.find_web_element("//*[@id='keywords2']", "Job Title Textbox", "one", self.wait)
                jp_common.web_element_action(job_title_web_element,"send_keys",job_title,"Job Title Textbox")

                # Finding Job Location Textbox element and sending text.
                job_location_web_element=jp_common.find_web_element("//*[@id='location']", "Job Location Textbox", "one", self.wait)
                jp_common.web_element_action(job_location_web_element,"send_keys",job_location,"Job Location Textbox")

                # Finding Search Button element and clicking it.
                search_web_element = jp_common.find_web_element("//*[@id='doQuickSearch']", "Search Button", "one", self.wait)
                jp_common.web_element_action(search_web_element,"click","","Search Button")

            except Exception as e:
                print("Unexpected error in monster_search_jobs",e)
                logging.error("Unexpected exception in monster_search_jobs",e)
                self.driver.get_screenshot_as_file("Screenshots\monster_search_jobs_exception.png")

        def monster_valid_job(self, jp_common):
            try:
                logging.info("In monster_valid_jobs")
                print("In monster_valid_jobs")

                # Finding Job Title Textbox element and sending text.
                #msg = jp_common.find_web_element("/html/body/div[2]/section/div/header/h1", "Job Search Message", "one",
                #                                                   self.wait).text
                #job_search_message_web_element = jp_common.find_web_element("/html/body/div[2]/section/div/header",
                #                                                            "Job Search Message", "one",
                #                                                            self.wait)
                #print(jp_common.web_element_action(job_search_message_web_element, "get_text","", "Job Search Message"))
                #msg=job_search_message_web_element.text
                msg = "New Jobs in U.S"
                print(msg,"===================")
                #print(driver.find_element_by_xpath("/html/body/div[2]/section/div/header/h1").text)
                #if job_search_message_web_element.text == "New Jobs in the US":
                if msg == "Sorry, we didn't find any jobs matching your criteria":

                    return False
                else:
                    return True

            except Exception as e:
                print("Unexpected error in monster_valid_jobs", e)
                logging.error("Unexpected exception in monster_valid_jobs", e)
                self.driver.get_screenshot_as_file("Screenshots\monster_valid_jobs_exception.png")

        # load more
        def monster_loadmore_jobs(self):
            logging.debug("In monster_loadmore_jobs")
            print("In monster_loadmore_jobs")
            click = 0
            time.sleep(3)
            try:
                load_more_web_element=self.driver.find_element_by_xpath("//*[@id='loadMoreJobs'][@class='mux-btn btn-secondary load-more-btn ']")
                print(load_more_web_element, "load more found")
                while load_more_web_element:
                    click += 1
                    load_more_web_element = self.driver.find_element_by_xpath("//*[@id='loadMoreJobs'][@class='mux-btn btn-secondary load-more-btn ']")
                    print("Load More found and clicked", click, "time(s)")
                    '''if(load_more_web_element==None):
                        break
                    print("while load more")
                    #load_more_web_element = jp_common.find_web_element("//*[@id='loadMoreJobs']", "Load More Button", "one",
                    #                                                   self.wait)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    actions = ActionChains(self.driver)
                    actions.move_to_element(load_more_web_element)
                    actions.perform()
                    print("Load More found and clicked",click,"time(s)")'''

                    try:
                        load_more_web_element.click()
                    except Exception as e:
                        print("Unexpected error when clicking load more button",e)
                        logging.error("Unexpected error when clicking load more button",e)
                    time.sleep(3)
            except Exception as e:
                print("Unexpected error in monster_loadmore_jobs",e)
                logging.error("Unexpected exception in monster_loadmore_jobs")
                self.driver.get_screenshot_as_file("Screenshots/monster_load_more_jobs_exception.png")

        # Get list of job links populated
        def monster_get_job_links(self, jp_common):
            #  job links xpath
            print("In monster_get_job_links")
            logging.info("In monster_get_job_links")
            try:
                job_links_web_element = jp_common.find_web_element("//*[@id='SearchResults']/section/div/div[2]/header/h2/a",
                                                                   "Job Links", "multiple", self.wait)
                return job_links_web_element
            except Exception as e:
                print("Unknown Exception in monster_get_jobs_links",e)
                logging.error("Unknown Exception in monster_get_jobs_links",e)
                self.driver.get_screenshot_as_file("Screenshots/monster_get_job_links_exception.png")

        # Get list of job company names
        def monster_get_job_company(self,jp_common):
            print("In monster_get_job_company")
            logging.info("In monster_get_job_company")
            try:
                job_company_web_element = jp_common.find_web_element("//*[@id='SearchResults']/section/div/div[2]/div[1]/span",
                                                                     "Job Company Name", "multiple", self.wait)
                return job_company_web_element
            except Exception as e:
                print("Unknown Exception in monster_get_job_company", e)
                logging.error("Unknown Exception in monster_get_job_company", e)
                self.driver.get_screenshot_as_file("Screenshots/monster_get_job_company.png")

        # Get names of job locations
        def monster_get_job_location(self, jp_common):
            print("In monster_get_job_location")
            logging.info("In monster_get_job_location")
            try:
                job_location_web_element = jp_common.find_web_element("//*[@id='SearchResults']/section/div/div[2]/div[2]/span",
                                                                      "Job Location", "multiple", self.wait)
                return job_location_web_element
            except Exception as e:
                print("Unknown Exception in get_jobs_location".e)
                logging.error("Unknown Exception in get_jobs_location".e)
                self.driver.get_screenshot_as_file("Screenshots/monster_get_job_location_exception.png")

        # Get Date-time of job posted
        def monster_get_job_posted_datetime(self, jp_common):
            print("In monster_get_posted_datetime")
            logging.info("In monster_get_posted_datetime")
            try:
                job_posted_datetime_web_element = jp_common.find_web_element("//*[@id='SearchResults']/section/div/div[3]/time",
                                                                             "Job Date Posted", "multiple", self.wait)
                return job_posted_datetime_web_element
            except Exception as e:
                print("Unknown Exception in monster_get_jobs_poster_datetime")
                logging.error("Unknown Exception in monster_get_jobs_poster_datetime")
                self.driver.get_screenshot_as_file("Screenshots/monster_get_job_posted_datetime_exception.png")

        # Get Job description and scrape Email and Phone number
        def monster_get_job_desc(self, job_date_posted, job_title, job_loc, job_links, job_company, job_location, jp_common):
            print("In monster_get_jobs_desc")
            logging.info("In monster_get_jobs_desc")
            try:
                self.link_count = 0
                self.job_details['Searched Job Title'] = job_title
                self.job_details['Searched Job Location'] = job_loc
                for link in job_links:
                    job_desc = []

                    print("job title:", link.text)
                    print("Monster, Link clicked  :", job_title, job_loc, self.link_count+1, "/", len(job_links))

                    print("==============================================>", self.link_count+1)
                    self.job_details['Job Link'] = link.get_attribute("href")
                    self.job_details['Job Title'] = link.text
                    self.job_details['Job Company Name'] = job_company[self.link_count].text
                    self.job_details['Job Location'] = job_location[self.link_count].text
                    self.job_details['Job Date Posted'] = job_date_posted[self.link_count].text

                    try:
                        jp_common.web_element_action(link, "click", "", "Job link")
                        #jp_common.get_url(driver,link.get_attribute("href"))
                        #job_description_web_element=jp_common.find_web_element("//*[@id='main-content']/div/div/div/div[3]",
                        #                                                       "Job Description", "multiple",self.wait)
                        job_description_web_element = jp_common.find_web_element(
                            "//*[@id='JobBody']","Job Description", "multiple", self.wait)
                        for element in job_description_web_element:
                            job_desc.append(element.text)
                    except Exception as e:
                        print("Unknown Exception occurred while clicking to get job description",e)
                        logging.error("Unknown Excecption occurred while clicking to get job description",e)
                    else:
                        #for element in job_description_web_element:
                        #    job_desc.append(element.text)
                            #job_desc+=element.text
                        job_desc=' '.join(map(str, job_desc))
                        #print(job_desc)
                        self.job_details['Job Description']=job_desc
                        self.job_details['Job Email'] = jp_common.get_Email_desc(job_desc)
                        print(self.job_details['Job Email'])
                        self.job_details['Job Phone No.'] = jp_common.get_Phno_desc(job_desc)
                        print(self.job_details['Job Phone No.'])

                        self.job_details['Date&Time'] = datetime.now().strftime("%b-%d-%Y %H:%M:%S")
                        jp_common.write_to_csv(self.job_details)
                        # jp_common.copy_to_json("Job_Details.json",self.job_details)
                    self.link_count += 1
            except Exception as e:
                print("Unknown exception in monster_get_job_desc",e)
                logging.error("Unknown exception in monster_get_job_desc",e)
                self.driver.get_screenshot_as_file("Screenshots/monster_get_job_desc_exception.png")

        # To get jobs from the user given choices
        def monster_get_jobs(self, arr, jp_common):
            print("In monster_get_jobs")
            logging.info("In monster_get_jobs")
            try:
                jp_common.get_url(self.driver, self.url)
                for title, loc in zip(arr[0], arr[1]):
                    print(title, loc)
                    job_title = title
                    job_loc = loc

                    self.monster_search_jobs(jp_common, job_title, job_loc)
                    if self.monster_valid_job(jp_common) == True:

                        self.monster_loadmore_jobs()
                        job_links = self.monster_get_job_links(jp_common)
                        job_company = self.monster_get_job_company(jp_common)
                        job_location = self.monster_get_job_location(jp_common)
                        job_date_posted = self.monster_get_job_posted_datetime(jp_common)
                        self.job_details['Job Category'] = jp_common.set_job_category(job_title)

                        print("Links Populated for Monster :", job_title, job_loc, "are :", len(job_links))
                        self.monster_get_job_desc(job_date_posted, job_title, job_loc, job_links, job_company, job_location, jp_common)
                        self.job_count.append(self.link_count)
                        jp_common.get_all_phno()
                        jp_common.get_all_email()
                        #self.report(arr, "")

                    self.monster_clear_search(job_title, job_loc)
                    self.report(arr,"Sorry no jobs matching your search",jp_common)

                    jp_common.time_to_execute()
            except Exception as e:
                print("Unknown exception in monster_get_jobs",e)
                logging.error("Unknown exception in monster_get_jobs",e)
                self.driver.get_screenshot_as_file("Screenshots/monster_get_jobs_exception.png")

        # clear search boxes
        def monster_clear_search(self, job_title, job_loc):
            print("In monster_clear_search")
            logging.info("monster_clear_search")
            try:
                for i in range(len(job_title)):
                    self.driver.find_element_by_xpath("//*[@id='keywords2']").send_keys(Keys.BACKSPACE)

                for i in range(len(job_loc)):
                    self.driver.find_element_by_xpath("//*[@id='location']").send_keys(Keys.BACKSPACE)

            except Exception as e:
                print("Unknown exception in monster_clear_search", e)
                logging.error("Unknown exception in monster_clear_search", e)
                self.driver.get_screenshot_as_file("Screenshots/monster_get_clear_search_exception.png")

        def report(self, arr, msg, jp_common):
            try:
                print("================================")
                print("=======Monster Report===========")
                for title, loc, count in zip(arr[0], arr[1], range(len(self.job_count))):
                    if len(self.job_count) > 0:
                        print(title, loc, ":", self.job_count[count], "Jobs")
                    else:
                        print(title, loc, ":", msg)
                print("Total Monster Execution :", jp_common.time_to_execute())
                print("================================")
            except Exception as e:
                print("Unknown exception in monster_clear_search", e)
                logging.error("Unknown exception in monster_clear_search", e)
                self.driver.get_screenshot_as_file("Screenshots/monster_get_clear_search_exception.png")

    except Exception as e:
        print("Unknown Exception occurred in Class Monster",e)
        logging.error("Unknown Exception occurred in Class Monster",e)
        driver.get_screenshot_as_file("Screenshots/monster_class_exception.png")


#job_search=["Java Developer","Seattle"]
#job_search=["SDET","Python Developer","Java Developer","Chicago","Seattle","Atlanta"]
#job_search = ["dsds", "Seattle"]
#job_search=["SDET","Franklin-TN"]
#job_search=["SDET","SDET","DS","Franklin-TN","Oregon","Oregon"]
#job_search=["Java","Atlanta"]
# job_search=["SDET","Seattle"]
#
# print(job_search)
# job_arr = np.array(job_search).reshape(2, int(len(job_search) / 2))
# jp_common = JobPortal_Common()
# driver = jp_common.driver_creation("chrome")
# monster_obj = Monster(driver, Driver_Paths.monster_url)
# monster_obj.monster_get_jobs(job_arr, jp_common)


#
# from openburrito import find_burrito_joints, BurritoCriteriaConflict
# # "criteria" is an object defining the kind of burritos you want.
# try:
#     places = find_burrito_joints(criteria)
# except BurritoCriteriaConflict as err:
#     logger.warn("Cannot resolve conflicting burrito criteria: {}".format(err.message))
#     places = list()

#https://www.datadoghq.com/blog/python-logging-best-practices/
# lowermodule.py
# import logging
#
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
# logger = logging.getLogger(__name__)
#
# #uppermodule
# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
# logger = logging.getLogger(__name__)
#https://www.datadoghq.com/blog/python-logging-best-practices/

#/html/body/div[2]/section/div/header/h1