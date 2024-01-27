#!/usr/bin/env python3

import argparse
from urllib.parse import urlparse, parse_qs, urlunparse
from termcolor import colored
import sys

def print_banner():
    banner = """
    ███████   ██ ██████   █████  ██████  ██    ██ ██████
    ██   ██ ███ ██   ██ ██   ██ ██   ██ ██    ██ ██   ██
    ███████   ██ ██████  ███████ ██   ██ ██    ██ ██████
    ██       ██ ██   ██ ██   ██ ██   ██ ██    ██ ██
    ██       ██ ██   ██ ██   ██ ██████   ██████  ██

    with <3 by @iambouali
    """

    print(colored(banner, 'green'))

def process_urls(input_file, output_file=None, soft_mode=False):
    seen_params = {}
    result_urls = []

    for line in input_file:
        url = line.strip()
        parsed_url = urlparse(url)
        hostname = parsed_url.netloc
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        if soft_mode:
            new_params = {param: value for param, value in query_params.items() if param not in seen_params.get((hostname, path), set())}
            seen_params.setdefault((hostname, path), set()).update(new_params.keys())
        else:
            new_params = {param: value for param, value in query_params.items() if param not in seen_params.get(hostname, set())}
            seen_params.setdefault(hostname, set()).update(new_params.keys())

        if new_params:
            new_query = "&".join([f"{param}={value[0]}" for param, value in new_params.items()])
            new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query, parsed_url.fragment))
            result_urls.append(new_url)

    if output_file:
        with open(output_file, 'w') as file:
            for url in result_urls:
                file.write(url + '\n')
    else:
        for url in result_urls:
            print(url)

def main():
    print_banner()

    parser = argparse.ArgumentParser(description='Process URLs and remove duplicate query parameters.')
    parser.add_argument('-i', '--input', help='Input file path')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-s', '--soft-mode', help='Enable soft mode to preserve duplicates in different paths and the same hostname', action='store_true')

    # Use stdin automatically if no input file is provided
    args = parser.parse_args()
    input_file = sys.stdin if args.input is None else open(args.input, 'r')

    process_urls(input_file, args.output, args.soft_mode)

    # Close the file if it was opened
    if args.input is not None:
        input_file.close()

if __name__ == '__main__':
    main()
