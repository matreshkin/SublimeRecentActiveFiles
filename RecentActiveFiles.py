import sublime, sublime_plugin
import os

class RecentActiveFilesEventListener(sublime_plugin.EventListener):
    def on_post_save(self, view):
        self.on_activated(view)

    def on_deactivated(self, view):
        self.on_activated(view)

    def on_activated(self, view):
        if view.file_name():
            view.window().run_command("recent_active_files", { "file_name": view.file_name() })

class RecentActiveFilesCommand(sublime_plugin.WindowCommand):
    def __init__(self, window):
        sublime_plugin.WindowCommand.__init__(self, window)
        self.recent_active_files = []

    def unshift(self, file_name):
        if file_name in self.recent_active_files:
            self.recent_active_files.remove(file_name)
        self.recent_active_files.insert(0, file_name)

    def path_form_project(self, path):
        for folder in self.window.folders():
            path = path.replace(folder + '/', '', 1)
        return path

    def run(self, file_name=None):
        view = self.window.active_view()
        if file_name:
            self.unshift(file_name)
        else:
            # items = [[basename, path_from_project, real_path], ...]
            items = [[os.path.basename(f), self.path_form_project(f), f] for f in self.recent_active_files]

            def on_done(index):
                if index >= 0:
                    self.window.open_file(items[index][2])
                else:
                    self.window.focus_view(view)

            def on_highlight(index):
                if index >= 0:
                    # for 8 - see https://sublimetext.userecho.com/communities/1/topics/2482-open-file-in-current-group-from-api
                    self.window.open_file(items[index][2], sublime.TRANSIENT|sublime.ENCODED_POSITION|8)

            self.window.show_quick_panel(items, on_done, sublime.MONOSPACE_FONT, 1, on_highlight)

