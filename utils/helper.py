import string
import random
import json

def generate_token(n=30):
    """ returns a n-digit letters-only random token """
    return ''.join(random.choice(string.ascii_letters) for i in xrange(n))

def json_safe(string, content_type='application/octet-stream'):
    """Returns JSON-safe version of `string`.

    If `string` is a Unicode string or a valid UTF-8, it is returned unmodified,
    as it can safely be encoded to JSON string.

    If `string` contains raw/binary data, it is Base64-encoded, formatted and
    returned according to "data" URL scheme (RFC2397). Since JSON is not
    suitable for binary data, some additional encoding was necessary; "data"
    URL scheme was chosen for its simplicity.

    Courtesy: httpbin
    """

    try:
        _encoded = json.dumps(string)
        return string
    except ValueError:
        return ''.join(['data:%s;base64,' % content_type,
                        base64.b64encode(string)])

