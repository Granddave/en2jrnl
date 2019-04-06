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

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

class Post():
    def __init__(self, filepath):
        self.filepath = filepath
        self.datetime = None
        self.content = None
        self.title = None

    def parseFile(self):
        if self.filepath is "":
            Print("Filename is empty")
            return False

        try:
            with open(self.filepath, encoding="utf-8") as f:
                content = f.read()
                h = html2text.HTML2Text()
                h.ignore_links = True
                htmlContent = h.handle(content)

                # Parse date.
                dateRegex = re.findall(r'\*\*Created:\*\*\|.._(\d*-\d*-\d* \d*:\d*)_', htmlContent)
                if len(dateRegex) > 0:
                    self.datetime = dateRegex[0]
                    print("Date:  " + self.datetime)
                else:
                    print("Could not find date")
                    return False

                # Set the first row as title, but without the pound sign before.
                # Example: '# My title' -> 'My title'
                self.title = htmlContent.split('\n', 1)[0][2:]
                print("Title: " + self.title)

                # Remove date and empty lines. Any other better way?
                self.content = '\n'.join(htmlContent.split('\n')[5:])
                self.content = stripEmptyLines(self.content)

                # Remove wierd trailing null byte.
                self.content = self.content.rstrip('\0')

                return True
        except IOError as e:
            print(e)
            return False

    def writeToFile(self, outputFile):
        with open(outputFile, "a") as f:
            f.write(self.datetime + ' ' + self.title + '\n')
            f.write(self.content)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="directory with exported html files to convert", type=dir_path, nargs=1, required=True)
    parser.add_argument("-o", "--output", help="jrnl output file", nargs=1)
    args = parser.parse_args()

    outputFile = "jrnl.txt"
    if args.output is not None:
        outputFile = args.output[0]

    fileDir = args.input[0]
    inputFiles = sorted(os.listdir(fileDir))
    inputFiles = [f for f in inputFiles if f.endswith(".html") and "index" not in f]

    print("Input directory:", fileDir)
    print("Output file:    ", outputFile)
    count = 0
    successful = 0
    for f in inputFiles:
        print("-------------------------")
        count += 1
        print("Current file: " + f)
        print("Post:  " + str(count))
        p = Post(fileDir + "/" + f)
        if p.parseFile() is False:
            continue
        successful += 1
        p.writeToFile(outputFile)

    print("-------------------------")
    print("""Done!
Parsed {}/{} posts from {}
Now available in {}""".format(successful, count, fileDir, outputFile))

if __name__ == '__main__':
    main()

