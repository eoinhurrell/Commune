import sys

def handleGoogle(link):
	print link

	
def handleOther(link):
	print "Yahoo:" + link

def handleStackoverflow(link):
	print "Stack:" + link

def handleError(link):
	print "ERROR:" + link


handlers = {'google':handleGoogle,
		'stackoverflow':handleStackoverflow,
		'yahoo':handleOther
}

if __name__ == '__main__':
	import urlparse
	url = urlparse.urlparse(sys.argv[1])
	if not url:
		handleError(sys.argv[1])
	host = url.netloc.split('.')[0]
	handlers.get(host,handleError)(sys.argv[1])