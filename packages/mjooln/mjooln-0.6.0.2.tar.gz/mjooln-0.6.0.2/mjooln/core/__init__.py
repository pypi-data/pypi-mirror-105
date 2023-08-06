import os
import logging
import base64
import re
import json
import simplejson
import yaml

from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from mjooln.environment import *
from mjooln.exception import *


class Crypt:
    """ Wrapper for best practice key generation and AES 128 encryption

    From `Fernet Docs <https://cryptography.io/en/latest/fernet/>`_:
    HMAC using SHA256 for authentication, and PKCS7 padding.
    Uses AES in CBC mode with a 128-bit key for encryption, and PKCS7 padding.
    """

    # TODO: Do QA on cryptographic strength

    @classmethod
    def generate_key(cls):
        """ Generates URL-safe base64-encoded random key with length 44 """
        return Fernet.generate_key()

    @classmethod
    def salt(cls):
        """ Generates URL-safe base64-encoded random string with length 24

        :return: bytes
        """

        # Used 18 instead of standard 16 since encode otherwise leaves
        # two trailing equal signs (==) in the resulting string
        return base64.urlsafe_b64encode(os.urandom(18))

    @classmethod
    def key_from_password(cls,
                          salt: bytes,
                          password: str):
        """ Generates URL-safe base64-encoded random string with length 44

        :type salt: bytes
        :type password: str
        :return: bytes
        """

        password = password.encode()  # Convert to type bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password))

    @classmethod
    def encrypt(cls,
                data: bytes,
                key: bytes):
        """ Encrypts input data with the given key

        :type data: bytes
        :type key: bytes
        :return: bytes
        """
        if key is None:
            raise CryptError(f'Encryption key missing, cannot encrypt')
        fernet = Fernet(key)
        return fernet.encrypt(data)

    @classmethod
    def decrypt(cls,
                data: bytes,
                key: bytes):
        """ Decrypts input data with the given key

        :type data: bytes
        :type key: bytes
        :return: bytes
        """
        if key is None:
            raise CryptError(f'Encryption key missing, cannot encrypt')
        fernet = Fernet(key)
        try:
            return fernet.decrypt(data)
        except InvalidToken as it:
            raise CryptError(f'Invalid token. Probably due to '
                             f'invalid password/key. Actual message: {it}')


class Glass:
    @classmethod
    def glass(cls, *args, **kwargs):
        """
        If input is a class instance, return instance. If not, call
        constructor with same input arguments
        """
        if args and len(args) == 1 and not kwargs and isinstance(args[0], cls):
            return args[0]
        else:
            return cls(*args, **kwargs)


class Math:
    @classmethod
    def human_size(cls, size_bytes: int):
        # 2**10 = 1024
        power = 2 ** 10
        n = 0
        size = size_bytes
        power_labels = {0: '', 1: 'k', 2: 'M', 3: 'G', 4: 'T'}
        while size > power:
            size /= power
            n += 1
        return size, power_labels[n] + 'B'

    @classmethod
    def bytes_to_human(cls,
                       size_bytes: int,
                       min_precision=5):
        value, unit = cls.human_size(size_bytes=size_bytes)
        len_int = len(str(int(value)))
        if len_int >= min_precision or unit == 'B':
            len_dec = 0
        else:
            len_dec = min_precision - len_int
        return f'{value:.{len_dec}f} {unit}'


class Name:
    _CAMEL_TO_SNAKE = r'(?<!^)(?=[A-Z])'
    _SNAKE_TO_CAMEL = r'(.+?)_([a-z])'
    _RE_CAMEL_TO_SNAKE = re.compile(_CAMEL_TO_SNAKE)
    _RE_SNAKE_TO_CAMEL = re.compile(_SNAKE_TO_CAMEL)

    @classmethod
    def camel_to_snake(cls, camel: str):
        """
        Convert camel to snake::

            Name.camel_to_snake('ThisIsCamel')
                this_is_camel
        """
        return cls._RE_CAMEL_TO_SNAKE.sub('_', camel).lower()

    @classmethod
    def snake_to_camel(cls, snake: str):
        """
        Convert snake to camel::

            Name.snake_to_camel('this_is_snake')
                ThisIsSnake
        """
        # TODO: Implement regex instead
        return ''.join(x[0].upper() + x[1:] for x in
                       snake.split('_'))


