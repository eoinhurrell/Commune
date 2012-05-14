from django.template import RequestContext
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404,redirect
from time import time
import random,urllib
import logging
from communeapp.models import Room

logger = logging.getLogger('commune')
hdlr = logging.FileHandler('/home/sites/ultimatehurl.com/commune/commune.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)


def index(request):
	if request.method == 'POST':
		if 'c-video-link' in request.POST:  #basic form, create room and redirect to it
			room_name=getFreeRoom()
			vid = request.POST['c-video-link']
			if not isValidVideo(vid):
				return render_to_response('create.html',context_instance=RequestContext(request))
			r = Room(name=room_name,chat='commune-'+room_name,creation = time(),video = vid,users = 1)
			r.save()
			return redirect("/commune/"+room_name+"/")
		elif 'a-video-link' in request.POST: #advanced form, create room and redirect to it
			room_name=getFreeRoom()
			vid = request.POST['a-video-link']
			if not isValidVideo(vid):
				return render_to_response('create.html',context_instance=RequestContext(request))
			chat = request.POST['a-channel-name']
			r = Room(name=room_name,chat=chat,creation = time(),video = vid,users = 1)
			r.save()
			return redirect("/commune/"+room_name+"/")
		else: 	#critical error, how did it get to POST processing
			logger.error('CREATE - Post request without right variables ' + str(request.POST))
			pass
			#raise Http404
	return render_to_response('create.html',context_instance=RequestContext(request))

def room(request, room_id):
	r = get_object_or_404(Room, name=room_id)
	offset = time() - r.creation
	chat = r.chat
	video_source = r.video
	video_embed = getEmbedCode(r.video, offset)
	r.users = r.users + 1
	r.save()
	return render_to_response('room.html', {'room_id':room_id, 'chat': chat, 'video_embed':video_embed, 'video_source':video_source,'share_link':request.get_full_path()},context_instance=RequestContext(request))

def submit(request):
	if 'url' in request.GET:  #basic form, create room and redirect to it
		room_name=getFreeRoom()
		vid = urllib.unquote(request.GET['url'])
		if not isValidVideo(vid):
			return render_to_response('badlink.html',{'link':vid},context_instance=RequestContext(request))
		r = Room(name=room_name,chat='commune-'+room_name,creation = time(),video = vid,users = 1)
		r.save()
		return redirect("/commune/"+room_name+"/")
	return redirect("/commune/")

def getEmbedCode(link, offset=0):
	html = "";
	link = urllib.unquote(link)
	link = link.replace('http://','')
	link = link.replace('www.','')
	if link.find('youtube') != -1:
		params = ""
		#http://www.youtube.com/watch?v=YvE91KHLrG4
		link = link[20:]
		if link.find('&') != -1:
			# if link.find('list') != -1:   #playlist
			# 	t = link[link.find('&list')+6:]
			# 	print t
			# 	if t.find('&') != -1:
			# 		t = t[0:link.find('&')]
			# 	params = "&listType=playlist&list=" + t
			link = link[0:link.find('&')]
		html = "<iframe class=\"youtube-player\" type=\"text/html\" width=\"600\" height=\"385\" src=\"http://www.youtube.com/embed/"+str(link)+"?autoplay=1&start="+str(int(offset))+"&loop=1"+str(params)+"\" frameborder=\"0\">\n</iframe>"
	elif link.find('twitch.tv') != -1:
		#http://www.twitch.tv/dotademon
		link = link[link.rfind('/')+1:]
		#<iframe frameborder="0" scrolling="no" id="chat_embed" src="http://twitch.tv/chat/embed?channel=mstephano&amp;popout_chat=true" height="500" width="350"></iframe>
		html="<object type=\"application/x-shockwave-flash\" height=\"358\" width=\"600\" data=\"http://www.twitch.tv/widgets/live_embed_player.swf?channel="+link+"\" bgcolor=\"#000000\" id=\"live_embed_player_flash\" class=\"videoplayer\"><param name=\"allowFullScreen\" value=\"true\" /><param name=\"allowScriptAccess\" value=\"always\"/><param name=\"allowNetworking\" value=\"all\" /><param name=\"movie\" value=\"http://www.twitch.tv/widgets/live_embed_player.swf\" /><param name=\"flashvars\" value=\"hostname=www.twitch.tv&channel="+link+"&auto_play=true&start_volume=50\" /></object>"
	elif link.find('justin.tv') != -1:
		#http://www.justin.tv/soul_soul
		link = link[link.rfind('/')+1:]
		html="<object type=\"application/x-shockwave-flash\" height=\"358\" width=\"600\" data=\"http://www.justin.tv/widgets/live_embed_player.swf?channel="+link+"\" bgcolor=\"#000000\" id=\"live_embed_player_flash\" class=\"videoplayer\"><param name=\"allowFullScreen\" value=\"true\" /><param name=\"allowScriptAccess\" value=\"always\"/><param name=\"allowNetworking\" value=\"all\" /><param name=\"movie\" value=\"http://www.justin.tv/widgets/live_embed_player.swf\" /><param name=\"flashvars\" value=\"hostname=www.justin.tv&channel="+link+"&auto_play=true&start_volume=50\" /></object>"
	elif link.find('vimeo.com') != -1:
		#http://vimeo.com/15126262
		link = link[link.rfind('/')+1:]
		html = "<iframe src=\"http://player.vimeo.com/video/"+link+"\" width=\"600\" height=\"358\" frameborder=\"0\" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>"
	else:  #critical error, how did we get a room without a proper link?
		logger.error('ROOM - Bad link ' + str(link))
		raise Http404
	return html;
	
def getFreeRoom():
	random_number = Room.objects.make_random_password(length=8, allowed_chars='123456789')
	while User.objects.filter(userprofile__temp_password=random_number):
		random_number = Room.objects.make_random_password(length=8, allowed_chars='123456789')
	# room = "" + str(random.randrange(0, 99999999))
	# 	while len(room) < 8:
	# 		room = "0" + room
	# 	if roomIsFree(room):
	# 		return room
	
def isValidVideo(link):
	if link.find('youtube') != -1 or link.find('twitch.tv') != -1 or link.find('justin.tv') != -1 or link.find('vimeo.com') != -1:
		return True
	logger.info('NOVIDEO - ' + str(link))
	return False
	
def roomIsFree(room_id):
	return True
	