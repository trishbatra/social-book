from django.shortcuts import  render, redirect, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import profile, post, likedpost, followersCount
from itertools import chain
import random
# Create your views here.

@login_required(login_url="signin")
def index(request):

    uO = User.objects.get(username=request.user.username)
    uP = profile.objects.get(user=uO)
    allp = profile.objects.all()
    myPOSTS = post.objects.all()

    userFollowing = []
    postsToShow = []
    peopleUserIsFollowing = followersCount.objects.filter(gotFollowedBy=request.user.username)
    for users in  peopleUserIsFollowing:
        userFollowing.append(users)
    for names in peopleUserIsFollowing:
        postsofthepeopleuserisfollowing = post.objects.filter(user=names )
        postsToShow.append(postsofthepeopleuserisfollowing)

    print(postsToShow)
    ffs = list(chain(*postsToShow))

    # all_users = User.objects.all()

    # for users in all_users:
    #     if followersCount.objects.filter():
            

    return render(request, "index.html",{"u": uP, "p": ffs, "allp": allp } )

@login_required(login_url="signin")
def search(request):
    currentUserObject = User.objects.get(username=request.user.username)
    curruentuserprofile = profile.objects.get(user=currentUserObject)
    if request.method == "POST":
        enteredInput = request.POST["userrname"]
        uO = User.objects.filter(username__icontains=enteredInput)
        # ud = profile.objects.filter(user=uO)
        userDetails = []
        userProfileDetails  = []
        for users in uO:
            userDetails.append(users.id)
        for ids in userDetails:
            userProfileDetailss = profile.objects.filter(id_user=ids )
            userProfileDetails.append(userProfileDetailss)
        let = list(chain(*userProfileDetails))
        print(let)
        return render(request, "search.html", {"user_profile": curruentuserprofile,"userDetails": let})
    else:
        messages.info(request,"bhai kya akr raha hin tu?")
        return redirect("/")
@login_required(login_url="signin")
def profilez(request,pk):
    uO = User.objects.get(username=pk)
    p =  post.objects.filter(user=pk)
    followers = followersCount.objects.filter(user=pk)
    following = followersCount.objects.filter(gotFollowedBy=pk)
    proFile =  profile.objects.get(user=uO)
    followerr = request.user.username 
    user = pk  

    if followersCount.objects.filter(gotFollowedBy=followerr, user=user ).first():
        buttonText = "Unfollow"
    else:
        buttonText= "Follow"
    l= len(p)
    followingLength = len(following)
    followersCountt = len(followers)
    print(f"lis {l}")
    return render(request, "profile.html", {"userPost": p, "userProfile" : proFile, "lenn": l, "u": uO, "noOFFollowers": followersCountt, "bTxt": buttonText, "flwing": followingLength })
@login_required(login_url="signin")
def like_post(request):
    i = request.GET['postId']
    userThatLiked = request.user.username
    thePost = post.objects.get(id=i)
    checkLiked = likedpost.objects.filter(postID=i,likedBy=userThatLiked).first()

    if checkLiked == None:
        thePost.noOfLikes += 1
        thePost.save()
        m = likedpost.objects.create(postID=i, likedBy=userThatLiked)
        m.save()
        return redirect("/")
    else:
        checkLiked.delete()
        thePost.noOfLikes -= 1
        thePost.save()        
        return redirect("/")
def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password =  request.POST["password"]
        u = auth.authenticate(username=username,password=password)
        if u is not None:
            auth.login(request,u)
            return redirect("/")
        else:
            messages.error(request,"Credentials Invalid")
            return redirect("signin")
    else:
        return render(request, "signin.html")
    
@login_required(login_url="signin")
def follow(request):
    if request.method == "POST":
        f  = request.POST['follower']
        followHuaHain  = request.POST['user']
        print(followHuaHain)
        if  followersCount.objects.filter(user=followHuaHain , gotFollowedBy=f).first() :
            removeFollower = followersCount.objects.get(user=followHuaHain,  gotFollowedBy=f)
            removeFollower.delete()
            return redirect("/profile/"+followHuaHain)
        else:
            removeFollower = followersCount.objects.create(user=followHuaHain,  gotFollowedBy=f)
            removeFollower.save()
            return redirect("/profile/"+followHuaHain)
    else:
        return redirect("/")
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
              messages.error(request,"Email already taken☹️")
              return redirect("signup")
            elif User.objects.filter(username=username).exists():
                messages.error(request,"Email already taken☹️")
                return redirect("signup")
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                
                userToLogIn = auth.authenticate(username=username, password=password)
                auth.login(request,userToLogIn)

                user_model =  User.objects.get(username=username)
                newP = profile.objects.create(user=user_model, id_user=user_model.id)
                newP.save()
                messages.error(request,"User created Successfully 👍")
                return redirect("settings")
        else:
            messages.error(request,"passwords dont match☹️")
            return redirect("signup")
            
    else:
        return render(request, "signup.html")
    
@login_required(login_url="signin")
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url="signin") 
def settings(request):       

    myUser = profile.objects.get(user=request.user)

    if request.method == "POST":
        if request.FILES.get('image') == None:
            i = myUser.profileImg
            location =  request.POST["location"]
            bio=  request.POST["Bio"]
            myUser.profileImg = i    
            myUser.bio = bio 
            myUser.location = location  
            myUser.save()
            messages.info(request,"updated your settings😉")
            return redirect("settings")
        if request.FILES.get('image') != None:
            i = request.FILES.get('image')
            location =  request.POST["location"]
            bio =  request.POST["Bio"]
            myUser.profileImg = i    
            myUser.bio = bio 
            myUser.location = location  
            myUser.save()
            messages.info(request,"updated your settings😉")
            return redirect("settings")
    
    return render(request, "setting.html", {"u": myUser})

@login_required(login_url="signin")
def upload(request):
    if request.method == "POST":
        cap  =  request.POST["cap"]
        file = request.FILES.get("p")
        createdP =  post.objects.create(user=request.user.username, caption=cap, image=file )
        createdP.save()
        messages.info(request,"Post uploaded successfully 🔥")
        return redirect("/")
    else:
        return redirect("/")