# URL Parameter Deduplicator (p1radup)

<img width="640" alt="SCR-20231213-rvti" src="https://github.com/iambouali/p1radup/assets/74378500/668d64da-46be-4e10-9c7a-271559ae7fa4">

## Overview

This Python script is designed to process a list of URLs from an input file, remove duplicate query parameters, and save the modified URLs to an output file. The primary goal is to ensure that each unique parameter is included only once for each distinct hostname.

## Features

- **Duplicate Query Parameter Removal:** The script identifies duplicate query parameters within each URL and retains only the first occurrence of each parameter for a given hostname.

- **Output Format:** The processed URLs are saved to an output file, preserving the original URL structure while removing redundant query parameters.

- **Soft Mode:** The "soft mode" option (-s/--soft-mode flag) allows users to keep duplicate query parameters in different paths and the same hostname.
  
## Usage

### Prerequisites

- Python 3.x installed on your system.

### Running the Script

1. Clone or download the script to your local machine.

2. Open a terminal and navigate to the directory containing the script.

3. Make sure you have Python installed on your system. You can install the required dependencies using the following command:

```bash
pip3 install -r requirements.txt
```

3. Run the script using the following command:

```bash
python3 p1radup.py -i input_file.txt -o output_file.txt
```

Replace input_file.txt with the path to your input file containing URLs, and output_file.txt with the desired output file path.

### Command-line Arguments

* **-i** or **--input**: Path to the input file containing a list of URLs (required).
* **-o** or **--output**: Path to the output file where processed URLs will be saved.
* **-s** or **--soft-mode**: Keep duplicates in different paths and the same hostname.
  
### Example

Suppose you have an input file (input_urls.txt) with the following content:

```
https://example.com/page?param1=value1&param2=value2
https://example.com/page?param1=value3&param4=value4
https://anotherdomain.com/path?param1=value5&param2=value6
```

### Running the script:

`python3 p1radup.py -i input_urls.txt -o output_urls.txt`

Will generate an output file (output_urls.txt) with the following content:

```
https://example.com/page?param1=value1&param2=value2
https://example.com/page?param4=value4
https://anotherdomain.com/path?param1=value5&param2=value6
```

### License

This script is released under the MIT License, allowing for free and open use, modification, and distribution.

### Acknowledgments

Feel free to contribute, report issues, or suggest improvements!
