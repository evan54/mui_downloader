from pathlib import Path
from private_config import HOME_DIR

MEDIA_PATHS = [Path(x) for x in [
    'WhatsApp/Media/WhatsApp Images/',
    'DCIM/Camera/',
    'viber/media/Viber Videos/',
    'viber/media/Viber Images/',
    'Pictures/scanner/',
    'Pictures/Messenger/',
]]

PICTURE_DIR = Path(HOME_DIR) / Path('Pictures')

FTP_ADDRESS = '10.0.0.138'
# FTP_ADDRESS = '192.168.1.26'
# FTP_ADDRESS = '10.0.79.77'
FTP_PORT = 2121
