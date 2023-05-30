from urllib.parse import urlparse, parse_qs, urlunparse


def pars_params(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    if query_params:
        new_query = ''
        parsed_url = parsed_url._replace(query=new_query)

    new_url = urlunparse(parsed_url)
    sub = parsed_url.netloc + parsed_url.path.split('/', 1)[1]
    return new_url, sub