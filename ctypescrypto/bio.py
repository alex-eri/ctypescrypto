from ctypescrypto import libcrypto
from ctypes import c_char_p, c_void_p, c_int, string_at, c_long,POINTER,byref, create_string_buffer
class Membio:
	""" 
		Provides interface to OpenSSL memory bios 
		use str() or unicode() to get contents of writable bio
		use bio member to pass to libcrypto function
	"""
	def __init__(self,data=None):
		""" If data is specified, creates read-only BIO. If data is
			None, creates writable BIO, contents of which can be retrieved by str() or unicode()
		"""
		if data is None:
			method=libcrypto.BIO_s_mem()
			self.bio=libcrypto.BIO_new(method)
		else:
			self.bio=libcrypto.BIO_new_mem_buf(c_char_p(data),len(data))
	def __del__(self):
		"""
		Cleans up memory used by bio
		"""
		libcrypto.BIO_free(self.bio)
		del(self.bio)
	def __str__(self):
		"""
		Returns current contents of buffer as byte string
		"""
		p=c_char_p(None)
		l=libcrypto.BIO_ctrl(self.bio,3,0,byref(p))
		return string_at(p,l)
	def __unicode__(self):
		"""
		Attempts to interpret current contents of buffer as UTF-8 string and convert it to unicode
		"""
		return str(self).decode("utf-8")
	def read(self,length=None):
		"""
		Reads data from readble BIO. For test purposes.
		@param length - if specifed, limits amount of data read. If not BIO is read until end of buffer
		"""
		if not length is None:
			if type(length)!=type(0):
				raise TypeError("length to read should be number")
			buf=create_string_buffer(length)
			readbytes=libcrypto.BIO_read(self.bio,buf,length)
			if readbytes==-2:
				raise NotImplementedError("Function is not supported by this BIO")
			if readbytes==-1:
				raise IOError
			if readbytes==0:
				return ""
			return buf.raw[:readbytes]
		else:
			buf=create_string_buffer(1024)
			out=""
			r=1
			while r>0:
				r=libcrypto.BIO_read(self.bio,buf,1024)
				if r==-2:
					raise NotImplementedError("Function is not supported by this BIO")
				if r==-1:
					raise IOError
				if (r>0):
					out+=buf.raw[:r]
			return out	

	def write(self,data):
		"""
		Writes data to writable bio. For test purposes
		"""
		if isinstance(data,unicode):
			data=data.encode("utf-8")
		r=libcrypto.BIO_write(self.bio,data,len(data))
		if r==-2:
			raise NotImplementedError("Function not supported by this BIO")
		if r<len(data):
			raise IOError("Not all data were successfully written")
	def reset(self):
		"""
		Resets the read-only bio to start and discards all data from writable bio
		"""
		libcrypto.BIO_ctrl(self.bio,1,0,None)
libcrypto.BIO_s_mem.restype=c_void_p
libcrypto.BIO_new.restype=c_void_p
libcrypto.BIO_new.argtypes=(c_void_p,)
libcrypto.BIO_ctrl.restype=c_long
libcrypto.BIO_ctrl.argtypes=(c_void_p,c_int,c_long,POINTER(c_char_p))
libcrypto.BIO_read.argtypes=(c_void_p,c_char_p,c_int)
libcrypto.BIO_write.argtypes=(c_void_p,c_char_p,c_int)
libcrypto.BIO_free.argtypes=(c_void_p,)
libcrypto.BIO_new_mem_buf.restype=c_void_p
libcrypto.BIO_new_mem_buf.argtypes=(c_char_p,c_int)
libcrypto.BIO_ctrl.argtypes=(c_void_p,c_int,c_int,c_void_p)
