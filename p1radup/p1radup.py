#!/usr/bin/env python3

import sys
import os
import datetime
import argparse
from termcolor import colored
from urllib.parse import urlparse, parse_qs
import queue
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

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
            parsed_url = urlparse(url)
            hostname = parsed_url.netloc
        except ValueError:
            print(f"Ignoring invalid URL: {parsed_url}")

        if hostname != current_hostname and len(current_chunk) >= chunk_size:
            chunks_queue.put(current_chunk)
            current_chunk = []

        current_chunk.append(parsed_url)
        current_hostname = hostname

    if current_chunk:  # Ensure the last chunk is added
        chunks_queue.put(current_chunk)

    # Signal that reading is done by adding None
    chunks_queue.put(None)

def worker(output_file, soft_mode, chunks_queue, output_file_lock):
    while True:
        chunk = chunks_queue.get()
        if chunk is None:  # End signal
            chunks_queue.put(None)  # Propagate the end signal for other workers
            break
        results = process_chunk(chunk, soft_mode)
        if output_file:
            with output_file_lock:
                with open(output_file, 'a') as file:
                    for result in results:
                        file.write(result + '\n')
        else:
            for result in results:
                print(result)

def process_urls_with_pool(input_file, output_file, soft_mode, chunk_size, num_workers):
    chunks_queue = queue.Queue()
    output_file_lock = threading.Lock()

    # Start the reader thread
    reader = threading.Thread(target=reader_thread, args=(input_file, chunks_queue, chunk_size))
    reader.start()

    # Create a pool of worker threads
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(worker, output_file, soft_mode, chunks_queue, output_file_lock) for _ in range(num_workers)]
        
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
        output_filename = f"input_{timestamp}.txt"
        
        with open(output_filename, 'a', buffering=-1) as file:
            for line in sys.stdin:
                file.write(line)          
    
    if input_source:
        input = input_source
        filename = os.path.splitext(os.path.basename(input_source))[0]
        output_filename = f"{filename}_sorted_{timestamp}.txt"

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
    if os.path.exists(args.output):
      os.remove(args.output)
    
    sorted_filename = sort_and_save_input_lines(args.input)
    sorted_file = open(sorted_filename, 'r')

    process_urls_with_pool(sorted_file, args.output, args.soft_mode, args.chunk_size, args.num_workers)

if __name__ == '__main__':
    main()