class Seed:
    """
    Convenience methods for string representation of an object

    Object can be created with the method ``from_seed()``, but the method
    must be overridden in child class. Find methods use the class variable
    ``REGEX``, which must also be overridden in child class

    If the seed has a fixed length, this can be specified in the class
    variable ``LENGTH``, and will speed up identification (or will it...)
    """

    #: Regex identifying seed must be overridden in child class
    REGEX = None

    #: If seed has a fixed length, override in child class
    LENGTH = None

    @classmethod
    def _search(cls, str_: str):
        if not cls.REGEX:
            raise BadSeed(f'_REGEX must be overridden in child class')
        return re.compile(cls.REGEX).search(str_)

    @classmethod
    def _exact_match(cls, str_: str):
        if not cls.REGEX:
            raise BadSeed(f'_REGEX must be overridden in child class')
        _regex_exact = rf'^{cls.REGEX}$'
        return re.compile(_regex_exact).match(str_)

    @classmethod
    def verify_seed(cls, str_: str):
        """
        Check if string is seed

        :raise BadSeed: If string is not seed
        :param str_: Seed to verify
        """
        if not cls.is_seed(str_):
            raise BadSeed(f'Sting is not seed: {str_}')

    @classmethod
    def is_seed(cls, str_: str):
        """
        Checks if input string is an exact match for seed

        :param str_: Input string
        :return: True if input string is seed, False if not
        """
        if cls.LENGTH and len(str_) != cls.LENGTH:
            return False
        return cls._exact_match(str_) is not None

    @classmethod
    def seed_in(cls, str_: str):
        """ Check if input string contains one or more seeds

        :param str_: String to check
        :type str_: str
        :return: True if input string contains one or more seeds, false if not
        """
        if cls._search(str_):
            return True
        else:
            return False

    @classmethod
    def find_seed(cls, str_: str):
        """
        Looks for and returns exactly one object from text

        Uses ``from_seed()`` to instantiate object from seed and will fail if
        there are none or multiple seeds.
        Use find_all() to return a list of identities in text, including
        an empty list if there are none

        :raise BadSeed: If none or multiple seeds are found in string
        :param str_: String to search for seed
        :type str_: str
        :return: Seed object
        """
        res = re.findall(cls.REGEX, str_)
        if len(res) == 1:
            return cls.from_seed(res[0])
        elif not res:
            raise BadSeed(
                f'No {cls.__name__} found in this text: \'{str_}\'; '
                f'Consider using find_seeds(), which will '
                f'return empty list if none are found.')
        else:
            raise BadSeed(
                f'Found {len(res)} instances of {cls.__name__} in this '
                f'text: \'{str_}\'; '
                f'Use find_all() to return a list of all instances'
            )

    @classmethod
    def find_seeds(cls,
                   str_: str):
        """ Finds and returns all seeds in text

        :type str_: str
        :return: List of objects
        """
        ids = re.findall(cls.REGEX, str_)
        return [cls.from_seed(x) for x in ids]

    @classmethod
    def from_seed(cls, str_: str):
        """
        Must be overridden in child class.

        Will create an object from seed

        :param str_: Seed
        :return: Instance of child class
        """
        raise BadSeed(f'Method from_seed() must be overridden '
                      f'in child class \'{cls.__name__}')

    def seed(self):
        """
        Get seed of current object.

        Default is ``str(self)``
        :return: Seed
        """
        return str(self)


