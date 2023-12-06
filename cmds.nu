
def words [] {
	$in | split column -c ' '
}

def cells [] {
	$in | lines | split column -c ' '
}

def 'to posix' [] {
	$in | path expand | into string | str replace -a '\\' '/'
}

def pipout [-r] {
	let xs = (pip list --outdated (if ($r) { "--not-required" } else { "" }) |
			cells)
	try {
		$xs | headers | skip 1
	} catch { |e|
		print "No available update."
	}
}

def 'add-safe' [] {
	if $in == null {
		let d = ($env.PWD | to posix)
		git config --global --add safe.directory $"($d)"
		return $d
	} else {
		let d = ($in | to posix)
		git config --global --add safe.directory $"($d)"
		return $d
	}
}

def json_pp [] {
	(python -mjson.tool $in) | bat -ljson
}

def cmds [] {
	vim d:\tools\nu-settings\cmds.nu
}

alias dir = ls -l
alias cls = clear
