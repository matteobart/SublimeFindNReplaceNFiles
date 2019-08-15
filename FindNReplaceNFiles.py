import sublime
import sublime_plugin
import re

pluginName = "FindNReplaceNFiles"
debugOn = True


class ExampleCommand(sublime_plugin.EventListener):
    def on_pre_close(self, view):
        if view.name() == "Find Results":
            # first lets save any files that are chilling
            # Write out every buffer (active window) with
            # changes and a file name.
            window = sublime.active_window()
            for view in window.views():
                if view.is_dirty() and view.file_name():
                    view.run_command('save')

            # actual logic
            contents = view.substr(sublime.Region(0, view.size()))
            lines = contents.split("\n")
            currentFileName = ""
            currentFile = None
            currentFileLines = []
            for line in lines:
                regex4file = "^([\/].*)+:"
                regex4line = "[\s]*([\d]+)(?:[\:][\s]+|[\s]{2,})(.+|)(?:\n|)"
                result4line = re.search(regex4line, line)
                result4file = re.search(regex4file, line)
                if result4file is not None:  # is a file
                    groups = result4file.groups()
                    if debugOn:
                        print ("FILE:" + line)
                        print (groups)
                        print ()
                    if currentFile is not None:
                        currentFile.close()
                        with open(currentFileName, "w") as file:
                            file.writelines(currentFileLines)
                    currentFileName = groups[0]
                    currentFile = open(currentFileName, "r")
                    currentFileLines = currentFile.readlines()
                elif result4line is not None:  # is a line
                    groups = result4line.groups()
                    if debugOn:
                        print ("LINE:" + line)
                        print (groups)
                        print ()
                    if currentFile is not None:
                        regex4spaces = "^([ \t]*).*"
                        # grab the line
                        lineNum = int(groups[0]) - 1
                        if debugOn:
                            print(lineNum)
                            print(currentFileLines)
                        # grab the whitespace from the line
                        result4spaces = re.search(
                            regex4spaces, currentFileLines[lineNum])
                        whitespace = result4spaces.groups()[0]
                        if lineNum < len(currentFileLines):
                            currentFileLines[lineNum] = \
                                whitespace + groups[1] + "\n"
                        elif lineNum == len(currentFileLines):
                            currentFileLines.append(
                                whitespace + groups[1] + "\n")
                        else:
                            print(pluginName + ": Error saving line, it's \
                                beyond the current file length")
                            print("\tFile: " + currentFileName +
                                  " on line " + str(lineNum + 1))
                            print("\tTried to save '" + groups[1] + "'")
            if currentFile is not None:  # one last save
                currentFile.close()
                with open(currentFileName, "w") as file:
                    file.writelines(currentFileLines)

        else:  # when the buffer that is closing is not a Find Results File
            if debugOn:
                print(pluginName + ": Nothing to do here")