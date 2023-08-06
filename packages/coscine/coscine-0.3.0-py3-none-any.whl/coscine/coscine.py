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

import os
import json
import urllib
import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm
import colorama
from .MetadataForm import MetadataForm
from .ProjectForm import ProjectForm
from .ResourceForm import ResourceForm
from .exceptions import *

###############################################################################

class CoscineClient:

	"""
	Provides a Client for the Coscine REST API
	"""

###############################################################################

	def __init__(self, token, verbose=True, lang="en", colors=True):

		"""
		Parameters
		----------
		
		Returns
		-------
		
		"""

		self.session = requests.Session()
		self.session.headers = {
			"Authorization": "Bearer " + token,
			"User-Agent": "Coscine Python Client v0.3.0"
		}
		self.verbose = verbose
		self.lang = lang
		self.colors = colors
		if colors:
			colorama.init(autoreset=True)

###############################################################################

	@staticmethod
	def _uri(api, endpoint, *args):
		API = "https://coscine.rwth-aachen.de/coscine/api/Coscine.Api.%s/%s"
		uri = API % (api, endpoint)
		if len(args) > 0:
			for arg in args:
				uri += "/" + urllib.parse.quote(arg, safe="")
		return uri

###############################################################################

	def _filter_array(self, array, kwargs):
		filtered = []
		for object in array:
			if self._filter_dict(object, kwargs):
				filtered.append(object)
		return filtered

	def _filter_dict(self, dict, kwargs):
		for kw in kwargs:
			if kw in dict:
				if dict[kw] != kwargs[kw]:
					return False
			else:
				return False
		return True

###############################################################################

	def get_projects(self, **kwargs):

		"""
		Get a list of projects matching certain criteria
		
		Parameters
		----------
		kwargs : unfolded dictionary containing filter criteria
			May contain any top-level key present in the project json
		
		Returns
		-------
		A list of projects as json objects or an empty list
		"""

		uri = self._uri("Project", "Project")
		projects = self.session.get(uri).json()
		if kwargs:
			projects = self._filter_array(projects, kwargs)
		return projects

###############################################################################

	def get_project(self, displayName):
		projects = self.get_projects(displayName = displayName)
		if projects and len(projects) == 1:
			return projects[0]
		else:
			raise NotFoundError(displayName)

###############################################################################

	def delete_project(self, project):

		"""
		Delete a project in Coscine
		
		Parameters
		----------
		project : JSON-object containing project information
		
		Returns
		-------
		Nothing
		"""

		uri = self._uri("Project", "Project", project["id"])
		self.session.delete(uri)

###############################################################################

	def create_project(self, form):

		"""
		Create a Project in Coscine
		
		Parameters
		----------
		form : ProjectForm
		
		Returns
		-------
		A handle to the new project
		"""

		data = form
		uri = self._uri("Project", "Project")
		r = self.session.post(uri, data)
		r.raise_for_status()
		return r.json()

###############################################################################

	def download_project(self, project, path="./"):

		"""
		Download a Coscine project including all of its resources to
		a directory on your harddrive
		
		Parameters
		----------
		project : Coscine Project Handle
		path : (optional) Path to the local save directory
		
		Returns
		-------
		Nothing
		"""

		path = os.path.join(path, project["displayName"])
		if not os.path.isdir(path):
			os.mkdir(path)
		for resource in self.get_resources(project):
			self.download_resource(resource, path=path)

###############################################################################

	def get_resources(self, project, **kwargs):

		"""
		Parameters
		----------
		
		Returns
		-------
		
		"""

		uri = self._uri("Project", "Project", project["id"], "resources")
		resources = self.session.get(uri).json()
		if kwargs:
			resources = self._filter_array(resources, kwargs)
		return resources

###############################################################################

	def get_resource(self, project, displayName):
		resources = self.get_resources(project, displayName = displayName)
		if resources and len(resources) == 1:
			return resources[0]
		else:
			raise NotFoundError(displayName)

###############################################################################

	def delete_resource(self, resource):

		"""
		Parameters
		----------
		
		Returns
		-------
		
		"""

		uri = self._uri("Resources", "Resource", resource["id"])
		self.session.delete(uri)

