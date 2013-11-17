# -*- coding: utf-8 -*-

from moth.views.base.html_template_view import HTMLTemplateView


class LanguageENView(HTMLTemplateView):
    title = 'English page'
    description = 'Page with English words'
    url_path = 'lang/en.html'
    
    HTML = '''WASHINGTON, Feb. 9 — The most lethal weapon directed against American troops
    in Iraq is an explosive-packed cylinder that United States intelligence
    asserts is being supplied by Iran.
    Skip to next paragraph
    The Reach of War
    Go to Complete Coverage »
    Multimedia
    A Deadly WeaponGraphic
    A Deadly Weapon
    
    The assertion of an Iranian role in supplying the device to Shiite militias
    reflects broad agreement among American intelligence agencies, although
    officials acknowledge that the picture is not entirely complete.
    
    In interviews, civilian and military officials from a broad range of
    government agencies provided specific details to support what until now has
    been a more generally worded claim, in a new National Intelligence Estimate,
    that Iran is providing “lethal support” to Shiite militants in Iraq. '''

class LanguageESView(HTMLTemplateView):
    title = 'Spanish page'
    description = 'Page with Spanish words'
    url_path = 'lang/es.html'
    
    HTML = '''
    Después de un viernes prácticamente perfecto, Argentina llegaba con gran
    comodidad al sábado para jugar el tercer punto ante Austria. El pase a
    cuartos de final de la Copa Davis estaba al alcance de la mano para el
    equipo de Mancini. En el dobles, José Acasuso y Sebastián Prieto enfrentaban
    a Julian Knowle y Jurgen Melzer en Linz.
    
    La firmeza en el saque de los zurdos locales se hizo sentir desde el
    arranque para los argentinos. Tres games ganados al hilo en cero fueron la
    clara muestra de lo que empezaba a ser un hueso duro de roer para Acasuso y
    Prieto, quienes casi no entraron en juegos con el servicio rival. La
    historia no era la misma cuando sacaban los dirigidos por Mancini, que sí
    encontraban resistencia enfrente.
    
    En el sexto game, con Chucho en el servicio, llegó la primera chance de
    quiebre del partido. Algo que se veía venir. Argentina la salvó y alcanzó el
    3-3, pero cada vez se pronunciaban más las diferencias. Y después de doce
    puntos consecutivos ganados por los austriacos desde su saque, los de Luli
    pudieron hacerle frente a lo que hasta ese momento parecía un obstáculo
    imposible de pasar. De todas formas y aunque más trabajadamente, Austria se
    puso 4-3.
    
    Las complicaciones desde el servicio propio continuaron y Austria alcanzó el
    segundo break point en el octavo juego. Esta vez no desaprovechó la
    oportunidad y quebró el saque de Prieto para quedar 5-3 arriba. Melzer
    sacaba para set. Y no fallaría. Los locales conseguían la primera ventaja.
    El 6-3 era un hecho. '''
