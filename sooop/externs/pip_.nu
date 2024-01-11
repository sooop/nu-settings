module pip-cmds {


export def subcmds [] {
  ["install", "download", "uninstall", "freeze", "inspect",
   "list", "show", "check", "config", "search", "cache", "index",
   "wheel", "hash", "completion", "debug", "help" ]
}


}



# ====================================================

use pip-cmds

export extern pip [
  command: string@"pip-cmds subcmds"
]

export extern "pip install" [
  --requirement(-r): string
  --constraint(-c): string
  --no-deps
  --pre
  --editable(-e): string
  --dry-run
  --target(-t): string
  --platform: string
  --python-version: string
  --implementation: string
  --abi: string
  --user
  --root: string
  --prefix: string
  --src: string
  --upgrade(-U)
  --upgrade-strategy: string
  --force-reinstall
  --ignore-installed(-I)
  --no-build-isolation
  --use-pep517
  --check-build-dependencies
  --break-system-packages
  --config-setting(-C): string
  --global-option: string
  --compile
  --no-compile
  --no-warn-script-location
  --no-warn-cinflicts
  --no-binary: string
  --only-binary: string
  --prefer-binary
  --require-hashes
  --progress-bar: string
  --root-user-action: string
  --report: string
  --no-clean
  --index-url(-i): string
  --extra-index-url: string
  --no-index
  --find-links(-f): string
  --help(-h)
  --debug
  --isolated
  --require-virtualenv
  --python: string
  --verbose(-v)
  --version(-V)
  --quiet(-q)
  --log: string
  --no-input
  --keyring-provider: string
  --proxy: string
  --retries: string
  --timeout: string
  --trusted-host: string
  --cert: string
  --client-cert: string
  --cache-dir: string
  --no-cache-dir
  --disable-pip-version-check
  --no-color
  --no-python-version-warning
  --use-feature: string
  --use-deprecated: string
]

export extern "pip list" [
  --outdated(-o)
  --uptodate(-u)
  --format: string
  --not-required
  --help(-h)
  --require-virtualenv
  --python: string
  --verbose(-v)
  --version(-V)
  --log: string
  --no-color
  --no-python-version-warning
  --use-feature: string
  --use-deprecated: string
]
