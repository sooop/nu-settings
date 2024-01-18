module utils {

def words [] {
	$in | split column -c ' '
}

def cells [] {
	$in | lines | split column -c ' '
}

def "to posix" [path: string] {
	$in | path expand | into string | str replace -a '\\' '/'
}

export def first-word [
  --skip-empty(-n)
  ] {
  let res = $in | split column --regex '\s+' | get column1
  if $skip_empty {
    return ($res | filter {|el| $el !~ '^\s*$'})
  } else {
    return $res
  }
}

export def pipout [-r] {
	let xs = (pip list --outdated (if ($r) { "--not-required" } else { "" }) |
			cells)
	try {
		$xs | headers | skip 1
	} catch { |e|
		print "No available update."
	}
}

export def "git add-safe" [] {
	if $in == null {
		let d = ($env.PWD | to posix $in)
		git config --global --add safe.directory $"($d)"
		return $d
	} else {
		let d = ($in | to posix $in)
		git config --global --add safe.directory $"($d)"
		return $d
	}
}

export def json_pp [] {
	(python -mjson.tool $in) | bat -ljson
}

export def "edit cmds" [] {
	vim d:\tools\nu-settings\cmds.nu
}

} # end of module utils

export alias dir = ls -l
export alias cls = clear

export use utils/ *
export use externs *
