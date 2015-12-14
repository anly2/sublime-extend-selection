# Sublime ExtendSelection

ExtendSelection is a [Sublime Text 2](http://www.sublimetext.com/2)[/3](http://www.sublimetext.com/3) plugin that allows you to make multiple selections more easily.

After triggering the "Extend Selection" command  (be it by using the key shortcuts, or the menu item in the "Selection" menu), you simply make a new selection and it will get added to the current one, instead of replacing it. You can make the new selection(s) in whatever way you would like - any method of navigation should be handled well.

## Usage

### Add the next selection to the current one

	alt+shift+m
    
It will listen for the next change in the selection and append it to the previous selection ("current selection" at time of pressing alt+shift+m).

#### Example

For example, if I want to keep my current selection at `line 15, column 10` and add to it a caret at line 12, I would trigger the "Extend Selection" command (default <kbd>alt+shift+m</kbd>), then call "Goto line", type ":12" and press enter. That will move my caret to the beginning of line 12 but because I triggered "Extend Selection" beforehand, the new selection will be added to the previous one, rather than replacing it. So I will have a multi-selection at `line 12, column 0` and `line 15, column 10`.


## Settings

### Combine 'one-move' change events

	"combine_onemove_events": true

The plugin by default tries to handle drag-selections (mouse dragging). This is achieved by combining new selections that are within one move from the recently-made new selection. While this does work, it also means that further selections made using the arrow keys, for example, will also be 'combined' with the latest one.

**Example of when this may be unwanted**

 >   selection at `row 10 column 2`
 >   trigger `ExtendSelection` (<kbd>alt+shift+m</kbd>)
 >   drag-select from `row 15 column 5` to `row 15 column 20`
 >   <kbd>shift+right</kbd> **This will add to the last selection, instead of doing <kbd>shift+right</kbd> for EVERY selection**

Please beware of this and disable the feature if that behaviour is undesired.


## Installation

### Install via PackageControl

If you have the [PackageControl](http://wbond.net/sublime_packages/package_control) plugin installed, you can use that to install `EasyMotion`.

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

- 1.0.0 - released 24/10/15
