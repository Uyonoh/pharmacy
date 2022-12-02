# def optgroups(self, name, value, attrs=None):
	# 	"""Return a list of optgroups for this widget."""
	# 	groups = []
	# 	has_selected = False
	# 	self.create_choices()
	# 	for option_value in self.choices:
	# 		if option_value is None:
	# 			option_value = ""
	# 		groups.append(option_value)

	# 	return groups




class ListChoiceWidget(forms.widgets.ChoiceWidget):
	input_type = "data_class"
	template_name = "drugs/datalist.html"
	option_template_name = "drugs/datalist_option.html"
	def __init__(self, attrs=None, choices=()):
		super().__init__(attrs)
		
		self.choices = choices
		# self.choices = self.tuple_choices()
		

	def tuple_choices(self):
		choices = self.choices
		_choices = []
		for choice in choices:
			_choices.append((choice, choice))
		return _choices

	def options(self, name, value, attrs=None):
		"""Yield a flat list of options for this widgets."""
		for group in self.optgroups(name, value, attrs):
			yield from group[1]

	def optgroups(self, name, value, attrs=None):
		"""Return a list of optgroups for this widget."""
		groups = []
		has_selected = False
		# self.choices = self.tuple_choices()
		# print(self.choices)
		
		
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


