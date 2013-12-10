import subprocess
import commands
import shlex

from django.shortcuts import render
from moth.views.base.vulnerable_template_view import VulnerableTemplateView


class TrivialOSCommandingView(VulnerableTemplateView):
    title = 'Trivial OS Commanding'
    tags = ['trivial', 'GET']
    description = 'The application executes the command passed as parameter'\
                  ' without any validation or restriction'
    url_path = 'trivial_osc.py?cmd=ls'
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        
        try:
            cmd_args = shlex.split(request.GET['cmd'])
        except ValueError:
            # ValueError, "No closing quotation"
            context['html'] = 'Invalid command'
        else:
            try:
                context['html'] = subprocess.check_output(cmd_args)
            except subprocess.CalledProcessError, cpe:
                context['html'] = cpe.output
        
        return render(request, self.template_name, context)
    
class ArgvOSCommandingView(VulnerableTemplateView):
    title = 'OS Commanding in command argument'
    tags = ['argument', 'GET']
    description = 'The application uses the user input as a parameter for'\
                  ' a fixed external command'
    url_path = 'param_osc.py?param=-la'
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        
        cmd = 'ls %s' % request.GET['param']
        context['html'] = commands.getoutput(cmd)

        return render(request, self.template_name, context)
    
class BlindOSCommandingView(VulnerableTemplateView):
    title = 'Blind OS Commanding'
    tags = ['blind', 'GET']
    description = 'The application executes user input but does NOT display'\
                  ' the output in the HTTP response body'
    url_path = 'blind_osc.py?cmd=ls'
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()
        context['html'] = 'Hiding command output!'

        try:
            cmd_args = shlex.split(request.GET['cmd'])
        except ValueError:
            # ValueError, "No closing quotation"
            context['html'] = 'Invalid command'
        else:
            try:
                subprocess.check_output(cmd_args)
            except subprocess.CalledProcessError:
                pass

        return render(request, self.template_name, context)