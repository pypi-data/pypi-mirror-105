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

###############################################################################

class ResourceForm(MutableMapping):

###############################################################################

	def __init__(self, handle):
		self.store = {}
		self.keys = {}

###############################################################################

	def __getitem__(self, key):
		return self.store[key]

###############################################################################

	def __setitem__(self, key, value):
		pass

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
		pass

###############################################################################

	def reset(self):
		pass

###############################################################################

	def generate(self):
		pass

###############################################################################