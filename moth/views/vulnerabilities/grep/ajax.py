from django.http import HttpResponse

from moth.views.base.html_template_view import HTMLTemplateView
from moth.views.base.vulnerable_template_view import VulnerableTemplateView


class XMLHttpRequestAjaxView(HTMLTemplateView):
    title = 'AJAX code which performs a simple XMLHttpRequest'
    description = 'Performs a simple XMLHttpRequest to retrieve ajax_info.txt'
    url_path = 'index.html'
    
    HTML = '''
    <script type="text/javascript">
    function loadXMLDoc()
    {
    if (window.XMLHttpRequest)
      {// code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
      }
      else
      {// code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
      }
    
      xmlhttp.onreadystatechange=function()
      {
        if (xmlhttp.readyState==4 && xmlhttp.status==200)
        {
          document.getElementById("myDiv").innerHTML=xmlhttp.responseText;
        }
      }
      xmlhttp.open("GET","ajax_info.txt",true);
      xmlhttp.send();
      }
    </script>
    
    <div id="myDiv">Let AJAX change this text</div>
    <button type="button" onclick="loadXMLDoc()">Change Content</button>
    '''

class AjaxInfoView(VulnerableTemplateView):
    title = 'Ajax info for XMLHttpRequest'
    description = 'Ajax info for XMLHttpRequest, not a vulnerability test.'
    url_path = 'ajax_info.txt'

    def get(self, request, *args, **kwds):
        ajax_info = 'foo\nbar'
        return HttpResponse(ajax_info)