class Dic:
    """Enables child classes to mirror attributes and dictionaries

    Private variables start with underscore, and are ignored by default.

    .. note:: Meant for inheritance and not direct use
    """
    # Maybe even require equal keys if adding. I.e. only to be used for
    # configuration, or serialization
    _PRIVATE_STARTSWITH = '_'

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            if isinstance(args[0], dict):
                self.add(args[0])
            elif PIXIE_IN_PIPELINE:
                raise PixieInPipeline(
                    'Only allowed argument for constructor is '
                    'a dict. Use kwargs, or inheritance for customization')
        elif len(args) > 1 and PIXIE_IN_PIPELINE:
            raise PixieInPipeline(
                'Dic cannot be instantiated with multiple args, only '
                'kwargs. Use inheritance for customization')
        self.add(kwargs)

    @classmethod
    def from_dict(cls,
                  di: dict):
        """
        Create a new object from input dictionary
        """
        return cls(**di)

    def to_vars(self,
                ignore_private: bool = True):
        di = vars(self).copy()
        if ignore_private:
            pop_keys = [x for x in di if x.startswith(self._PRIVATE_STARTSWITH)]
            for key in pop_keys:
                di.pop(key)

        return di

    def to_dict(self,
                ignore_private: bool = True,
                recursive: bool = False):
        # TODO: Populate to_doc etc with recursive, same way as ignoreprivate
        """ Return dictionary with a copy of attributes

        :param ignore_private: Ignore private attributes flag
        :return: dict
        """
        di = self.to_vars(ignore_private=ignore_private)
        if recursive:
            for key, item in di.items():
                if isinstance(item, Dic):
                    di[key] = item.to_vars(ignore_private=ignore_private)
        return di

    def keys(self, ignore_private=True):
        dic = self.to_dict(ignore_private=ignore_private)
        return [str(x) for x in dic.keys()]

    def __repr__(self):
        di = self.to_vars()
        dicstr = []
        for key, item in di.items():
            dicstr.append(f'{key}={item.__repr__()}')
        dicstr = ', '.join(dicstr)
        return f'{type(self).__name__}({dicstr})'

    def _add_item(self, key, item, ignore_private=True):
        # Add item and ignore private items if ignore_private is set to True
        if not ignore_private or not key.startswith(self._PRIVATE_STARTSWITH):
            self.__setattr__(key, item)

    def _add_dict(self,
                  dic: dict,
                  ignore_private: bool = True):
        for key, item in dic.items():
            self._add_item(key, item, ignore_private=ignore_private)

    def add(self,
            dic: dict,
            ignore_private: bool = True):
        """ Add dictionary to class as attributes

        :param dic: Dictionary to add
        :param ignore_private: Ignore private attributes flag
        :return: None
        """
        self._add_dict(dic, ignore_private=ignore_private)

    # TODO: Consider always requiring equal
    def add_only_existing(self, dic, ignore_private=True):
        """ Add dictionary keys and items as attributes if they already exist
        as attributes

        :param dic: Dictionary to add
        :param ignore_private: Ignore private attributes flag
        :return: None
        """
        dic_to_add = {}
        for key in dic:
            if hasattr(self, key):
                dic_to_add[key] = dic[key]
        self._add_dict(dic_to_add, ignore_private=ignore_private)

    # TODO: Consider decprecation
    def force_equal(self, dic, ignore_private=True):
        """ Add all dictionary keys and items as attributes in object, and
        delete existing attributes that are not keys in the input dictionary

        :param dic: Dictionary to add
        :param ignore_private: Ignore private attributes flag
        :return: None
        """
        self._add_dict(dic, ignore_private=ignore_private)
        for key in self.to_dict(ignore_private=ignore_private):
            if key not in dic:
                self.__delattr__(key)

    def print(self,
              ignore_private=True,
              indent=4 * ' ',
              width=80,
              flatten=False,
              separator=ELEMENT_SEPARATOR):
        """
        Pretty print object attributes in terminal

        :param ignore_private: Ignore private variables flag
        :param indent: Spacing for sub dictionaries
        :param width: Target width of printout
        :param flatten: Print as joined keys
        :param separator: Key separator when flattening
        """
        text = f'--{indent}[[ {type(self).__name__} ]]{indent}'
        text += (width - len(text)) * '-'
        print(text)
        if not flatten:
            dic = self.to_dict(ignore_private=ignore_private)
        else:
            dic = self.to_flat(sep=separator)
        self._print(dic, level=0)
        print(width * '-')

    def _print(self, dic, level=0, indent=4 * ' '):
        for key, item in dic.items():
            if isinstance(item, dict):
                print(level * indent + f'{key}: [dict]')
                self._print(item, level=level + 1)
            elif isinstance(item, Dic) and not isinstance(item, Seed):
                item = item.to_dict()
                print(level * indent + f'{key}: [{type(item).__name__}]')
                self._print(item, level=level + 1)
            else:
                print(level * indent + f'{key}: '
                                       f'[{type(item).__name__}] {item} ')

    def print_flat(self,
                   ignore_private=True,
                   separator=ELEMENT_SEPARATOR):
        self.print(ignore_private=ignore_private,
                   separator=separator, flatten=True)

    # TODO: Move to flag in to_dict etc., and unflatten in from_dict etc
    # TODO: Replace sep with Key sep.
    # TODO: Require var names not to have double underscores
    # TODO: Figure out how to handle __vars__, what is the difference with _vars

    def to_flat(self,
                sep=ELEMENT_SEPARATOR,
                ignore_private=True):
        """
        Flatten dictionary to top level only by combining keys with the
        given separator

        :param sep: Separator to use, default is double underscore (__)
        :type sep: str
        :param ignore_private: Flags whether to ignore private attributes,
            identified by starting with underscore
        :return: Flattened dictionary
        :rtype: dict
        """
        di = self.to_dict(ignore_private=ignore_private)
        return self.flatten(di, sep=sep)

    @classmethod
    def from_flat(cls,
                  di_flat: dict,
                  sep=ELEMENT_SEPARATOR):
        return cls.from_dict(cls.unflatten(di_flat,
                                           sep=sep))

    @classmethod
    def _flatten(cls, di: dict, parent_key='', sep=ELEMENT_SEPARATOR):
        items = []
        for key, item in di.items():
            if parent_key:
                new_key = parent_key + sep + key
            else:
                new_key = key
            if isinstance(item, dict):
                items.extend(cls._flatten(item, new_key, sep=sep).items())
            else:
                items.append((new_key, item))
        return dict(items)

    @classmethod
    def flatten(cls, di: dict, sep=ELEMENT_SEPARATOR):
        return cls._flatten(di, sep=sep)

    @classmethod
    def unflatten(cls, di_flat: dict, sep=ELEMENT_SEPARATOR):
        di = dict()
        for flat_key, item in di_flat.items():
            keys = flat_key.split(sep)
            di_tmp = di
            for key in keys[:-1]:
                if key not in di_tmp:
                    di_tmp[key] = dict()
                di_tmp = di_tmp[key]
            di_tmp[keys[-1]] = item
        return di


