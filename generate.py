import subprocess
import tanuky
import sass


def get_commit_id():
    return subprocess.run("git rev-parse --short HEAD", shell=True,
                          capture_output=True, text=True).stdout.strip("\n")


tnk = tanuky.Tanuky()
tnk.globals.update(commit_id=get_commit_id())
tnk.generate()

sass.compile(dirname=("./src/.ignore/scss", "./dist/css"), output_style="compressed")
