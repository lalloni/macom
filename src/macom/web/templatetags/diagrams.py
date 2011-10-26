# -*- coding: UTF-8 -*-

from django.template.base import Library, Node, TemplateSyntaxError
from django.utils.encoding import smart_str
from django.template.loader import get_template
from django.core.urlresolvers import reverse
from django.template.context import Context
from django.template.defaulttags import kwarg_re
from django.conf import settings 
from django.template.defaultfilters import stringfilter
import re

register = Library()

class DiagramNode(Node):
    def __init__(self, view_name, args, kwargs):
        self.view_name = view_name
        self.args = args
        self.kwargs = kwargs
    def render(self, context):
        args = [arg.resolve(context) for arg in self.args]
        kwargs = dict([(smart_str(k, 'ascii'), v.resolve(context)) for k, v in self.kwargs.items()])
        diagram_source_url = context['request'].build_absolute_uri(reverse(self.view_name, args=args, kwargs=kwargs, current_app=context.current_app))
        new_context = Context(context, autoescape=context.autoescape)
        new_context['diagram_render_url'] = "%s/%s" % (settings.DIAGRAM_SERVICE_URL, diagram_source_url)
        new_context['diagram_source_url'] = diagram_source_url
        if not getattr(self, 'nodelist', False):
            self.nodelist = get_template('diagram.html')
        return self.nodelist.render(new_context)

@register.tag
def diagram(parser, token):
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument"
                                  " (path to a view)" % bits[0])
    viewname = bits[1]
    args = []
    kwargs = {}
    bits = bits[2:]
    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError("Malformed arguments to diagram tag")
            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)
            else:
                args.append(parser.compile_filter(value))
    return DiagramNode(viewname, args, kwargs)

FORBIDDEN_RE = re.compile(r'\W')

@register.filter
@stringfilter
def as_id(value):
    return FORBIDDEN_RE.sub('_', value)

@register.filter
def direction(value):
    inbound = outbound = ''
    if value.direction_inbound:
        inbound = 'in'
    if value.direction_outbound:
        outbound = 'out'
    return '%s%s' % (inbound, outbound)

@register.filter
def single(value):
    return value.replace('\n', r'\n').replace('\r', r'\n')
