"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from random import choice, randint, sample
import string

from si.models import Result, Test

def create_results(x):
    for tests in xrange(x):
        test = Test(name="test%s"%tests, desc="desc for %s"%tests)
        test.save()
        for i in xrange(randint(1,5)):
            r = Result(test=test)
            r.name =  ''.join(sample(string.letters, randint(4,10)))
            r.status = choice(("pass","fail"))
            r.save()
create_results(100)

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
