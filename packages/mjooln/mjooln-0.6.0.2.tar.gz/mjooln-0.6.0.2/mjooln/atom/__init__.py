import logging
import string
import re
import uuid
import datetime
import pytz
import dateutil
from dateutil.parser import parse as dateparser
from collections import namedtuple

from mjooln.environment import *
from mjooln.exception import *
from mjooln.core import Seed, Glass, Doc


class Element(str, Seed, Glass):
    """
    Defines element string with limitations

    - Minimum length is 2
    - Allowed characters are

        - Lower case ascii ``a-z``
        - Digits ``0-9``
        - Underscore ``_``
    - Underscore and digits can not be the first character
    - Underscore can not be the last character
    - Can not contain double underscore since it acts as separator for elements
      in :class:`.Key`

    Sample elements::

        'simple'
        'with_longer_name'
        'digit1'
        'longer_digit2'

    """
    logger = logging.getLogger(__name__)

    REGEX = r'(?!.*__.*)[a-z0-9][a-z_0-9]*[a-z0-9]'

    #: Allowed characters
    ALLOWED_CHARACTERS = string.ascii_lowercase + string.digits + '_'

    #: Allowed first characters
    ALLOWED_STARTSWITH = string.ascii_lowercase + string.digits

    #: Allowed last characters
    ALLOWED_ENDSWITH = string.ascii_lowercase + string.digits

    NONE = 'n_o_n_e'

    @classmethod
    def is_seed(cls, str_: str):
        if len(str_) == 1:
            if MINIMUM_ELEMENT_LENGTH > 1:
                return False
            else:
                return str_ in cls.ALLOWED_STARTSWITH
        else:
            return super().is_seed(str_)

    @classmethod
    def pixie(cls, str_: str):
        if not cls.__pixie:
            cls.verify_element(str_)
        return cls(str_)

    @classmethod
    def verify_element(cls, str_: str):
        """
        Verify that string is a valid element

        :param str_: String to verify
        :return: True if str_ is valid element, False if not
        """
        if len(str_) < MINIMUM_ELEMENT_LENGTH:
            raise InvalidElement(
                f'Element too short. Element \'{str_}\' has '
                f'length {len(str_)}, while minimum length '
                f'is {MINIMUM_ELEMENT_LENGTH}')
        if not str_[0] in cls.ALLOWED_STARTSWITH:
            raise InvalidElement(f'Invalid startswith. Element \'{str_}\' '
                                 f'cannot start with \'{str_[0]}\'. '
                                 f'Allowed startswith characters are: '
                                 f'{cls.ALLOWED_STARTSWITH}')
        if not str_[-1] in cls.ALLOWED_ENDSWITH:
            raise InvalidElement(f'Invalid endswith. Element \'{str_}\' '
                                 f'cannot end with \'{str_[-1]}\'. '
                                 f'Allowed endswith characters are: '
                                 f'{cls.ALLOWED_ENDSWITH}')
        invalid_characters = [x for x in str_ if x not in
                              cls.ALLOWED_CHARACTERS]
        if len(invalid_characters) > 0:
            raise InvalidElement(
                f'Invalid character(s). Element \'{str_}\' cannot '
                f'contain any of {invalid_characters}. '
                f'Allowed characters are: '
                f'{cls.ALLOWED_CHARACTERS}')
        if ELEMENT_SEPARATOR in str_:
            raise InvalidElement(
                f'Element contains element separator, which is '
                f'reserved for separating Elements in a Key.'
                f'Element \'{str_}\' cannot contain '
                f'\'{CLASS_SEPARATOR}\'')

    # @classmethod
    # def elf(cls, element):
    #     """ Allows key class to pass through instead of throwing exception
    #
    #     :param element: Input element string or element class
    #     :type element: str or Element
    #     :return: Element
    #     """
    #     # Convert to snake_case if is CamelCase
    #     if not element[0].isdigit() and
    #     # TODO: Handle input and guess a conversion that would match criteria
    #     if isinstance(element, Element):
    #         return element
    #     else:
    #         return cls(element)

    def __new__(cls,
                element: str):
        if PIXIE_IN_PIPELINE:
            try:
                cls.verify_element(element)
            except InvalidElement as ie:
                raise PixieInPipeline('Invalid element') from ie
        else:
            if not cls.is_seed(element):
                raise InvalidElement(f'Invalid element: {element}')
        self = super(Element, cls).__new__(cls, element)
        return self

    def __repr__(self):
        return f'Element(\'{self}\')'


