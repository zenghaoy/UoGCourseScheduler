import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

sleepTime = 1


# unit testing on switching fall and winter term
def test_switchBetweenTerms():
    options = Options()
    options.add_argument("start-maximized")
    s = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)
    driver.get("https://cis3760team204.com/")

    driver.implicitly_wait(30)
    driver.set_page_load_timeout(50)

    driver.find_element(By.XPATH, "//select[@class='form-select form-select-sm']").click()

    time.sleep(5)
    select = Select(driver.find_element(By.XPATH, "//select[@class='form-select form-select-sm']"))
    select.select_by_visible_text("Winter 2023")
    print("[Selected " + select.first_selected_option.text+"]")
    assert "Winter 2023" in select.first_selected_option.text

    time.sleep(5)
    driver.find_element(By.XPATH, "//select[@class='form-select form-select-sm']").click()

    time.sleep(5)
    select = Select(driver.find_element(By.XPATH, "//select[@class='form-select form-select-sm']"))
    select.select_by_visible_text("Fall 2022")
    print("[Selected " + select.first_selected_option.text+"]")
    assert "Fall 2022" in select.first_selected_option.text

    driver.close()


# unit testing on generating pdf course schedule
def test_generatePDFSchdule():
    options = Options()
    options.add_argument("start-maximized")
    s = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)
    driver.get("https://cis3760team204.com/")
    selectedCourses = [
        'SOC*1100'
    ]

    for i in range(0, len(selectedCourses)):
        driver.find_element("xpath", "//input[@id='searchCourse']") \
            .clear()
        time.sleep(sleepTime)
        driver.find_element("xpath", "//input[@id='searchCourse']") \
            .send_keys(selectedCourses[i])
        time.sleep(sleepTime)
        driver.find_element("xpath", "//button[@id='submitButton2']")\
            .click()
        time.sleep(sleepTime)
        element = driver \
            .find_element("xpath", "//button[@id='addButton']")
        driver \
            .execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(sleepTime)
        driver.find_element("xpath", "//button[@id='addButton']") \
            .click()
        time.sleep(sleepTime)

    time.sleep(sleepTime)

    driver.find_element(By.ID, "pdfButton").click()
    time.sleep(5)

    driver.close()

'''
# unit testing on all buttons
def test_allButtons():
    options = Options()
    options.add_argument("start-maximized")
    s = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)
    driver.get("https://cis3760team204.com/")
    driver.find_element("xpath", "//input[@id='searchCourse']") \
        .send_keys('CIS*3760')

    time.sleep(sleepTime)

    driver.find_element("xpath", "//button[@id='submitButton2']") \
        .click()
    print("[Search Button Passed]")

    time.sleep(sleepTime)

    # unit testing on add button           
    driver.find_element("xpath", "//button[@id='addButton']") \
        .click()
    print("[Add Button Passed]")

    time.sleep(sleepTime)

    # unit testing on remove button
    driver.find_element("xpath", "//button[@id='removeButton']") \
        .click()
    print("[Remove Button Passed]")
    time.sleep(sleepTime)
    driver.close()


# unit testing on max course number
def test_maxCourse():
    options = Options()
    options.add_argument("start-maximized")
    s = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)
    driver.get("https://cis3760team204.com/")
    selectedCourses = [
        'CIS*1200',
        'ACCT*1220',
        'ECON*1050',
        'SOC*1100',
        'MATH*1030',
        'FIN*2000'
    ]

    for i in range(0, len(selectedCourses)):
        driver.find_element("xpath", "//input[@id='searchCourse']") \
            .clear()
        time.sleep(sleepTime)
        driver.find_element("xpath", "//input[@id='searchCourse']") \
            .send_keys(selectedCourses[i])
        time.sleep(sleepTime)
        driver.find_element("xpath", "//button[@id='submitButton2']")\
            .click()
        time.sleep(sleepTime)
        element = driver \
            .find_element("xpath", "//button[@id='addButton']")
        driver \
            .execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(sleepTime)
        driver.find_element("xpath", "//button[@id='addButton']") \
            .click()
        time.sleep(sleepTime)
        try:
            WebDriverWait(driver, sleepTime) \
                .until(EC.alert_is_present())
            # switch_to.alert for switching to alert and accept
            alert = driver.switch_to.alert
            alert.accept()
            print("[Alert on max course number]")
        except TimeoutException:
            pass

    driver.close()


# unit testing on adding same course
def test_addSameCourse():
    options = Options()
    options.add_argument("start-maximized")
    s = Service("chromedriver.exe")
    driver = webdriver.Chrome(service=s, options=options)
    driver.get("https://cis3760team204.com/")
    selectedCourses = ['CIS*1200', 'CIS*1200']
    for i in range(0, len(selectedCourses)):
        driver.find_element("xpath", "//input[@id='searchCourse']") \
            .clear()
        time.sleep(sleepTime)
        driver.find_element("xpath", "//input[@id='searchCourse']") \
            .send_keys(selectedCourses[i])
        time.sleep(sleepTime)
        driver.find_element("xpath", "//button[@id='submitButton2']")\
            .click()
        time.sleep(sleepTime)
        driver.find_element("xpath", "//button[@id='addButton']") \
            .click()
        time.sleep(sleepTime)
        try:
            WebDriverWait(driver, sleepTime) \
                .until(EC.alert_is_present())
            # switch_to.alert for switching to alert and accept
            alert = driver.switch_to.alert
            alert.accept()
            print("[Alert on adding same course", selectedCourses[1], "]")
        except TimeoutException:
            pass
    driver.close()
'''
