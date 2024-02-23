#!/usr/bin/env python3

import sys
import os
import datetime
import argparse
import threading
from multiprocessing import Manager
import unicodedata
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial
from urllib.parse import urlparse, parse_qs
from termcolor import colored

from p1radup.sort import batch_sort
from p1radup.url_parser import URLProcessor

def print_banner():
    banner = """
    ███████   ██ ██████   █████  ██████  ██    ██ ██████
    ██   ██ ███ ██   ██ ██   ██ ██   ██ ██    ██ ██   ██
    ███████   ██ ██████  ███████ ██   ██ ██    ██ ██████
    ██       ██ ██   ██ ██   ██ ██   ██ ██    ██ ██
    ██       ██ ██   ██ ██   ██ ██████   ██████  ██

    with <3 by @iambouali and aaznar
    """

    print(colored(banner, 'green'))

def is_text(s):
    # Check if a string contains only printable characters
    return all(True for c in s if not unicodedata.category(c).startswith('C'))

def process_chunk(chunk, soft_mode):
    url_processor = URLProcessor()
    results = []

    for parsed_url in chunk:
        try:
            query_params = parse_qs(parsed_url.query, keep_blank_values=True)
            new_url = url_processor.process_url(parsed_url, query_params, soft_mode)
            if new_url:
                results.append(new_url)

        except ValueError:
            print(f"Ignoring invalid URL: {parsed_url}")

    return results

def reader_thread(input_file, chunks_queue, chunk_size):
    current_chunk = []
    current_hostname = ''

    for line in input_file:
        try:
            url = line.strip()
            if is_text(url):
                parsed_url = urlparse(url)
                hostname = parsed_url.netloc
            else:
                print(f"Ignoring binary data: {url}")
                continue
        except ValueError:
            print(f"Ignoring invalid URL: {url}")
            continue

        if hostname != current_hostname and len(current_chunk) >= chunk_size:
            chunks_queue.put(current_chunk)
            current_chunk = []

        current_chunk.append(parsed_url)
        current_hostname = hostname

    if current_chunk:  # Ensure the last chunk is added
        chunks_queue.put(current_chunk)

    # Signal that reading is done by adding None
    chunks_queue.put(None)

def worker(chunks_queue, output_file=None, soft_mode=None, output_file_lock=None):
    while True:
        chunk = chunks_queue.get()
        if chunk is None:  # End signal
            chunks_queue.put(None)  # Propagate the end signal for other workers
            break
        results = process_chunk(chunk, soft_mode)
        if output_file:
            with output_file_lock:
                with open(output_file, 'a', encoding='utf-8', errors='ignore') as file:
                    for result in results:
                        file.write(result + '\n')
        else:
            for result in results:
                print(result)

def process_urls_with_pool(input_file, output_file, soft_mode, chunk_size, num_workers):
    m = Manager()
    chunks_queue = m.Queue(num_workers * 2)
    output_file_lock = m.Lock()

    # Start the reader thread
    reader = threading.Thread(target=reader_thread, args=(input_file, chunks_queue, chunk_size))
    reader.start()

    # Create a pool of worker processes
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        # Use partial to create a function with fixed arguments (output_file, soft_mode, output_file_lock)
        worker_partial = partial(worker, output_file=output_file, soft_mode=soft_mode, output_file_lock=output_file_lock)
        futures = [executor.submit(worker_partial, chunks_queue) for _ in range(num_workers)]

        # Wait for all futures to complete. This loop is not strictly necessary in this setup,
        # but it's useful if you want to handle exceptions or results from workers.
        for future in as_completed(futures):
            try:
                future.result()  # If a worker raised an exception, it will be re-raised here.
            except Exception as e:
                print(f"Worker error: {e}")

    # Wait for the reader thread to finish
    reader.join()

def sort_and_save_input_lines(input_source):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    if not input_source:
        output_filename = f"/tmp/input_{timestamp}.txt"

        with open(output_filename, 'a', buffering=-1, encoding='utf-8') as file:
            for line in sys.stdin:
                file.write(line)

    if input_source:
        input = input_source
        filename = os.path.splitext(os.path.basename(input_source))[0]
        output_filename = f"/tmp/{filename}_sorted_{timestamp}.txt"

        batch_sort(input, output_filename)

    return output_filename

def main():
    print_banner()

    parser = argparse.ArgumentParser(description='Process URLs and remove duplicate query parameters.')
    parser.add_argument('-i', '--input', help='Input file path')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-s', '--soft-mode', help='Enable soft mode to preserve duplicates in different paths and the same hostname', action='store_true')
    parser.add_argument('-c', '--chunk-size', type=int, default=50000, help='The size of each chunk of URLs to process at a time')
    parser.add_argument('-w', '--num-workers', type=int, default=4, help='The number of worker processes (an additional thread is used for reading the input file)')

    args = parser.parse_args()

    # Delete output file if it already exists
    if args.output is not None and os.path.exists(args.output):
        os.remove(args.output)

    sorted_filename = sort_and_save_input_lines(args.input)
    sorted_file = open(sorted_filename, 'r', encoding='utf-8')

    process_urls_with_pool(sorted_file, args.output, args.soft_mode, args.chunk_size, args.num_workers)

    # After processing URLs
    sorted_file.close()  # Close the file handle

    # Attempt to delete the sorted file
    if os.path.exists(sorted_filename):
        try:
            os.remove(sorted_filename)
        except Exception as e:
            print(f"Error deleting sorted file: {e}")
    else:
        print(f"Sorted file {sorted_filename} does not exist.")

if __name__ == '__main__':
    main()
