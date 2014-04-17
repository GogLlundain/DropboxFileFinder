__author__ = 'GogLlundain'

import os
from os.path import join, getsize
from shutil import move

# 1..   Enumerate all the files in the dropbox folder. Name, date, and size
# 2..   Find each entry in the target folder.
#           If found delete the file from the source folder
#           If not found, leave it where it is.

def enumerateFilesInDirectory(sourceFolder):
    fileInformation = enumerateFilesInFolder(sourceFolder)
    return fileInformation


def enumerateFilesInFolder(rootFolder):
    filesInThisFolder = dict()
    for root, dirs, files in os.walk(rootFolder):
        for fileName in files:
            fileInfo = FileInformation(fileName, root, getsize(join(root, fileName)))
            filesInThisFolder[fileInfo.fullFilePath()] = fileInfo

        if len(dirs) > 0:  # We have sub-folders to consider...
            for directory in dirs:
                subFiles = enumerateFilesInFolder(join(rootFolder, directory))
                for subfile in subFiles.values():
                    filesInThisFolder[subfile.fullFilePath()] = subfile
    return filesInThisFolder


class FileInformation(object):
    name = ""
    folder = ""
    size = 0

    def fullFilePath(self):
        return join(self.folder, self.name)

    def __init__(self, name, folder, size):
        self.name = name
        self.folder = folder
        self.size = size


sourceFolder = 'D:\\DropboxSource'
targetFolder = 'D:\\Llyniau\\'
deletedFolder = 'D:\\DropboxDeleted'

sourceFileDictionary = enumerateFilesInDirectory(sourceFolder)
print len(sourceFileDictionary), 'files found in source'

targetFileDictionary = enumerateFilesInDirectory(targetFolder)
print len(targetFileDictionary), 'files found in target'

print 'Finding source files in the target'
filesCompared = 0
filesFound = 0
# Looping over the target because it's the bigger of the two collections
for key, value in targetFileDictionary.iteritems():
    filesCompared += 1
    for sourceKey, sourceValue in sourceFileDictionary.iteritems():
        if value.name == sourceValue.name and value.size == sourceValue.size:
            filesFound += 1
            sourceFileDictionary.pop(sourceKey)
            move(sourceKey, join(deletedFolder, sourceValue.name))
            break

print filesCompared, 'were looked for,', filesFound, 'were found'
print len(sourceFileDictionary), 'items remain in the source dictionary'