class Identity(str, Seed, Glass):
    """ UUID string generator with convenience functions

    Inherits str, and is therefore an immutable string, with a fixed format
    as illustrated below.

    Examples::

        Identity()
            'BD8E446D_3EB9_4396_8173_FA1CF146203C'

        Identity.is_in('Has BD8E446D_3EB9_4396_8173_FA1CF146203C within')
            True

        Identity.find_one('Has BD8E446D_3EB9_4396_8173_FA1CF146203C within')
            'BD8E446D_3EB9_4396_8173_FA1CF146203C'

    """

    REGEX = r'[0-9A-F]{8}\_[0-9A-F]{4}\_[0-9A-F]{4}\_[0-9A-F]{4}' \
            r'\_[0-9A-F]{12}'

    REGEX_CLASSIC = r'[0-9a-f]{8}\-[0-9a-f]{4}\-[0-9a-f]{4}\-[0-9a-f]{4}' \
                    r'\-[0-9a-f]{12}'
    REGEX_COMPACT = r'[0-9a-f]{32}'
    LENGTH = 36

    @classmethod
    def from_seed(cls, str_: str):
        return cls(str_)

    @classmethod
    def is_classic(cls, str_: str):
        if len(str_) != 36:
            return False
        _regex_exact = rf'^{cls.REGEX_CLASSIC}$'
        return re.compile(_regex_exact).match(str_) is not None

    @classmethod
    def from_classic(cls, str_: str):
        str_ = str_.replace('-', '_').upper()
        return cls(str_)

    @classmethod
    def is_compact(cls, str_: str):
        if len(str_) != 32:
            return False
        _regex_exact = rf'^{cls.REGEX_COMPACT}$'
        return re.compile(_regex_exact).match(str_) is not None

    @classmethod
    def from_compact(cls, str_: str):
        str_ = '_'.join([
            str_[:8],
            str_[8:12],
            str_[12:16],
            str_[16:20],
            str_[20:]
        ]).upper()
        return cls(str_)

    @classmethod
    def elf(cls, str_):
        if isinstance(str_, Identity):
            return str_
        elif isinstance(str_, str):
            if cls.is_seed(str_):
                return cls(str_)
            elif cls.is_classic(str_):
                return cls.from_classic(str_)
            elif cls.is_compact(str_):
                return cls.from_compact(str_)
            elif cls.is_classic(str_.lower()):
                return cls.from_classic(str_.lower())
            elif cls.is_compact(str_.lower()):
                return cls.from_compact(str_.lower())

            # Try to find one or more identities in string
            ids = cls.find_seeds(str_)
            if len(ids) > 0:
                # If found, return the first
                return ids[0]
        raise IdentityError(
            f'This useless excuse for a string has no soul, '
            f'and hence no identity: \'{str_}\''
        )

    def __new__(cls,
                identity: str = None):
        if not identity:
            identity = str(uuid.uuid4()).replace('-', '_').upper()
        elif not cls.is_seed(identity):
            raise IdentityError(f'String is not valid identity: {identity}')
        instance = super(Identity, cls).__new__(cls, identity)
        return instance

    def __repr__(self):
        return f'Identity(\'{self}\')'

    def classic(self):
        return str(self).replace('_', '-').lower()

    def compact(self):
        return str(self).replace('_', '').lower()


