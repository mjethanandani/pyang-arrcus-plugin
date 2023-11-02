"""Arrcus usage guidelines plugin
"""

import optparse
import sys

from pyang import plugin
from pyang import statements
from pyang import error
from pyang.error import err_add
from pyang.plugins import lint
import re

def pyang_plugin_init():
    plugin.register_plugin(ArrcusPlugin())

class ArrcusPlugin(lint.LintPlugin):
    def __init__(self):
        lint.LintPlugin.__init__(self)
        self.namespace_prefixes = ['http://yang.arrcus.com/arcos/']
        self.modulename_prefixes = ['arcos-']
        self.mmap = {}

    def add_opts(self, optparser):
        optlist = [
            optparse.make_option("--arrcus",
                                 dest="arrcus",
                                 action="store_true",
                                 help="Validate the module(s) according " \
                                 "to Arrcus rules."),
            ]
        optparser.add_options(optlist)

    def v_chk_description(self, ctx, s):
        # if s.i_module.arg not in self.mmap:
        #    return
        arg = re.sub(r'\s+', ' ', s.arg)
        if s.parent.keyword == 'module' or s.parent.keyword == 'submodule':
            if s.parent.arg.startswith('arcos-'):
                m = re_copyright.search(arg)
                if m is None:
                    err_add(ctx.errors, s.pos, 
                            'ARRCUS_MISSING_COPYRIGHT_STATEMENT', ())
                else:
                    # Check that the year is up-to-date w.r.t the 
                    # last revision statement.
                    y = int(m.group(1))

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
            'grammar', ['description'],
            lambda ctx, s: self.v_chk_description(ctx, s))

        # register our error codes
        error.add_error_code(
            'LINT_MISSING_REQUIRED_SUBSTMT', 3,
            '%s: '
            + 'statement "%s" must have a "%s" substatement')
        
        error.add_error_code(
            'ARRCUS_MISSING_COPYRIGHT_STATEMENT', 3,
            'the module must have a Copyright statement, '
            + 'something like '
            + 'Copyright (c) 2016-2022 by Arrcus, Inc. '
            + 'All rights reserved.')

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

copyright_str = \
r"""Copyright \(c\) (20\d{2})-(20\d{2}) by Arrcus\, Inc\.
    All rights reserved\."""

re_copyright = re.compile(re.sub(r'\s+', ' ', copyright_str))