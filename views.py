import requests
import markdown
import os
import glob
from django.http import HttpResponse
from django.shortcuts import render
def index(request):
    # This is similar to ones we have done before. Instead of keeping
    # the HTML / template in a separate directory, we just reply with
    # the HTML embedded here.
    md = markdown.Markdown(extensions = ['markdown.extensions.meta'])
    html = md.convert(open("content/index.md").read())
    context = { "content": html,
                "links": update_navbar(),
              }
    return render(request, "base.html", context)


def about(request):
    # Django comes with a "shortcut" function called "render", that
    # lets us read in HTML template files in separate directories to
    # keep our code better organized.
    md = markdown.Markdown(extensions = ['markdown.extensions.meta'])
    html = md.convert(open("content/about.md").read())
    context = { "content": html, }
    return render(request, 'base.html', context)

def contact(request):
    md = markdown.Markdown(extensions = ['markdown.extensions.meta'])
    html = md.convert(open("content/contact.md").read())
    context = { "content": html, }
    return render(request, 'base.html', context)

def services(request):
    md = markdown.Markdown(extensions = ['markdown.extensions.meta'])
    html = md.convert(open("content/services.md").read())
    context = { "content": html, }
    return render(request, 'base.html', context)

def github_api(request):
    # We can also combine Django with APIs
    response = requests.get('https://api.github.com/users/michaelpb/repos')
    repos = response.json()
    context = {
        'github_repos': repos,
    }
    return render(request, 'github.html', context)

def update_navbar():
    navbar_links = []
    content = []
    content_files = glob.glob("content/*.md")
    for file in content_files:
        md = markdown.Markdown(extensions = ['markdown.extensions.meta'])
        page = {}
        html = md.convert(open(file).read())
        page['filename'] = os.path.basename(file).replace('content/','').replace('.md','.html')
        page['title'] = md.Meta["title"][0]
        page['md'] = html
        content.append(page)
    for page in content:
        # # TODO: put the HTML on jinja side, then allow sorting by alphabetical
        navbar_links.append([page['title'], page['title'].lower()])
        #f'''<li class="nav-item"> <a class="nav-link {page['title']}class" href="{page['filename']}"> {page['title']}</a></li>'''
    navbar_links.remove(['Home', 'home'])
    navbar_links.append(['Blog', 'blog'])
    return(navbar_links)
