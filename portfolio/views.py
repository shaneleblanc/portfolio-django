import requests
import markdown
import os
import glob
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from portfolio.forms import ContactForm
from django.core.mail import send_mail, BadHeaderError, EmailMessage
import sendgrid
from sendgrid.helpers.mail import *


def update_navbar():
    navbar_links = []
    content = []
    content_files = glob.glob("./content/*.md")
    for file in content_files:
        md = markdown.Markdown(extensions=['markdown.extensions.meta'])
        page = {}
        html = md.convert(open(file).read())
        page['filename'] = os.path.basename(file).replace('content/', '').replace('.md', '.html')
        page['title'] = md.Meta["title"][0]
        page['md'] = html
        content.append(page)
    for page in content:
        # # TODO: put the HTML on jinja side, then allow sorting by alphabetical
        navbar_links.append([page['title'], page['title'].lower()])
        #f'''<li class="nav-item"> <a class="nav-link {page['title']}class" href="{page['filename']}"> {page['title']}</a></li>'''
    navbar_links.remove(['Home', 'home'])
    navbar_links.append(['GitHub', 'github'])
    #navbar_links.append(['Blog', 'blog'])
    return navbar_links


nav_links = update_navbar()


def index(request):
    # This is similar to ones we have done before. Instead of keeping
    # the HTML / template in a separate directory, we just reply with
    # the HTML embedded here.
    md = markdown.Markdown(extensions=['markdown.extensions.meta'])
    html = md.convert(open("content/index.md").read())
    context = {"content": html,
               "page": "home",
               "links": nav_links,
               }
    return render(request, "base.html", context)


def about(request):
    # Django comes with a "shortcut" function called "render", that
    # lets us read in HTML template files in separate directories to
    # keep our code better organized.
    md = markdown.Markdown(extensions=['markdown.extensions.meta'])
    html = md.convert(open("content/about.md").read())
    context = {"content": html,
               "page": "about",
               "links": nav_links}
    return render(request, 'base.html', context)


def services(request):
    md = markdown.Markdown(extensions=['markdown.extensions.meta'])
    html = md.convert(open("content/services.md").read())
    context = {"content": html,
               "page": "services",
               "links": nav_links}
    return render(request, 'base.html', context)


def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Message from contact form shaneleblanc.net"
            message = """New message received from %s:
            %s
            """ % (form.cleaned_data['email'], form.cleaned_data['message'])
            try:
                email = EmailMessage(subject, message, "shane@xs.vc", to=["shane@xs.vc"])
                email.send()
            except BadHeaderError:
                return render(request, "contact.html", {
                    "submitted": True,
                    "send_error": True,
                    "links": nav_links
                })
            return render(request, "contact.html", {
                "submitted": True,
                "send_error": False,
                "links": nav_links
            })
    context = {"form": form,
               "page": "contact",
               "links": nav_links}
    return render(request, "contact.html", context)


def resume(request):
    md = markdown.Markdown(extensions=['markdown.extensions.meta'])
    html = md.convert(open("content/Resume.md").read())
    context = {"content": html,
               "page": "resume",
               "links": nav_links}
    return render(request, 'base.html', context)


def music(request):
    md = markdown.Markdown(extensions=['markdown.extensions.meta'])
    html = md.convert(open("content/music.md").read())
    context = {
        "content": html,
        "page": "music",
        "links": nav_links
    }
    return render(request, 'base.html', context)


def github(request):
    response = requests.get('https://api.github.com/users/shaneleblanc/repos?sort=updated')
    repos = response.json()
    response2 = requests.get('https://api.github.com/orgs/OpenPledge/repos')
    org_repos = response2.json()
    context = {
        "github_repos": org_repos + repos,
        "page": "github",
        "links": nav_links
    }
    return render(request, 'github.html', context)


