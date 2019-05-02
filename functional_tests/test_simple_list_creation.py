import time
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self):
        # Naomi has heard about an online to-do app. She goes
        # to view its homepage
        self.browser.get(self.live_server_url)

        # She sees the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item on the frontpage
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates and now the page lists:
        # "1: Buy peacock feathers" as an item in the to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        
        # There is still a text box inviting her to add another item.
        # She enters "Use peacock feathers to make a fly"
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        
        # The page updates again and now shows both items in the list
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # Satisfied, she exits the website
        

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Naomi starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # She notices her list has a unique URL
        naomi_list_url = self.browser.current_url
        self.assertRegex(naomi_list_url, '/lists/.+')

        # Now a new user, Megan, comes to the site.

        ## We use a new browser session to make sure that no information
        ## of Naomi's is coming through from cookies, etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Megan visits the home page. There's no sign of Naomi's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Megan starts a new list by entering a new item.
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Megan gets her own unique URL
        megan_list_url = self.browser.current_url
        self.assertRegex(megan_list_url, '/lists/.+')
        self.assertNotEqual(megan_list_url, naomi_list_url)

        # There is no sign of Naomi's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they leave the website
