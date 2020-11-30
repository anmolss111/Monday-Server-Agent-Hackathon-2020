# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Brand(models.Model):

	id = models.AutoField(primary_key=True)
	name = models.TextField(blank=True, null=True)
	logo = models.TextField(blank=True, null=True)
	createdAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updatedAt = models.DateTimeField(auto_now=True, blank=True, null=True)

	def jsonToClass(self, data):

		if('name' in data):
			self.name = data['name']

		if('logo' in data):
			self.logo = data['logo']

