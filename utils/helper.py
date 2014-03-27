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


def dummy_text(n=5):
    """ returns dummy text repeated n times """
    msg = """Collaboratively administrate empowered markets via plug-and-play networks. Dynamically procrastinate B2C users after installed base benefits. Dramatically visualize customer directed convergence without revolutionary ROI.

Efficiently unleash cross-media information without cross-media value. Quickly maximize timely deliverables for real-time schemas. Dramatically maintain clicks-and-mortar solutions without functional solutions.

Completely synergize resource sucking relationships via premier niche markets. Professionally cultivate one-to-one customer service with robust ideas. Dynamically innovate resource-leveling customer service for state of the art customer service.
    """
    return "".join([msg for i in range(n)])

def dummy_xml(n=5):
    """ returns dummy xml repeated n times """
    header = """<?xml version='1.0' encoding='UTF-8'?>
    <listofnotes> """
    content = """ <note>
    <from>Alice</from>
    <to>Bob</to>
    <message>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent eleifend mi vel ligula ultricies, sit amet fringilla nisi consectetur. Aenean pretium risus lacus, a posuere libero mollis tincidunt. Aliquam id fermentum tellus. Vivamus sollicitudin elementum dui nec semper. Curabitur consequat lacinia risus. Praesent suscipit venenatis lectus sed pharetra. Etiam id nulla id leo elementum malesuada. Donec faucibus, mi eget hendrerit tincidunt, libero purus tincidunt tortor, at auctor ipsum sem vel quam.</message>
    </note> """
    footer = "</listofnotes>"
    return header + "".join([content for i in range(n)]) + footer

def dummy_json(n=5):
    """ returns dummy json repeated n times """
    msg = ["Collaboratively administrate empowered markets via plug-and-play networks. Dynamically procrastinate B2C users after installed base benefits. Dramatically visualize customer directed convergence without revolutionary ROI.",
           "Efficiently unleash cross-media information without cross-media value. Quickly maximize timely deliverables for real-time schemas. Dramatically maintain clicks-and-mortar solutions without functional solutions.",
           "Completely synergize resource sucking relationships via premier niche markets. Professionally cultivate one-to-one customer service with robust ideas. Dynamically innovate resource-leveling customer service for state of the art customer service."]
    resp = {}
    for i in range(n):
        resp["message-"+str(i+1)] = random.choice(msg)
    return resp

