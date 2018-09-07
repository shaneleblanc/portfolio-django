import requests
import markdown
import os
import glob
import json
from django.http import HttpResponse
from django.shortcuts import render
from forms import ContactForm


def update_navbar():
    navbar_links = []
    content = []
    content_files = glob.glob("content/*.md")
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
               "links": nav_links}
    return render(request, 'base.html', context)


def contact(request):
    md = markdown.Markdown(extensions=['markdown.extensions.meta'])
    html = md.convert(open("content/contact.md").read())
    context = {"content": html,
               "links": nav_links}
    return render(request, 'contact.html', context)


def services(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    context = {"form": form,
               "links": nav_links}
    return render(request, "contact.html", context)


def successView(request):
    return HttpResponse('Success! Thank you for your message.')



def resume(request):
    md = markdown.Markdown(extensions=['markdown.extensions.meta'])
    html = md.convert(open("content/Resume.md").read())
    context = {"content": html,
               "links": nav_links}
    return render(request, 'base.html', context)


def music(request):
    md = markdown.Markdown(extensions=['markdown.extensions.meta'])
    html = md.convert(open("content/music.md").read())
    context = {
        "content": html,
        "links": nav_links
    }
    return render(request, 'base.html', context)


def github(request):
    # We can also combine Django with APIs
    response = requests.get('https://api.github.com/users/shaneleblanc/repos?sort=updated')
    repos = response.json()
    response2 = requests.get('https://api.github.com/orgs/OpenPledge/repos')
    org_repos = response2.json()
    context = {
        "github_repos": org_repos + repos,
        "links": nav_links
    }
    return render(request, 'github.html', context)


