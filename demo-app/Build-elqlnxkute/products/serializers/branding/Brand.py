# -*- coding: utf-8 -*-
from rest_framework import serializers
from products.models.branding.Brand import Brand

class BrandSerializer(serializers.ModelSerializer):

	class Meta:

		model = Brand
		fields = (

			'id',
			'name',
			'logo',
			'createdAt',
			'updatedAt'
		)
