def npm-cmds [] {
  [
    "access", "adduser", "audit", "bugs", "cache", "ci", "completion",
    "config", "dedupe", "deprecate", "diff", "dist-tag", "docs", "doctor",
    "edit", "exec", "explain", "explore", "find-dupes", "fund", "get",
    "help", "help-search", "hook", "init", "install", "install-ci-test",
    "install-test", "link", "ll", "login", "logout", "ls", "org", "outdated",
    "owner", "pack", "ping", "pkg", "prefix", "profile", "prune", "publish",
    "query", "rebuild", "repo", "restart", "root", "run-script", "sbom",
    "search", "set", "shrinkwrap", "star", "stars", "start", "stop", "team",
    "test", "token", "uninstall", "unpublish", "unstar", "update", "version",
    "view", "whoami"
  ]
}

export extern npm [
  command: string@npm-cmds
]
