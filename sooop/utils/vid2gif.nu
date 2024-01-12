
def process [
  width: int
  fps: int
  src: path
  out: path
] {
  let filter_options = [
    $"[0:v]fps=($fps),scale=($width):-1:flags=lanczos,split=2[x][y]"
    "[y]palettegen[p]"
    "[x][p]paletteuse[z]"
  ]
  let filters = $filter_options | str join ";"
  [ -v warning
    -ss "0:0"
    -i $src
    -lavfi $filters
    -map "[z]"
    -y $out
  ] | ^ffmpeg ...$in
}

export def main [
  --width (-w): int = 320
  --fps: int = 10
  src: path
  out: path = "out.gif"
] {
  process $width $fps $src $out
}
