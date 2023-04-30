from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from inconsistencyFixer import fix_str

import time 


#Ground constants 
delay = 2
d_angle = '140s' #s 

def search_question(name, RAh, RAm, RAs, DE, DEd, DEm, DEs, Epoch):
    if str(RAh) == '0':
        RAh = '00'
    if str(RAm) == '0':
        RAm = '00'
    if str(DEd) == '0':
        DEd = '00'
    if str(DEm) == '0':
        DEm = '00'

    return '{0} {1} {2} {3} {4}{5} {6} {7} {8}'.format(name, RAh, RAm, RAs, DE, DEd, DEm, DEs, Epoch)

class Searcher():
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()

    def search(self, name, RAh, RAm, RAs, DE, DEd, DEm, DEs, Epoch, save_adress = '', *tags):
        probably_tags = ['All', 'Radio', 'Infra Red', 'Selected', 'Objects', 'X-Ray']
        links = ['cats_match_all', 
                 'r_cats_match_sel',
                 'ir_cats_match_sel',
                 'cats_match_sel',
                 'o_cats_match_sel',
                 'x_cats_match_sel'
                 ]
        url = 'https://www.sao.ru/cats/'
        suffix = '.html'
        
        for tag in tags:
            if tag in probably_tags:
                self.driver.get(url + links[probably_tags.index(tag)] + suffix)
                #elems = self.driver.find_element(by=By.CSS_SELECTOR, value ='a')
                #elems.find_element(by=By., value=)

                #to select all possible sets 
                all_on = self.driver.find_element(by=By.XPATH, value = '//a[@href="{0}"]'.format(links[probably_tags.index(tag)] + '_a' + suffix))
                all_on.click()

                #to set off few sets due to a need of search
                if tag == 'Radio':
                    RFC = self.driver.find_element(by=By.XPATH, value = '//input[@value="RFC"]')
                    RFC.click()
                    ICRF = self.driver.find_element(by=By.XPATH, value = '//input[@value="ICRF"]')
                    ICRF.click()

                
                #time.sleep(delay)

                #setup the search   

                input_angle = self.driver.find_element(by=By.XPATH, value = '//input[@name="X_RADIUS"]')
                input_angle.clear()
                input_angle.send_keys(d_angle)

                epoch = self.driver.find_element(by=By.XPATH, value = '//input[@name="EPOCH"]')
                epoch.clear()
                epoch.send_keys(Epoch)

                #time.sleep(delay)
                textarea = self.driver.find_element(by=By.XPATH, value = '//textarea[@name="LIST_OBJ"]')
                textarea.send_keys(search_question(name, RAh, RAm, RAs, DE, DEd, DEm, DEs, Epoch))

                submit = self.driver.find_element(by=By.XPATH, value = '//input[@type="SUBMIT"]')
                submit.click()

                download = self.driver.find_element(by=By.XPATH, value = '//a[contains(.,"Here are search results")]')
                download.click()

                with open('{0}{1}.txt'.format(save_adress, name), 'w') as f:
                    f.write(fix_str(self.driver.find_element(by=By.TAG_NAME, value = "body").text))

                #time.sleep(delay * 200)
                #self.driver.close()
            