###############################################################################

	def create_resource(self, project, form):

		"""
		Parameters
		----------
		
		Returns
		-------
		
		"""

		uri = self._uri("Resources", "Resource", "Project", project["id"])
		self.session.post(uri, form.generate())

###############################################################################

	def download_resource(self, resource, path="./"):

		"""
		Parameters
		----------
		
		Returns
		-------
		
		"""

		dirpath = os.path.join(path, resource["displayName"])
		if not os.path.isdir(dirpath):
			os.mkdir(dirpath)
		files = self.get_files(resource)
		for file in files:
			filepath = os.path.join(dirpath, file["Path"].strip("/"))
			self.download(resource, file["Path"], path=filepath)

###############################################################################

	@staticmethod
	def _get_lang(entry, lang):
		for it in entry:
			if it["@language"] == lang:
				return it
		return None

	@staticmethod
	def _parse_application_profile(profile):
		W3PREFIX = "http://www.w3.org/ns/shacl#%s"
		data = {}
		profile = profile[0]
		data["id"] = profile["@id"]
		graph = []
		for entry in profile["@graph"]:
			obj = {}
			if W3PREFIX % "name" not in entry:
				continue
			obj["id"] = entry["@id"]
			obj["path"] = entry[W3PREFIX % "path"][0]["@id"]
			obj["order"] = int(entry[W3PREFIX % "order"][0]["@value"])
			if W3PREFIX % "minCount" in entry:
				obj["minCount"] = int(entry[W3PREFIX % "minCount"][0]["@value"])
			if W3PREFIX % "maxCount" in entry:
				obj["maxCount"] = int(entry[W3PREFIX % "maxCount"][0]["@value"])
			obj["name"] = {
				"de": CoscineClient._get_lang(entry[W3PREFIX % "name"], "de")["@value"],
				"en": CoscineClient._get_lang(entry[W3PREFIX % "name"], "en")["@value"]
			}
			if W3PREFIX % "datatype" in entry:
				obj["datatype"] = entry[W3PREFIX % "datatype"][0]["@id"]
				obj["type"] = "literal"
			if W3PREFIX % "class" in entry:
				obj["class"] = entry[W3PREFIX % "class"][0]["@id"]
				obj["datatype"] = obj["class"]
				obj["type"] = "uri"
			graph.append(obj)
		data["graph"] = graph
		return data

	def get_application_profile(self, resource, parse=False):

		"""
		Parameters
		----------
		
		Returns
		-------
		
		"""

		uri = self._uri("Metadata", "Metadata", "profiles", \
			resource["applicationProfile"], resource["id"])
		profile = self.session.get(uri).json()
		if parse:
			profile = CoscineClient._parse_application_profile(profile)
		return profile

###############################################################################

	def get_quota(self, resource):

		"""
		Parameters
		----------
		
		Returns
		-------
		
		"""

		uri = self._uri("Blob", "Blob", resource["id"], "quota")
		data = self.session.get(uri).json()
		quota = int(data["data"]["usedSizeByte"])
		return quota

###############################################################################

	def get_files(self, resource, **kwargs):

		"""
		Parameters
		----------
		
		Returns
		-------
		
		"""

		uri = self._uri("Tree", "Tree", resource["id"])
		data = self.session.get(uri).json()
		list = []
		for entry in data["data"]["fileStorage"]:
			info = {
				"Name": entry["Name"],
				"Path": entry["Path"],
				"Size": entry["Size"],
				"Type": entry["Kind"],
				"Provider": entry["Provider"]
			}
			list.append(info)
		if kwargs:
			list = self._filter_array(list, kwargs)
		return list

###############################################################################

	def get_metadata(self, resource, filename):

		"""
		Parameters
		----------
		
		Returns
		-------
		
		"""

		uri = self._uri("Tree", "Tree", resource["id"], filename)
		metadata = self.session.get(uri).json()
		return metadata

