from django.shortcuts import render

from moth.utils.plugin_families import get_plugin_families


def home(request):
    plugin_families = get_plugin_families()
    context = {'families': plugin_families}
    return render(request, 'moth/home.html', context)

def about(request):
    return render(request, 'moth/about.html')
