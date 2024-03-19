from urllib.parse import urlunparse, quote_plus, parse_qsl

from p1radup.utils import is_url_valid

class URLProcessor:
    def __init__(self, soft_mode=False):
        self.urls = []
        self.processed_params_by_hostname = {}
        self.soft_mode = soft_mode

    def add_url(self, url):
        """Add a URL to the list of URLs to process."""
        self.urls.append(url)

    def _mark_as_processed(self, hostname, param):
        """Mark a parameter as processed for a given hostname."""
        # Initialize the set if the hostname doesn't exist yet
        if hostname not in self.processed_params_by_hostname:
            self.processed_params_by_hostname[hostname] = set()

        # Add the parameter to the set of processed parameters
        self.processed_params_by_hostname[hostname].add(param)

    def _is_processed(self, hostname, param):
        """Check if a parameter has already been processed for a given hostname."""
        return (hostname in self.processed_params_by_hostname) and (param in self.processed_params_by_hostname[hostname])
    
    def _generate_new_url(self, parsed_url, new_params):
        """
        Generates a new URL with the updated query parameters.
        """
        new_query = "&".join(f"{param}={value}" for param, value in new_params)
        return urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            new_query,
            parsed_url.fragment
        ))

    def _process_url(self, parsed_url):
        """
        Processes the URL by filtering out seen query parameters and generating a new URL if needed.
        Returns the new URL or None if no new parameters were added.
        """
        if not is_url_valid(parsed_url.geturl()):
            print("Invalid URL couldn't be processed: " + parsed_url.geturl())
            return None

        hostname, path, query = parsed_url.netloc, parsed_url.path, parsed_url.query
        key_for_lookup = (hostname, path) if self.soft_mode else hostname

        # Parse the query string using parse_qsl
        query_params = parse_qsl(query, keep_blank_values=True, strict_parsing=False)

        # Filter out query parameters that have already been processed.
        new_params = []
        for param, value in query_params:
            if not self._is_processed(key_for_lookup, param):
                new_params.append([param, value])
                self._mark_as_processed(key_for_lookup, param)

        # Generate and return the new URL if there are new parameters.
        if new_params:
            # Re-encode the parameters            
            encoded_query_params = [(key, quote_plus(value)) for key, value in new_params]

            new_url = self._generate_new_url(parsed_url, encoded_query_params)
            if not is_url_valid(new_url):
                print("Invalid URL generated from new params: " + new_url)
                return None
            else:
                return new_url
        else:
            return None

    def process_urls(self):
        """
        Process all URLs and return a list of the new URLs.
        """
        results = []

        for parsed_url in self.urls:
            try:
                new_url = self._process_url(parsed_url)
                if new_url:
                    results.append(new_url)
            except Exception as e:
                print(f"Error processing URL: {parsed_url} - {e}")

        return results