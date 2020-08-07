from django.shortcuts import render,get_object_or_404
from testapp.models import  Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from testapp.forms import EmailSendForm
from django.core.mail import send_mail
from taggit.models import Tag

# Create your views here.
def post_view(request,tag_slug=None):
    post_info=Post.objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_info=post_info.filter(tags__in=[tag])
    paginator=Paginator(post_info,1)
    page_number=request.GET.get('nextpage')
    try:
         post_info=paginator.page(page_number)
    except PageNotAnInteger:
         post_info=paginator.page(1)
    except EmptyPage:
         post_info=paginator.page(paginator,num_pages)
    return render(request,'testapp/post_list.html',{'post_info':post_info,'tag':tag},)

def post_details_view(request,year,month,day,post):
     post=get_object_or_404(Post,slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
     print('post is:',post)
     return render(request,'testapp/post_detail.html',{'post':post})

def EmailSendForm_view(request,id):
     post=get_object_or_404(Post,id=id,status='published')
     sent=False
     if request.method=='POST':
         print('hello.............iam if')
         form=EmailSendForm(request.POST)
         if form.is_valid():
           cd=form.cleaned_data
           subject='{} from "{}" recomends you to read the Post: "{}"'.format(cd['Name'],cd['Email'],post.title)
           post_url=request.build_absolute_uri(post.get_absolute_url())
           message='Read post at:\n {} \n\n{}\'s comments:\n{}'.format(post_url,cd['Name'],cd['Comments'])
           send_mail(subject,message,'learningcourse116@gmail.com',[cd['To'],])
           sent=True
     else:
         print('hello.............iam else')
         form=EmailSendForm()
     return render(request,'testapp/sharebyemail.html',{'form':form,'post':post,'sent':sent})
