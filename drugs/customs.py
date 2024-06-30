from random import choices
# from attr import field
from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from drugs.models import Drug

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
		if isinstance(value, str):
			value = value.upper()
		self.validate(value)
		print(value)
		self.run_validators(value)
		return value

	def create_choices(self):
		try:
			self.model.objects.all()
			self.queryset = self.create_queryset(self.model)
			self.choices = self.get_list(self.queryset, self.field)
			self.choices = self.tuple_choices()
			self._set_choices(self.choices)
		except Exception:
			self._set_choices(())

	def create_queryset(self, model):
		queryset = self.queryset
		if not self.queryset:
			queryset = model.objects.all()
		return queryset
	
	def get_list(self, queryset, field=""):
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
			print("validation error!!")
			raise ValidationError(
				self.error_messages["invalid_choice"],
				code="invalid_choice",
				params={"value": value},
			)

def edit_tab(name:str, exp_date:str, tab_cd:str):
	name = name.upper()
	drug = Drug.objects.filter(drug_name=name, exp_date=exp_date)
	if not drug.count():
		drug = Drug.objects.filter(brand_name=name, exp_date=exp_date)
	
	print(drug[0])

	if drug[0].state == "Tab":
		drug = drug[0]
		tablet = drug.Tablet
		tablet.tab_cd = tab_cd
		tablet.save(sale=True)
	
