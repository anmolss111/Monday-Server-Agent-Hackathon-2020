# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Users(models.Model):

	id = models.AutoField(primary_key=True)
	firstName = models.TextField(blank=True, null=True)
	lastName = models.TextField(blank=True, null=True)
	emailAddress = models.TextField(blank=True, null=True)
	password = models.TextField(blank=True, null=True)
	createdAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updatedAt = models.DateTimeField(auto_now=True, blank=True, null=True)

	def jsonToClass(self, data):

		if('firstName' in data):
			self.firstName = data['firstName']

		if('lastName' in data):
			self.lastName = data['lastName']

		if('emailAddress' in data):
			self.emailAddress = data['emailAddress']

		if('password' in data):
			self.password = data['password']

