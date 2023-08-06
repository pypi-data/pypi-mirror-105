#!/usr/bin/python3

import os
import sys
import typing

#import jk_typing
#import jk_utils
import jk_sysinfo
import jk_argparsing
import jk_argparsing.textmodel





def getAllProcessNames() -> list:
	allProcesses = {}
	for p in jk_sysinfo.get_ps():
		allProcesses[p["pid"]] = p

	currentPID = os.getpid()
	processNames = []

	while True:
		procInfo = allProcesses.get(currentPID)
		if procInfo is None:
			break
		cmd = procInfo["cmd"]
		if cmd:
			if cmd.endswith(":"):
				cmd = cmd[:-1]
			if cmd:
				processNames.append(cmd)

		currentPID = allProcesses[currentPID].get("ppid")
		if not currentPID:
			break

	return processNames
#





ap = jk_argparsing.ArgsParser(os.path.basename(__file__), "Checks if a specified program is a parent of the current process.")

ap.optionDataDefaults.set("help", False)
ap.optionDataDefaults.set("list", False)
ap.optionDataDefaults.set("check", None)

ap.createOption("h", "help", "Display this help text.").onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("help", True)
ap.createOption("l", "list", "List all parent process names.").onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("list", True)
ap.createOption("c", "check", "Check if the specified process name is part of the parent process names.").expectString("cmd", minLength=1).onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("check", argOptionArguments[0])

ap.createAuthor("Jürgen Knauth", "pubsrc@binary-overflow.de")

ap.setLicense("Apache")

ap.createReturnCode(0, "Everything is okay.")
ap.createReturnCode(1, "Something went wrong.")
ap.createReturnCode(2, "The help text has been displayed.")

ap.addDescriptionChapter(None, [
	"This program can be used to check if the current process tree contains a specific type of process.",
	"Of course, there is only a very limited range of uses for this tool. Of application would be to use it within bash initialization to determine if a user logged in via ssh. "
	+ "Here is an example of how this could be done in principle:",
	"if jkcheckpproc.py -c bash; then echo \"bash is parent\"; else echo \"no, bash is not parent\"; fi",
])

parsedArgs = ap.parse()

if parsedArgs.optionData["list"]:
	for s in getAllProcessNames():
		print(s)
	sys.exit(0)

if parsedArgs.optionData["check"] is not None:
	bResult = False
	sCheck = parsedArgs.optionData["check"]
	for s in getAllProcessNames():
		if s == sCheck:
			bResult = True
			break
	if bResult:
		sys.exit(0)
	else:
		sys.exit(1)

ap.showHelp()
sys.exit(1)





















