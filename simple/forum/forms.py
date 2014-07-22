from django.forms import ModelForm
from models import *
from forum.shared.utils import ContainerFormMixin

class ProfileForm(ModelForm):
	class Meta:
		model   = UserProfile
		exclude = ["posts", "user"]

class PostForm(ContainerFormMixin, ModelForm):
	class Meta:
		model   = Post
		exclude = ["creator", "thread"]