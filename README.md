# en2jrnl

A journal converter from [Evernote](https://www.evernote.com) export to [Jrnl](http://jrnl.sh/).

The supported setup in Evernote is as follows, a notebook where each note is an journal entry. In my case the title of the entry is the date like so `YYMMDD`, but any title should work.

The creation date of the Evernote entry is used as creation date in Jrnl.


## How to use

Export your notebook in html format. run `en2jrnl.py` with `-i [export-directory]` where export-directory is the directory with all `.html` files.

To specify output file, pass `-o [outputfile]`. If `-o` isn't passed, the journal will be printed to stdout.


## Dependencies

* `html2text`


## Example

Here is an export example from Evernote on Windows.

```
$ ./en2jrnl.py -i example/ -o example/jrnl-output.txt
Input directory: example
Output file:     example/jrnl-output.txt
-------------------------
Current file: 190405.html
Post:  1
Date:  2019-04-05 12:50
Title: 190405
-------------------------
Current file: 190406.html
Post:  2
Date:  2019-04-06 16:51
Title: 190406
-------------------------
Parsed 2/2 posts from example
Now available in example/jrnl-output.txt

$ cat example/jrnl-output.txt
[2019-04-05 12:50] 190405
Started writing my memoirs. On the command line.

Like a boss.

[2019-04-06 16:51] 190406
I use jrnl to keep track of accomplished tasks.

The done.txt for my todo.txt
```


# License

See [LICENSE.md](LICENSE.md)
