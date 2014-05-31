'''
Utilities to make secret box encryption simple
'''
# Import libnacl
import libnacl
import libnacl.utils


class SecretBox(object):
    '''
    Manage symetric encryption using the salsa20 algorithm
    '''
    def __init__(self, key=None):
        if key is None:
            key = libnacl.utils.salsa_key()
        if len(key) != libnacl.crypto_secretbox_KEYBYTES:
            raise ValueError('Invalid key')
        self._k = key

    def encrypt(self, msg, nonce=None):
        '''
        Encrypt the given message. If a nonce is not given it will be
        generated via the time_nonce function
        '''
        if nonce is None:
            nonce = libnacl.utils.time_nonce()
        if len(nonce) != libnacl.crypto_secretbox_NONCEBYTES:
            raise ValueError('Invalid Nonce')
        ctxt = libnacl.crypto_secretbox(self._k, msg, nonce)
        return nonce + ctxt

    def decrypt(self, ctxt, nonce=None):
        '''
        Decrypt the given message, if no nonce is given the nonce will be
        extracted from the message
        '''
        if nonce is None:
            nonce = ctxt[:libnacl.crypto_secretbox_NONCEBYTES]
            ctxt = ctxt[libnacl.crypto_secretbox_NONCEBYTES:]
        if len(nonce) != libnacl.crypto_secretbox_NONCEBYTES:
            raise ValueError('Invalid nonce')
        return libnacl.crypto_secretbox_open(self._k, ctxt, nonce)