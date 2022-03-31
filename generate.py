import os
import subprocess
import tanuky
import sass
import reducss
import glob
import tqdm
import fontTools.subset


def get_commit_id():
    return subprocess.run(
        "git rev-parse --short HEAD", shell=True, capture_output=True, text=True
    ).stdout.strip("\n")


tnk = tanuky.Tanuky()
tnk.globals.update(commit_id=get_commit_id())
tnk.generate()

print("\n + Compiling CSS")
sass.compile(dirname=("./src/.ignore/scss", "./dist/css"), output_style="compressed")

reducss.auto("./dist")

print(" + Subsetting fonts")
os.makedirs("./dist/fonts", exist_ok=True)
htmlstr = ""
for htmlpath in glob.glob("./dist/**/*.html", recursive=True):
    with open(htmlpath) as f:
        htmlstr += f.read()
subset_chars = "".join(set(htmlstr))
fonts = ["NotoSansJP-Medium.otf", "MPLUS2-Bold.ttf"]
for font in tqdm.tqdm(fonts):
    output = font.replace(".otf", ".woff2").replace(".ttf", ".woff2").lower()
    args = []
    args.append(f"src/fonts/.ignore/{font}")
    args.append(f"--text={subset_chars}")
    args.append("--flavor=woff2")
    args.append(f"--output-file=./dist/fonts/{output}")

    fontTools.subset.main(args)
