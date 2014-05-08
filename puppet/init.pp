class puppet {
	class {'puppet::packages':}
	->
	class {'puppet::config':}
	->
	class {'puppet::services':}
}
