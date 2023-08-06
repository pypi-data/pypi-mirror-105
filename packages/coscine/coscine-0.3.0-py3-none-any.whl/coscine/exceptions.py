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

class VocabularyError(Exception):
	def __init__(self, msg=None):
		Exception.__init__(self, msg)

###############################################################################

class KeyError(Exception):
	def __init__(self, msg=None):
		Exception.__init__(self, msg)

###############################################################################

class RequirementError(Exception):
	def __init__(self, list):
		msg = "Required fields missing:\n%s" % "\n".join(list)
		Exception.__init__(self, msg)

###############################################################################

class TypeError(Exception):
	def __init__(self, msg=None):
		Exception.__init__(self, msg)

###############################################################################

class ValueError(Exception):
	def __init__(self, msg=None):
		Exception.__init__(self, msg)

###############################################################################

class NotFoundError(Exception):
	def __init__(self, msg=None):
		Exception.__init__(self, msg)

###############################################################################