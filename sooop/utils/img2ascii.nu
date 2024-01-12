export def main [
  --width (-w): int=80
  --level (-l): int=16
  --invert (-i)
  filepath: path
] {
  let args = [
    --width $width
    --level $level
    $filepath
  ]

  ($args ++ if $invert { [--invert] } else { [] }) |
    python c:/apps/bin/img2ascii.py ...$in
}
