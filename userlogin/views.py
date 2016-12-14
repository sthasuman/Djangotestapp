import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.views.generic import FormView, View, TemplateView
from userlogin.forms import UserForm, UserProfileForm
# Create your views here.
from userlogin.models import UserProfile, Notice, Blog, BlogLike
from userlogin.models import Message


def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # If so, we need to get it from the input form and put it in the UserProfile model.

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print (user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
        context)

def index(request):
    users = User.objects.all()
    context = {'userall': users

    }
    return render( request,
        'index.html',context
    )

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print( "Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('login.html', {}, context)

@login_required
def user_logout(request):

        logout(request)

        return HttpResponseRedirect('/')

def update(request,pk = None):
    user = User.objects.get(pk = pk)
    user_form = UserForm(instance=user)
    try:

        profile_form = UserProfileForm(instance=user.userprofile)

        if request.method == 'POST':
            user_form = UserForm(data=request.POST, instance=user)
            profile_form = UserProfileForm(data=request.POST, instance=user.Userprofile)

            if user_form.is_valid() and profile_form.is_valid():
                # Save the user's form data to the database.
                user = user_form.save()

                # Now we hash the password with the set_password method.
                # Once hashed, we can update the user object.
                user.set_password(user.password)
                user.save()

                # Now sort out the UserProfile instance.
                # Since we need to set the user attribute ourselves, we set commit=False.
                # This delays saving the model until we're ready to avoid integrity problems.
                profile = profile_form.save(commit=False)
                profile.user = user

                # If so, we need to get it from the input form and put it in the UserProfile model.

                # Now we save the UserProfile model instance.
                profile.save()

        context = {
            'user_form':user_form,'profile_form':profile_form
        }
    except AttributeError:
        if request.method == 'POST':
            user_form = UserForm(data=request.POST, instance=user)

            if user_form.is_valid():
                # Save the user's form data to the database.
                user = user_form.save()

                # Now we hash the password with the set_password method.
                # Once hashed, we can update the user object.
                user.set_password(user.password)
                user.save()

        context = {
        'user_form':user_form
        }
    return render (request,'update.html',context)

def delete(request, pk = None):
    user = User.objects.get(pk = pk)
    user_form = UserForm(instance=user)

    try:
        profile_form = UserProfileForm(instance=user.UserProfile)
        user.delete()
        UserProfile.delete()
    except AttributeError:
        user.delete()

    return HttpResponseRedirect('/')


class MessageView(LoginRequiredMixin, TemplateView):
    template_name = 'message.html'
    model = Message

    def get(self, request, pk):
        inbox = Message.objects.filter(sender=self.request.user).order_by('-time_sent').filter(receiver=User.objects.get(pk=pk))
        context = {"inbox":inbox}
        return render(request,'message.html',context)

    def post(self, request, pk ):
        message_text = request.POST['message_text']
        response_data ={}

        message_text = request.POST['message_text']
        message = Message(message=message_text)
        message.sender = self.request.user
        message.receiver = User.objects.get(pk=pk)
        message.save()
        response_data['message'] = message.message
        response_data['sender'] = message.sender.username
        response_data['time'] = message.time_sent.strftime('%B %d, %Y %I:%M %p')
        if request.is_ajax():
            return HttpResponse(json.dumps(response_data),content_type='application/json')
        return HttpResponse('No ajax requested')

class InboxView(TemplateView):
    template_name = 'inbox.html'

    def get(self, request, pk):
        inbox = Message.objects.filter(receiver = self.request.user).order_by('-time_sent')
        context = {"inbox":inbox}
        return render(request,'inbox.html',context)

class CreateNoticeView(LoginRequiredMixin,TemplateView):
    template_name = 'addnotice.html'
    model = Notice

    def post(self, request):
        notice_text = request.POST['notice_text']
        notice = Notice(notice_text= notice_text)
        notice.save()
        return HttpResponse('Notice has been sent to all users')

class NoticeView(TemplateView):
    template_name = 'notice.html'

    def get(self, request):
        notice = Notice.objects.all().order_by('-time_added')
        context = {"notice": notice}
        return render(request,'notice.html',context)

class CreateBlogView(LoginRequiredMixin,TemplateView):
    template_name = 'addblog.html'
    model = Blog

    def post(self, request, pk):
        blog_title = request.POST['blog_title']
        blog_text = request.POST['blog_text']
        blog = Blog(blog_text= blog_text)
        blog.blog_publisher = self.request.user
        blog.blog_title = blog_title
        blog.save()
        return HttpResponse('Blog is posted!!!')

class BlogView(TemplateView):
    template_name = 'blog.html'

    def get(self, request):
        blog = Blog.objects.all().order_by('-time_added')
        context = {"blog": blog}
        return render(request,'blog.html',context)

class BlogpostView(TemplateView):
    template_name = 'blogpost.html'

    def get(self, request, pk):
        titleid= Blog.objects.get(pk=pk)
        like = BlogLike.objects.filter(like_blog=titleid)
        if BlogLike.objects.filter(like_blog=titleid).filter(like_done=request.user):
            liked= True
        else:
            liked=False
        context = {'blogpost':titleid,'like':like, 'liked':liked}
        return render(request,'blogpost.html',context)

    def post(self, request, pk):
        titleid= Blog.objects.get(pk=pk)
        response_data={}
        if BlogLike.objects.filter(like_blog=titleid).filter(like_done=request.user):
            instance= BlogLike.objects.filter(like_blog=titleid).filter(like_done=request.user)
            instance.delete()
            response_data['liked'] = False
        else:
            instance= BlogLike.objects.create(like_blog=titleid, like_done=request.user)
            instance.save()
            response_data['liked'] = True

        instance =BlogLike.objects.filter(like_blog=titleid)
        response_data['like'] = instance.count()

        if request.is_ajax():
            return HttpResponse(json.dumps(response_data),content_type='application/json')
        return HttpResponse('No ajax requested')

class NotificationView(TemplateView):
    template_name = 'notification.html'

    def get(self, request,pk):
        liked_blog= BlogLike.objects.filter(like_blog__blog_publisher= request.user).order_by('-time_liked')
        return render(request,"notification.html",context={'notify':liked_blog})










