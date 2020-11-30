# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Table4(models.Model):

	id = models.AutoField(primary_key=True)
	column1 = models.CharField(max_length=255, blank=True, null=True)
	createdAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updatedAt = models.DateTimeField(auto_now=True, blank=True, null=True)

	def jsonToClass(self, data):

		if('column1' in data):
			self.column1 = data['column1']

