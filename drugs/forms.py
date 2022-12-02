from random import choices
from attr import field
from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from .models import Drug, Sale, Tablet, Suspension, Injectable, state_choices

unit_choices = (("Cartons", "Cartons"), ("Packets", "Packets"), ("Sachets", "Sachets"))
units_list = ["cart", "pack", "sach"]

# datalist and moeldatalist widgets

class DataList(forms.widgets.ChoiceWidget):
	input_type = "data_class"
	template_name = "drugs/datalist.html"
	option_template_name = "drugs/datalist_option.html"

class ModelChoicesWidget(DataList):
	def __init__(self, model=None, field=None, queryset=None, attrs=None, choices=()):
		super().__init__(attrs)
		self.choices = choices
		self.model = model
		self.field = field
		self.queryset = queryset
		# self.create_choices()


	
	
	def get_context(self, name: str, value, attrs):
		context = super().get_context(name, value, attrs)
		context["widget"]["datalist"] = self.datalist
		return context

	def get_list(self, queryset, field):
		choices = []
		for item in queryset:			
			choice = getattr(item, field)
			if not choice in choices:
				choices.append(choice)
		return choices

	def datalist(self):
		return self.choices

	def optgroups(self, name, value, attrs=None):
		"""Return a list of optgroups for this widget."""
		groups = []
		has_selected = False
		# self.create_choices()
		# self.choices = self.tuple_choices()
		print(self.choices)
		
		for index, (option_value, option_label) in enumerate(self.choices):
			if option_value is None:
				option_value = ""

			subgroup = []
			if isinstance(option_label, (list, tuple)):
				group_name = option_value
				subindex = 0
				choices = option_label
			else:
				group_name = None
				subindex = None
				choices = [(option_value, option_label)]
			groups.append((group_name, subgroup, index))

			for subvalue, sublabel in choices:
				selected = (not has_selected or self.allow_multiple_selected) and str(
					subvalue
				) in value
				has_selected |= selected
				subgroup.append(
					self.create_option(
						name,
						subvalue,
						sublabel,
						selected,
						index,
						subindex=subindex,
						attrs=attrs,
					)
				)
				if subindex is not None:
					subindex += 1
		# print(groups)
		return groups


def choice_tuple(choices):
	_choices = []
	for choice in choices:
		_choices.append((choice, choice))
	return _choices

class ChoiceField(forms.ChoiceField):
	def __init__(self, *, choices=(), list=False, **kwargs):
		super().__init__(**kwargs)
		if list:
			choices = choice_tuple(choices)
		self.choices = choices


class CallableChoiceIterator:
	def __init__(self, choices_func):
		self.choices_func = choices_func

	def __iter__(self):
		yield from self.choices_func()

class ModelChoiceField(forms.ChoiceField):
	widget = ModelChoicesWidget
	def __init__(self, model, field, check=True, **kwargs):
		super(ModelChoiceField, self).__init__(**kwargs)
		self.queryset = None
		self.model = self.widget.model = model
		self.field = self.widget.field = field
		self.check = check
		self.create_choices()

	def clean(self, value):
		"""
		Validate the given value and return its "cleaned" value as an
		appropriate Python object. Raise ValidationError for any errors.
		"""
		value = self.to_python(value)
		self.validate(value)
		print(value)
		self.run_validators(value)
		return value

	def create_choices(self):
		if self.model:
			self.queryset = self.create_queryset(self.model)
			self.choices = self.get_list(self.queryset, self.field)
			self.choices = self.tuple_choices()
			self._set_choices(self.choices)

	def create_queryset(self, model):
		queryset = self.queryset
		if not self.queryset:
			queryset = model.objects.all()
		return queryset
	
	def get_list(self, queryset, field):
		choices = []
		for item in queryset:			
			choice = getattr(item, field)
			if not choice in choices:
				choices.append(choice)
		return choices

	def tuple_choices(self):
		choices = self.choices
		_choices = []
		for choice in choices:
			_choices.append((choice, choice))
		return _choices


	def _get_choices(self):
		return self._choices

	def _get_model(self):
		return self.model

	def _set_choices(self, value):
		# Setting choices also sets the choices on the widget.
		# choices can be any iterable, but we call list() on it because
		# it will be consumed more than once.
		if callable(value):
			value = CallableChoiceIterator(value)
		else:
			value = list(value)

		self._choices = self.widget.choices = value
		# self.widget.model = self.model
		# self.widget.field = self.field

	choices = property(_get_choices, _set_choices)

	def validate(self, value):
		"""Validate that the input is in self.choices."""
		# print(super(forms.ChoiceField, self))
		super(forms.ChoiceField, self).validate(value)
		
		if value and not self.valid_value(value) and self.check:
			print("errorr!!")
			raise ValidationError(
				self.error_messages["invalid_choice"],
				code="invalid_choice",
				params={"value": value},
			)

	

