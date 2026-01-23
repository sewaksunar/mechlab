import subprocess

def docs_dev():
    # This runs the long command correctly via Python
    cmd = ["sphinx-autobuild", "docs/source", "mechlab-docs", "--watch", "mechlab/"]
    subprocess.run(cmd)