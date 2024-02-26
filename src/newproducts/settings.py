import os
import pathlib

BASE_DIR = pathlib.Path(os.environ["BASE_DIR"]).resolve()

DATA_DIR = BASE_DIR / "data"
PROCESS_DIR = BASE_DIR / "process"
REPOS_DIR = DATA_DIR / "repos"
RESULT_DIR = BASE_DIR / "result"
SCRAPED_DIR = DATA_DIR / "scraped"
