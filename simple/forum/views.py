from django.shortcuts import render
from PIL import Image as PImage

from forum.settings import MEDIA_URL
from forum.forum.models import *
from forum.shared.utils import *
from forum.shared.utils import ContainerFormMixin

from forum.simple.detail import DetailView
from forum.simple.edit import CreateView, UpdateView
from forum.simple.list_custom import ListView, ListRelated

from forms import ProfileForm, PostForm
# Create your views here.


class Main(ListView):
	list_model = Forum
	template_name = "forum/list.html"

class ForumView(ListRelated):
	detail_model = Forum
	list_model = Thread
	related_name = "posts"
	template_name = "thread.html"

class EditProfile(UpdateView):
	form_model = UserProfile
	modelform_class = ProfileForm
	success_url = '#'
	template_name = "profile.html"

	def modelform_valid(self, modelform):
		"""Resize and save profile image."""
		# remove old image if changed
		name = modelform.cleaned_data.get("avatar")
		pk = self.kwargs.get("mfpk")
		old = UserProfile.obj.get(pk=pk).avatar

		if old.name and old.name != name:
			old.delete()

		# save new image to disk and resize new image
		self.modelform_object = modelform.save()
		if self.modelform_object.avatar:
			img = PImage.open(self.modelform_object.avatar.path)
			img.thumbnail((160,160), PImage.ANTIALIAS)
			img.save(img.filename, "JPEG")
		return redir(self.success_url)


class NewTopic(DetailView, CreateView):
	detail_model = Forum
	form_model = Post
	modelform_class = PostForm
	title = "Start New Topic"
	template_name = "forum/post.html"

	def get_thread(self, modelform):
		title = modelform.cleaned_data.title
		return Thread.obj.create(forum=self.get_detail_object(), title=title, creator=self.user)

	def modelform_valid(self, modelform):
		"""Create new thread and it's first post."""
		data = modelform.cleaned_data
		thread = self.get_thread(modelform)

		Post.obj.create(thread=thread, title=data.title, body=data.body, creator=self.user)
		self.user.profile.increment_posts()
		return redir(self.get_success_url())

	def get_success_url(self):
		return self.get_detail_object().get_absolute_url()


class Reply(NewTopic):
	detail_model = Thread
	title = "Reply"

	def get_thread(self, modelform):
		return self.get_detail_object()

	def get_success_url(self):
		return self.get_detail_object().get_absolute_url() + "?page=last"


class PostForm(ContainerFormMixin, ModelForm):
	class Meta:
		model = PostFormexclude = ["creator", "thread"]

	def form_context(request):
		return dict(media_url=MEDIA_URL)