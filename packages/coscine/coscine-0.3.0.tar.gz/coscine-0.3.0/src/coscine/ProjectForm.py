###############################################################################
# Coscine Python3 Client
# Version 0.3.0
# Copyright (c) 2018-2021 RWTH Aachen University
# Contact: coscine@itc.rwth-aachen.de
# Git: https://git.rwth-aachen.de/coscine/docs/public/wiki/-/tree/master/
# Please direct bug reports, feature requests or questions at the URL above
# by opening an issue.
###############################################################################
# This python wrapper implements a client for the Coscine API.
# Coscine is an open source project at RWTH Aachen University for
# the management of research data.
# Visit https://coscine.rwth-aachen.de for more information.
###############################################################################

from collections.abc import MutableMapping
from .FormFlags import FormFlags
from .exceptions import *

###############################################################################

KEYS = [
	{
		"name": {
			"de": "Projektname",
			"en": "Project Name"
		},
		"flags": FormFlags.REQUIRED,
		"field": "ProjectName"
	},
	{
		"name": {
			"de": "Anzeigename",
			"en": "Display Name"
		},
		"flags": FormFlags.REQUIRED,
		"field": "DisplayName"
	},
	{
		"name": {
			"de": "Projektbeschreibung",
			"en": "Project Description"
		},
		"flags": FormFlags.REQUIRED,
		"field": "Description"
	},
	{
		"name": {
			"de": "Principal Investigators",
			"en": "Principal Investigators"
		},
		"flags": FormFlags.REQUIRED,
		"field": "PrincipleInvestigators"
	},
	{
		"name": {
			"de": "Projektstart",
			"en": "Project Start"
		},
		"flags": FormFlags.REQUIRED,
		"field": "StartDate"
	},
	{
		"name": {
			"de": "Projektende",
			"en": "Project End"
		},
		"flags": FormFlags.REQUIRED,
		"field": "EndDate"
	},
	{
		"name": {
			"de": "Disziplin",
			"en": "Discipline"
		},
		"flags": FormFlags.REQUIRED | FormFlags.CONTROLLED,
		"vocabulary": "Discipline",
		"field": "Discipline"
	},
	{
		"name": {
			"de": "Teilnehmende Organisation",
			"en": "Participating Organisations"
		},
		"flags": FormFlags.CONTROLLED,
		"vocabulary": "Organisation",
		"field": "Organization"
	},
	{
		"name": {
			"de": "Projektschlagwörter",
			"en": "Project Keywords"
		},
		"flags": FormFlags.NONE,
		"field": "Keywords"
	},
	{
		"name": {
			"de": "Sichtbarkeit",
			"en": "Visibility"
		},
		"flags": FormFlags.REQUIRED | FormFlags.CONTROLLED,
		"vocabulary": "Visibility",
		"field": "Visibility"
	},
	{
		"name": {
			"de": "Grant ID",
			"en": "Grant ID"
		},
		"flags": FormFlags.NONE,
		"field": "GrantId"
	},
	{
		"name": {
			"de": "Features",
			"en": "Features"
		},
		"flags": FormFlags.CONTROLLED,
		"vocabulary": "Features",
		"field": "Features"
	}
]

###############################################################################

class ProjectForm(MutableMapping):

###############################################################################

	def __init__(self, handle, parent=None, data=None):
		self.store = {}
		self.keys = {}
		self.lang = handle.lang
		disciplines = handle.get_disciplines()
		organizations = handle.get_organizations()
		visibility = handle.get_visibility()
		#features = handle.get_features()
		self.vocabulary = {
			"Discipline": disciplines,
			"Organisation": organizations,
			"Visibility": visibility,
			"Features": {}
		}
		self.parent = parent
		self.reset()

###############################################################################

	def __getitem__(self, key):
		return self.store[key]

###############################################################################

	def __setitem__(self, key, value):
		if key not in self.keys:
			raise KeyError()
		elif self.keys[key]["flags"] & FormFlags.CONTROLLED:
			vocabulary = self.keys[key]["vocabulary"]
			if type(value) is list:
				self.store[key] = []
				for val in value:
					if val in vocabulary:
						self.store[key].append(vocabulary[val])
					else:
						raise VocabularyError(value)
			else:
				if value in vocabulary:
					self.store[key] = vocabulary[value]
				else:
					raise VocabularyError(value)
		else:
			self.store[key] = value

###############################################################################

	def __delitem__(self, key):
		del self.store[key]

###############################################################################

	def __iter__(self):
		return iter(self.store)

###############################################################################

	def __len__(self):
		return len(self.store)

###############################################################################

	def is_required(self, key):
		if self.keys[key]["flags"] & FormFlags.REQUIRED:
			return True
		else:
			return False

###############################################################################

	def is_controlled(self, key):
		if self.keys[key]["flags"] & FormFlags.CONTROLLED:
			return True
		else:
			return False

###############################################################################

	def __repr__(self):
		text = "Coscine ProjectForm\n---------------------\n" \
				"R: required, C: controlled\n---------------------\n"
		for key in self.keys:
			status = ""
			value = ""
			if self.is_required(key):
				status = "R"
			if self.is_controlled(key):
				status += "C"
			if key in self.store:
				value = " = %s" % self.store[key]
			text += "[%s]%s%s\n" % (status, key, value)
		text += "----------------------\n"
		return text

###############################################################################

	def reset(self):
		for key in KEYS:
			self.keys[key["name"][self.lang]] = key
			if key["flags"] & FormFlags.CONTROLLED:
				key["vocabulary"] = self.vocabulary[key["vocabulary"]]

###############################################################################

	def generate(self):
		data = {}
		missing = []
		self.store.clear()
		for key in self.keys:
			value = self.keys[key]
			if key not in self.store:
				if self.is_required(key):
					missing.append(key)
			else:
				data[value["field"]] = self.store[key]

		if len(missing) > 0:
			raise RequirementError(missing)

		if self.parent:
			data["ParentId"] = self.parent["id"]

		return data

###############################################################################