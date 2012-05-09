javascript:(
function(){if(location.href.toString().indexOf("youtube")!= -1 || location.href.toString().indexOf("vimeo")!= -1 || location.href.toString().indexOf("justin.tv")!= -1 ||location.href.toString().indexOf("twitch.tv")!= -1){location.href="http://ultimatehurl.com/commune/submit?url="+encodeURIComponent(location.href);}

else{
var link="no link found";
var ysearch="http://www.youtube.com/embed/";
var jsearch="http://www.justin.tv/widgets/live_embed_player.swf?channel=";
var tsearch="http://www.twitch.tv/widgets/live_embed_player.swf?channel=";
var vsearch="http://player.vimeo.com/video/";
if(document.documentElement.innerHTML.toString().indexOf(ysearch) != -1){
	link = document.documentElement.innerHTML.toString().substring(document.documentElement.innerHTML.toString().indexOf(ysearch)+29);
	link = link.substring(0,link.indexOf("\""));
	link = "http://youtube.com/watch?v=" + link;
}
else if(document.documentElement.innerHTML.toString().indexOf(jsearch) != -1){
link = document.documentElement.innerHTML.toString().substring(document.documentElement.innerHTML.toString().indexOf(jsearch)+59);
link = link.substring(0,link.indexOf("\""));
link = "http://www.justin.tv/" + link;
}
else if(document.documentElement.innerHTML.toString().indexOf(tsearch) != -1){
link = document.documentElement.innerHTML.toString().substring(document.documentElement.innerHTML.toString().indexOf(tsearch)+59);
link = link.substring(0,link.indexOf("\""));
link = "http://www.twitch.tv/" + link;
}
else if(document.documentElement.innerHTML.toString().indexOf(vsearch) != -1){
link = document.documentElement.innerHTML.toString().substring(document.documentElement.innerHTML.toString().indexOf(vsearch)+30);
link = link.substring(0,link.indexOf("\""));
link = "http://vimeo.com/" + link;
}
location.href="http://ultimatehurl.com/commune/submit?url="+encodeURIComponent(link);
}
})();