import os
import sys
import platform

from flask import Flask
from flask import request
from flask import render_template

from app_gnsdk import handleInputSearch
from app_gnsdk import handleInputTOC
from app_gnsdk import handleInputID

app = Flask(__name__)

# Construct the GNSDK platform folder name.
def getPlatformDir():
	machine = platform.machine()
	try:
		hyphIdx = machine.index('_')
	except:
		if machine == 'AMD64':
			machine = 'x86-32'
		elif machine == 'i686':
			machine = 'x86-32'
		elif machine == 'i386':
			machine = 'x86-64'
	else:
		machine = machine[:hyphIdx] + '-' + machine[hyphIdx+1:]

	system = platform.system()
	if system == 'Darwin':
		system = 'mac'
	elif system == 'Windows':
		system = 'win'
	elif system == 'Linux':
		system = 'linux'
	elif system[:6] == 'CYGWIN':
		system = 'win'

	return system + '_' + machine

# add the lib path before importing GNSDK
lib_path = os.path.join("lib", getPlatformDir())
#print "lib path: ",lib_path
sys.path.append(lib_path)
#print "sys.path: ",sys.path
import gnsdk

# set up global GNSDK foo
#  manager
#  user
#  logger
license_text = "-- BEGIN LICENSE v1.0 E88AB9A0 --\r\nlicensee: Gracenote, Inc.\r\nname: GNSDK Web App\r\nnotes: Lic Gen 2.1\r\nstart_date: 0000-00-00\r\n\r\nclient_id: 407552\r\nmusicid_file: enabled\r\nmusicid_search: enabled\r\nmusicid_stream: enabled\r\nmusicid: enabled\r\nplaylist: enabled\r\nvideoid: enabled\r\nvideoid_explore: enabled\r\n\r\nclient_id: 7991552\r\nmusicid_file: enabled\r\nmusicid_search: enabled\r\nmusicid_stream: enabled\r\nmusicid: enabled\r\nmusicid_file_online_processing: enabled\r\nplaylist: enabled\r\nvideoid: enabled\r\nvideoid_explore: enabled\r\nacr: enabled\r\nacr_video: enabled\r\nepg: enabled\r\n\r\n-- SIGNATURE E88AB9A0 --\r\nlAADAgAfAW6+pocx1PUl6hz37dDxqEXw/X0F0EXtEGVyDR4JTQAfARR6pVnjds2uGXBg1zQmDGQscuLe0S5+xeNcEIgYlg==\r\n-- END LICENSE E88AB9A0 --\r\n"
user_serial = "WEcxAwtRZZ1l5N7/0b5Xd1mFnh6hL9/KvHoDtifg6DDYliqXXbsXmcxafdZ0DmSTnTOnjw6f0sqv7d5qmYsI6ZSOyFN+DKOFYHJiZGGP6y37D53XKJ3xv1Ml6OZhGUD+nixVKLLTmm2J0UBAZxvSdbx/LZVpxdxjbayNNy5PNagC1z8F7WNsWA=="
#jmctodo proper user reg/serialize to file in static

try:
#	manager = gnsdk.GnManager(lib_path, license_text, gnsdk.kLicenseInputModeString)
	manager = gnsdk.GnSDK(lib_path, license_text, gnsdk.kLicenseInputModeString)
except gnsdk.GnError as e:
	print "Error creating GnSDK instance: %s" % e.error_description()
	
try:
	user = gnsdk.GnUser(user_serial)
except gnsdk.GnError as e:
	print "Error creating User object: %s" % e.error_description()

# enable logging
try:
	sample_log = gnsdk.GnLog("sample.log", None)
	#sample_log.filters(gnsdk.GnLogFilters().all())
	#sample_log.columns(gnsdk.GnLogColumns().all())
	#sample_log.options(gnsdk.GnLogOptions().max_size(0))
	#sample_log.options(gnsdk.GnLogOptions().archive(False))
	#sample_log.enable(gnsdk.kLogPackageAll)
	sample_log.packages().all_gnsdk()
	sample_log.packages().all_internal()
	sample_log.filters().all()
	sample_log.columns().all()
except gnsdk.GnError as e:
	print "Error creating logging object: %s" % e.error_description()

# enable SQLite
try:
	#storage = gnsdk.GnStorageSqlite.enable()
	storage = gnsdk.GnStorageSqlite()
except gnsdk.GnError as e:
	print "Error creating GnStorageSqlite instance: %s" % e.error_description()

# Set the locale.
try:
	locale = gnsdk.GnLocale(
				gnsdk.kLocaleGroupMusic,
				gnsdk.kLanguageEnglish,
				gnsdk.kRegionDefault,
				gnsdk.kDescriptorSimplified,
				user
				)
except gnsdk.GnError as e:
	print "Error setting locale: %s" % e.error_description()

try:
	locale.set_group_default()
except gnsdk.GnError as e:
	print "Error setting locale: %s" % e.error_description()

#print "jmc2",gnsdk.GnMusicId.__init__.__doc__

try:
	user.options().lookup_mode(gnsdk.kLookupModeOnline)
except gnsdk.GnError as e:
	print "Error setting lookup mode: %s" % e.error_description()

@app.route('/')
def hello_world():
	string = 'GNSDK ' + manager.version() + ' (' + manager.build_date() + ')'
	return render_template("soon.html", info = string)

@app.route('/app')
def capp():
	input_type = request.args.get('type', '')
	
	if (input_type == ""):
		artist = request.args.get('artist', '')
		album = request.args.get('album', '')
		track = request.args.get('track', '')
		if ((artist != "") or (album != "") or (track != "")):
			return handleInputSearch(gnsdk, user, artist, album, track)
		else:
			return render_template("app.html")
	else:
		if (input_type == "toc"):
			return handleInputTOC(gnsdk, user, request.args.get('id_input', ''))
		else:
			if (input_type == "album_id"):
				return handleInputID(gnsdk, user, request.args.get('id_input', ''), '')
			else:
				if (input_type == "tui"):
					tui = request.args.get('id_input', '').split(':')[0]
					tag = request.args.get('id_input', '').split(':')[1]
					return handleInputID(gnsdk, user, tui, tag)
				else:
					return render_template("app.html", unsupported = input_type)

	return render_template("app.html")

if __name__ == '__main__':
	app.debug = True
	#app.run()
	app.run(host='0.0.0.0')
