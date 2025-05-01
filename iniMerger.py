import glob # to get all inis within the ini folder
import datetime # to timestamp the backup Engine.ini

"""
Parse a provided ini file, return a dict representation of it,
and add any sections it contains to the global sectionList
"""
def parseIni(iniPath):
    global sectionList
    parsedIni = {}
    currentSection = []
    currentSectionLabel = ""
    print("Parsing " + iniPath)
    with open(iniPath) as baseFile:
        lines = baseFile.readlines()
        for line in lines:
            strippedLine = line.strip()
            if (strippedLine): # Check if empty line
                if (strippedLine.startswith('[')):
                    # this is a section header
                    currentSectionLabel = strippedLine
                    parsedIni[currentSectionLabel] = []
                    currentSection = parsedIni[currentSectionLabel]
                    if (currentSectionLabel not in sectionList):
                        sectionList.append(currentSectionLabel)
                elif (not strippedLine.startswith('#') and not strippedLine.startswith(';')):
                    # this is (probably) a key/val pair
                    # split on the =, then try to split val on ; to strip inline comments
                    splitKeyVal = strippedLine.split('=', 1)
                    key = splitKeyVal[0]
                    val = splitKeyVal[1].split(';', 1)[0].strip()
                    currentSection.append([key, val])

    return parsedIni

"""
Take inputIni and merge its contents into mergedIni
"""
def mergeIni(inputIni, mergedIni, filename):
    global sectionList
    overwritten = ""
    print("Merging " + filename)
    for section in sectionList:
        # run through all known sections
        if (section not in mergedIni):
            # this section isn't in mergedIni yet, add it
            mergedIni[section] = []

        # select the current section in mergedIni, to make things easier
        mergedCurrentSection = mergedIni[section]
        if (section in inputIni):
            # the input ini also has this section, merge it in
            for mergeKey, mergeVal in inputIni[section]:
                # run through each pair in the current input ini section
                existingIndex = -1

                # check if this mergedIni section already has this key,
                # or in the case of a Paths or +Suppress key, this value
                for index, existingPair in enumerate(mergedCurrentSection):
                    splitExistingVal = existingPair[1].split(';',1)
                    if (mergeKey == "Paths" or mergeKey == "+Suppress"):
                        if (existingPair[0] == mergeKey and splitExistingVal[0].strip() == mergeVal):
                            existingIndex = index
                            overwritten = splitExistingVal[1].strip()

                    elif (existingPair[0] == mergeKey):
                        existingIndex = index
                        overwritten = splitExistingVal[1].strip()

                # add the pair if it's new, update it if it isn't
                if (existingIndex == -1):
                    mergedCurrentSection.append([mergeKey, (mergeVal + " ; " + filename)])
                else:
                    mergedCurrentSection[existingIndex][1] = (mergeVal + " ; " + filename + ", overwrote " + overwritten)



# =========================================================================================== #
# ======================================Execution Start====================================== #
# =========================================================================================== #

inis = glob.glob("mergeinis/*.ini")
inis.sort()

sectionList = []
combinedIni = {}
for iniPath in inis:
    filenameOnly = iniPath.split('\\')[1]
    mergeIni(parseIni(iniPath), combinedIni, filenameOnly)

with open("Engine.ini", "w") as mergedFile:
    mergedFile.write("; This merged ini was created at " + str(datetime.datetime.now()) + '\n\n')
    for sectionName, pairs in combinedIni.items():
        mergedFile.write(sectionName + '\n')
        for key, val in pairs:
            pairText = key + '=' + val
            mergedFile.write(pairText + '\n')

input("Done. Press Enter to close this window.")