class DrugForm(forms.ModelForm):
	drug_name = ModelChoiceField(model=Drug, field="drug_name", check=False)
	brand_name = ModelChoiceField(model=Drug, field="brand_name", check=False)
	drug_type = ModelChoiceField(model=Drug, field="drug_type", check=False)
	class Meta:
		model = Drug
		fields = ["drug_name", "brand_name", "drug_type", "state", "weight",
		"manufacturer", "exp_date", "units", "purchase_amount", "price", "category",
		"purpose", "location"]

	def upper(self):
		# try:
		# 	v = getattr(self, "drug_name")()
		# except ValidationError as e:
		# 	print(f"error 2 - {e.message}")
			
		form = super(DrugForm, self).save(commit=False)
		for field in ["drug_name", "brand_name", "drug_type", "manufacturer", "category", "purpose", "location"]:
			val = getattr(form, field)
			if val:
				setattr(form, field, val.upper())

	def save(self, commit=False):
		form = super(DrugForm, self).save(commit=False)
		form.save(commit)

class TabletForm(forms.ModelForm):
	class Meta:
		model = Tablet
		fields = ["tab_cd", "no_packs"]

		def save(self):
			super(TabletForm, self).save()

class SuspensionForm(forms.ModelForm):
	class Meta:
		model = Suspension
		fields = ["no_bottles", "no_packs"]

class InjectableForm(forms.ModelForm):
	class Meta:
		model = Injectable
		fields = ["no_bottles", "no_packs"]

class SaleForm(forms.ModelForm):
	# state = ChoiceField(choices=units_list, list=True)
	state = ChoiceField(widget=DataList, choices=units_list, list=True)
	# status = ChoiceField(widget=DataList, choices=units_list, list=True)
	drug_name = ModelChoiceField(model=Drug, field="drug_name")
	brand_name = ModelChoiceField(model=Drug, field="brand_name")
	class Meta:
		model = Sale
		fields = ["drug_name", "brand_name", "weight", "amount"]
	
	names = []
	ids = []
	total_price = 0
	
	def upper(self):
		form = super(SaleForm, self).save(commit=False)
		for field in ["drug_name", "brand_name"]:
			val = getattr(form, field)
			if val:
				setattr(form, field, val.upper())

	def add(self, drug, is_tab = False, register=False):
		
		# print(self.i)
		# if not self.i:
		# 	self.names = []
		# 	self.i += 1
		sale = super(SaleForm, self).save(commit=False)
		print(sale)
		print(sale.drug_name)
		print(self.instance.total_price)
		
		
		#self.add_list(sale, drug)

		print(sale.drug_name)
		print(sale.drug_name)
		print(self.instance.drug_name)


		drug.sell(sale.amount, is_tab)
		if register:
			sale.save()
			print(self.fields)
			return self.total_price

	def add_list(self, sale, drug):
		#self.names = sale.drug_name.append(sale.drug_name)
		self.ids.append(drug.id)
		self.total_price += (drug.price * sale.amount)
		sale.drug_name = sale.drug_name #", ".join(self.names)
		sale.total_price = self.total_price
		