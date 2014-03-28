import subprocess

from django.shortcuts import render

from moth.views.base.vulnerable_template_view import VulnerableTemplateView


class EvalDelayView(VulnerableTemplateView):
    title = 'Python eval() vulnerability'
    tags = ['GET', 'blind']
    description = 'eval() the text query string without any validation and'\
                  ' do NOT output the result.'
    url_path = 'eval_blind.py?text=1'
    
    def get(self, request, *args, **kwds):
        context = self.get_context_data()

        try:
            eval(request.GET['text'])
        except SyntaxError:
            pass

        context['html'] = 'Static placeholder.'
        return render(request, self.template_name, context)


class EvalPythonCView(VulnerableTemplateView):
    title = 'Python execute vulnerability'
    tags = ['GET', 'execute', '-c', 'single-quote']
    description = 'Runs the provided input through "python -c ..." and'\
                  ' returns the output. The command line argument is delimited'\
                  ' using single quotes.'
    url_path = 'eval_single.py?text=1'

    CMD_FMT = "python -c '%s'"

    def get(self, request, *args, **kwds):
        context = self.get_context_data()

        python_code = request.GET['text']
        run_cmd = self.CMD_FMT % python_code

        try:
            output = subprocess.check_output(run_cmd, shell=True)
        except subprocess.CalledProcessError, cpe:
            context['html'] = 'Found execution error: %s' % cpe
        except:
            context['html'] = 'Generic crash!'
        else:
            context['html'] = output

        return render(request, self.template_name, context)


class EvalPythonCDoubleQuoteView(EvalPythonCView):
    title = 'Python execute vulnerability'
    tags = ['GET', 'execute', '-c', 'double-quote']
    description = 'Runs the provided input through "python -c ..." and'\
                  ' returns the output. The command line argument is delimited'\
                  ' using double quotes.'
    url_path = 'eval_double.py?text=1'

    CMD_FMT = 'python -c "%s"'
