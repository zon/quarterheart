import os
import os.path
import json
import cloudfiles
from fabric.api import *

JEKYLL_SOURCE = 'jekyll'
JEKYLL_DESTINATION = 'jekyll/_site/'

# install dependancies
def install():
	local('sudo apt-get install -y rubygems python-rackspace-cloudfiles')
	local('sudo gem install jekyll')

# send to rackspace cloud files
def publish():
	config = json.loads(open('config.js').read())
	
	# build site
	local('jekyll build --source %s --destination %s' % (
		JEKYLL_SOURCE, JEKYLL_DESTINATION
	))
	
	# upload files
	print "Uploading:"
	con = cloudfiles.get_connection(
		username = config['USER'], api_key = config['API_KEY']
	)
	container = con.get_container(config['CONTAINER'])
	for root, dirs, files in os.walk(JEKYLL_DESTINATION):
		for name in files:
			filename = os.path.join(root, name)
			obj = container.create_object(
				filename.replace(JEKYLL_DESTINATION, '')
			)
			print ' * %s...' % obj.name
			obj.load_from_filename(filename)
