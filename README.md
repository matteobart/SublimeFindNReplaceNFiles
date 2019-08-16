# SublimeFindNReplaceNFiles
The faster (better) way to use Sublime to Find &amp; Replace in multiple files.

A lightweight Sublime 3 plugin that allows users to quickly Find & Replace right from the `Find in Files` 
tool. As Uncle Ben once said, 'with great power comes great responsibility.'

## Use

To use open a `Find In Files` window (Command + Shift + f on Mac or `Find` on the top bar -> `Find in Files...`). Once the window is open with all of the find results, simply start editing right in the window. Once you try to close the `Find Results` a pop up will come up asking if you would like to save changes. Tapping on yes will write the changes to the file, otherwise tapping on no will ignore any changes. 

Please also read the Notes section below for corner use cases. 

## ~~_Limitations_~~ Notes
Once the `Find In Files` window is open, do not go back and change the files directly. If any changes are made to the files after the window is open, any changes that are made from the `Find Results` window will *not* be made. 

Files are *automatically* saved after making changes from the `Find Results` window. Any files that are currently opened are also saved.

When making changes to lines that are already tabbed, the plugin will always keep the spacing from the original line, and simply replace just the text. In other words, you can not change preceding spacing from `Find Results` window. 

On a similar note, if writing on a new line (no spacing or characters). Then the line will default to have no preceding spaces. This is especially true if writing on the last line.

## Installation
To manually add this plugin to Sublime, download the [file](FindNReplaceNFiles.py). Open Sublime -> go to `Preferences` (on Mac go to `Sublime Text` first) -> `Browse Packages` -> Open the folder `User` -> drag the python file `FindNReplaceNFiles.py` (into the folder) -> Enjoy!

By manually adding the file, any changes made to the file will affect the plugin. Feel free to edit the project, and submit a pull request! 

## Why
I was once asked to make one small change to a large number of files. The task was essentially to do a quick find and replace that spanned about 70 files. Using the Find & Replace in All Files worked okay, but it was more effort than it should have been. It opens up all the relevent files and makes you check each one and close each one individually. Does this work well with 3 files? Yes. Does this work well with 20 files? Ehh. Does it work well with 70 files? Nope. Hopefully this plugin is the solution.
