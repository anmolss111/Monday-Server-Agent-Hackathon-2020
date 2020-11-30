# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from users.models.sub_component_1.Users import Users


class Table3(models.Model):

	id = models.AutoField(primary_key=True)
	column1 = models.CharField(max_length=255, blank=True, null=True)
	column2 = models.ForeignKey(Users, on_delete=models.CASCADE, blank=True, null=True)
	createdAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updatedAt = models.DateTimeField(auto_now=True, blank=True, null=True)

	def jsonToClass(self, data):

		if('column1' in data):
			self.column1 = data['column1']

		if('column2' in data):
			modelObject = Users.objects.filter(id=data['column2']).first()
			self.column2 = modelObject

