#-- Selenium Imports --
from pymstodo import ToDoConnection
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

import os
import time


class MSTodo:
    # TODO Organize MStodo Class
    
    """The main purpose of this class is to fetch the tasks from a microsoft todo account
    NOTE: Please set the following information as environment variables:
    
    // Microsoft account
    'LIVE_USER' 
    'LIVE_PASS'
    
    // Azure App Information
    'AZURE_CLIENT_ID'
    'AZURE_CLIENT_SECRET'
    """
    # -- Initial Config --
    
    list_name = "Tasks"
    list = []
        
    
    @classmethod
    def parse_list(self, list):
        try:
            for i in list:
                self.list.append(i.title)
        except TypeError:
            print("WARNING: MSTodo list is empty.")
    
    @classmethod
    def fetch_anki_list(self):
        print(f"Fetching anki list '{self.list_name}' from MSTodo...")
        self.parse_list(MSTodo.get_tasks())
        
        if not self.list:
            return
        
        print("Fetched tasks:\n")
        print(*self.list, sep='\n')
        print("Developer note: 'List is not yet added to csv.")
    
    @classmethod
    def get_tasks(self):
        client_id = os.getenv('AZURE_CLIENT_ID')
        client_secret = os.getenv('AZURE_CLIENT_SECRET')

        print('Setting Up Browser...')
        try:
            auth_url = ToDoConnection.get_auth_url(client_id)
            
            redirect_resp = self.get_redirect_url(auth_url)
            token = ToDoConnection.get_token(client_id, client_secret, redirect_resp)
            todo_client = ToDoConnection(client_id=client_id, client_secret=client_secret, token=token)
        except Exception:
            print ("ERROR: Credential Error. Please make sure the environment variables are properly set up!")
            return
        
        print('Fetching List...')
        
        lists = todo_client.get_lists()
        
        for i in range(len(lists)):
            if lists[i].displayName == self.list_name:
                task_list = lists[i]
        
        tasks = todo_client.get_tasks(task_list.list_id)
        
        print('Marking tasks as complete...')
        
        for task in tasks:
            todo_client.complete_task(task.task_id, task_list)
        
        if not tasks:
            return
        
        return tasks
    
    @staticmethod
    def set_driver():
        options = webdriver.ChromeOptions()
        options.add_argument("disable-infobars")
        options.add_argument("start-maximized")
        options.add_argument("disable-dev-shm-usage")
        options.add_argument("no-sandbox")
        options.add_argument("disable-blink-features=AutomationControlled")
        options.add_argument("headless")
        options.add_argument("--log-level=3")

        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        driver = webdriver.Chrome(options=options)
        return driver
    
    @staticmethod
    def get_redirect_url(url):
        try:
            driver = MSTodo.set_driver()
            driver.get(url)
            user_in = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="i0116"]')))
            user_in.send_keys(os.getenv('LIVE_USER'))
            user_in.send_keys(Keys.ENTER)
            time.sleep(1)
            pass_in = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="i0118"]')))
            pass_in.send_keys(os.getenv('LIVE_PASS'))
            pass_in.send_keys(Keys.ENTER)
        except TypeError:
            return
        
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="idSIButton9"]'))).click()

        return driver.current_url
    