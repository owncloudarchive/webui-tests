# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
sys.path.append('../')
from config import Config
import utilities
import time

from pages import LoginPage
from pages import FilesPage
from pages import AppsPage
from pages import AdminPage


class ExternalStorage(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        #self.driver = webdriver.Chrome()
        #self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1280, 720)
    


    #LOGIN
    def step1(self):
        driver = self.driver
        login_page = LoginPage.LoginPage(driver)
        login_page.open()
        login_page.login()
        time.sleep(2)

    
    #Go TO APPs
    def step2(self):
        driver = self.driver
        self.files_page = FilesPage.FilesPage(driver)
        self.files_page.go_to_apps_menu()
        time.sleep(2)


    #ENABLE EXTERNAL STORAGE APP
    def step3(self):
        driver = self.driver
        self.apps_page = AppsPage.AppsPage(driver)
        self.apps_page.enable_app('app-files_external')
        self.assertTrue(utilities.is_element_present_waiting(driver, By.ID, "app-files_external", 20))


    #Go BACK TO FILES VIEW
    def step4(self):
        self.apps_page.go_to_files_page()
        time.sleep(2)
    


    #Go TO ADMIN PAGE
    def step5(self):
        driver = self.driver
        self.files_page = FilesPage.FilesPage(driver)
        self.files_page.go_to_admin_page()
        time.sleep(2)

    #SET UP SFTP
    def step6(self):
        driver = self.driver
        self.admin_page = AdminPage.AdminPage(driver)
        self.admin_page.set_up_sftp()
        
    #CHECK OUT
    def step7(self):
        driver = self.driver
        self.admin_page.go_to_files_page()
        time.sleep(2)
        self.files_page = FilesPage.FilesPage(driver)
        time.sleep(3)
        self.assertTrue(self.files_page.look_for_element_in_visible_files_list('SFTP'))


    #Go BACK TO APPS PAGE
    def step8(self):
        driver = self.driver
        self.files_page = FilesPage.FilesPage(driver)
        self.admin_page.go_to_apps_menu()
        time.sleep(2)

    #DISABLE EXTERNAL STORAGE APP
    def step9(self):
        driver = self.driver
        self.apps_page = AppsPage.AppsPage(driver)
        self.apps_page.disable_app('app-files_external')
        self.apps_page.go_to_disabled_apps()
        time.sleep(2)
        self.assertTrue(utilities.is_element_present(driver, By.ID, "app-files_external"))

    '''
    #DISABLE EXTERNAL STORAGE APP
    def step8(self):
        driver = self.driver
        self.admin_page = AdminPage.AdminPage(driver)
        self.admin_page.go_to_apps_menu()
        self.apps_page.disable_app('app-files_external')
        self.assertTrue(utilities.is_element_present(driver, By.ID, "app-files_external"))
    '''

    def steps(self):
        for name in sorted(dir(self)):
            if name.startswith("step"):
                yield name, getattr(self, name) 

    def test_steps(self):
        for name, step in self.steps():
            try:
                step()
            except Exception as e:
                self.fail("{} failed ({}: {})".format(step, type(e), e))
    
    
    
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
