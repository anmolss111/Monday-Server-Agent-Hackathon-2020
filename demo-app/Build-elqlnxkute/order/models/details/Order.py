# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Order(models.Model):

	id = models.AutoField(primary_key=True)
	firstName = models.	lastName = models.	emailId = models.	phoneNumber = models.	createdAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updatedAt = models.DateTimeField(auto_now=True, blank=True, null=True)

	def jsonToClass(self, data):

		if('firstName' in data):
			self.firstName = data['firstName']

		if('lastName' in data):
			self.lastName = data['lastName']

		if('emailId' in data):
			self.emailId = data['emailId']

		if('phoneNumber' in data):
			self.phoneNumber = data['phoneNumber']

