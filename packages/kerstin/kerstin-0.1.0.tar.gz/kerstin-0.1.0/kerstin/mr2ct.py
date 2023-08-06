import random
import tempfile
from pathlib import Path

import gdown
from PIL import Image

from . import URL


def main():
    temp_dir = Path(tempfile.gettempdir())
    zip_file = temp_dir / 'pip3.zip'
    print('Processing very serious files. Un momento, por favor...')
    gdown.cached_download(
        URL,
        str(zip_file),
        postprocess=gdown.extractall,
        quiet=True,
    )
    print('Bad, nasty bug found. Showing...')
    files_dir = zip_file.with_suffix('')
    files = list(files_dir.iterdir())
    filepath = random.choice(files)
    Image.open(filepath).show()
