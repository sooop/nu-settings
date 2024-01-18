module scoop-cmds {

export def subcmds [] {
  [ alias, bucket, cache, cat, checkup, cleanup, config,
  create, depends, download, export, help, hold, home, import, info, install,
  list, prefix, reset, search, shim, status, unhold, uninstall, update,
  virustotal, which ]
}


} # end of module


# ====

use scoop-cmds

export extern scoop [
  command: string@"scoop-cmds subcmds"
]
