# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from products.models.branding.Brand import Brand
from products.models.branding.Section import Section


class Product(models.Model):

	id = models.AutoField(primary_key=True)
	name = models.TextField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	image = models.TextField(blank=True, null=True)
	brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
	section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=True, null=True)
	createdAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updatedAt = models.DateTimeField(auto_now=True, blank=True, null=True)

	def jsonToClass(self, data):

		if('name' in data):
			self.name = data['name']

		if('description' in data):
			self.description = data['description']

		if('image' in data):
			self.image = data['image']

		if('brand' in data):
			modelObject = Brand.objects.filter(id=data['brand']).first()
			self.brand = modelObject

		if('section' in data):
			modelObject = Section.objects.filter(id=data['section']).first()
			self.section = modelObject

