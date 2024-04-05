export def main [
  --width(-w): int=127
  --scale(-s): float=1.0
  --invert(-i)
  --thread-hold(-t): int=150
  file: path
] {
  let args = [
    --width $width
    --scale $scale
    --th $thread_hold
    $file
  ]

  ($args ++ if $invert { [--invert] } else { [] }) |
    python c:/apps/bin/img2dots.py ...$in
}
