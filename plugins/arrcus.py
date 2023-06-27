"""Arrcus usage guidelines plugin
"""

import optparse
import sys

from pyang import plugin
from pyang import statements
from pyang import error
from pyang.error import err_add
from pyang.plugins import lint

def pyang_plugin_init():
    plugin.register_plugin(ArrcusPlugin())

class ArrcusPlugin(lint.LintPlugin):
    def __init__(self):
        lint.LintPlugin.__init__(self)
        self.namespace_prefixes = ['http://yang.arrcus.com/arcos/']
        self.modulename_prefixes = ['arcos-']

    def add_opts(self, optparser):
        optlist = [
            optparse.make_option("--arrcus",
                                 dest="arrcus",
                                 action="store_true",
                                 help="Validate the module(s) according " \
                                 "to Arrcus rules."),
            ]
        optparser.add_options(optlist)

    def setup_ctx(self, ctx):
        if not ctx.opts.arrcus:
            return
        self._setup_ctx(ctx)

    def _setup_ctx(self, ctx):
        ctx.max_line_len = 70

        # register our grammar validation funs
        statements.add_validation_var(
            '$chk_required',
            lambda keyword: keyword in _required_substatements)

        statements.add_validation_fun(
            'grammar', ['$chk_required'],
            lambda ctx, s: lint.v_chk_required_substmt(ctx, s))

        # register our error codes
        error.add_error_code(
            'LINT_MISSING_REQUIRED_SUBSTMT', 3,
            '%s: '
            + 'statement "%s" must have a "%s" substatement')

_required_substatements = {
    'module': (('contact', 'organization', 'description', 'revision'),
               "RFC 8407: 4.8"),
    'submodule': (('contact', 'organization', 'description', 'revision'),
                  "RFC 8407: 4.8"),
    'extension':(('description',), "RFC 8407: 4.14"),
    'feature':(('description',), "RFC 8407: 4.14"),
    'identity':(('description',), "RFC 8407: 4.14"),
    'typedef':(('description',), "RFC 8407: 4.13,4.14"),
    'grouping':(('description',), "RFC 8407: 4.14"),
    'augment':(('description',), "RFC 8407: 4.14"),
    'rpc':(('description',), "RFC 8407: 4.14"),
    'notification':(('description',), "RFC 8407: 4.14,4.16"),
    'container':(('description',), "RFC 8407: 4.14"),
    'leaf':(('description',), "RFC 8407: 4.14"),
    'leaf-list':(('description',), "RFC 8407: 4.14"),
    'list':(('description',), "RFC 8407: 4.14"),
    'choice':(('description',), "RFC 8407: 4.14"),
    'anyxml':(('description',), "RFC 8407: 4.14"),
    }