class Key(str, Seed, Glass):
    """
    Defines key string with limitations:

    - Minimum length is 2
    - Allowed characters are:

        - Lower case ascii (a-z)
        - Digits (0-9)
        - Underscore (``_``)
        - Double underscore (``__``)
    - Underscore and digits can not be the first character
    - Underscore can not be the last character
    - The double underscore act as separator for :class:`.Element`s
      in the key
    - Triple underscore is reserved for separating keys from other keys or
      seeds, such as in class :class:`.Atom`

    Sample keys::

        'simple'
        'with_longer_name'
        'digit1'
        'longer_digit2'
        'element_one__element_two__element_three'
        'element1__element2__element3'
        'element_1__element_2__element_3'

    """

    #: Allowed characters
    ALLOWED_CHARACTERS = string.ascii_lowercase + string.digits + '_'

    #: Allowed first characters
    ALLOWED_STARTSWITH = string.ascii_lowercase

    #: Allowed last characters
    ALLOWED_ENDSWITH = string.ascii_lowercase + string.digits

    #: Regular expression for verifying and finding keys
    REGEX = rf'(?!.*{CLASS_SEPARATOR}.*)[a-z][a-z_0-9]*[a-z0-9]'

    def __new__(cls,
                key: str):
        if PIXIE_IN_PIPELINE:
            try:
                cls.verify_key(key)
            except InvalidElement as ie:
                raise PixieInPipeline('Invalid element in key') from ie
            except InvalidKey as ik:
                raise PixieInPipeline('Invalid key') from ik
        if not cls.is_seed(key):
            raise InvalidKey(f'Invalid key: {key}')
        self = super(Key, cls).__new__(cls, key)
        return self

    def __repr__(self):
        return f'Key(\'{self}\')'

    @classmethod
    def verify_key(cls, key: str):
        """
        Verify that string is a valid key

        :param key: String to check
        :return: True if string is valid key, False if not
        """
        if not len(key) >= MINIMUM_ELEMENT_LENGTH:
            raise InvalidKey(f'Key too short. Key \'{key}\' has length '
                             f'{len(key)}, while minimum length is '
                             f'{MINIMUM_ELEMENT_LENGTH}')
        if CLASS_SEPARATOR in key:
            raise InvalidKey(f'Key contains element reserved as class '
                             f'separator. '
                             f'Key \'{key}\' cannot contain '
                             f'\'{CLASS_SEPARATOR}\'')
        if not key[0] in cls.ALLOWED_STARTSWITH:
            raise InvalidKey(f'Invalid startswith. Key \'{key}\' '
                             f'cannot start with \'{key[0]}\'. '
                             f'Allowed startswith characters are: '
                             f'{cls.ALLOWED_STARTSWITH}')

        elements = key.split(ELEMENT_SEPARATOR)
        for element in elements:
            Element.verify_element(element)

    def elements(self):
        """
        Return list of elements in key (separated by double underscore)

        Example::

            key = Key('some_key__with_two__no_three_elements')
            key.elements()
                ['some_key', 'with_two', 'three_elements']
            key.elements()[0]
                Element('some_key)

        :returns: [Element]
        """
        return [Element(x) for x in self.split(ELEMENT_SEPARATOR)]

    def with_separator(self,
                       separator: str):
        """ Replace separator

        Example::

            key = Key('some__key_that_could_be__path')
            key.with_separator('/')
                'some/key_that_could_be/path'

        :param separator: Separator of choice
        :type separator: str
        :return: str
        """
        return separator.join(self.elements())

    @classmethod
    def elf(cls, key):
        """ Allows key class to pass through instead of throwing exception

        :param key: Input key string or key class
        :type key: str or Key
        :return: Key
        """
        if isinstance(key, Key):
            return key
        else:
            _original_class = None
            if not isinstance(key, str):
                _original_class = type(key).__name__
                key = str(key)

            _original = key
            if Key.is_seed(key):
                return cls(key)
            key = key.strip()
            if Key.is_seed(key):
                return cls(key)
            key = key.replace(' ', '_')
            if Key.is_seed(key):
                return cls(key)
            key = key.lower()
            if Key.is_seed(key):
                return cls(key)
            if _original_class:
                raise InvalidKey(f'Creating '
                                 f'a key from \'{_original_class}\' is, as '
                                 f'you should have known, not meant to be. '
                                 f'Resulting string was: {_original}')
            raise InvalidKey(f'I tried but no way I can make a key out of '
                             f'this excuse of a string: {_original}')


