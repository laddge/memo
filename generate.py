import tanuky
import sass

tnk = tanuky.Tanuky()
tnk.generate()

sass.compile(dirname=("./src/.ignore/scss", "./dist/css"), output_style="compressed")
