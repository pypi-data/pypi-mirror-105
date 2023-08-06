from typing import Type
from hkserror.hkserror import HTypeError
from hks_pylib.cryptography.ciphers import HKSCipher
from hks_pylib.cryptography.hashes import SHA1, SHA256, HKSHash

from hks_pylib.errors.cryptography.ciphers.cipherid import CipherIDError


__default_sha1 = SHA1()
__default_sha256 = SHA256()


def hash_cls_name(
            obj: object,
            hash_obj_1: HKSHash = __default_sha1,
            hash_obj_2: HKSHash = __default_sha256
        ) -> bytes:
    if not isinstance(hash_obj_1, HKSHash):
        raise HTypeError("hash_obj_1", hash_obj_1, HKSHash)

    if not isinstance(hash_obj_2, HKSHash):
        raise HTypeError("hash_obj_2", hash_obj_2, HKSHash)

    if type(obj).__name__ == 'type' or\
        type(obj).__name__ == 'builtin_function_or_method':
        cls_name = str(obj).split(".")[-1][:-2].encode()
    else:
        cls_name = type(obj).__name__.encode()

    hash_obj_1.reset()
    hash_obj_2.reset()
    hash_value_1 = hash_obj_1.finalize(cls_name)
    hash_value_2 = hash_obj_2.finalize(cls_name)

    hash_value = bytearray(b"\x00\x00")
    for c in hash_value_1:
        hash_value[0] = hash_value[0] ^ c

    for c in hash_value_2:
        hash_value[1] = hash_value[1] ^ c

    return bytes(hash_value)


class CipherID(object):
    _cipher_hashs = {}
    _cipher_names = {}
    _cipher_hashs_invert = {}
    _cipher_names_invert = {}

    @staticmethod
    def register(cipher_cls: Type[HKSCipher]):
        if not issubclass(cipher_cls, HKSCipher):
            raise HTypeError("cipher_cls", cipher_cls, Type[HKSCipher])

        if hash_cls_name(cipher_cls) in CipherID._cipher_hashs.keys():
            raise CipherIDError()

        CipherID._cipher_hashs[hash_cls_name(cipher_cls)] = cipher_cls
        CipherID._cipher_names[cipher_cls.__name__] = cipher_cls
        CipherID._cipher_hashs_invert[cipher_cls] = hash_cls_name(cipher_cls)
        CipherID._cipher_names_invert[cipher_cls] = cipher_cls.__name__
        return cipher_cls

    @staticmethod
    def hash2cls(hash_value):
        return CipherID._cipher_hashs.get(hash_value, None)

    @staticmethod
    def name2cls(name):
        return CipherID._cipher_names.get(name, None)

    @staticmethod
    def cls2hash(cipher_cls):
        return CipherID._cipher_hashs_invert.get(cipher_cls, None)

    @staticmethod
    def cls2name(cipher_cls):
        return CipherID._cipher_names_invert.get(cipher_cls, None)
