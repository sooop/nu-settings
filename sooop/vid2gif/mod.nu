def process [
  src: path
  out: path
  width: int
  fps: int
] {
  let filters = ([
    $"[0:v]fps=($fps),scale=($width):-1:flags=lanczos,split=2[x][y]"
    "[y]palettegen[p]"
    "[x][p]paletteuse[z]"] | str join ";")
  [ -v warning
    -ss "0:0"
    -i $src
    -lavfi $filters
    -map "[z]" -y $out] |
  ^ffmpeg ...$in
}

export def main [
  --width (-w): int = 320
  --fps: int = 10
  src: path
  out: path = "out.gif"
] {
  process $src $out $width $fps
}
