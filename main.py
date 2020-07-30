from Indeed import IndeedMain
import numpy as np
import sys
import Driver_Paths
from JobPortal_Common_Defs import JobPortal_Common
print("Starting, Job Search....")

'Creating numpy array'
job_search = [i for i in sys.argv[1].split(',')]
job_arr = np.array(job_search).reshape(2, int(len(job_search)/2))

'Create JobPortal_Common() object to access common functions'
jp_common = JobPortal_Common()

'Create browser driver'
browser_list = ["chrome", "gecko", "msedge"]
driver=jp_common.driver_creation("chrome")

'Monster Search, Create Monster object and get jobs'
# monster_obj = Monster(driver,Driver_Paths.monster_url)
# monster_obj.monster_get_jobs(job_arr,jp_common)
# from Monster import Monster

'Indeed Search,Create Glassdoor object and get jobs'
indeed_obj = IndeedMain(driver, Driver_Paths.indeed_url)
indeed_obj.indeed_iterating_job_location(job_arr, jp_common)

'Quit Browser'
jp_common.time_to_execute()
jp_common.exit_browser(driver)
print("Job Search Ended.")
