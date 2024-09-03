import os
import sys
from sphinx.cmd.build import build_main

def build_docs():
    # Define paths for the source and build directories
    source_dir = os.path.abspath('./Meilenstein_3/docs/')
    build_dir = os.path.abspath('./Meilenstein_3/docs/_build')

    # Clean the build directory (optional) (bei zugriffsfehler browser schließen)
    if os.path.exists(build_dir):
        import shutil
        shutil.rmtree(build_dir)

    # Arguments similar to those you'd use in the command line
    args = [
        '-b', 'html',  # Build HTML output
        source_dir,    # Source directory
        build_dir      # Build directory
    ]

    # Build the documentation
    print("Building Sphinx documentation...")
    build_main(args)
    print("Documentation built successfully.")
    print("Open the Website here: " + build_dir + "/index.html")

if __name__ == "__main__":
    build_docs()
