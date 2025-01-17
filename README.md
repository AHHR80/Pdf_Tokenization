### Download
```sh
git clone --recurse-submodules https://github.com/AHHR80/Pdf_Tokenization
cd Pdf_Tokenization
```


# PDF-Tokenization

This tool tokenize pdf files with pdf bookmarks for Traning LLM Models.


# PDF-Bookmark

[![PyPI](https://badge.fury.io/py/pdf-bookmark.svg)](https://pypi.org/project/pdf-bookmark/)

PDF-Bookmark is a tool for importing and exporting pdf bookmark
with the `bmk` format.


## Installation

```shell
$ pip install pdf-bookmark
```

`pdf-bookmark` utilizes
[PDFtk](https://www.pdflabs.com/tools/pdftk-server/)
and [Ghostscript](https://www.ghostscript.com/)
to export and import pdf bookmarks.
They must be installed before running `pdf-bookmark`.


### PDFtk

PDFtk is used here to export bookmark from pdf file.
The java port [pdftk-java](https://gitlab.com/pdftk-java/pdftk)
may also be OK.

On Arch Linux, `pdftk-java` could be installed by:

```shell
$ sudo apt  install pdftk-java
```

Verify the installation:

```shell
$ pdftk --version
```


### Ghostscript

Ghostscript is used here to import bookmark to pdf file.

On Arch Linux, it could be installed by:

```shell
$ sudo apt -y install ghostscript
```

Verify the installation:

```shell
$ gs --version
```


## bmk format

The `bmk` format is used to describe the bookmark of a pdf file.
It will be used to import bookmark into a pdf file.

`bmk` format is easy to write.
It looks quite like the content of a book.
So you can copy the content and modify from it.

Each line represents a bookmark item. The title and the page number are
separated by at least 4 dots "`.`".

The level of a bookmark is specified by the indentation of spaces.
The default indentation is 2 spaces, and the number of spaces could be
configured with inline command.

This is a simple example of a `bmk` file.

```
序................1
Chapter 1................4
Chapter 2................5
  2.1 Section 1................6
    2.1.1 SubSection 1................6
    2.1.2 SubSection 2................8
  2.2 Section 2................12
Chapter 3................20
Appendix................36
```

Import the bookmark and create a new pdf file:

```shell
$ pdf-bookmark -p input.pdf -b bookmark.bmk -o new.pdf
```


### Export bmk format

The `bmk` format could also be exported from a pdf file with bookmark.
You may also modify the bookmark from the exported one.

```shell
$ pdf-bookmark -p input.pdf
```


### Inline command

There could also be inline commands in the file to do more controls
on the bookmark. These commands start with `!!!` and modify some
properties of bookmark. The new property will affect bookmarks after
the line until it is changed again.

It is normal that the main body of a pdf file does not start from the
first page of pdf, and the page number is not always arabic.

```
!!! collapse_level = 2

!!! num_style = Roman
Preface................I
Content................IV

!!! new_index = 12
!!! num_style = Arabic
Introduction................1
Chapter 1................4
Chapter 2................5
  2.1 Section 1................6
  2.2 Section 2................7
Chapter 3................10
Appendix................11
```

With these inline commands, you do not need to recalculate the index
number for each page.

Here are all supported inline commands:

* `new_index`. Default: 1.
   The following bookmark index will be recalculated from the
   new index number (`new_index + page - 1`).
* `num_start`. Default: 1.
   Specify the number of first page if it does not start from 1
   (`new_index + page - num_start`).
* `num_style`. Default: `Arabic`.
   The page number style. Could be `Arabic`, `Roman` and `Letters`.
* `collapse_level`. Default: 0.
   On which level the bookmarks are collapsed. 0 means expand all.
* `level_indent`. Default: 2.
   Number of indentation spaces for a new level.


## pdf-bookmark command

The `pdf-bookmark` command is installed by `pip install pdf-bookmark`.

```
usage: pdf-bookmark [-h] [-f {bmk,none,pdftk,pdfmark,json}]
                    [-l COLLAPSE_LEVEL] [-b BOOKMARK] [-p PDF] [-o OUTPUT_PDF]

Import and export PDF bookmark

optional arguments:
  -h, --help            show this help message and exit
  -f {bmk,none,pdftk,pdfmark,json}, --format {bmk,none,pdftk,pdfmark,json}
                        the output format of bookmark
  -l COLLAPSE_LEVEL, --collapse-level COLLAPSE_LEVEL
                        the min level to be collapsed, 0 to expand all
  -b BOOKMARK, --bookmark BOOKMARK
                        the bookmark file to be imported
  -p PDF, --pdf PDF     the input PDF file
  -o OUTPUT_PDF, --output-pdf OUTPUT_PDF
                        the output PDF file
```


## Example

### Import bookmark

This will import the `bmk` bookmark into a pdf file:

```shell
$ pdf-bookmark -p input.pdf -b bookmark.bmk -o new.pdf
```

If you would like to have a quite output:

```shell
$ pdf-bookmark -p input.pdf -b bookmark.bmk -f none -o new.pdf
```

### Export bookmark

This will export the `bmk` bookmark to stdout from a pdf file:

```shell
$ pdf-bookmark -p input.pdf
```

The output format could be changed to `pdfmark`, `json`:

```shell
$ pdf-bookmark -p input.pdf -f pdfmark
$ pdf-bookmark -p input.pdf -f json
```

### Change the collapse level

This will only change the collapse level of the pdf.

```shell
$ pdf-bookmark -p input.pdf -l 2 -o new.pdf
```