class JSON:
    """Dict to/from JSON string, with optional human readable"""

    @classmethod
    def dumps(cls, dic, human=True, sort_keys=False, indent=4 * ' '):
        """Convert from dict to JSON string

        :param dic: Input dictionary
        :type dic: dict
        :param human: Human readable flag
        :param sort_keys: Sort key flag (human readable only)
        :param indent: Indent to use (human readable only)
        """
        if human:
            return simplejson.dumps(dic, sort_keys=sort_keys, indent=indent)
        else:
            return json.dumps(dic)

    @classmethod
    def loads(cls, json_string):
        """ Parse JSON string to dictionary

        :param json_string: JSON string
        :return: dict
        """
        return simplejson.loads(json_string)


class YAML:

    @classmethod
    def dumps(cls, dic):
        """
        Convert dictionary to yaml
        """
        return yaml.safe_dump(dic)

    @classmethod
    def loads(cls, yaml_str):
        """
        Convert yaml string to dictionary
        """
        return yaml.safe_load(yaml_str)


# TODO: Rewrite as serializer/deserializer
# TODO: In other words, doc will be dic with dates as strings.
# TODO: Atom can be builtin, otherwise it will be a bit tricky.
# TODO: SHould zulu/key/identity also be builtin?
class Doc(Dic):
    """
    Enables child classes to mirror attributes, dictionaries, JSON and
    YAML

    ..note:: to_doc and from_doc are meant to be overridden in child class if
    elements are not serializable
    """

    @classmethod
    def from_doc(cls, doc: dict):
        """
        Convert input dictionary to correct types and return object

        ..note:: Override in child class to handle custom types

        :param doc: Dictionary with serializable items only
        :return: New Doc object instantiated with input dictionary
        :rtype: Doc
        """
        return cls.from_dict(doc)

    @classmethod
    def from_json(cls,
                  json_string: str):
        doc = JSON.loads(json_string=json_string)
        return cls.from_doc(doc)

    @classmethod
    def from_yaml(cls,
                  yaml_string: str):
        doc = YAML.loads(yaml_string)
        return cls.from_doc(doc)

    def add_yaml(self,
                 yaml_string: str,
                 ignore_private=True):
        dic = YAML.loads(yaml_string)
        self.add(dic, ignore_private=ignore_private)

    def add_json(self,
                 json_string: str,
                 ignore_private=True):
        dic = JSON.loads(json_string)
        self.add(dic, ignore_private=ignore_private)

    def to_doc(self):
        """
        Converts class attributes to dictionary of serializable attributes

        ..note:: Override in child class to handle custom types

        :param ignore_private: Ignore private flag
        :return: Dictionary of serialized objects
        """
        doc = self.to_dict(ignore_private=True)
        return doc

    def to_json(self, human: bool = False):
        doc = self.to_doc()
        return JSON.dumps(doc, human=human)

    def to_yaml(self):
        doc = self.to_doc()
        return YAML.dumps(doc)
