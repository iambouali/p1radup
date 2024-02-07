#!/usr/bin/env python
# base on Gabriel Genellina http://code.activestate.com/recipes/576755-sorting-big-files-the-python-26-way/
# based on Recipe 466302: Sorting big files the Python 2.4 way
# by Nicolas Lehuen
from __future__ import print_function

import os
import re
from tempfile import gettempdir
from itertools import islice, cycle
from collections import namedtuple
import heapq

Keyed = namedtuple("Keyed", ["key", "obj"])

def merge(key=None, *iterables):
    if key is None:
        for element in heapq.merge(*iterables):
            yield element
    else:
        keyed_iterables = [(Keyed(key(obj), obj) for obj in iterable)
                        for iterable in iterables]
        for element in heapq.merge(*keyed_iterables):
            yield element.obj


def batch_sort(input, output, key=None, buffer_size=1024000, tempdirs=None, uniq=False):
    if tempdirs is None:
        tempdirs = []
    if not tempdirs:
        tempdirs.append(gettempdir())

    chunks = []
    try:
        with open(input, 'rb', 64*1024) as input_file:
            input_iterator = iter(input_file)
            for tempdir in cycle(tempdirs):
                current_chunk = list(islice(input_iterator, buffer_size))
                if not current_chunk:
                    break
                if uniq:
                    current_chunk = list(set(current_chunk))
                current_chunk.sort(key=key)
                output_chunk = open(os.path.join(tempdir, 'sort{0:06d}'.format(len(chunks))), 'w+b', 64*1024)
                chunks.append(output_chunk)
                output_chunk.writelines(current_chunk)
                output_chunk.flush()
                output_chunk.seek(0)
        with open(output, 'wb', 64*1024) as output_file:
            output_file.writelines(merge(key, *chunks))
    finally:
        for chunk in chunks:
            try:
                chunk.close()
                os.remove(chunk.name)
            except Exception:
                pass


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Sort a text file by a key in lines of file. This script is compatible with very large files.")
    parser.add_argument(
        'input_file',
        help='Text file to sort'
    )
    parser.add_argument(
        'output_file',
        help='Sorted text file'
    )
    parser.add_argument(
        '-b','--buffer',
        dest='buffer_size',
        default=32000,
        help='''Size of the line buffer. The file to sort is
            divided into chunks of that many lines. Default : 32,000 lines.'''
    )
    parser.add_argument(
        '-k','--key',
        dest='key',
        help='''Python expression used to compute the key for each
            line, "lambda line:" is prepended.\n
            Example : -k "line[5:10]". By default, the whole line is the key.'''
    )
    parser.add_argument(
        '-s','--split',
        dest='split_pattern',
        help='''Python regexp to extract the line key.\n
            Example : -s "^[\w_]+{(?:.+)?}\s+[0-9+.e-]+\s([0-9]+)". By default no regexp work on line chars directly.'''
    )
    parser.add_argument(
        '-t','--tempdir',
        dest='tempdirs',
        action='append',
        default=[],
        help='''Temporary directory to use. You might get performance
            improvements if the temporary directory is not on the same physical
            disk than the input and output directories. You can even try
            providing multiples directories on differents physical disks.
            Use multiple -t options to do that.'''
    )
    parser.add_argument(
        '-u','--uniq',
        dest='uniq',
        action='store_true',
        default=False,
        help='''Sort uniq values.'''
    )
    parser.add_argument(
        '-p','--psyco',
        dest='psyco',
        action='store_true',
        default=False,
        help='''Use Psyco lib to improve execution speed.'''
    )
    options = parser.parse_args()

    lambda_key = None
    if options.split_pattern:
        # If user type --split "^[\w_]+{(?:.+)?}\s+[0-9+.e-]+\s([0-9]+)" --key 1, key will be lasts numbers
        split_pattern = re.compile(options.split_pattern)
        lambda_key = eval('lambda line : (split_pattern.match(line).group({key_index}))'.format(key_index=options.key))
    elif options.key:
        # If user type --key [5:10], key will be extracted as chars between 5 and 10 in line
        lambda_key = eval('lambda line : (line{key_range})'.format(key_range=options.key))

    if options.psyco:
        import psyco
        psyco.full()

    batch_sort(options.input_file, options.output_file, lambda_key, options.buffer_size, options.tempdirs, options.uniq)
