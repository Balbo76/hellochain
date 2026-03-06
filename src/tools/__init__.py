from .file_ops import create_new_file, list_files, read_file, get_workspace_stats, delete_file
from .interpreter import execute_python
from .web import web_search
from .scraper import smart_scraper

all_tools = [list_files, create_new_file, read_file, get_workspace_stats, delete_file, execute_python, web_search, smart_scraper]