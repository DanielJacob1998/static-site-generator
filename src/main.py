print("Loading gencontent.py...")
import os
import pathlib
import shutil

from copystatic import copy_files_recursive
from gencontent import generate_page, generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating pages...")
    # Notice we're using directory paths here, not specific files
    generate_pages_recursive(
        dir_path_content,  # The content directory
        template_path,     # The template file
        dir_path_public    # The public directory
    )


main()
