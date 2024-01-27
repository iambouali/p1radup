# p1radup

```
 ██████   ██ ██████   █████  ██████  ██    ██ ██████
 ██   ██ ███ ██   ██ ██   ██ ██   ██ ██    ██ ██   ██
 ██████   ██ ██████  ███████ ██   ██ ██    ██ ██████
 ██       ██ ██   ██ ██   ██ ██   ██ ██    ██ ██
 ██       ██ ██   ██ ██   ██ ██████   ██████  ██

 with <3 by @iambouali
```

## Overview

This tool is designed to process a list of URLs from an input file, remove duplicate query parameters, and save the modified URLs to an output file. The primary goal is to ensure that each unique parameter is included only once for each distinct hostname.

## Features

- **Duplicate Query Parameter Removal:** The script identifies duplicate query parameters within each URL and retains only the first occurrence of each parameter for a given hostname.

- **Output Format:** The processed URLs are saved to an output file, preserving the original URL structure while removing redundant query parameters.

- **Soft Mode:** The `-s` flag allows users to keep duplicate query parameters in different paths and the same hostname.
  
## Usage

### Prerequisites

- Python 3.x installed on your system.

### Installation 

`pip3 install p1radup`

### Command-line Arguments

* **-i** or **--input**: Path to the input file containing a list of URLs (required).
* **-o** or **--output**: Path to the output file where processed URLs will be saved.
* **-s** or **--soft-mode**: Keep duplicates in different paths and the same hostname.
  
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
