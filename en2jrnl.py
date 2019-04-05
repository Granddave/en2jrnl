#!/usr/bin/env python3
import html2text
import os
import re
import argparse

def stripEmptyLines(s):
    lines = s.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return '\n'.join(lines)

class Post():
    def __init__(self, filepath):
        self.filepath = filepath
        self.datetime = None
        self.content = None
        self.title = None

    def parseFile(self):
        if self.filepath is "":
            Print("Filename is empty")
            return

        f = open(self.filepath, encoding="utf-8")
        content = f.read()
        dateRegex = re.findall(r'<tr><td><b>Created:<\/b><\/td><td><i>(\d*-\d*-\d* \d*:\d*)', content)
        if len(dateRegex) > 0:
            self.datetime = dateRegex[0]
            print("Date:  " + self.datetime)
        else:
            print("Could not find date")

        h = html2text.HTML2Text()
        h.ignore_links = True
        htmlContent = h.handle(content)

        # Set the first row as title, but without the pound sign before.
        # Example: '# My title' -> 'My title'
        self.title = htmlContent.split('\n', 1)[0][2:]

        self.content = '\n'.join(htmlContent.split('\n')[5:])
        self.content = stripEmptyLines(self.content)
        self.content = self.content.rstrip('\0')
        print("Title: " + self.title)

    def writeToFile(self, outputfile):
        with open(outputfile, "a") as f:
            f.write(self.datetime + ' ' + self.title + '\n')
            f.write(self.content)

def main():
    outputfile = "loggbok.txt"
    fileDir = "Evernote"

    filesToScan = sorted(os.listdir(fileDir))
    filesToScan = [x for x in filesToScan if
            os.path.isfile(x) or
            x.endswith(".html")]

    print("==============")
    count = 0
    for f in filesToScan:
        count = count + 1
        print("Post " + str(count))
        print("Current file: " + f)
        p = Post(fileDir + "/" + f)
        p.parseFile()
        p.writeToFile(outputfile)
        print("--------------")

if __name__ == '__main__':
    main()

