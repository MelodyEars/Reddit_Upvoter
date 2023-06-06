from urllib.parse import urlparse, parse_qs, urlunparse


def pars_params(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    if query_params:
        # if query_params is not empty
        new_query = ''
        parsed_url = parsed_url._replace(query=new_query)

    # clear url
    new_url = urlunparse(parsed_url)

    # for pars sub
    path_parts = parsed_url.path.split('/')
    sub = path_parts[1:3] if len(path_parts) >= 3 else ''
    sub = '/'.join(sub)

    return new_url, sub