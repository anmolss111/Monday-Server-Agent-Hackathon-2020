# -*- coding: utf-8 -*-
from rest_framework import serializers
from products.models.products.Product import Product

class ProductSerializer(serializers.ModelSerializer):

	class Meta:

		model = Product
		fields = (

			'id',
			'name',
			'description',
			'image',
			'brand',
			'section',
			'createdAt',
			'updatedAt'
		)
