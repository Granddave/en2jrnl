#!/usr/bin/env python3
import argparse
import os
import re

import html2text


def _strip_empty_lines(lines):
    lines = [line.strip() for line in lines]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return '\n'.join(lines)


class Entry():
    def __init__(self, filepath):
        self.filepath = filepath
        self.datetime = None
        self.content = None
        self.title = None
        self.is_parsed = False

    def parse_file(self):
        with open(self.filepath, "r", encoding="utf-8") as f:
            content = f.read()
            h = html2text.HTML2Text()
            h.ignore_links = True

            # Parse html and strip whitespace and trailing null terminator
            html_content = h.handle(content).strip().rstrip('\0')

            # Parse date.
            date_regex = re.findall(r'\*\*Created:\*\*\|.._(\d*-\d*-\d* \d*:\d*)_',
                                    html_content)
            if len(date_regex) == 1:
                self.datetime = f'{date_regex[0]}'
            else:
                raise ValueError("Failed to parse date")

            # Set the first row as title, but without the pound sign before.
            # Example: '# My title' -> 'My title'
            self.title = html_content.split('\n', 1)[0][2:]

            # Remove date and empty lines. Any other better way?
            self.content = _strip_empty_lines(html_content.split('\n')[5:])
            self.content += '\n'*2
            self.is_parsed = True

    def get_full_entry(self):
        if not self.is_parsed:
            raise Exception("Entry not parsed")
        return f"[{self.datetime}] {self.title}\n{self.content}"


def _get_input_files(directory):
    """Takes a directory path.
    Returns a list of all html files except the index file."""
    files = sorted(os.listdir(directory))
    files = [f for f in files if f.endswith(".html") and "index" not in f]
    return files


def parse_journal(directory, log_to_stdout=False):
    """Takes a `directory` with `.html` journal entries.
    Returns the journal in jrnl text format.
    """
    input_files = _get_input_files(directory)
    num_successful = 0
    journal = ""
    for i, filename in enumerate(input_files):
        if log_to_stdout:
            print("-"*25)
            print("Current file: " + filename)
            print("Entry:  " + str(i+1))

        entry = Entry(f"{directory}/{filename}")
        try:
            entry.parse_file()
        except Exception as e:
            print(e)
            continue
        if log_to_stdout:
            print(f"Date:  {entry.datetime}")
            print(f"Title: {entry.title}")
        num_successful += 1
        journal += entry.get_full_entry()

    if log_to_stdout:
        print("-"*25)
        print("Parsed {}/{} entries from {}".format(num_successful,
                                                  len(input_files),
                                                  directory))
    return journal


def _dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i",
                        "--input",
                        help="directory with exported html files to convert",
                        type=_dir_path,
                        nargs=1,
                        required=True)
    parser.add_argument("-o",
                        "--output",
                        help="jrnl output file. If not supplied, result will be printed to stdout",
                        nargs=1)
    return parser.parse_args()


def _main():
    args = _get_args()

    file_dir = args.input[0]
    output_file = None if args.output is None else args.output[0]
    log_to_stdout = args.output is not None

    if log_to_stdout:
        print(f"Input directory: {file_dir}")
        print(f"Output file:     {output_file}")

    journal = parse_journal(file_dir, log_to_stdout=log_to_stdout)

    if output_file is not None:
        with open(output_file, "w") as f:
            f.write(journal)
        print(f"Now available in {output_file}")
    else:
        print(journal)


if __name__ == '__main__':
    _main()
