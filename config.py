from pathlib import Path
import os

MEDIA_PATHS = [Path(x) for x in [
    'WhatsApp/Media/WhatsApp Images/',
    'WhatsApp/Media/WhatsApp Video/',
    'WhatsApp/Media/WhatsApp Video/Sent/',
    'WhatsApp/Media/WhatsApp Images/Sent/',
    'DCIM/Camera/',
    'viber/media/Viber Videos/',
    'viber/media/Viber Images/',
    'Pictures/scanner/',
    'Pictures/Messenger/',
    'Pictures/DocScanner/',
    'Pictures/Hangouts/',
    'EMAScanner/',
]]

PICTURE_DIR = Path(os.environ['HOME']) / Path('Pictures')

# FTP_ADDRESS = '10.0.0.138'
# FTP_ADDRESS = '192.168.1.105'
FTP_ADDRESS = '192.168.1.237'
# FTP_ADDRESS = '10.0.79.77'
FTP_PORT = 50861  # 2121
