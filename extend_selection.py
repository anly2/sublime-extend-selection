import sublime, sublime_plugin;

#Global vars
STATE = "inactive"
VIEW_HAS_FOCUS = True
VIEW = None
STORED_SELECTION = []
LAST_SEL = None;

SETTINGS_DEFAULT = {
	"combine_onemove_events" : False
}


def plugin_loaded():
	#load settings
	globals()['user_settings'] = sublime.load_settings('Preferences.sublime-settings')
	globals()['settings'] = sublime.load_settings('ExtendSelection.sublime-settings')
	global SETTINGS_DEFAULT;

	for setting, defaultValue in SETTINGS_DEFAULT.items():
		value = settings.get(setting);
		if value is None:
			settings.set(setting, defaultValue);

		value = user_settings.get(setting);
		if value is not None:
			settings.set(setting, value);


class ExtendSelectionCommand(sublime_plugin.WindowCommand):
	'''
	Listen for the next change in the selection and add the new region to the current selection,
	instead of replacing the current selection with that new one.
	'''

	def description(self):
		return "Listen for the next change in the selection and add that new selection to the current selection";

	def is_enabled(self):
		global STATE;
		return STATE == "inactive";


	def run(self, reset=False):
		global STATE, VIEW, VIEW_HAS_FOCUS, STORED_SELECTION;
		view = self.window.active_view();

		if reset:
			STATE = "inactive";
			VIEW = None;
			view.settings().set("extend_selection_active", False);  #To allow contextual binding of "escape"
			return;

		STATE = "active";
		view.settings().set("extend_selection_active", True); #To allow contextual binding of "escape"
		
		VIEW = view;
		VIEW_HAS_FOCUS = True;

		STORED_SELECTION = [];
		for r in view.sel():
			STORED_SELECTION.append(r);

		VIEW.set_status("extend_selection_status", "Listening for changes in the selection");


def complete():
	global STATE, VIEW, STORED_SELECTION;
	
	sel = VIEW.sel();


	if (sel == STORED_SELECTION):
		return False; #should we actually finish?

	enabled_combine = settings.get('combine_onemove_events');
	if (enabled_combine and len(sel) == 1):
		STATE = "standby";

		global LAST_SEL;
		LAST_SEL = sel[0];

	else:
		STATE = "inactive";


	for r in STORED_SELECTION:
		sel.add(r);

	VIEW.settings().set("extend_selection_active", False);  #To allow contextual binding of "escape"

	VIEW.erase_status("extend_selection_status");
	sublime.status_message("Selection was extended");

	if not STATE == "standby":
		#Needs to be retained for use in STANDBY mode
		VIEW = None;
		STORED_SELECTION = []; 
		#VIEW_HAS_FOCUS = True;

	return True;



class SelectionChangeListener(sublime_plugin.EventListener):
	def on_deactivated(self, view):
		global VIEW, VIEW_HAS_FOCUS;

		if view == VIEW:
			VIEW_HAS_FOCUS = False;
			VIEW.set_status("extend_selection_status", "Paused listening for selection changes");

	def on_activated(self, view):
		global VIEW, VIEW_HAS_FOCUS, STORED_SELECTION;

		if view == VIEW:
			VIEW_HAS_FOCUS = True;
			VIEW.set_status("extend_selection_status", "Resumed listening for selection changes");

			complete(); # (view.sel() != STORED_SELECTION) is checked inside

	def on_selection_modified_async(self, view):
		global STATE, VIEW, VIEW_HAS_FOCUS, LAST_SEL, STORED_SELECTION;

		if STATE != "inactive" and view == VIEW and VIEW_HAS_FOCUS:
			if STATE == "active":
				complete();
				return;

			if STATE == "standby":
				sel = view.sel();
				for r in STORED_SELECTION:
					sel.subtract(r);
				s = sel[0];

				if within1Move(s, LAST_SEL):
					LAST_SEL = s; #update

					for r in STORED_SELECTION:
						sel.add(r);

				else:
					STATE = "inactive";
					LAST_SEL = None;
					STORED_SELECTION = [];
					VIEW = None;


def within1Move(s1, s2):
	if s1.begin() == s2.begin() or s1.end() == s2.end():
		return True;
		
	if d1(s1.begin(), s2.begin()) or d1(s1.end(), s2.end()):
		return True;

	global VIEW;

	if (s1.size() == 0 and s2.size() == 0):
		return False;

	(s1y1,s1x1) = VIEW.rowcol(s1.begin());
	(s1y2,s1x2) = VIEW.rowcol(s1.end());
	(s2y1,s2x1) = VIEW.rowcol(s2.begin());
	(s2y2,s2x2) = VIEW.rowcol(s2.end());

	if (d1(s1y1, s2y1) or d1(s1y1, s2y2))  or  (d1(s1y2, s2y1) or d1(s1y2, s2y2)):
		return True;

	return False;

def d1(i1, i2):
	return (abs(i2 - i1) == 1);
