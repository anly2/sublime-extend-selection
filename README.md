# Sublime ExtendSelection

ExtendSelection is a [Sublime Text 2](http://www.sublimetext.com/2)[/3](http://www.sublimetext.com/3) plugin that allows you to make multiple selections more easily.

After triggering the "Extend Selection" command  (be it by using the key shortcuts, or the menu item in the "Selection" menu), you simply make a new selection and it will get added to the current one, instead of replacing it. You can make the new selection(s) in whatever way you would like - any method of navigation should be handled well.

## Recommendation

Before you continue, do consider the package [MultiEditUtils](https://packagecontrol.io/packages/MultiEditUtils). It offers a lot more and can be used to achieve the same functionality as this plugin's.


## Usage

### Add the next selection to the current one

	alt+shift+m
    
It will listen for the next change in the selection and append it to the previous selection ("current selection" at time of pressing alt+shift+m).

#### Example

For example, if I want to keep my current selection at `line 15, column 10` and add to it a caret at line 12, I would trigger the "Extend Selection" command (default <kbd>alt+shift+m</kbd>), then call "Goto line", type ":12" and press enter. That will move my caret to the beginning of line 12 but because I triggered "Extend Selection" beforehand, the new selection will be added to the previous one, rather than replacing it. So I will have a multi-selection at `line 12, column 0` and `line 15, column 10`.

### Manually completing "Extend Selection"

You can also extend the current selection with multiple new selections. Trigger "Start extending the selection" which is bound to <kbd>ctrl+alt+m</kbd> by default. Then make as many selections as you want. They will all add to the current one rather than overriding it. When you are done making selections, complete the command by calling "Finish extending the selection", bound to <kbd>ctrl+alt+m</kbd> again (<kbd>Esc</kbd> would also work).

You may also have a look at the "Stay active until timeout expires" setting described below.

#### Example

 >   selection at `row 9 column 5`  
 >   trigger "Start extending the selection" (<kbd>ctrl+alt+m</kbd>)  
 >   make selection at `row 10 column 0 to row 12 column 51`  
 >   make selection at `row 0 column 0 to row 0 column 27`  
 >   call "Finish extending the selection" (<kbd>ctrl+alt+m</kbd> again, or <kbd>Esc</kbd>)  
 >   selection is now multi-selection at `9:5`, `10:0 to 12:51` and `0:0 to 0:27`  


## Settings

### Combine 'one-move' change events

	"combine_onemove_events": true

The plugin by default tries to handle drag-selections (mouse dragging). This is achieved by combining new selections that are within one move from the recently-made new selection. While this does work, it also means that further selections made using the arrow keys, for example, will also be 'combined' with the latest one.

**Example of when this may be unwanted**

 >   selection at `row 10 column 2`  
 >   trigger `ExtendSelection` (<kbd>alt+shift+m</kbd>)  
 >   drag-select from `row 15 column 5` to `row 15 column 20`  
 >   <kbd>shift+right</kbd>  
 >   **This will add to the last selection, instead of doing <kbd>shift+right</kbd> for EVERY selection**

Please beware of this and disable the feature if that behaviour is undesired.

### Stay active until timeout expires

    "active_until_timeout": 0 //ms

The completion of the command can be delayed for a specified amount of time. This means that selection changes will continue to be handled by the command even after the first one, until the timeout expires. The timeout refreshes after each selection change, so if frequent enough changes are made all of them will be handled by the command.

This is potentially confusing, even with a small timeout delay. Because of that, this feature is disabled by default.

The setting specifies the time to delay the completion by. The value is in milliseconds. Negative values and zero effectively disable the behaviour.

##### Example

 >   "active_until_timeout" is set to 500  
 >   selection at `row 11 column 3`  
 >   trigger `ExtendSelection` (<kbd>alt+shift+m</kbd>)  
 >   make a selection at `row 16 column 6`  
 >   within 0.5 second, make a selection at `row 17 column 7`  
 >   the actual selection is now multi-selection at `11:3` , `16:6` and `17:7`  
 >   wait 0.5 second, and the command completes  




## Installation

### Install via PackageControl

If you have the [PackageControl](http://wbond.net/sublime_packages/package_control) plugin installed, you can use that to install `ExtendSelection`.

Just type `cmd-shift-p` (`ctrl-shift-p` on win/linux) to bring up the command palette then type `install` and pick `Package Control: Install Package` from the dropdown.

Then type `ExtendSelection` and choose the ExtendSelection plugin from the dropdown.  Hit `enter` and it will install.

### Manual Installation

Manual installation should be as easy as cloning this git repository into your Sublime `Packages` directory.  
*(mind the version of sublime)*

On Windows:

	cd "%AppData%\Sublime Text 2\Packages"
	git clone git://github.com/anly2/sublime-extend-selection.git ExtendSelection

Or you can copy the files manually into a folder `\Packages\ExtendSelection`, if you do not have git or are not feeling comfortable with it.


# Versions

##### [1.2.0] - released 15/12/15
###### Added:
- a feature named 'active_until_timeout' that delays the actual completion of the command for a specified time

##### [1.1.1] - released 14/12/15
###### Added:
- a feature named 'combine_onemove_events' that handles drag-selections

##### [1.0.0] - released 24/10/15
Initial release with basic functionality.
