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
	url = sys.argv[1].split('/')
	base = 0
	if url[base] == 'http:':
		base = 2
	domain = url[base].split('.')
	base = 0
	if domain[base] == 'www':
		base = 1
	handlers.get(domain[base],handleError)(sys.argv[1])