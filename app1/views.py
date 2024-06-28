from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from . models import Product
from . forms import ProductForm
from . models import Flag
from . models import Board
from . forms import BoardForm
from . models import Answer
from . forms import AnswerForm
from . models import Attempt
from datetime import datetime
from . models import complete
from . forms import completeForm
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import cache_control, never_cache
from django.urls import reverse
from django.utils.decorators import method_decorator
from datetime import datetime
from django.views.decorators.cache import never_cache
from django.views import View
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from . forms import FlagsForm
from . models import Flags
from . models import Scene
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt




@login_required(login_url='login')
def HomePage(request):
    return render(request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        domain = email.split("@")[1]
        if(uname!='' and email!='' and pass1!='' and pass2!='' and pass2!='' and first_name!='' and last_name!=''):
            try:
                validate_password(pass1)
            except ValidationError as validation_error:
                error_message = validation_error.messages[0]
                return render(request,'signup.html',{'error': error_message})

            if(domain != 'qburst.com'):
                error_message = 'Please enter qburst mail id'
                return render(request,'signup.html',{'error': error_message})

            else:
                if pass1!=pass2:
                    return render(request,'signup.html',{'error':'Passwords did not match'})
                else:
                    if(User.objects.filter(username = uname).count() == 0 and User.objects.filter(email = email).count() == 0):
                        my_user=User.objects.create_user(
                            uname,
                            email=email,
                            password=pass1,
                            first_name=first_name,
                            last_name=last_name)
                        my_user.save()
                        return redirect('login')
                    else:
                        return render(request,'signup.html',{'error':'Username already exists'})
        else:
            return render(request,'signup.html',{'error':'Fill all the required fields'})
    return render(request,'signup.html')

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        boards = Board.objects.all()
        value = 0
        if user is not None:
            login(request,user)
            for board in boards:
                if board.user.id == user.id:
                    value = 1
            if value == 0:
                order = Board.objects.create(
                user = request.user,
                score = 0
                )
            return redirect('index')
        else:
            return render(request,'login.html',{'error':'Username or password is wrong'})
        
    return render(request,'login.html')    

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def LogoutPage(request):
    logout(request)
    return redirect('index')

def IndexPage(request):
    products = Product.objects.all()[:3]
    user = request.user

    context = {
        "products" : products,
        "user" : user
    }
    return render(request,'index.html',context)

@staff_member_required
# @cache_control(no_cache=True, must_revalidate=True,no_store=True)
def addProduct(request):
    form = ProductForm()
    user = request.user

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('showProducts')
            # return redirect('addhint form.id')

        else:
            form = ProductForm()

    context = {
        "form":form,
        "user": user
    }

    return render(request, 'addProduct.html', context)

@staff_member_required
def ShowAllProducts(request):
    products = Product.objects.all()
    user = request.user

    context = {
        "products": products,
        "user" : user
    }

    return render(request,'showProducts.html',context)

@staff_member_required
def productDetail(request,pk):
    eachProduct = Product.objects.get(id=pk)
    hints = Flags.objects.all()
    user = request.user


    context = {
        # "hints" : hints
        # "eachProduct" : eachProduct
    }

    contest = {
        "hints" : hints,
        "user": user
    }

    return render(request, 'productDetail.html',{'eachProduct':Product.objects.get(id=pk),'hints':Flags.objects.all()})

@staff_member_required
# @cache_control(no_cache=True, must_revalidate=True,no_store=True)
def updateProduct(request,pk):
    product = Product.objects.get(id=pk)
    
    form = ProductForm(instance=product)
    user = request.user

    if request.method == 'POST':
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            
            return redirect('showProducts')

    context = {
        "form":form,
        "user": user
    }

    return render(request, 'updateProduct.html', context)

@staff_member_required
# @cache_control(no_cache=True, must_revalidate=True,no_store=True)
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return redirect('showProducts')

@staff_member_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def addhint(request,pk):
    from django import forms
    form = FlagsForm()
    quest = Product.objects.get(id=pk)
    user = request.user
    if request.method == 'POST':
        form = FlagsForm(request.POST, request.FILES)
        if form.is_valid():
            # form.q1 = pk
            # form.save()
            # # return redirect('showProducts')
            h1 = form.cleaned_data['h1']
            f1 = form.cleaned_data['f1']
            image = request.FILES.get('image')
            score = form.cleaned_data['score']

            order = Flags.objects.create(
                quest = quest,
                h1 = h1,
                image = image,
                f1 = f1,
                score = score
            )
            return redirect('product', pk = pk)

        else:
            form = FlagsForm()

    context = {
        "form":form,
        "user":user
    }

    return render(request, 'addhint.html', context)

@staff_member_required
# @cache_control(no_cache=True, must_revalidate=True,no_store=True)
# @method_decorator(never_cache())
# @cache_control(no_store=True)
def updateHint(request,pk):
    hint = Flags.objects.get(id=pk)
    form = FlagsForm(instance=hint)
    user = request.user

    if request.method == 'POST':
        form = FlagsForm(request.POST,request.FILES,instance=hint)
        if form.is_valid():
            form.save()
            # rendered_html = render(request, 'showProducts.html')
            # response = HttpResponse(rendered_html, content_type='text/html')
            # response['Cache-Control'] = 'no-store'
            # return response
            # response = HttpResponse( '''
            #     <script>
            #     if (window.history.replaceState) {
            #         window.history.replaceState({},document.title,"/showProducts/");
            #         }else{
            #             window.location.href = "/showProducts/";
            #         }
            #     window.location.replace("/showProducts/");
            #     </script>
            # ''')
            # return response
            # return HttpResponseRedirect('/showProducts/')
            return redirect('product', pk = hint.quest.id)
            # return redirect('updateHint',pk = hint.id)
            # return reverse('product', pk = hint.q1)
            # named_redirect = reverse('Welcome_page')
            # return redirect(named_redirect)

    context = {
        "form":form
    }

    return render(request, 'updateHint.html', {'form':form,'hint':hint,'user' : user})

@staff_member_required
# @cache_control(no_cache=True, must_revalidate=True,no_store=True)
def deleteHint(request, pk):
    hint = Flags.objects.get(id=pk)
    var = hint.quest.id
    hint.delete()
    return redirect('product',pk = var)

@login_required(login_url='login')
def ShowAllQuests(request):
    products = Product.objects.all()
    user = request.user

    context = {
        "products": products,
        "user" : user
    }

    return render(request,'showQuests.html',context)

@login_required(login_url='login')
# @cache_control(no_store=True)
def questDetail(request,pk):
    eachProduct = Product.objects.get(id=pk)
    hints = Flags.objects.all()
    completeds = complete.objects.all()
    user = request.user
    if 'error' in request.session:
        del request.session['error']

    context = {
        # "hints" : hints
        # "eachProduct" : eachProduct
    }

    contest = {
        "hints" : hints
    }

    return render(request, 'questDetail.html',{'eachProduct':Product.objects.get(id=pk),'hints':Flags.objects.all(),'completeds':complete.objects.all(),'user':user})

@login_required(login_url='login')
# @cache_control(no_store=True)
# @cache_control(private=True, max_age=0, no_cache=True, no_store=True, must_revalidate=True)
@cache_control(no_cache=True, must_revalidate=True)
def addFlag(request,pk):
    hints = Flags.objects.get(id=pk)
    form = AnswerForm()
    completeds = complete.objects.all()
    attempts = Attempt.objects.all()
    user= request.user
    boards = Board.objects.get(user=user)
    var = hints.quest.id
    value = '0'
    pin = '0'
    error = '0'
    token = 0
    token = int(hints.quest.id)
    for completed in completeds:
        if hints.id == completed.hint.id:
            user = request.user
            if user.id == completed.user.id:
                value = '1'
    if request.method=='POST':
        if value == '0':
            form = AnswerForm(request.POST)
            # flag = form.cleaned_data['answer']
            flag = request.POST.get('answer')
            # flag=request.POST.get('flag')
            if form.is_valid():
                for piece in attempts:
                    if(piece.user == user):
                        if(piece.flag.id == hints.id):
                            temp = piece.attempt
                            change = temp + 1
                            Attempt.objects.filter(user=user,flag_id=hints.id).update(attempt=change)
                            pin = '1'
                if(pin == '0'):
                    order = Attempt.objects.create(
                        user= user,
                        flag= hints,
                        attempt= 1
                    )
                            

                if (hints.f1.lower() == flag.lower()):
                    order = complete.objects.create(
                    user = request.user,
                    hint = hints,
                    completed = True
                    )
                    mark = boards.score
                    per = hints.score
                    new_mark = mark + per
                    Board.objects.filter(user=user).update(score=new_mark)
                    Board.objects.filter(user=user).update(finished_at = datetime.now())
                    # if request.session['error']:
                    #     del request.session['error']
                    return redirect('quest',pk = var)
                else:
                    error = 'Flag is not correct'
                    token = int(hints.quest.id)
                    request.session['error'] = error
                    form = AnswerForm()
                    # return redirect('addFlag',pk = hints.id)
                    # return redirect('/addFlag/',pk = hints.id,'?error={error}')
                    return render(request, 'addFlag.html',{'hints':Flags.objects.get(id=pk),'completeds':complete.objects.all(),'value':value,'error':error,'token':token,'form':form,'user':request.user})
            else:
                form = AnswerForm()
        else:
            return redirect('quest',pk = var)

    context = {
        "hints" : hints
    }
    return render(request, 'addFlag.html',{'hints':Flags.objects.get(id=pk),'completeds':complete.objects.all(),'value':value,'form':form,'error':error,'token':token,'user':request.user})

@login_required(login_url='login')
def leaderboard(request):
    completeds = complete.objects.all()
    user = request.user
    boards = Board.objects.all().order_by('-score','finished_at')
    # n = boards.count()
    # for board in boards:
    #     for i in range(1,n-1):
    #         if(board.score != 0):
    #             if (board.score == boards[i].score):
    #                 comp1 = complete.objects.filter(user_id = board.user.id).reverse()[:1]
    #                 comp2 = complete.objects.filter(user_id = boards[i].user.id).reverse()[:1]
    #                 hi = comp2[0].finished_at
    #                 if(comp1[0].finished_at < comp2[0].finished_at):
    #                     temp = boards[i]
    #                     boards[i] = boards[i-1]
    #                     boards[i-1] = temp
    context = {
        "boards": boards,
        "user" : user
    }

    return render(request,'Leaderboard.html',context)

# @login_required(login_url='login')
# def profile(request,pk):
#     user = User.objects.get(id = pk)
#     boards = Board.objects.all().order_by('score').reverse()
#     completeds = complete.objects.filter(user = user)
#     hints = Flags.objects.all()
#     products = Product.objects.all()
#     array = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#     n = 0 
#     total = 0
#     finish = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#     for board in boards:
#         if board.user.id == user.id:
#             score = board.score 

#     for product in products:
#         for hint in hints:
#             if(hint.q1 != product):
#                 array[n] += 1
#             for completed in completeds:
#                 if(completed.hint.id == hint.id):
#                     finish[n] += 1
#         n += 1

#     numbers = range(n+1)

#     context = {
#         "boards": boards
#     }

#     idor = request.user
#     if (pk != idor.id):
#         order = Scene.objects.create(
#             user= idor,
#             hecker = 1
#         )

#     return render(request,'profile.html',{'score':score,'completeds':completeds,'hints':hints,'products':products,'array':array,'finish':finish,'numbers':numbers,'n':1})

@staff_member_required
@login_required(login_url='login')
def finish(request,pk):
    completeds = complete.objects.filter(hint_id = pk)
    object = completeds.first()
    # token = int(object.hint.q1)
    context = {
        "completeds": completeds
    }

    return render(request,'finish.html',{'completeds':complete.objects.filter(hint_id = pk),'user' : request.user})

@staff_member_required
def users(request):

    boards = Board.objects.all().order_by('score').reverse()
    user = request.user
    scenes = Scene.objects.all()

    context = {
        "users": boards,
        "user" : user,
        "scenes" : scenes
    }

    return render(request,'users.html',context)

@staff_member_required
def details(request, pk):
    User = get_user_model()
    user = User.objects.get(id=pk)
    board = Board.objects.get(user=user)
    hints = Flags.objects.all()
    products = Product.objects.all()
    completeds = complete.objects.filter(user = user)
    attempts = Attempt.objects.filter(user = user)
    man = request.user


    
    return render(request, 'details.html',{'board':board,'hints':hints,'products':products,'completeds':completeds,'attempts':attempts,'user':man})

@staff_member_required
# @cache_control(no_cache=True, must_revalidate=True,no_store=True)
def deleteUser(request, pk):
    User = get_user_model()
    user = User.objects.get(id=pk)
    user.delete()
    return redirect('users')

@login_required(login_url='login')
@csrf_exempt
def profile(request,pk):
    user = User.objects.get(id = pk)
    boards = Board.objects.all().order_by('score').reverse()
    completeds = complete.objects.filter(user = user)
    hints = Flags.objects.all()
    products = Product.objects.all()
    array = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    n = 0 
    total = 0
    finish = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    # for board in boards:
    #     if board.user.id == user.id:
    #         score = board.score 

    # for product in products:
    #     for hint in hints:
    #         if(hint.q1 != product):
    #             array[n] += 1
    #         for completed in completeds:
    #             if(completed.hint.id == hint.id):
    #                 finish[n] += 1
    #     n += 1

    # numbers = range(n+1)

    # context = {
    #     "boards": boards
    # }

    idor = request.user
    # if (pk != idor.id):
    #     order = Scene.objects.create(
    #         user= idor,
    #         hecker = 1
    #     )

    idor = request.user
    if (pk == idor.id):
        for board in boards:
            if board.user.id == user.id:
                score = board.score 

        for product in products:
            for hint in hints:
                if(hint.q1 != product):
                    array[n] += 1
                for completed in completeds:
                    if(completed.hint.id == hint.id):
                        finish[n] += 1
            n += 1

        numbers = range(n+1)

        context = {
            "boards": boards
        }

        return render(request,'profile.html',{'score':score,'completeds':completeds,'hints':hints,'products':products,'array':array,'finish':finish,'numbers':numbers,'n':1})

    else:
        if request.method=='POST':
            if (pk != idor.id):
                order = Scene.objects.create(
                user= idor,
                hecker = 1
                )
            for board in boards:
                if board.user.id == user.id:
                    score = board.score 

            for product in products:
                for hint in hints:
                    if(hint.q1 != product):
                        array[n] += 1
                    for completed in completeds:
                        if(completed.hint.id == hint.id):
                            finish[n] += 1
            n += 1

            numbers = range(n+1)

            context = {
                "boards": boards
            }
            return render(request,'profile.html',{'score':score,'completeds':completeds,'hints':hints,'products':products,'array':array,'finish':finish,'numbers':numbers,'n':1})


    return render(request,'profile.html',{'score':score,'completeds':completeds,'hints':hints,'products':products,'array':array,'finish':finish,'numbers':numbers,'n':1})

    