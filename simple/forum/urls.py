from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required as LR
from forum.models import *
from views import *

urlpatterns = patterns("simple.forum.views",
	url(r'^login/$', 'django.contrib.auth.views.login'),
	url(r'^logout/$','django.contrib.auth.views.logout'),

	(r"^forum/(?P<dpk>\d+)/$"             , ForumView.as_view(), {}, "forum"),
	(r"^thread/(?P<dpk>\d+)/$"            , ThreadView.as_view(), {}, "thread"),

	(r"^new_topic/(?P<dpk>\d+)/$"          , LR(NewTopic.as_view()), {}, "new_topic"),
	(r"^reply/(?P<dpk>\d+)/$"              , LR(Reply.as_view()), {}, "reply"),
	(r"^profile/(?P<mfpk>\d+)/$"           , LR(EditProfile.as_view()), {}, "profile"),

	(r""                                   , Main.as_view(), {}, "forum_main"),


)