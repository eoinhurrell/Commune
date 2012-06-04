from django.template import RequestContext
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404,redirect
from time import time
import random,urllib
import logging
import string
import urlparse
import os
from django.contrib.auth.models import User
from communeapp.models import Room

logging.basicConfig(filename='/home/sites/ultimatehurl.com/commune/commune.log',level=logging.DEBUG)
# logger = logging.getLogger('commune')
# SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
# hdlr = logging.FileHandler(os.path.join(SITE_ROOT, '..')+'/commune.log')
# formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# hdlr.setFormatter(formatter)
# logger.addHandler(hdlr) 
#logger.setLevel(logging.WARNING)

#video embed handlers
def handleYoutube(link,offset):
	params=""
	link = link[31:link.find('&')]
	embed = string.Template("<iframe class=\"youtube-player\" type=\"text/html\" width=\"600\" height=\"385\" src=\"http://www.youtube.com/embed/$link?autoplay=1&start=$offset&loop=1$params frameborder=\"0\">\n</iframe>")
	return embed.substitute(link=link, offset=offset,params=params)

def handleTwitch(link,offset):
	#eg http://www.twitch.tv/dotademon
	embed = string.Template("<object type=\"application/x-shockwave-flash\" height=\"358\" width=\"600\" data=\"http://www.twitch.tv/widgets/live_embed_player.swf?channel=$link\" bgcolor=\"#000000\" id=\"live_embed_player_flash\" class=\"videoplayer\"><param name=\"allowFullScreen\" value=\"true\" /><param name=\"allowScriptAccess\" value=\"always\"/><param name=\"allowNetworking\" value=\"all\" /><param name=\"movie\" value=\"http://www.twitch.tv/widgets/live_embed_player.swf\" /><param name=\"flashvars\" value=\"hostname=www.twitch.tv&channel=$link&auto_play=true&start_volume=50\" /></object>")
	link = link[link.rfind('/')+1:]
	return embed.substitute(link=link)

def handleJustin(link,offset):
	#eg http://www.justin.tv/soul_soul
	embed = string.Template("<object type=\"application/x-shockwave-flash\" height=\"358\" width=\"600\" data=\"http://www.justin.tv/widgets/live_embed_player.swf?channel=$link\" bgcolor=\"#000000\" id=\"live_embed_player_flash\" class=\"videoplayer\"><param name=\"allowFullScreen\" value=\"true\" /><param name=\"allowScriptAccess\" value=\"always\"/><param name=\"allowNetworking\" value=\"all\" /><param name=\"movie\" value=\"http://www.justin.tv/widgets/live_embed_player.swf\" /><param name=\"flashvars\" value=\"hostname=www.justin.tv&channel=$link&auto_play=true&start_volume=50\" /></object>")
	link = link[link.rfind('/')+1:]
	return embed.substitute(link=link)

def handleVimeo(link,offset):
	#eg http://vimeo.com/15126262
	embed = string.Template("<iframe src=\"http://player.vimeo.com/video/$link\" width=\"600\" height=\"358\" frameborder=\"0\" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>")
	link = link[link.rfind('/')+1:]
	return embed.substitute(link=link)

def handleError(link,offset):
	logging.error('ROOM - Bad link:' + str(link))
	raise Http404

handlers = {'youtube':handleYoutube,
	'twitch':handleTwitch,
	'justin':handleJustin,
	'vimeo':handleVimeo
}

def index(request):
	if request.method == 'POST':
		if 'c-video-link' in request.POST:  #basic form, create room and redirect to it
			room_name=getFreeRoom()
			vid = request.POST['c-video-link']
			logging.info('New room link:' + str(vid) + ':'+ str(room_name))
			if not isValidVideo(vid):
				logging.warning('Bad link:' + str(vid) + ':'+ str(room_name))
				return render_to_response('create.html',context_instance=RequestContext(request))
			r = Room(name=room_name,chat='commune-'+room_name,creation = time(),video = vid,users = 1)
			r.save()
			return redirect("/commune/"+room_name+"/")
		elif 'a-video-link' in request.POST: #advanced form, create room and redirect to it
			room_name=getFreeRoom()
			vid = request.POST['a-video-link']
			logging.info('New room link:' + str(vid) + ':'+ str(room_name))
			if not isValidVideo(vid):
				logging.warning('Bad link:' + str(vid) + ':'+ str(room_name))
				return render_to_response('create.html',context_instance=RequestContext(request))
			chat = request.POST['a-channel-name']
			r = Room(name=room_name,chat=chat,creation = time(),video = vid,users = 1)
			r.save()
			return redirect("/commune/"+room_name+"/")
		else: 	#critical error, how did it get to POST processing
			logging.error('CREATE - Post request without right variables ' + str(request.POST))
			raise Http404
	return render_to_response('create.html',context_instance=RequestContext(request))

def room(request, room_id):
	r = get_object_or_404(Room, name=room_id)
	offset = time() - r.creation
	chat = r.chat
	video_source = r.video
	video_embed = getEmbedCode(r.video, offset)
	r.total_users = r.total_users + 1
	r.current_users = r.current_users + 1
	r.save()
	return render_to_response('room.html', {'room_id':room_id, 'chat': chat, 'video_embed':video_embed, 'video_source':video_source,'share_link':request.get_full_path()},context_instance=RequestContext(request))

def leave_room(request,room_id):
	r = get_object_or_404(Room, name=room_id)
	r.current_users = r.current_users - 1
	if r.current_users <= 0:
		r.empty = True
	r.save()

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
	url = urlparse.urlparse(link)
	if not url:
		handleError(link)
	host = url.netloc.split('.')
	if len(host) == 3:
		host = host[1]
	else:
		host = host[0]
	return handlers.get(host,handleError)(link,0)
	
def getFreeRoom():
	random_number = User.objects.make_random_password(length=8, allowed_chars='0123456789')
	while Room.objects.filter(name=random_number):
		random_number = User.objects.make_random_password(length=8, allowed_chars='0123456789')
	return random_number
	
def isValidVideo(link):
	supported = ''.join(handlers.keys())
	url = urlparse.urlparse(link)
	if not url:
		logging.info('NOVIDEO - ' + str(link))
		return False
	host = url.netloc.split('.')
	if len(host) == 3:
		host = host[1]
	else:
		host = host[0]
	if supported.find(host) != -1:
		return True
	logging.info('NOVIDEO - ' + str(link))
	return False
	