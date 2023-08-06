import os

HOME = os.getenv('MJOOLN__HOME',
                 os.path.join(os.path.expanduser('~'),
                              '.mjooln')).replace('\\', '/')

PIXIE_IN_PIPELINE = \
    os.getenv('MJOOLN__PIXIE_IN_PIPELINE', 'true') == 'true'

MINIMUM_ELEMENT_LENGTH = \
    os.getenv('MJOOLN__MINIMUM_ELEMENT_LENGTH', 1)

ELEMENT_SEPARATOR = \
    os.getenv('MJOOLN__ELEMENT_SEPARATOR', '__')

CLASS_SEPARATOR = \
    os.getenv('MJOOLN__CLASS_SEPARATOR', '___')

COMPRESSED_EXTENSION = \
    os.getenv('MJOOLN__COMPRESSED_EXTENSION', 'gz')

ENCRYPTED_EXTENSION = \
    os.getenv('MJOOLN__ENCRYPTED_EXTENSION', 'aes')

TRUNK_PATH = \
    os.getenv('MJOOLN__TRUNK_PATH',
              os.path.join(HOME, 'trunk.yaml')).replace('\\', '/')

TRUNK_EXTENSION = \
    os.getenv('MJOOLN__TRUNK_EXTENSION', 'yaml')

TRUNK_AUTO_SCAN = \
    os.getenv('MJOOLN__TRUNK_AUTO_SCAN', 'true') == 'true'

#: None will use all mountpoints
TRUNK_AUTO_SCAN_FOLDERS = \
    os.getenv('MJOOLN__TRUNK_AUTO_SCAN_FOLDERS', 'none') == 'none'
