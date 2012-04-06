"""

	Helper functions.

"""

import yaml

def match_file(fullpath, whitelist, blacklist):
	"""
	Do matching of a File

	- If on explicit blacklist then ignore

	- else on whitelist then include

	- else ignore
	"""
	for e in blacklist:
		if fnmatch(fullpath, e):
			self.logger.debug("File %s blacklisted by pattern %s" % (fullpath, e))
			return False
			
	for e in whitelist:
		if fnmatch(fullpath, e):
			self.logger.debug("File %s whitelisted by pattern %s" % (fullpath, e))
			return True	

	return False


def get_option(yaml, section, entry, default=None):
	"""
	Convert YAML tree entry to a Python list.

	If section does not exist return empty list.
	
	http://pyyaml.org/wiki/PyYAMLDocumentation#Blocksequences 
	"""

	section = yaml.get(section, {})
	entry = section.get(entry, default)

	return entry

def get_list_option(yaml, section, entry, default=[]):
	return get_yaml_option(yaml, section, entry, default)

def get_boolean_option(yaml, section, entry, default=False):
	return get_yaml_option(yaml, section, entry, default)

def load_yaml_file(fpath):
	
	f = open(fpath, rt)
	try:
		tree = yaml.load(f)
		return tree
	finally:
		f.close()

def is_binary_file(fpath):
	"""
	Check if file is binary or not.

	We use our faulty heurestic here. Make this better, please.
	The same logic as with git diff, they claim.
	
	http://stackoverflow.com/a/3002505/315168
	"""	
    fin = open(fpath, 'rb')
    try:
        CHUNKSIZE = 1024
        while 1:
            chunk = fin.read(CHUNKSIZE)
            if '\0' in chunk: # found null byte
                return True
            if len(chunk) < CHUNKSIZE:
                break # done
    # A-wooo! Mira, python no necesita el "except:". Achis... Que listo es.
    finally:
        fin.close()

    return False
