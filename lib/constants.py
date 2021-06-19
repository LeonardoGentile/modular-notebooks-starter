from pathlib import Path
from typing import Union
import toml

# File handling
READ = 'READ'
WRITE = 'WRITE'
CSV = 'CSV'
XLS = 'XLS'


# For the current working directory:
CWD = Path().resolve()
# CWD = pathlib.Path().absolute()
PARENT_DIR = Path(__file__).parent.resolve()
ROOT_DIR = PARENT_DIR.parents[0].resolve()

config = toml.load(Path(ROOT_DIR, 'config.toml'))
PATHS = config.get('paths')

DATA_DIR_NAME = PATHS.get('data_dir')
DATA_FILE_NAME = PATHS.get('data_file_name', None)

DATA_DIR_PATH: Path = Path(ROOT_DIR, DATA_DIR_NAME)  # load and save data
DATA_FILE_ABS_PATH: str = PATHS.get('data_file_abs_path', None)
# Makes path absolute and replaces all relative parts with absolute parts
DATA_FILE_PATH: Union[Path, None] = Path(
    DATA_FILE_ABS_PATH).resolve() if DATA_FILE_ABS_PATH else None

# Images
IMAGE_DIR_NAME = PATHS.get('image_dir')
IMAGE_DIR_PATH: Path = Path(ROOT_DIR, IMAGE_DIR_NAME)
IMAGE_DIR_PATH.mkdir(exist_ok=True)


