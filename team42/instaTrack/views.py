from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from django.views import generic
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from mongoengine.errors import NotUniqueError

from .models import UserProfile, WeFollowID, WeTrackID, WeFollowUser, WeTrackUser, NrFollowers
from .forms import UserForm, UserProfileForm
from .fetch_data import *
from .data_functions import track_new, untrack, get_unfollow_suggestions, \
get_best_tags,get_best_time, update_followings, get_tracked_users, update_tracked_data, get_full_user_data, get_all_comments
#from .authentication import direct_to_instagram_log_in
from .authentication import get_token


# Home page
def index(request):

    if request.user.is_authenticated():
        local_user = request.user
        local_userprofile = local_user.userprofile
        print('Logged in UserProfile: ',local_userprofile)
        print('UserProfiles ID: ',local_userprofile.instagram_id)

        return HttpResponseRedirect('/dandli/app')

    else:
        return render(request, 'instaTrack/index.html', {})



def about(request):
    return render(request, 'instaTrack/about.html', {})


@never_cache
def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dandli/app')
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False
    user_form = None
    profile_form = None
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if not check_user(request.POST.get('instagram_username')):
            print('instagram_username is invalid!')
            user_form = UserForm()
            profile_form = UserProfileForm()
            error_message = 'The instagram account does not exist or is private.'
            context = {
                'user_form': user_form,
                'profile_form': profile_form,
                'registered': False,
                'login_error': error_message,
            }
            return render(request, 'instaTrack/register.html', context)

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
            insta_id = get_user_id(profile.instagram_username)
            print('insta_id: ',insta_id)
            profile.instagram_id = insta_id
            profile.nr_followers = int(n_followers_of_user(profile.instagram_username)[0])
            try:
                new_nr_foll_doc = NrFollowers(instagram_username=profile.instagram_username)
                new_nr_foll_doc.save()
            except NotUniqueError:
                print(new_nr_foll_doc, ' already exists')


            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    }
    return render(request, 'instaTrack/register.html', context)



def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dandli/app')
    # If the request is a HTTP POST, try to pull out the relevant information.
    error_message = ''
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
        # because the request.POST.get('<variable>') returns None, if the value does not exist,
        # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')
        redirect_url = request.POST.get('redirect_url')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                print('DEBUG: user is now logged in!')
                return HttpResponseRedirect(redirect_url)
            else:
                # An inactive account was used - no logging in!
                error_message = 'Your account is disabled'
                return render(request, 'instaTrack/login.html', {
                    'redirect_url': redirect_url,
                    'login_error': error_message
                })
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            error_message = 'Invalid login details'
            return render(request, 'instaTrack/login.html', {
                'redirect_url': redirect_url,
                'login_error': error_message
            })

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        redirect_url = request.GET.get('next')
        if redirect_url is None:
            redirect_url = '/dandli/app'
        context = {'redirect_url': redirect_url, 'login_error': error_message}
        return render(request, 'instaTrack/login.html', context)


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/dandli/')


# single page APP view
# TODO: add login required and other checks
@login_required
def app(request):
    return render(request, 'instaTrack/app.html', {})
    # if(request.user.userprofile.access_token):
    #     return render(request, 'instaTrack/app.html', {})
    #
    # to_render = get_token(request)
    # if(not to_render):  # Either token is saved or user refused to give access or any other has occured.
    #                     # Just show the /app.html
    #     return render(request, 'instaTrack/app.html', {})
    # else:               # Redirect to the instagram app to get the token
    #     return to_render



# for testing
def test(request):
    return render(request, 'instaTrack/test.html',{})
