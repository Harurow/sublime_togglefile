# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import os.path
import fnmatch

class ToggleFile(sublime_plugin.TextCommand):
	def run(self, edit):
		file_name = self.view.file_name()

		if not file_name:
			return

		self.toggle(file_name)

	def getfiles(self, paths, dir_name, body_name):
		for dirpath, dirnames, filenames in os.walk(dir_name):
			for f in filenames:
				p = os.path.join(dirpath, f)
				if f.startswith(body_name) and self.is_match(f):
					paths.append(p)

	def toggle(self, file_name):
		base_name = os.path.basename(file_name)
		dir_name = os.path.dirname(file_name)

		first_dot_index = base_name.find('.')
		if first_dot_index == -1:
			return

		settings = sublime.load_settings("togglefile.sublime-settings");
		seach_other_folder = settings.get("seach_other_folder");
		self.exclude_patterns = self.view.settings().get("file_exclude_patterns")

		body_name = base_name[0:first_dot_index + 1]

		if seach_other_folder:
			dirs = self.view.window().folders()
			dirs.sort()
			same_names = []
			for dname in dirs:
				self.getfiles(same_names, dname, body_name)
		else:
			same_names = []
			for fname in os.listdir(dir_name):
				if fname.startswith(body_name) and self.is_match(fname):
					same_names.append(os.path.join(dir_name, fname))

		if len(same_names) <= 1:
			return

		same_names.sort()
		if self.reverse:
			same_names.reverse()

		open_name = same_names[(same_names.index(file_name) + 1) % len(same_names)]

		self.view.window().open_file(open_name)

	def is_match(self, file_name):
		for p in self.exclude_patterns:
			if fnmatch.fnmatch(file_name, p):
				return False
		return True


class TogglefileCommand(ToggleFile):
	def __init__(self, view):
		ToggleFile.__init__(self, view)
		self.reverse = False


class TogglefilerevCommand(ToggleFile):
	def __init__(self, view):
		ToggleFile.__init__(self, view)
		self.reverse = True
