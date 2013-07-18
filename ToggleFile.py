# -*- coding: utf-8 -*-
import sublime
import sublime_plugin
import os.path
import fnmatch

class TogglefileCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		file_name = self.view.file_name()
		base_name = os.path.basename(file_name)
		dir_name = os.path.dirname(file_name)

		first_dot_index = base_name.find('.')
		if first_dot_index == -1:
			return

		body_name = base_name[0:first_dot_index + 1]
		exclude_patterns = self.view.settings().get("file_exclude_patterns")
		same_names = [f for f in os.listdir(dir_name)
						if f.startswith(body_name)
							and self.is_match(f, exclude_patterns)]

		if len(same_names) <= 1:
			return

		same_names.sort()

		open_name = same_names[(same_names.index(base_name) + 1) % len(same_names)]

		self.view.window().open_file(open_name)

	def is_match(self, file_name, exclude_patterns):
		for p in exclude_patterns:
			if fnmatch.fnmatch(file_name, p):
				return False
		return True
