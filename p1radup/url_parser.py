from urllib.parse import urlunparse

class URLProcessor:
    def __init__(self):
        self.seen_params = {}

    def _update_seen_params(self, hostname, path, new_params, soft_mode):
        """
        Updates the seen parameters with the new parameters based on the soft mode.
        """
        key = (hostname, path) if soft_mode else hostname
        self.seen_params.setdefault(key, set()).update(new_params.keys())

    def _generate_new_url(self, parsed_url, new_params):
        """
        Generates a new URL with the updated query parameters.
        """
        new_query = "&".join(f"{param}={value[0]}" for param, value in new_params.items())
        return urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            new_query,
            parsed_url.fragment
        ))

    def process_url(self, parsed_url, query_params, soft_mode):
        """
        Processes the URL by filtering out seen query parameters and generating a new URL if needed.
        Returns the new URL or None if no new parameters were added.
        """
        hostname, path = parsed_url.netloc, parsed_url.path
        key_for_lookup = (hostname, path) if soft_mode else hostname
        seen_set = self.seen_params.get(key_for_lookup, set())

        # Filter out query parameters that have already been seen.
        new_params = {param: value for param, value in query_params.items() if param not in seen_set}

        # Update the seen parameters.
        self._update_seen_params(hostname, path, new_params, soft_mode)

        # Generate and return the new URL if there are new parameters.
        if new_params:
            return self._generate_new_url(parsed_url, new_params)

        return None
