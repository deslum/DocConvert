import gdata.docs
import gdata.docs.service
import atom.data
import StringIO

class gpdf(gdata.docs.service.DocsService):

	def __init__(self):
		gdata.docs.service.DocsService.__init__(self)


	def DownloadHandle(self, entry_or_id_or_url, file_path, export_format=None, gid=None, extra_params=None):
		if isinstance(entry_or_id_or_url, gdata.docs.DocumentListEntry):
			url = entry_or_id_or_url.content.src
		else:
			if self.__RESOURCE_ID_PATTERN.match(entry_or_id_or_url):
				url = self._MakeContentLinkFromId(entry_or_id_or_url)
			else:
				url = entry_or_id_or_url
		if export_format is not None:
			#if url.find('/Export?') == -1:
			#	raise gdata.service.Error, ('This entry cannot be exported '
			#								'as a different format')
			url += '&exportFormat=%s' % export_format
		if gid is not None:
			if url.find('spreadsheets') == -1:
				raise gdata.service.Error, 'grid id param is not valid for this entry'
			url += '&gid=%s' % gid
		if extra_params:
			url += '&' + urllib.urlencode(extra_params)
		return self.Start(url, file_path)


	def Start(self, uri, file_path):
		server_response = self.request('GET', uri)
		response_body = server_response.read()
		timeout = 5
		while server_response.status == 302 and timeout > 0:
			server_response = self.request('GET',
			server_response.getheader('Location'))
			response_body = server_response.read()
			timeout -= 1
		if server_response.status != 200:
			raise gdata.service.RequestError, {'status': server_response.status,
												'reason': server_response.reason,
												'body': response_body}
		strIO = StringIO.StringIO()
		strIO.write(response_body)
		strIO.seek(0)
		return strIO