import sublime
import sublime_plugin
import re

pluginName = "FindNReplaceNFiles"
debugOn = True

# Plugin print for more readability
def pprint(message, addNewLine=False):
    if debugOn:
        print("{}: {}".format(pluginName, message))
        if addNewLine:
            print()

class FindNReplaceCommand(sublime_plugin.EventListener):
    def on_pre_close(self, view):
        if view.name() != "Find Results":
            pprint("Nothing to do here")
            return 

        # When the name is 'Find Results'
        should_make_changes = sublime.ok_cancel_dialog(
            "{}: Would you like to inflict any changes on your local copy?".format(pluginName),
            "Yes")
        if not should_make_changes:
            pprint("User chose to not save changes")
            return 

        # save any open tabs, so changes don't get mix-matched
        window = sublime.active_window()
        for view in window.views():
            if view.is_dirty() and view.file_name():
                view.run_command('save')

        # main logic
        contents = view.substr(sublime.Region(0, view.size()))
        results_lines = contents.split("\n")
        current_filename = ""
        current_file = None
        current_file_lines = []
        for line in results_lines:
            regex4file = "^([\/].*)+:"
            regex4line = "[\s]*([\d]+)(?:[\:][\s]+|[\s]{2,})(.+|)(?:\n|)"
            result4line = re.search(regex4line, line)
            result4file = re.search(regex4file, line)
            if result4file is not None:  # is a file
                pprint("FILE:{}".format(line))
                if current_file is not None:
                    current_file.close()
                    with open(current_filename, "w") as file:
                        file.writelines(current_file_lines)
                current_filename = result4file.groups()[0]  # set the new filename
                current_file = open(current_filename, "r")
                current_file_lines = current_file.readlines()
            elif result4line is not None:  # is a line
                groups = result4line.groups()
                line_num = int(groups[0]) - 1
                pprint("LINE: {}".format(line))
                pprint(groups, addNewLine=True)
                if current_file is not None:  # will always be true 
                    pprint(line_num)
                    pprint(current_file_lines)
                    if line_num < len(current_file_lines):
                        regex4spaces = "^([ \t]*).*"
                        result4spaces = re.search(
                        regex4spaces, current_file_lines[line_num])
                        whitespace = result4spaces.groups()[0]
                        current_file_lines[line_num] = \
                            whitespace + groups[1] + "\n"
                    elif line_num == len(current_file_lines):
                        current_file_lines.append(groups[1] + "\n")
                    else:
                        pprint("Error saving line, it's beyond the current file length")
                        pprint("File: {} on line {}".format(current_filename, line_num + 1))
                        pprint("Tried to save '{}'".format(groups[1]))

        if current_file is not None:  # one last save
            current_file.close()
            with open(current_filename, "w") as file:
                file.writelines(current_file_lines)