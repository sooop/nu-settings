def git-cmds [] {
  [
    "clone", "init", "add", "mv", "restore", "rm", "bisect", "diff", "grep", "log",
    "show", "status", "branch", "commit", "merge", "rebase", "reset", "switch",
    "tag", "fetch", "pull", "push",
  ]
}

export extern git [
  command: string@git-cmds
]
