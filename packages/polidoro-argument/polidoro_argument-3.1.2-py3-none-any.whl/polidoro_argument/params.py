"""
Classes to inspect the methods signature and configure the Argument or Command
"""

import inspect

from polidoro_argument.action import ArgumentAction, CommandAction


class _Params(object):
    def __init__(self, method, aliases=None, command_alias=None, **kwargs):
        self.method = method
        self.method_name = method.__name__
        self.kwargs = kwargs
        self.positional = []
        self.var_positional = None
        self.keyword = []
        self.var_keyword = None
        self.nargs = None
        self.added = False
        self.remainder = False
        self.command_alias = [] if command_alias is None else command_alias
        self.aliases = getattr(method, 'aliases', {}) if aliases is None else aliases

        self.inspect_signature()
        self.kwargs.setdefault('help', '')

    def inspect_signature(self):
        for name, info in inspect.signature(self.method).parameters.items():
            if name == '_remainder':
                self.remainder = True
            elif not name.startswith('_'):
                if info.kind == inspect.Parameter.VAR_POSITIONAL:
                    self.var_positional = name
                elif info.kind == inspect.Parameter.VAR_KEYWORD:
                    self.var_keyword = name
                elif info.default == info.empty:
                    self.positional.append(name)
                else:
                    self.keyword.append(name)

        nargs = len(self.positional)
        if self.var_positional or self.var_keyword:
            nargs = '%d+' % nargs
        elif self.keyword:
            nargs = '%d-%d' % (nargs, len(self.keyword))

        self.nargs = nargs

    @staticmethod
    def get_final_parser(parser, method):
        # Get the final parser based on method.__qualname__
        full_name = method.__qualname__.replace('setup.<locals>.', '')
        for name in [n.lower() for n in reversed(full_name.split('.')[:-1])]:
            subparsers = _Params.get_subparsers(parser)
            sub_parser = subparsers.choices.get(name, None)
            if sub_parser is None:
                clazz = _Params.get_class_that_defined_object(method)
                clazz_attrs = {k: v for k, v in clazz.__dict__.items() if
                               not k.startswith('__') and not isinstance(v, staticmethod) and not inspect.isfunction(v)}
                clazz_attrs.setdefault('help', '')
                clazz_attrs.setdefault('description', clazz_attrs['help'])
                sub_parser = subparsers.add_parser(
                    name,
                    prog='%s %s' % (parser.prog, name),
                    **clazz_attrs
                )
            parser = sub_parser

        return parser

    @staticmethod
    def get_subparsers(parser):
        # Return the subparsers or create if not exists
        if parser.subparsers:
            return parser.subparsers
        return parser.add_subparsers()

    @staticmethod
    def get_class_that_defined_object(obj):
        if inspect.ismethod(obj):
            for cls in inspect.getmro(obj.__self__.__class__):
                if cls.__dict__.get(obj.__name__) is obj:
                    return cls
            obj = obj.__func__  # fallback to __qualname__ parsing
        if inspect.isfunction(obj):
            try:
                cls = getattr(inspect.getmodule(obj),
                              obj.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
                if isinstance(cls, type):
                    return cls
            except AttributeError:
                pass
        return getattr(obj, '__objclass__', None)


class _ArgumentParams(_Params):
    def add_argument(self, parser):
        parser = self.get_final_parser(parser, self.method)
        parser.add_argument(
            '--' + self.method_name,
            action=ArgumentAction,
            method=self.method,
            nargs=self.nargs,
            positional=self.positional,
            var_positional=self.var_positional,
            keyword=self.keyword,
            var_keyword=self.var_keyword,
            remainder=self.remainder,
            **self.kwargs
        )


class _CommandParams(_Params):
    def add_command(self, parser):
        parser = self.get_final_parser(parser, self.method)
        subparsers = self.get_subparsers(parser)
        sub_parser = subparsers.add_parser(
            self.method_name,
            aliases=self.command_alias,
            prog='%s %s' % (parser.prog, self.method_name),
            add_help=not self.remainder,
            **self.kwargs
        )

        if self.positional:
            self.kwargs.setdefault('metavar', ' '.join(self.positional))

        sub_parser.add_argument(
            'positional',
            action=CommandAction,
            method=self.method,
            nargs=self.nargs,
            positional=self.positional,
            var_positional=self.var_positional,
            keyword=self.keyword,
            var_keyword=self.var_keyword,
            remainder=self.remainder,
            **self.kwargs
        )

        for kw in self.keyword:
            argument_kwargs = {}
            default = inspect.signature(self.method).parameters[kw].default
            if isinstance(default, bool):
                argument_kwargs = {
                    'action': ('store_%s' % (not default)).lower(),
                    'default': default
                }
            name = ('--' + kw, )
            if kw in self.aliases:
                name += ('-' + self.aliases[kw], )
            sub_parser.add_argument(*name, **argument_kwargs)
