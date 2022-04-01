"""Arrcus usage guidelines plugin
"""

import optparse
import sys

from pyang import plugin
from pyang import statements
from pyang import error
from pyang.error import err_add
from pyang.plugins import lint
from pyang import grammar

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

        statements.add_validation_fun(
            'grammar', ['*'],
            lambda ctx, s: v_chk_hyphenated_names(ctx, s))

        # register our error codes
        error.add_error_code(
            'LINT_MISSING_REQUIRED_SUBSTMT', 3,
            '%s: '
            + 'statement "%s" must have a "%s" substatement')
        error.add_error_code(
            'LINT_NOT_HYPHENATED', 4,
            '%s is not hyphenated, e.g., using underscore')

_required_substatements = {
    'module': (('contact', 'organization', 'description', 'revision'),
               "RFC 8407: 4.8"),
    'submodule': (('contact', 'organization', 'description', 'revision'),
                  "RFC 8407: 4.8"),
    'revision':(('reference',), "RFC 8407: 4.8"),
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

def v_chk_hyphenated_names(ctx, stmt):
    if stmt.keyword in grammar.stmt_map:
        (arg_type, subspec) = grammar.stmt_map[stmt.keyword]
        if ((arg_type == 'identifier') and
            not_hyphenated(stmt.arg)):
            error.err_add(ctx.errors, stmt.pos, 'LINT_NOT_HYPHENATED', stmt.arg)

def not_hyphenated(name):
    ''' Returns True if name is not hyphenated '''
    if name == None:
        return False
    # Check for upper-case and underscore
    return ("_" in name)
