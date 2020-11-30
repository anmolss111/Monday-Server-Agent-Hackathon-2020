# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from order.models.details.Order import Order
from products.models.products.Product import Product


class OrderProduct(models.Model):

	id = models.AutoField(primary_key=True)
	order_id = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
	product_id = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
	createdAt = models.DateTimeField(auto_now_add=True, blank=True, null=True)
	updatedAt = models.DateTimeField(auto_now=True, blank=True, null=True)

	def jsonToClass(self, data):

		if('order_id' in data):
			modelObject = Order.objects.filter(id=data['order_id']).first()
			self.order_id = modelObject

		if('product_id' in data):
			modelObject = Product.objects.filter(id=data['product_id']).first()
			self.product_id = modelObject

