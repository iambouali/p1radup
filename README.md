# p1radup

```
 ██████   ██ ██████   █████  ██████  ██    ██ ██████
 ██   ██ ███ ██   ██ ██   ██ ██   ██ ██    ██ ██   ██
 ██████   ██ ██████  ███████ ██   ██ ██    ██ ██████
 ██       ██ ██   ██ ██   ██ ██   ██ ██    ██ ██
 ██       ██ ██   ██ ██   ██ ██████   ██████  ██

 with <3 by @iambouali and aaznar
```

## Overview

This tool is designed to process a list of URLs from an input file, remove duplicate query parameters, and save the modified URLs to an output file. The primary goal is to ensure that each unique parameter is included only once for each distinct hostname.

## Usage

### Prerequisites

- Python 3.x installed on your system.

### Installation 

`pip3 install p1radup`

### Command-line Arguments

* **-i** or **--input**:
   - Path to the input file containing a list of URLs (required).
   - Example: `-i input.txt or --input /path/to/input/file.txt`.
* **-o** or **--output**:
   - Path to the output file where processed URLs will be saved.
   - Example: `-o output.txt` or `--output /path/to/output/file.txt`.
   - If not provided, the processed URLs will be printed to the console.
* **-s** or **--soft-mode**:
   - Keep duplicates in different paths and the same hostname.
   - This mode is useful for certain analysis or data processing tasks where keeping duplicates may be useful.
* **-c** or **--chunk-size**:
  - Specifies the size of each chunk of URLs to process at a time.
  - This allows the program to break down the list of URLs into more manageable parts, which can be especially helpful when dealing with very large datasets.
  - The default chunk size is 50,000 URLs. Adjusting this value can affect performance and memory usage.
  - Example: `-c 10000` or `--chunk-size 10000`.
  - A larger chunk size might improve processing speed by reducing overhead but can also increase memory usage, while a smaller chunk size might be more memory efficient but could potentially slow down processing due to increased overhead.
* **-w** or **--num-workers**:
   - Specifies the number of worker processes to use for processing URLs concurrently.
   - Increasing the number of workers can improve processing speed, especially for large input files.
   - However, using too many workers may overload system resources.
   - The default value is 4 if not specified.
   - Example: `-w 8` or `--num-workers 8`.
* **-gs** or **--gnu-sort**:
  - Enables the use of GNU sort for sorting URLs instead of the program's custom sorting mechanism.
  - GNU sort is a powerful, efficient sorting tool available on Unix-like systems, known for handling large files and complex sorting tasks efficiently.
  - This option might be preferable in scenarios where GNU sort's specific features or sorting behavior are desired or when dealing with extremely large datasets that benefit from GNU sort's performance optimizations.
  - Example: `-gs` or `--gnu-sort`.
  - When this option is enabled, the program will rely on the system's GNU sort utility, which must be installed and accessible in the system's path.


### Example

Suppose you have an input file `urls.txt` with the following content:

```
https://example.com/path/
https://example.com/page?param1=value1&param2=value2
https://example.com/page?param1=value3&param4=value4
https://anotherdomain.com/path?param1=value5&param2=value6
```

### Running the script:

`p1radup -i urls.txt -o param_urls.txt`

or

`cat urls.txt | p1radup -o param_urls.txt`


Will generate an output file `param_urls.txt` with the following content:

```
https://example.com/page?param1=value1&param2=value2
https://example.com/page?param4=value4
https://anotherdomain.com/path?param1=value5&param2=value6
```

### License

This script is released under the MIT License, allowing for free and open use, modification, and distribution.

### Acknowledgments

Feel free to contribute, report issues, or suggest improvements!
