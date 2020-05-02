#!/usr/bin/env python3
import argparse
import os
import re

import html2text


def _strip_empty_lines(multiline_text):
    lines = multiline_text.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return '\n'.join(lines)


def _dir_path(string):
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

    def parse_file(self):
        if self.filepath is "":
            print("Filename is empty")
            return False

        try:
            with open(self.filepath, encoding="utf-8") as f:
                content = f.read()
                h = html2text.HTML2Text()
                h.ignore_links = True
                html_content = h.handle(content)

                # Parse date.
                date_regex = re.findall(r'\*\*Created:\*\*\|.._(\d*-\d*-\d* \d*:\d*)_',
                                       html_content)
                if len(date_regex) > 0:
                    self.datetime = date_regex[0]
                    print("Date:  " + self.datetime)
                else:
                    print("Could not find date")
                    return False

                # Set the first row as title, but without the pound sign before.
                # Example: '# My title' -> 'My title'
                self.title = html_content.split('\n', 1)[0][2:]
                print("Title: " + self.title)

                # Remove date and empty lines. Any other better way?
                self.content = '\n'.join(html_content.split('\n')[5:])
                self.content = _strip_empty_lines(self.content)

                # Remove wierd trailing null byte.
                self.content = self.content.rstrip('\0')

                return True
        except IOError as e:
            print(e)
            return False

    def write_to_file(self, outputFile):
        with open(outputFile, "a") as f:
            f.write(self.datetime + ' ' + self.title + '\n')
            f.write(self.content)


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i",
                        "--input",
                        help="directory with exported html files to convert",
                        type=_dir_path,
                        nargs=1, required=True)
    parser.add_argument("-o",
                        "--output",
                        help="jrnl output file",
                        nargs=1)
    args = parser.parse_args()

    output_file = "jrnl.txt"
    if args.output is not None:
        output_file = args.output[0]

    file_dir = args.input[0]
    input_files = sorted(os.listdir(file_dir))
    input_files = [f for f in input_files
                   if f.endswith(".html") and "index" not in f]

    print("Input directory:", file_dir)
    print("Output file:    ", output_file)
    count = 0
    successful = 0
    for f in input_files[3:4]:
        print("-------------------------")
        count += 1
        print("Current file: " + f)
        print("Post:  " + str(count))
        p = Post(file_dir + "/" + f)
        if p.parse_file() is False:
            continue
        successful += 1
        p.write_to_file(output_file)

    print("-------------------------")
    print("""Done!
Parsed {}/{} posts from {}
Now available in {}""".format(successful, count, file_dir, output_file))


if __name__ == '__main__':
    _main()
