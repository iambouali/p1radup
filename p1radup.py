import argparse
from urllib.parse import urlparse, parse_qs, urlunparse
from termcolor import colored

def print_banner():
    banner = """
        _               _             
  _ __ / |_ __ __ _  __| |_   _ _ __  
 | '_ \| | '__/ _` |/ _` | | | | '_ \ 
 | |_) | | | | (_| | (_| | |_| | |_) |
 | .__/|_|_|  \__,_|\__,_|\__,_| .__/ 
 |_|                           |_|   
by @iambouali                                                   
    """

    print(colored(banner, 'green'))

def process_urls(input_file, output_file=None, soft_mode=False):
    seen_params = {}
    result_urls = []

    with open(input_file, 'r') as file:
        for line in file:
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
    parser.add_argument('-i', '--input', help='Input file path', required=True)
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-s', '--soft-mode', help='Enable soft mode to preserve duplicates in different paths and the same hostname', action='store_true')
    args = parser.parse_args()

    process_urls(args.input, args.output, args.soft_mode)

if __name__ == '__main__':
    main()