class Zulu(datetime.datetime, Seed, Glass):
    # TODO: Revise documentation
    # TODO: Round to millisecond etc. And floor. Check Arrow how its done
    # TODO: Move elf doc to elf method
    # TODO: Same date in all examples?
    # TODO: Move examples to separate documentation page?

    """Timezone aware datetime objects in UTC

    Create using constructor::

        Zulu() or Zulu.now()
            Zulu(2020, 5, 21, 20, 5, 31, 930343)

        Zulu(2020, 5, 12)
            Zulu(2020, 5, 12)

        Zulu(2020, 5, 21, 20, 5, 31)
            Zulu(2020, 5, 21, 20, 5, 31)

    Zulu.seed() is a string on the format ``<date>T<time>u<microseconds>Z``,
    and is \'designed\'
    to be file name and double click friendly, as well as easily recognizable
    within some string when using regular expressions.
    Printing a Zulu object returns seed, and Zulu can be created using
    from_seed()::

        z = Zulu(2020, 5, 12)
        print(z)
            20200512T000000u000000Z

        z.seed()
            '20200512T000000u000000Z'

        str(z)
            '20200512T000000u000000Z'

        Zulu.from_seed('20200512T000000u000000Z')
        z = Zulu(2020, 5, 12)

    For an ISO 8601 formatted string, use custom function::

        z = Zulu('20200521T202041u590718Z')
        z.iso()
            '2020-05-21T20:20:41.590718+00:00'

    Similarly, Zulu can be created from ISO string::

        Zulu.from_iso('2020-05-21T20:20:41.590718+00:00')
            Zulu(2020, 5, 21, 20, 20, 41, 590718)


    Inputs or constructors may vary, but Zulu objects are *always* UTC. Hence
    the name Zulu.

    Constructor also takes regular datetime objects, provided they have
    timezone info::

        dt = datetime.datetime(2020, 5, 23, tzinfo=pytz.utc)
        Zulu(dt)
            Zulu(2020, 5, 23, 0, 0, tzinfo=<UTC>)

        dt = datetime.datetime(2020, 5, 23, tzinfo=dateutil.tz.tzlocal())
        Zulu(dt)
            Zulu(2020, 5, 22, 22, 0, tzinfo=<UTC>)

    Zulu has element access like datetime, in addition to string convenience
    attributes::

        z = Zulu()
        print(z)
            20200522T190137u055918Z
        z.month
            5
        z.str.month
            '05'
        z.str.date
            '20200522'
        z.str.time
            '190137'

    Zulu has a delta convenience function for timedelta, as well as a function
    to add deltas directly to generate a new Zulu::

        Zulu.delta(hours=1)
            datetime.timedelta(seconds=3600)

        z = Zulu(2020, 1, 1)
        z.add(days=2)
            Zulu(2020, 1, 3)

    For more flexible ways to create a Zulu object, see :meth:`Zulu.elf`

    .. warning:: Elves are fickle and rude


    """

    _ZuluStr = namedtuple('ZuluStr', [
        'year',
        'month',
        'day',
        'hour',
        'minute',
        'second',
        'microsecond',
        'date',
        'time',
        'seed',
    ])

    _FORMAT = '%Y%m%dT%H%M%Su%fZ'
    REGEX = r'\d{8}T\d{6}u\d{6}Z'
    LENGTH = 23

    ISO_REGEX_STRING = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-' \
                       r'(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):' \
                       r'([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-]' \
                       r'(?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
    ISO_REGEX = re.compile(ISO_REGEX_STRING)

    ############################################################################
    # String methods
    ############################################################################

    @classmethod
    def is_iso(cls, str_):
        # TODO: Use regex instead, and include check on timezone (optional)
        """Check if input string is
        `ISO 8601 <https://en.wikipedia.org/wiki/ISO_8601>`_

        Check is done using regex ``Zulu.ISO_REGEX``

        :param ts_str: Maybe an ISO formatted string
        :return: True if str_ is iso, False if not
        :rtype: bool
        """
        try:
            if cls.ISO_REGEX.match(str_) is not None:
                return True
        except:
            pass
        return False

    ############################################################################
    # Timezone methods
    ############################################################################

    @classmethod
    def all_timezones(cls):
        """
        Returns a list of all allowed timezone names

        Timezone \'local\' will return a datetime object with local timezone,
        but is not included in this list

        Wrapper for ``pytz.all_timezones``

        :return: List of timezones
        :rtype: list
        """
        return pytz.all_timezones

    @classmethod
    def _to_utc(cls, ts):
        return ts.astimezone(pytz.utc)

    @classmethod
    def _tz_from_name(cls, tz='utc'):
        if tz == 'local':
            tz = dateutil.tz.tzlocal()
        else:
            try:
                tz = pytz.timezone(tz)
            except pytz.exceptions.UnknownTimeZoneError as ue:
                raise ZuluError(f'Unknown timezone: \'{tz}\'. '
                                f'Use Zulu.all_timezones() for a list '
                                f'of actual timezones')
        return tz

    ############################################################################
    # Create methods
    ############################################################################

    @classmethod
    def now(cls,
            tz=None):
        """
        Overrides ``datetime.datetime.now()``. Equivalent to ``Zulu()``

        :raise ZuluError: If parameter ``tz`` has a value. Even if value is UTC
        :param tz: Do not use. Zulu is always UTC
        :return: Zulu
        """
        if tz:
            raise ZuluError(f'Zulu.now() does not allow input time zone info. '
                            f'Zulu is always UTC. Hence the name')
        return cls()

    @classmethod
    def _from_unaware(cls, ts, tz=None):
        if not tz:
            raise ZuluError('No timezone info. Set timezone to use '
                            'with \'tz=<timezone string>\'. \'local\' will '
                            'use local timezone info. Use '
                            'Zulu.all_timezones() for a list of actual '
                            'timezones')
        return ts.replace(tzinfo=cls._tz_from_name(tz))

    @classmethod
    def _elf(cls, ts, tz=None):
        # Takes a datetime.datetime object and adds the input tzinfo if
        # none is present
        if not ts.tzinfo:
            ts = cls._from_unaware(ts, tz=tz)
        return ts

    @classmethod
    def from_unaware(cls, ts, tz='utc'):
        """ Create Zulu from timezone unaware datetime

        :param ts: Unaware time stamp
        :type ts: datetime.datetime
        :param tz: Time zone, with 'utc' as default.
            'local' will use local time zone
        :return: Zulu
        :rtype: Zulu
        """
        if ts.tzinfo:
            raise ZuluError(f'Input datetime already has '
                            f'time zone info: {ts}. '
                            f'Use constructor or Zulu.elf()')
        else:
            ts = cls._from_unaware(ts, tz=tz)
        return cls(ts)

    @classmethod
    def from_unaware_local(cls, ts):
        """ Create Zulu from timezone unaware local timestamp

        :param ts: Timezone unaware datetime
        :type ts: datetime.datetime
        :return: Zulu
        :rtype: Zulu
        """
        return cls.from_unaware(ts, tz='local')

    @classmethod
    def from_unaware_utc(cls, ts):
        """ Create Zulu from timezone unaware UTC timestamp

        :param ts: Timezone unaware datetime
        :type ts: datetime.datetime
        :return: Zulu
        :rtype: Zulu
        """
        return cls.from_unaware(ts, tz='utc')

    @classmethod
    def _parse_iso(cls,
                   iso: str):
        ts = dateparser(iso)
        if ts.tzinfo and str(ts.tzinfo) == 'tzutc()':
            ts = ts.astimezone(pytz.utc)
        return ts

    @classmethod
    def from_iso(cls,
                 str_: str,
                 tz=None):
        """
        Create Zulu object from ISO 8601 string

        :param iso: ISO 8601 string
        :param tz: Timezone string to use if missing in ts_str
        :return: Zulu
        :rtype: Zulu
        """
        ts = cls._parse_iso(str_)
        if tz and not ts.tzinfo:
            ts = cls._from_unaware(ts, tz)
        elif ts.tzinfo and tz:
            raise ZuluError(f'Timezone info found in ISO string as well as '
                            f'input timezone argument (tz). Keep tz=None, '
                            f'or use Zulu.elf()')
        elif not tz and not ts.tzinfo:
            raise ZuluError('No timezone info in neither ISO string '
                            'nor tz argument')
        return cls(ts)

    @classmethod
    def _parse(cls,
               ts_str: str,
               pattern: str):
        return datetime.datetime.strptime(ts_str, pattern)

    @classmethod
    def parse(cls,
              ts_str: str,
              pattern: str,
              tz=None):
        """Parse time stamp string with the given pattern

        :param ts_str: Timestamp string
        :type ts_str: str
        :param pattern: Follows standard
            `python strftime reference <https://strftime.org/>`_
        :param tz: Timezone to use if timestamp does not have timezone info
        :return: Zulu
        """
        ts = cls._parse(ts_str, pattern)
        if not ts.tzinfo:
            ts = cls._from_unaware(ts, tz=tz)
        elif tz:
            raise ZuluError('Cannot have an input timezone argument when '
                            'input string already has timezone information')
        return cls(ts)

    @classmethod
    def from_seed(cls, str_: str):
        """
        Create Zulu object from Zulu seed

        :param str_: Zulu seed
        :return: Zulu
        :rtype: Zulu
        """
        if not cls.is_seed(str_):
            raise ZuluError(f'String is not Zulu seed: {str_}')
        ts = cls._parse(str_, cls._FORMAT)
        ts = cls._from_unaware(ts, tz='utc')
        return cls(ts)

    @classmethod
    def _from_epoch(cls, epoch):
        ts = datetime.datetime.utcfromtimestamp(epoch)
        return ts.replace(tzinfo=pytz.UTC)

    @classmethod
    def from_epoch(cls, epoch):
        """
        Create Zulu object from UNIX Epoch

        :param epoch: Unix epoch
        :type epoch: float
        :return: Zulu
        :rtype: Zulu
        """
        ts = cls._from_epoch(epoch)
        return cls(ts)

    @classmethod
    def _fill_args(cls, args):
        if len(args) < 8:
            # From date
            args = list(args)
            args += (8 - len(args)) * [0]
            if args[1] == 0:
                args[1] = 1
            if args[2] == 0:
                args[2] = 1
            args = tuple(args)

        if args[-1] not in [None, 0, pytz.utc]:
            raise ZuluError(f'Zulu can only be UTC. '
                            f'Invalid timezone: {args[-1]}')

        args = list(args)
        args[-1] = pytz.utc
        return tuple(args)

    @classmethod
    def elf(cls, *args, tz='local'):
        """General input Zulu constructor

        .. warning:: Elves are fickle and rude

        ``Zulu.elf()`` takes the same inputs as constructor, and also allows Zulu
        objects to pass through. If timeozone is missing it will assume the input
        timezone ``tz``, which is set to local as default

        It takes both seed strings and iso strings::

            Zulu.elf('20201112T213732u993446Z')
                Zulu(2020, 11, 12, 21, 37, 32, 993446)

            Zulu.elf('2020-11-12T21:37:32.993446+00:00')
                Zulu(2020, 11, 12, 21, 37, 32, 993446)

        It takes UNIX epoch::

            e = Zulu(2020, 1, 1).epoch()
            e
                1577836800.0
            Zulu.elf(e)
                Zulu(2020, 1, 1)

        It will guess the missing values if input integers are not a full date
        and/or time::

            Zulu.elf(2020)
                Zulu(2020, 1, 1)

            Zulu.elf(2020, 2)
                Zulu(2020, 2, 1)

            Zulu.elf(2020,1,1,10)
                Zulu(2020, 1, 1, 10, 0, 0)

        .. warning:: Elves are fickle and rude

        :param args: Input arguments
        :param tz: Time zone to assume if missing. 'local' will use local
            time zone. Use Zulu.all_timezones() for a list of actual
            timezones. Default is 'local'
        :return: Zulu
        """
        ts = None
        if len(args) == 0:
            return cls()
        elif len(args) > 1:
            args = cls._fill_args(args)
            ts = datetime.datetime(*args)
            if not ts.tzinfo:
                ts = cls._from_unaware(ts, tz)
        elif len(args) == 1:
            arg = args[0]
            if isinstance(arg, Zulu):
                return arg
            elif isinstance(arg, datetime.datetime):
                # Add timzone if missing
                ts = cls._elf(arg, tz=tz)
                return cls(ts)
            elif isinstance(arg, float):
                return cls.from_epoch(arg)
            elif isinstance(arg, int):
                # Instantiate as start of year
                return cls(arg, 1, 1)
            elif isinstance(arg, str):
                if cls.is_seed(arg):
                    return cls.from_seed(arg)
                elif cls.is_iso(arg):
                    ts = cls._parse_iso(arg)
                    # Add timzone if missing
                    ts = cls._elf(ts, tz=tz)
                else:
                    raise ZuluError(f'String is neither zulu, nor ISO: {arg}. '
                                    f'Use Zulu.parse() and enter the format '
                                    f'yourself')
            else:
                raise ZuluError(f'Found no way to interpret input '
                                f'argument as Zulu: {arg} [{type(arg)}]')
        return cls(ts)

    @classmethod
    def range(cls,
              start=None,
              n=10,
              delta=datetime.timedelta(hours=1)):
        """Generate a list of Zulu of fixed intervals

        .. warning:: Mainly for dev purposes. There are far better
            ways of creating a range of timestamps, such as using pandas.

        :param start: Start time Zulu, default is *now*
        :type start: Zulu
        :param n: Number of timestamps in range, with default 10
        :type n: int
        :param delta: Time delta between items, with default one hour
        :type delta: datetime.timedelta
        :return: [Zulu]
        """
        if not start:
            start = cls()
        return [Zulu.elf(start + x * delta) for x in range(n)]

    def __new__(cls, *args, **kwargs):
        if len(args) == 0 and len(kwargs) == 0:
            ts = datetime.datetime.utcnow()
            ts = ts.replace(tzinfo=pytz.UTC)
        elif len(args) == 1 and len(kwargs) == 0:
            arg = args[0]
            if isinstance(arg, str):
                raise ZuluError('Cannot instantiate Zulu with a string. Use '
                                'Zulu.from_iso(), Zulu.from_seed(), '
                                'Zulu.from_string() or Zulu.parse()')
            elif isinstance(arg, float):
                raise ZuluError(f'Cannot create Zulu object from a float: '
                                f'{arg}; If float is unix epoch, '
                                f'use Zulu.from_epoch()')
            elif isinstance(arg, Zulu):
                raise ZuluError(f'Input argument is already Zulu: {arg}. '
                                f'Use Zulu.glass() to allow passthrough')
            elif isinstance(arg, datetime.datetime):
                ts = arg
                if not ts.tzinfo:
                    raise ZuluError('Cannot create Zulu from datetime if '
                                    'datetime object does not have timezone '
                                    'info. Use Zulu.from_unaware()')
                ts = ts.astimezone(pytz.UTC)
            else:
                raise ZuluError(f'Unable to interpret input argument: '
                                f'{arg} [{type(arg).__name__}]')
        else:
            # Handle input as regular datetime input (year, month, day etc)
            try:
                ts = datetime.datetime(*args)
            except TypeError as te:
                raise ZuluError from te
            # Add timezone info if missing (assume utc, of course)
            if not ts.tzinfo:
                ts = ts.replace(tzinfo=pytz.UTC)

        # Create actual object
        args = tuple([ts.year, ts.month, ts.day,
                      ts.hour, ts.minute, ts.second,
                      ts.microsecond, ts.tzinfo])
        self = super(Zulu, cls).__new__(cls, *args)
        seed = self.strftime(self._FORMAT)
        self.str = self._ZuluStr(
            year=seed[:4],
            month=seed[4:6],
            day=seed[6:8],
            hour=seed[9:11],
            minute=seed[11:13],
            second=seed[13:15],
            microsecond=seed[16:22],
            date=seed[:8],
            time=seed[9:15],
            seed=seed,
        )
        return self

    def __str__(self):
        return self.str.seed

    def __repr__(self):
        times = [self.hour, self.minute, self.second]
        has_micro = self.microsecond > 0
        has_time = sum(times) > 0
        nums = [self.year, self.month, self.day]
        if has_time or has_micro:
            nums += times
        if has_micro:
            nums += [self.microsecond]
        numstr = ', '.join([str(x) for x in nums])
        return f'Zulu({numstr})'

    def epoch(self):
        """
        Get UNIX epoch (seconds since January 1st 1970)

        Wrapper for ``datetime.datetime.timestamp()``

        :return: Seconds since January 1st 1970
        :rtype: float
        """
        return self.timestamp()

    @classmethod
    def from_str(cls, str_):
        if cls.is_seed(str_):
            return cls.from_seed(str_)
        elif cls.is_iso(str_):
            return cls.from_iso(str_)
        else:
            raise ZuluError(f'Unknown string format (neither seed nor iso): '
                            f'{str_}; '
                            f'Use Zulu.parse() to specify format pattern and '
                            f'timezone')

    def iso(self, full=False):
        # TODO: Implement full flag
        """Create `ISO 8601 <https://en.wikipedia.org/wiki/ISO_8601>`_ string

        Example::

            z = Zulu(2020, 5, 21)
            z.iso()
                '2020-05-21T00:00:00+00:00'

        :return: str
        """
        if full:
            raise ZuluError('Full isoformat not implemented. Full means it '
                            'has fixed length no matter the value. Is needed '
                            'for certain document database based tools')
        return self.isoformat()

    def format(self, pattern):
        """Format Zulu to string with the given pattern

        :param pattern: Follows standard
            `Python strftime reference <https://strftime.org/>`_
        :return: str
        """
        return self.strftime(pattern)

    def to_unaware(self):
        """
        Get timezone unaware datetime object in UTC

        :return: Timezone unaware datetime
        :rtype: datetime.datetime
        """
        return datetime.datetime.utcfromtimestamp(self.epoch())

    def to_tz(self, tz='local'):
        """ Create regular datetime with input timezone

        For a list of timezones use :meth:`.Zulu.all_timezones()`, which is a
        wrapper for

        :param tz: Time zone to use. 'local' will return the local time zone.
            Default is 'local'
        :return: datetime.datetime
        """
        ts_utc = datetime.datetime.utcfromtimestamp(self.epoch())
        ts_utc = ts_utc.replace(tzinfo=pytz.UTC)
        return ts_utc.astimezone(self._tz_from_name(tz))

    def to_local(self):
        """ Create regular datetime with local timezone

        :return: datetime.datetime
        """
        return self.to_tz(tz='local')

    @classmethod
    def delta(cls,
              days=0,
              hours=0,
              minutes=0,
              seconds=0,
              microseconds=0,
              weeks=0):
        """Wrapper for datetime.timedelta

        :param days: Number of days
        :param hours: Number of hours
        :param minutes: Number of minutes
        :param seconds: Number of seconds
        :param microseconds: Number of microseconds
        :param weeks: Number of weeks
        :return: datetime.timedelta
        """
        return datetime.timedelta(days=days,
                                  hours=hours,
                                  minutes=minutes,
                                  seconds=seconds,
                                  microseconds=microseconds,
                                  weeks=weeks)

    def add(self,
            days=0,
            hours=0,
            minutes=0,
            seconds=0,
            microseconds=0,
            weeks=0):
        """Adds the input to current Zulu object and returns a new one

        :param days: Number of days
        :param hours: Number of hours
        :param minutes: Number of minutes
        :param seconds: Number of seconds
        :param microseconds: Number of microseconds
        :param weeks: Number of weeks
        :return: Zulu
        """
        delta = self.delta(days=days,
                           hours=hours,
                           minutes=minutes,
                           seconds=seconds,
                           microseconds=microseconds,
                           weeks=weeks)
        return self + delta


class Atom(Doc, Seed, Glass):
    """
    Triplet identifier intended for objects and data sets alike

    Format: ``<zulu>___<key>___<identity>``

    :class:`.Zulu` represents t0 or creation time

    :class:`.Key` defines grouping of the contents

    :class:`.Identity` is a unique identifier for the contents

    Constructor initializes a valid atom, and will raise an ``AtomError``
    if a valid atom cannot be created based on input parameters.

    The constructor must as minimum have :class:`.Key` as input::

        a = Atom('some_key')
        a.key
            'some_key'
        a.zulu
            Zulu(2020, 5, 22, 13, 13, 18, 179169, tzinfo=<UTC>)
        a.identity
            '060AFBD5_D865_4974_8E37_FDD5C55E7CD8'
        str(a)
            '20200522T131318u179169Z___some_key___060AFBD5_D865_4974_8E37_FDD5C55E7CD8'

    ``

    """

    REGEX = r'\d{8}T\d{6}u\d{6}Z\_\_\_[a-z][a-z_0-9]*[a-z0-9]\_\_\_' \
            r'[0-9A-F]{8}\_[0-9A-F]{4}\_[0-9A-F]{4}\_[0-9A-F]{4}\_[0-9A-F]{12}'

    @classmethod
    def from_seed(cls,
                  seed: str):
        if not cls.is_seed(seed):
            raise AtomError(f'Invalid atom seed: {seed}')
        zulu, key, identity = seed.split(CLASS_SEPARATOR)
        return cls(key=Key(key),
                   zulu=Zulu.from_seed(zulu),
                   identity=Identity(identity))

    @classmethod
    def elf(cls, *args, **kwargs):
        if len(args) == 1 and not kwargs:
            arg = args[0]
            if isinstance(arg, Atom):
                return arg
            if isinstance(arg, Key):
                return cls(arg)
            elif isinstance(arg, str):
                if Key.is_seed(arg):
                    return cls(arg)
                elif cls.is_seed(arg):
                    return cls.from_seed(arg)
                else:
                    raise AtomError(f'This input string is nowhere near '
                                    f'what I need to create an Atom: {arg}')
            elif Key.is_seed(arg):
                return cls(arg)
            else:
                raise AtomError(f'How the fuck am I supposed to create an atom '
                                f'based on this ridiculous excuse for an '
                                f'input: {arg} [{type(arg)}]')
        elif len(args) == 0:
            if 'key' not in kwargs:
                raise AtomError(f'At the very least, give me a key to work '
                                f'on. You know, key as thoroughly described '
                                f'in class Key')
            key = Key.elf(kwargs['key'])
            identity = None
            zulu = None
            if 'identity' in kwargs:
                identity = Identity.elf(kwargs['identity'])
            if 'zulu' in kwargs:
                zulu = Zulu.elf(kwargs['zulu'])
            return cls(key,
                       zulu=zulu,
                       identity=identity)
        raise AtomError(f'This is rubbish. Cannot make any sense of this '
                        f'mindless junk of input: '
                        f'args={args}; kwargs={kwargs}')

    @classmethod
    def default(cls):
        raise AtomError('Atom does not have a default value')

    @classmethod
    def from_dict(cls,
                  di: dict):
        return cls(key=di['key'],
                   zulu=di['zulu'],
                   identity=di['identity'])

    def __init__(self,
                 key,
                 zulu: Zulu = None,
                 identity: Identity = None):
        """ Initializes a valid atom

        :param args: One argument is treated as a atom string and parsed.
        Three arguments is treated as (zulu, key, identity), in that order.
        :param kwargs: key, zulu, identity. key is required, while zulu and
        identity are created if not supplied.
        """
        super(Atom, self).__init__()
        if isinstance(key, str):
            if Key.is_seed(key):
                key = Key(key)
            elif Atom.is_seed(key):
                raise AtomError(f'Cannot instantiate Atom with seed. '
                                f'Use Atom.from_seed()')
            else:
                raise AtomError(f'Invalid key: {key} [{type(key).__name__}]')

        if not isinstance(key, Key):
            raise AtomError(f'Invalid instance of key: {type(key)}')

        if not zulu:
            zulu = Zulu()
        if not identity:
            identity = Identity()

        self.__zulu = zulu
        self.__key = key
        self.__identity = identity

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return CLASS_SEPARATOR.join([str(self.__zulu),
                                     str(self.__key),
                                     str(self.__identity)])

    def __repr__(self):
        return f'Atom(key=\'{self.__key}\', ' \
               f'zulu={self.__zulu.__repr__()}, ' \
               f'identity={self.__identity.__repr__()})'

    def __hash__(self):
        return hash((self.__zulu, self.__key, self.__identity))

    def __lt__(self, other):
        return (self.__zulu, self.__key, self.__identity) < \
               (other.__zulu, other.__key, other.__identity)

    def __gt__(self, other):
        return (self.__zulu, self.__key, self.__identity) > \
               (other.__zulu, other.__key, other.__identity)

    def key(self):
        return self.__key

    def zulu(self):
        return self.__zulu

    def identity(self):
        return self.__identity

    def to_dict(self,
                ignore_private: bool = True,
                recursive: bool = False):
        return {
            'zulu': self.__zulu,
            'key': self.__key,
            'identity': self.__identity,
        }

    def to_doc(self,
               ignore_private: bool = True):
        return {
            'zulu': self.__zulu.iso(),
            'key': self.__key.seed(),
            'identity': self.__identity.seed(),
        }

    @classmethod
    def from_doc(cls, doc: dict):
        return cls(
            zulu=Zulu.from_iso(doc['zulu']),
            key=Key(doc['key']),
            identity=Identity(doc['identity']),
        )

    def with_sep(self,
                 sep: str):
        """ Atom string with custom separator

        :param sep: Custom separator
        :return: str
        """
        return sep.join(str(self).split(Config.CLASS_SEPARATOR))

    @classmethod
    def level_count(cls,
                    level: int = None):
        if level is None or level < 0:
            return 1
        else:
            return level

    @classmethod
    def _elements(cls, parts, level, sep=''):
        if level == 0:
            return []
        elif level > 0:
            return parts[:level]
        else:
            return [sep.join(parts[:-level])]

    def key_elements(self, elements=None):
        if elements is None:
            return [str(self.__key)]
        return self._elements(self.__key.elements(), elements,
                              sep=Config.ELEMENT_SEPARATOR)

    def date_elements(self, elements=3):
        if elements is None:
            return [self.__zulu.str.date]
        return self._elements([self.__zulu.str.year,
                               self.__zulu.str.month,
                               self.__zulu.str.day], elements)

    def time_elements(self, elements=0):
        if elements is None:
            return [self.__zulu.str.time]
        return self._elements([self.__zulu.str.hour,
                               self.__zulu.str.minute,
                               self.__zulu.str.second], elements)
