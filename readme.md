# dm42coder.py

Encoder for [Swiss Micros][sm] [DM42][] calculator programs.

This encoder should work for [Free42][] as well, though I have not yet included any of the mobile-only functions.  There is little real need to use an encoder for [Free42][] since it will import programs directly from the text listings.  Hopefully one day the [DM42][] will gain this feature from [Free42][] making this program pointless.

[sm]: https://www.swissmicros.com/
[DM42]: https://www.swissmicros.com/dm42.php
[Free42]: http://thomasokken.com/free42/

## Requirements

`dm42coder.py` is written in Python.  It was tested using Python 3.6.5 on MacOS.  The Python installation was from [Anaconda][], though any Python 3.6 or higher should work.  It will likely work on lower versions of Python as well.

Three modules from the standard library are used that might have issues in earlier versions of Python: *binascii*, *argparse*, and *fileinput*.  *argparse* is similar to the old *optparse* and should not be too difficult to backport to Python 2 if interested.  *fileinput* is only used in reading the input files or stdin, and could easily be replaced.  *binascii* is only used in writing the converted hex values to binary and could be replaced by the appropriate Python 2 method.

[Anaconda]: https://www.anaconda.com/download/

## Usage

The program is designed to be used from the command line.  Program files to be converted can either be piped to it or specified as an argument.  Output can be either written directly to a file (with automatic naming or a specified name), or can be printed to stdout as a 'normalized' text listing, a hex line-by-line listing, a fully compressed hex listing, or a binary stream that can be piped directly to a file.

### Specifying input

`dm42coder.py` accepts input either by specifying a file name or piping a file to the script.  To use stdin, a `-` must be used for the input filename.

    dm42coder.py program.txt
    cat program.txt | dm42coder.py -

### Printing program files

With no options specified, a prettified version of the input code is printed to stdout.  Escaped characters are translated, command names are normalized, line numbers are added, and a byte count is inserted at the beginning of the file.  The output can also be explicitly specified with the `-p` option.

    dm42coder.py program.txt
    dm42coder.py program.txt -p

To print a line-by-line listing of the converted hex values, use the `-l` option.  The `--hex` option prints the same output with all whitespace removed, i.e. in one compact line.  Lastly, the `-b` option can be used to print a binary stream to stdout that is suitable to be piped to another file.

    dm42coder.py program.txt -b | out.raw


### Writing raw files

To write to a file with the name `program.raw` in the same directory as the input file:

    dm42coder.py program.txt -w

To write to a file with a name and location of your choosing:

    dm42coder.py program.txt -o ~/output.raw

If the input is from stdin and no file name is specified, the output file will be named `out.raw` in the directly in which the command was run.

For the files created without the `-o` option (no specified name), the script will not overwrite existing files, instead adding a *-x* to the name where *x* is an incrementing number.

## TODO

I'd like to add decoding functionality as well, but have not started working on that.

## Disclaimer

The code has been tested on a few DM42 programs of mine.  I've also checked it with the [`stress`][stress] program from [Free42][].

[stress]: http://thomasokken.com/free42/42progs/stress.txt
