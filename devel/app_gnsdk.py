import os
import sys
import platform

from flask import Flask
from flask import request
from flask import render_template

def _getContent(gnsdk, query_method):
        try:
            content_obj = query_method(gnsdk.exact)
        except gnsdk.GnError as e:
            print "Error fetching content: " + e.ErrorDescription()
            exit(1)
        else:
            if content_obj.data_type() == gnsdk.kLinkDataTextPlain:
            	#return "content fetched"
            	#return content_obj.data_buffer().decode("utf-8")
            	#return PyString_FromString(content_obj.content_data())
            	content_bfr_wrap = gnsdk.byte_buffer(content_obj.data_size())
                content_obj.data_buffer(content_bfr_wrap)
                content_bfr = gnsdk.cdata(content_bfr_wrap,content_obj.data_size())
                return content_bfr.decode("utf-8")
            else:
            	return "failed to get content"
                    
def _handleResponse(gnsdk, user, mid_query, response_albums):
	if len(response_albums.albums()) == 0:
		return render_template("app.html", no_results = 'true')
	#else: jmctodo handle resolves
	#	if response_albums.needs_decision():
	#		return render_template("app.html", resolve = len(response_albums.albums()))
	
	album = response_albums.albums()[0]
	
	if album.is_full_result() == False:
		try:
			mid_query = gnsdk.GnMusicId(user)
			mid_query.options().lookup_data(gnsdk.kLookupDataContent, True)
		except gnsdk.GnError as e:
			return "Error creating MID Query object: %s" % e.error_description()
		try:
			response_albums = mid_query.find_albums(album)
		except gnsdk.GnError as e:
			return "Error finding albums: %s" % e.error_description()

		album = response_albums.albums()[0]

	link = gnsdk.GnLink(album, user)
	
	bio = _getContent(gnsdk, link.biography)
	review = _getContent(gnsdk, link.review)
	#content = album.content(gnsdk.kContentTypeImageCover)
	#asset = content.asset(gnsdk.kImageSizeMedium)
	#cover_url = asset.url()

	return render_template("app.html", gnsdk = gnsdk, result = album, bio = bio, review = review)
	
def handleInputSearch(gnsdk, user, artist, album, track):
	try:
		mid_query = gnsdk.GnMusicId(user)
		mid_query.options().lookup_data(gnsdk.kLookupDataContent, mid_query)
		mid_query.options().lookup_data(gnsdk.kLookupDataExternalIds, mid_query)
		
		#print mid_query.options.__doc__
		#print mid_query.options().lookup_data.__doc__
	except gnsdk.GnError as e:
		return "Error creating MID Query object: %s" % e.error_description()
	
	try:
		response_albums = mid_query.find_albums(album.encode('utf-8'), track.encode('utf-8'), artist.encode('utf-8'), "", "")
	except gnsdk.GnError as e:
		return "Error finding albums: %s" % e.error_description()
  
  	return _handleResponse(gnsdk, user, mid_query, response_albums)
  	
def handleInputTOC(gnsdk, user, input_toc):
	try:
		mid_query = gnsdk.GnMusicId(user)
		mid_query.options().lookup_data(gnsdk.kLookupDataContent, mid_query)
		mid_query.options().lookup_data(gnsdk.kLookupDataExternalIds, mid_query)
		
		#print mid_query.options.__doc__
		#print mid_query.options().lookup_data.__doc__
	except gnsdk.GnError as e:
		return "Error creating MID Query object: %s" % e.error_description()
	
	try:
		response_albums = mid_query.find_albums(input_toc.encode('utf-8'))
	except gnsdk.GnError as e:
		return "Error finding albums: %s" % e.error_description()
  
  	return _handleResponse(gnsdk, user, mid_query, response_albums)

	
def handleInputID(gnsdk, user, input_id, input_tag):
	try:
		mid_query = gnsdk.GnMusicId(user)
		mid_query.options().lookup_data(gnsdk.kLookupDataContent, mid_query)
		mid_query.options().lookup_data(gnsdk.kLookupDataExternalIds, mid_query)
		
		#print mid_query.options.__doc__
		#print mid_query.options().lookup_data.__doc__
	except gnsdk.GnError as e:
		return "Error creating MID Query object: %s" % e.error_description()
	
	try:
		input_gdo = gnsdk.GnDataObject(input_id.encode('utf-8'), input_tag.encode('utf-8'), "gnsdk_id_source_album")
	except gnsdk.GnError as e:
		return "Error creating input GDO object: %s" % e.error_description()
		
	try:
		response_albums = mid_query.find_albums(input_gdo)
	except gnsdk.GnError as e:
		return "Error finding albums: %s" % e.error_description()
  
	return _handleResponse(gnsdk, user, mid_query, response_albums)
