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
from collections import OrderedDict
from .FormFlags import FormFlags
from .exceptions import *

###############################################################################

class MetadataForm(MutableMapping):

	"""
	Coscine Metadata Input Form
	
	Can be used to generate json-ld formatted metadata
	"""

###############################################################################

	def __init__(self, handle, project, resource):
		self.store = {}
		self.keys = {}
		self.vocabulary = {}
		self.lang = handle.lang
		profile = handle.get_application_profile(resource, parse=True)
		self.profile = profile
		for entry in profile["graph"]:
			if "class" in entry:
				uri = entry["class"]
				name = entry["name"][self.lang]
				data = handle.get_instance(project, uri)
				lang = self.lang
				vocabulary = {}
				if lang not in data:
					lang = "en"
				for entry in data[lang]:
					vocabulary[entry["name"]] = entry["value"]
				self.vocabulary[name] = vocabulary
		self.reset()

###############################################################################

	def __getitem__(self, key):
		return self.store[key]

###############################################################################

	def __setitem__(self, key, value):
		if key not in self.keys:
			raise KeyError(key)
		elif "vocabulary" in self.keys[key]:
			vocabulary = self.keys[key]["vocabulary"]
			if type(value) is list:
				self.store[key] = []
				for val in value:
					if val in vocabulary:
						self.store[key].append(vocabulary[val])
					else:
						raise VocabularyError()
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

	def __repr__(self):
		text = "Coscine MetadataForm\n----------------------\n" \
				"R: required, C: controlled\n---------------------\n"
		for key in self.keys:
			status = ""
			value = ""
			if self.is_required(key):
				status = "R"
			if "vocabulary" in self.keys[key]:
				status += "C"
			if key in self.store:
				value = " = %s" % self.store[key]
			text += "[%s] %s%s\n" % (status, key, value)
		text += "----------------------\n"
		return text

###############################################################################

	def is_required(self, key):
		info = self.keys[key]
		if "minCount" in info and info["minCount"] > 0:
			return True
		else:
			return False

###############################################################################

	def is_controlled(self, key):
		if key in self.vocabulary:
			return True
		else:
			return False

###############################################################################

	def reset(self):
		self.store.clear()
		for entry in self.profile["graph"]:
			name = entry["name"][self.lang]
			self.keys[name] = entry

			if self.is_controlled(name):
				self.keys[name]["vocabulary"] = self.vocabulary[name]

		# Sort the keys according to their application profile order
		tuples = sorted(self.keys.items(), key = lambda x: x[1]["order"])
		self.keys = OrderedDict(tuples)

###############################################################################

	def generate(self):

		"""
		Generates JSON-LD formatted metadata representation
		
		Raises
		------
		RequirementError
			When one or more required have not been set

		Returns
		--------
		JSON-LD formatted metadata
		"""

		metadata = {}
		RDFTYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"

		# Set application profile type used for the metadata
		metadata[RDFTYPE] = [{
			"type": "uri",
			"value": self.profile["id"]
		}]
		
		# Collect missing required fields
		missing = []
		
		# Set metadata fields
		for key in self.keys:
			if key not in self.store:
				if self.is_required(key):
					missing.append(key)
			else:
				field = self.keys[key]
				path = field["path"]
				metadata[path] = [{
					"value": self.store[key],
					"datatype": field["datatype"],
					"type": field["type"]
				}]
		
		# Check missing field list
		if len(missing) > 0:
			raise RequirementError(missing)
		
		return metadata

###############################################################################