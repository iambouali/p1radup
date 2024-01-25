import argparse
from urllib.parse import urlparse, parse_qs, urlunparse
from termcolor import colored
import sys
import concurrent.futures

def print_banner():
    banner = """
        _               _
  _ __ / |_ __ __ _  __| |_   _ _ __
 | '_ \| | '__/ _` |/ _` | | | | '_ \
 | |_) | | | | (_| | (_| | |_| | |_) |
 | .__/|_|_|  \__,_|\__,_|\__,_| .__/
 |_|                           |_|

 with <3 by @iambouali
    """

    print(colored(banner, 'green'))

def process_url(url, seen_params, soft_mode):
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
        return urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query, parsed_url.fragment))
    else:
        return None

def process_urls(input_file, output_file=None, soft_mode=False, num_threads=5):
    seen_params = {}
    result_urls = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Process each URL asynchronously
        futures = [executor.submit(process_url, url.strip(), seen_params, soft_mode) for url in input_file]

        # Collect results as they become available
        for future in concurrent.futures.as_completed(futures):
            processed_url = future.result()
            if processed_url:
                result_urls.append(processed_url)

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
    parser.add_argument('-t', '--threads', type=int, default=5, help='Number of threads for parallel processing')

    # Use stdin automatically if no input file is provided
    args = parser.parse_args()
    input_file = sys.stdin if args.input is None else open(args.input, 'r')

    process_urls(input_file, args.output, args.soft_mode, args.threads)

    # Close the file if it was opened
    if args.input is not None:
        input_file.close()

if __name__ == '__main__':
    main()
