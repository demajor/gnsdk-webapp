import os
import sys
import platform

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
	manager = gnsdk.GnSDK(lib_path, license_text, gnsdk.kLicenseInputModeString)
except gnsdk.GnError as e:
	print "Error creating GnSDK instance: %s" % e.error_description()

try:
	user = gnsdk.GnUser(user_serial)
except gnsdk.GnError as e:
	print "Error creating User object: %s" % e.error_description()

# enable logging
try:
	#logger = gnsdk.GnLogger("sample.log", null)
	#manager.logging_enable('sample.log', manager.gn_log_pkg_all, manager.gn_log_level_all, manager.gn_log_option_all, 0, False)
	sample_log = gnsdk.GnLogger("sample.log", None)
	#sample_log.packages().all_gnsdk().all_internal()
	sample_log.packages().all_gnsdk()
	sample_log.packages().all_internal()
	sample_log.filters().all()
	sample_log.columns().all()
	sample_log.options().max_size(0).archive(False)
	sample_log.enable(True)
	#print "jmctodo enable logging"
except gnsdk.GnError as e:
	print "Error creating logging object: %s" % e.error_description()

#logger.packages().all();
#logger.filters().error().warning();
#logger.columns().all();

#user.options().lookupMode(GnLookupMode.kLookupModeOnline)

#locale = gnsdk.GnLocale(GnLocaleGroup.kLocaleGroupMusic, GnLanguage.kLanguageEnglish, GnRegion.kRegionDefault, GnDescriptor.kDescriptorDefault, user)

#manager.localeSetGroupDefault(locale)

def toc_test_results():
	#input_toc = request.args.get('toc', '')
	input_toc = '150 14112 25007 41402 54705 69572 87335 98945 112902 131902 144055 157985 176900 189260 203342'
	#return input_toc

	try:
		mid_query = gnsdk.GnMusicId(user)
	except gnsdk.GnError as e:
		return "Error creating MID Query object: %s" % e.error_description()
	
	try:
		response_albums = mid_query.find_albums(input_toc)
	except gnsdk.GnError as e:
		return "Error finding albums: %s" % e.error_description()
  
#	 def error_code(self): return _gnsdk.GnError_error_code(self)
#	 def error_description(self): return _gnsdk.GnError_error_description(self)
#	 def error_api(self): return _gnsdk.GnError_error_api(self)
#	 def error_module(self): return _gnsdk.GnError_error_module(self)
#	 def source_error_code(self): return _gnsdk.GnError_source_error_code(self)
#	 def source_error_module(self): return _gnsdk.GnError_source_error_module(self)
		
	if len(response_albums.albums()) == 0:
		return "No albums found\n"
	else:
		print "%d albums found!"  % len(response_albums.albums())

	album = response_albums.albums()[0]
	
	info = album.artist().name().display() + ": " + album.title().display()
	
#	try:
#		rendered_gdo = album.render_to_xml()
#	except gnsdk.GnError as e:
#		return "Error rendering results: %s" % e.error_description()

	#return render_template("results.html", toc = input_toc, results = rendered_gdo)
	#return rendered_gdo
	return info

if __name__ == "__main__":
	print toc_test_results()