###############################################################################

	def put_metadata(self, resource, filename, metadata):

		"""
		Parameters
		----------
		
		Returns
		-------
		
		"""

		if type(metadata) is MetadataForm:
			metadata = metadata.generate()
		if type(metadata) is dict:
			metadata = json.dumps(metadata)
		uri = self._uri("Tree", "Tree", resource["id"], filename)
		self.session.put(uri, data=metadata)

###############################################################################

	def download_file(self, resource, filename, path):

		"""
		Parameters
		----------
		
		Returns
		-------
		
		"""

		uri = self._uri("Blob", "Blob", resource["id"], filename)
		r = self.session.get(uri, stream=True)
		r.raise_for_status()
		filesize = self.get_files(resource, Name=filename)[0]["Size"]
		fd = open(path, "wb")
		CHUNK_SIZE = 4096
		bar = tqdm(total=filesize, unit="B", unit_scale=True, \
								desc="↓ %s" % filename)
		for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
			fd.write(chunk)
			bar.update(len(chunk))
		bar.close()
		fd.close()

###############################################################################

	def upload_file(self, resource, filename, path, metadata):

		"""
		Parameters
		----------
		
		Returns
		-------
		
		"""

		fd = open(path, "rb")
		self.upload_data(resource, filename, fd, metadata)
		fd.close()

###############################################################################

	@staticmethod
	def _callback(monitor, bar):
		bar.update(monitor.bytes_read - bar.n)

	def upload_data(self, resource, filename, data, metadata):

		"""
		Parameters
		----------
		
		Returns
		-------
		
		"""

		uri = self._uri("Blob", "Blob", resource["id"], filename)
		self.put_metadata(resource, filename, metadata)
		encoder = MultipartEncoder(fields={"files": (filename, data, 'application/octet-stream')})
		filesize = encoder.len
		bar = tqdm(total=filesize, unit="B", unit_scale=True, \
									desc = "↑ %s" % filename)
		m = MultipartEncoderMonitor(encoder, \
			lambda monitor: self._callback(monitor, bar))
		resp = self.session.put(uri, data=m, headers={"Content-Type": m.content_type})
		resp.raise_for_status()
		bar.close()

###############################################################################

	def delete_file(self, resource, filename):

		"""
		Parameters
		----------
		
		Returns
		-------
		
		"""

		uri = self._uri("Blob", "Blob", resource["id"], filename)
		self.session.delete(uri)

###############################################################################

	def MetadataForm(self, project, resource, data=None):

		"""
		Parameters
		----------
		
		Returns
		-------
		
		"""

		form = MetadataForm(self, project, resource)
		return form

###############################################################################

	def ProjectForm(self, parent=None, data=None):

		"""
		Parameters
		----------
		
		Returns
		-------
		
		"""

		form = ProjectForm(self, parent=parent, data=data)
		return form

###############################################################################

	def ResourceForm(self):

		"""
		Parameters
		----------
		
		Returns
		-------
		
		"""

		form = ResourceForm(self)
		return form

###############################################################################

	def get_disciplines(self):

		"""
		Parameters
		----------
		
		Returns
		-------
		
		"""

		disciplines = {}
		uri = self._uri("Project", "Discipline")
		data = self.session.get(uri).json()
		for entry in data:
			disciplines[entry["displayNameEn"]] = entry
		return disciplines

###############################################################################

	def get_organizations(self, filter=None):

		"""
		Parameters
		----------
		
		Returns
		-------
		
		"""

		organizations = {}
		uri = self._uri("Organization", "Organization")
		data = self.session.get(uri).json()
		for entry in data["data"]:
			organizations[entry["displayName"]] = entry
		return organizations

###############################################################################

	def get_visibility(self):
		visibility = {}
		uri = self._uri("Project", "Visibility")
		data = self.session.get(uri).json()
		for entry in data:
			visibility[entry["displayName"]] = entry
		return visibility

###############################################################################

	def get_features(self):
		#uri = self._uri("")
		#features = self.session.get(uri).json()
		#return features
		pass

###############################################################################

	def get_instance(self, project, link):
		uri = self._uri("Metadata", "Metadata", "instances", \
										project["id"], link)
		instance = self.session.get(uri).json()
		return instance

###############################################################################