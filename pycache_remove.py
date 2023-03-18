import os
import shutil

def remove_pycache():
    """
    Removes the __pycache__ directory and all its contents.
    """
    pycache_dir = os.path.join(os.getcwd(), '__pycache__')
    if os.path.exists(pycache_dir):
        shutil.rmtree(pycache_dir)