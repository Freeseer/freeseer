#!/usr/bin/python

import unittest

from freeseer.framework.presentation import Presentation

class TestPresentation(unittest.TestCase):
	
	def setUp(self):
		self.pres = Presentation("John Doe", event="haha", time="NOW")

	def test_correct_time_set(self):
		self.assertTrue(self.pres.time == "NOW")
		self.pres.speaker = "John Doe"

	def test_speaker_not_first_param(self):
		self.assertNotEquals(self.pres.speaker, "John Doe")

	def test_event_is_default(self):
		self.assertTrue(self.pres.event == "haha")
