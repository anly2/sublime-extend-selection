import sublime, sublime_plugin

#Constants
STATUS_MESSAGE_ = None

#Global vars
COMMAND_ACTIVE = False
VIEW_HAS_FOCUS = True
VIEW = None
STORED_SELECTION = []

class ExtendSelectionCommand(sublime_plugin.WindowCommand):
	'''
	Listen for the next change in the selection and add the new region to the current selection,
	instead of replacing the current selection with that new one.
	'''

	def description(self):
		return "Listen for the next change in the selection and add that new selection to the current selection"

	def is_enabled(self):
		return not COMMAND_ACTIVE


	def run(self, reset=False):
		global COMMAND_ACTIVE, VIEW, VIEW_HAS_FOCUS, STORED_SELECTION
		view = self.window.active_view()

		if reset:
			COMMAND_ACTIVE = False
			VIEW = None
			view.settings().set("extend_selection_active", False);  #To allow contextual binding of "escape"
			return

		COMMAND_ACTIVE = True
		view.settings().set("extend_selection_active", True); #To allow contextual binding of "escape"
		
		VIEW = view
		VIEW_HAS_FOCUS = True

		STORED_SELECTION = []
		for r in view.sel():
			STORED_SELECTION.append(r)

		VIEW.set_status("extend_selection_status", "Listening for changes in the selection")

def complete():
	global COMMAND_ACTIVE, VIEW, STORED_SELECTION
	
	sel = VIEW.sel()

	if (sel == STORED_SELECTION):
		return False #should we actually finilze?

	for r in STORED_SELECTION:
		sel.add(r)

	COMMAND_ACTIVE = False
	VIEW.settings().set("extend_selection_active", False);  #To allow contextual binding of "escape"

	VIEW.erase_status("extend_selection_status")
	sublime.status_message("Selection was extended")

	VIEW = None
	#VIEW_HAS_FOCUS = True

	return True

class SelectionChangeListener(sublime_plugin.EventListener):
	def on_deactivated(self, view):
		global VIEW, VIEW_HAS_FOCUS

		if view == VIEW:
			VIEW_HAS_FOCUS = False
			VIEW.set_status("extend_selection_status", "Paused listening for selection changes")

	def on_activated(self, view):
		global VIEW, VIEW_HAS_FOCUS, STORED_SELECTION

		if view == VIEW:
			VIEW_HAS_FOCUS = True
			VIEW.set_status("extend_selection_status", "Resumed listening for selection changes")

			complete() # (view.sel() != STORED_SELECTION) is checked inside

	def on_selection_modified_async(self, view):
		global COMMAND_ACTIVE, VIEW, VIEW_HAS_FOCUS

		if COMMAND_ACTIVE and view == VIEW and VIEW_HAS_FOCUS:
		   complete()

