from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_add_a_review_and_retrieve_it_later(self):
        # Clark gets wind of a hot new online movie review app. They 
        # go to check out its homepage
        self.browser.get('http://localhost:8000')
        
        # They notice the header and title on the page mention movie reviews
        self.assertIn('Movie Review', self.browser.title)
        self.fail('Finish the test!')

        # They see a list of movies and reviews for each movie
        
        # They can click on a movie link and go to a page with the
        # reviews for that movie. 
        
        # They can leave a review for the movie by filling in the text
        # boxes
        
        # After clicking the submit box, the app takes them back to the
        # home page where their review is listed 
        
        # They can click on the review link and see the details of the
        # review
        
        # At the top of the page is a link back to the home page.
        
        # Also in the nav bar is a link to a list of the latest reviews
        # This list of latest reviews includes Clarks latest review.
        
        # Clark feels satisfied

if __name__ == '__main__':
    unittest.main(warnings='ignore')
