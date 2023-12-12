import argparse
from urllib.parse import urlparse, parse_qs, urlunparse

def process_urls(input_file, output_file):
    seen_params = {}
    result_urls = []

    with open(input_file, 'r') as file:
        for line in file:
            url = line.strip()
            parsed_url = urlparse(url)
            hostname = parsed_url.netloc
            query_params = parse_qs(parsed_url.query)

            new_params = {param: value for param, value in query_params.items() if param not in seen_params.get(hostname, {})}

            if hostname not in seen_params:
                seen_params[hostname] = set(query_params.keys())
            else:
                seen_params[hostname].update(new_params.keys())

            if new_params:
                new_query = "&".join([f"{param}={value[0]}" for param, value in new_params.items()])
                new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query, parsed_url.fragment))
                result_urls.append(new_url)

    with open(output_file, 'w') as file:
        for url in result_urls:
            file.write(url + '\n')

def main():
    parser = argparse.ArgumentParser(description='Process URLs and remove duplicate query parameters.')
    parser.add_argument('-i', '--input', help='Input file path', required=True)
    parser.add_argument('-o', '--output', help='Output file path', required=True)
    args = parser.parse_args()

    process_urls(args.input, args.output)

if __name__ == '__main__':
    main()
