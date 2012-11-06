"""


"""

from pyjade import utils as jadeutils
from pyramid.compat import escape
from pyjade.compiler import Compiler

prefix = 'pyjade.'
list_attributes = ['inlineTags', 'selfClosing', 'autocloseCode']
bool_attributes = ['pretty', 'compileDebug']

def includeme(config):
    """


    """

    def process(src, filename = None, parser = jadeutils.Parser,
                compiler = jadeutils.Compiler):
        """


        """

        _parser = parser(src, filename = filename)
        block = _parser.parse()
        pyjade_settings = {key[len(prefix):] : value for key, value in
            config.registry.settings.iteritems() if key.startswith(prefix)}

        for attr in list_attributes:
            parse_list(pyjade_settings, attr)

        for attr in bool_attributes:
            parse_bool(pyjade_settings, attr)

        _compiler = compiler(block, **pyjade_settings)
        return _compiler.compile().strip()

    jadeutils.process = process

    Compiler.filters.update({
        'plain': filter_plain,
        'css': filter_css,
        'javascript': filter_javascript,
        'escaped': filter_escaped
    })

    # Load pyjade.
    config.include('pyjade.ext.pyramid')

def parse_list(settings, attribute):
    """


    """

    if attribute in settings:
        settings[attribute] = (
            settings[attribute].split(','))

def parse_bool(settings, attribute):
    """


    """

    if attribute in settings:
        settings[attribute] = not (settings[attribute].lower() == 'false'
                                   or settings[attribute].lower() == 'no'
                                   or settings[attribute].lower() == 'off')

def filter_plain(x, y):
    """


    """

    return x

def filter_css(x, y):
    """


    """

    return '<style type="text/css">{0}</style>'.format(x)

def filter_javascript(x, y):
    """


    """

    return '<script type="text/javascript">{0}</script>'.format(x)

def filter_escaped(x, y):
    """

    
    """

    return escape(x)
