from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class LayoutAndStylingTest(FunctionalTest):

    def test_layout_and_styling(self):
        # Naomi goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She sees the input box is centered
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta = 30
        )

        # She starts a new list and sees the input is centered there too
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta = 30
        )
