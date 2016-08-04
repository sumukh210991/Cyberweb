# -*- coding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1468782476.17732
_enable_loop = True
_template_filename = '/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/gallery.mako'
_template_uri = '/gallery.mako'
_source_encoding = 'utf-8'
from webhelpers.html import escape
_exports = ['headtags', 'footer']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/layout.mako', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        c = context.get('c', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'<style>\nh2 {\n    display: block;\n    font-size: 2.5em;\n    margin-top: 0.83em;\n    margin-bottom: 0.83em;\n    margin-left: 6.83em;\n    margin-right: 0;\n    font-weight: bold;\n\tcolor: purple;\n}\n</style>\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n<h2> Welcome to Coastal Ocean Dynamics group at SDSU </h2> <br>\n<!--#BEGIN col2-main1-->\n\n<div class="col2-main1">\n  <div class="resourcesandservices">\n     <h3>Resources</h3>\n')
        for i in c.resources:
            __M_writer(u'\t<div class="res_entry">')
            __M_writer(escape(i.name))
            __M_writer(u'</div>\n')
        __M_writer(u'  </div>\n  <div class="resourcesandservices">\n     <h3>Services</h3>\n')
        for i in c.service_names:
            __M_writer(u'\t<div class="srv_entry">')
            __M_writer(escape(i.name))
            __M_writer(u'</div>\n')
        __M_writer(u'  </div>\n</div>\n<!--#End col2-main1-->\n\n<!--#BEGIN col2-main2-->\n<div class="col2-main2">\n  <div id="gallery">\n      <a href="#" class="show"><img src="')
        __M_writer(escape(c.images[0]))
        __M_writer(u'" rel="')
        __M_writer(escape(c.captions[c.images[0]]))
        __M_writer(u'" alt="" /></a>\n')
        for i in c.images[1:]:
            __M_writer(u'      <a href="#"><img src="')
            __M_writer(escape(i))
            __M_writer(u'" alt="" rel="')
            __M_writer(escape(c.captions[i]))
            __M_writer(u'"/></a>\n')
        __M_writer(u'\t<div class="caption"><div class="content"></div></div>\n  </div>\n  <div class="clear"></div>\n</div>\n <div id="calendar">\n<iframe src="http://www.google.com/calendar/embed?height=600&amp;wkst=1&amp;bgcolor=%23FFFFFF&amp;src=gbkea1jbsuei2klp6cj9ek5ge4%40group.calendar.google.com&amp;color=%231B887A&amp;ctz=Europe%2FParis" style=" border-width:0 " width="280" height="260" frameborder="0" scrolling="yes"></iframe>\n </div>\n<!--#End col2-main2-->\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headtags(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n    <script type="text/javascript">\n\t\t$(document).ready(function() {\n\n\t\t\t//Execute the slideShow\n\t\t\tslideShow();\n\n\t\t});\n\n\t\tfunction slideShow() {\n\n\t\t\t//Set the opacity of all images to 0\n\t\t\t$(\'#gallery a\').css({opacity: 0.0});\n\n\t\t\t//Get the first image and display it (set it to full opacity)\n\t\t\t$(\'#gallery a:first\').css({opacity: 1.0});\n\n\t\t\t//Set the caption background to semi-transparent\n\t\t\t$(\'#gallery .caption\').css({opacity: 0.7});\n\n\t\t\t//Resize the width of the caption according to the image width\n\t\t\t$(\'#gallery .caption\').css({width: $(\'#gallery a\').find(\'img\').css(\'width\')});\n\n\t\t\t//Get the caption of the first image from REL attribute and display it\n\t\t\t$(\'#gallery .content\').html($(\'#gallery a:first\').find(\'img\').attr(\'rel\'))\n\t\t\t.animate({opacity: 0.7}, 400);\n\n\t\t\t//Call the gallery function to run the slideshow, 6000 = change to next image after 6 seconds\n\t\t\tsetInterval(\'gallery()\',6000);\n\n\t\t}\n\n\t\tfunction gallery() {\n\n\t\t\t//if no IMGs have the show class, grab the first image\n\t\t\tvar current = ($(\'#gallery a.show\')?  $(\'#gallery a.show\') : $(\'#gallery a:first\'));\n\n\t\t\t//Get next image, if it reached the end of the slideshow, rotate it back to the first image\n\t\t\tvar next = ((current.next().length) ? ((current.next().hasClass(\'caption\'))? $(\'#gallery a:first\') :current.next()) : $(\'#gallery a:first\'));\n\n\t\t\t//Get next image caption\n\t\t\tvar caption = next.find(\'img\').attr(\'rel\');\n\n\t\t\t//Set the fade in effect for the next image, show class has higher z-index\n\t\t\tnext.css({opacity: 0.0})\n\t\t\t.addClass(\'show\')\n\t\t\t.animate({opacity: 1.0}, 1000);\n\n\t\t\t//Hide the current image\n\t\t\tcurrent.animate({opacity: 0.0}, 1000)\n\t\t\t.removeClass(\'show\');\n\n\t\t\t//Display the content\n\t\t\t$(\'#gallery .content\').html(caption);\n\n\t\t}\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_footer(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "utf-8", "line_map": {"28": 0, "34": 1, "35": 14, "36": 73, "37": 76, "38": 83, "39": 84, "40": 84, "41": 84, "42": 86, "43": 89, "44": 90, "45": 90, "46": 90, "47": 92, "48": 99, "49": 99, "50": 99, "51": 99, "52": 100, "53": 101, "54": 101, "55": 101, "56": 101, "57": 101, "58": 103, "64": 16, "68": 16, "74": 75, "78": 75, "84": 78}, "uri": "/gallery.mako", "filename": "/home/sumukh/Documents/thesis/Cyberweb/cyberweb/cyberweb/templates/gallery.mako"}
__M_END_METADATA
"""
