import os, sublime, sublime_plugin, glob
# super+alt+6
class RelatedFilesCommand(sublime_plugin.TextCommand):
  def run(self, edit):

    file_name         = self.view.file_name()
    source_path       = os.path.dirname(file_name)
    rails_view_path   = os.path.dirname(source_path)
    files_and_folders = []
    files             = []

    if 'controllers' in source_path:
      only_file_name = file_name.split('/')[-1].split('_controller.rb')[0]
      if file_name.split('/')[-2] != 'controllers':
        files_source_path = rails_view_path.replace('controllers', 'views/') + file_name.split('/')[-2] + '/' + only_file_name +'/'
      else:
        files_source_path = rails_view_path + '/views/' + only_file_name +'/'
    else:
      only_file_name    = source_path.split('/')[-1]
      files_source_path = source_path

      if file_name.split('/')[-1] != 'views':
        controller_file   = rails_view_path.replace('views', 'controllers') + '/' + only_file_name + '_controller.rb'
      else:
        controller_file   = rails_view_path + '/controllers/' + only_file_name + '_controller.rb'

      files.append(controller_file)

    result = glob.glob(files_source_path + '/*')

    for _file_or_folder in result:
      files_and_folders.append(_file_or_folder)

    for _file in files_and_folders:
      if '.' in _file:
        files.append(_file)
      else:
        folder_result = glob.glob(_file + '/*')
        for _f_file in folder_result:
            files.append(_f_file)

    self.files = files
    sublime.active_window().show_quick_panel(files, self.open_file)

  def open_file(self, index):
    if index >= 0:
      sublime.active_window().open_file(os.path.join(self.files[index]))