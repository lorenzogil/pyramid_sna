import sys

# True if we are running on Python 3.
PY3 = sys.version_info[0] == 3

if PY3:  # pragma: no cover
    from urllib import parse
    urlparse = parse
    from urllib.parse import quote as url_quote
    from urllib.parse import urlencode as url_encode
else:  # pragma: no cover
    import urlparse
    from urllib import quote as url_quote
    from urllib import urlencode as url_encode
