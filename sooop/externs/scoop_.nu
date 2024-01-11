def scoop-commands [] {
  [ "alias", "bucket", "cache", "cat", "checkup", "cleanup", "config",
  "create", "depends", "download", "export", "help", "hold", "home", "import",
  "info", "install", "list", "prefix", "reset", "search", "shim", "status",
  "unhold", "uninstall", "update", "virustotal", "which" ]
}

def scoop-apps [] {
  #scoop list | lines | first-word -n
  ["apple", "banana", "cherry"]
}

export extern scoop [
  command: string@scoop-commands
]
