import string
import random

def generate_token(n=30):
    """ returns a n-digit letters-only random token """
    return ''.join(random.choice(string.ascii_letters) for i in xrange(n))
