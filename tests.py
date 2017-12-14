from app import JenkinsFinder
import unittest
from unittest.mock import Mock

class TestJenkinsFinder(unittest.TestCase):
    def test_if_true(self):
        jenkinsfinder = JenkinsFinder("","")
        jenkinsfinder._api_call = Mock(return_value={
  "builds" : [
    {
      "number" : 3,
      "url" : "http://szkola.hellgate.pl:8080/job/homebrew/3/"
    },
    {
      "number" : 2,
      "url" : "http://szkola.hellgate.pl:8080/job/homebrew/2/"
    },
    {
      "number" : 1,
      "url" : "http://szkola.hellgate.pl:8080/job/homebrew/1/"
    }
  ],
  "nextBuildNumber" : 4
})
        self.assertEqual(jenkinsfinder.builds_urls(), ['http://szkola.hellgate.pl:8080/job/homebrew/3/', 'http://szkola.hellgate.pl:8080/job/homebrew/2/', 'http://szkola.hellgate.pl:8080/job/homebrew/1/'])
    def test_else(self):
        jenkinsfinder = JenkinsFinder("","")
        jenkinsfinder._api_call = Mock(return_value={
  "builds" : [
    {
      "number" : 3,
      "url" : "http://szkola.hellgate.pl:8080/job/homebrew/3/"
    },
    {
      "number" : 2,
      "url" : "http://szkola.hellgate.pl:8080/job/homebrew/2/"
    },
    {
      "number" : 1,
      "url" : "http://szkola.hellgate.pl:8080/job/homebrew/1/"
    }
  ],
  "nextBuildNumber" : 4
})
        self.assertEqual(jenkinsfinder.builds_urls(1), ['http://szkola.hellgate.pl:8080/job/homebrew/3/'])



if __name__ == "__main__":
    unittest.main()
