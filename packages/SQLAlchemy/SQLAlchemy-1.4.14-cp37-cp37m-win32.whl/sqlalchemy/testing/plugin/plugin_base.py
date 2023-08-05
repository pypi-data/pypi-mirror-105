# plugin/plugin_base.py
# Copyright (C) 2005-2021 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""Testing extensions.

this module is designed to work as a testing-framework-agnostic library,
created so that multiple test frameworks can be supported at once
(mostly so that we can migrate to new ones). The current target
is pytest.

"""

from __future__ import absolute_import

import abc
import logging
import re
import sys

# flag which indicates we are in the SQLAlchemy testing suite,
# and not that of Alembic or a third party dialect.
bootstrapped_as_sqlalchemy = False

log = logging.getLogger("sqlalchemy.testing.plugin_base")


py3k = sys.version_info >= (3, 0)

if py3k:
    import configparser

    ABC = abc.ABC
else:
    import ConfigParser as configparser
    import collections as collections_abc  # noqa

    class ABC(object):
        __metaclass__ = abc.ABCMeta


# late imports
fixtures = None
engines = None
exclusions = None
warnings = None
profiling = None
provision = None
assertions = None
requirements = None
config = None
testing = None
util = None
file_config = None

logging = None
include_tags = set()
exclude_tags = set()
options = None


def setup_options(make_option):
    make_option(
        "--log-info",
        action="callback",
        type=str,
        callback=_log,
        help="turn on info logging for <LOG> (multiple OK)",
    )
    make_option(
        "--log-debug",
        action="callback",
        type=str,
        callback=_log,
        help="turn on debug logging for <LOG> (multiple OK)",
    )
    make_option(
        "--db",
        action="append",
        type=str,
        dest="db",
        help="Use prefab database uri. Multiple OK, "
        "first one is run by default.",
    )
    make_option(
        "--dbs",
        action="callback",
        zeroarg_callback=_list_dbs,
        help="List available prefab dbs",
    )
    make_option(
        "--dburi",
        action="append",
        type=str,
        dest="dburi",
        help="Database uri.  Multiple OK, " "first one is run by default.",
    )
    make_option(
        "--dbdriver",
        action="append",
        type="string",
        dest="dbdriver",
        help="Additional database drivers to include in tests.  "
        "These are linked to the existing database URLs by the "
        "provisioning system.",
    )
    make_option(
        "--dropfirst",
        action="store_true",
        dest="dropfirst",
        help="Drop all tables in the target database first",
    )
    make_option(
        "--disable-asyncio",
        action="store_true",
        help="disable test / fixtures / provisoning running in asyncio",
    )
    make_option(
        "--backend-only",
        action="store_true",
        dest="backend_only",
        help="Run only tests marked with __backend__ or __sparse_backend__",
    )
    make_option(
        "--nomemory",
        action="store_true",
        dest="nomemory",
        help="Don't run memory profiling tests",
    )
    make_option(
        "--notimingintensive",
        action="store_true",
        dest="notimingintensive",
        help="Don't run timing intensive tests",
    )
    make_option(
        "--profile-sort",
        type=str,
        default="cumulative",
        dest="profilesort",
        help="Type of sort for profiling standard output",
    )
    make_option(
        "--profile-dump",
        type=str,
        dest="profiledump",
        help="Filename where a single profile run will be dumped",
    )
    make_option(
        "--postgresql-templatedb",
        type=str,
        help="name of template database to use for PostgreSQL "
        "CREATE DATABASE (defaults to current database)",
    )
    make_option(
        "--low-connections",
        action="store_true",
        dest="low_connections",
        help="Use a low number of distinct connections - "
        "i.e. for Oracle TNS",
    )
    make_option(
        "--write-idents",
        type=str,
        dest="write_idents",
        help="write out generated follower idents to <file>, "
        "when -n<num> is used",
    )
    make_option(
        "--reversetop",
        action="store_true",
        dest="reversetop",
        default=False,
        help="Use a random-ordering set implementation in the ORM "
        "(helps reveal dependency issues)",
    )
    make_option(
        "--requirements",
        action="callback",
        type=str,
        callback=_requirements_opt,
        help="requirements class for testing, overrides setup.cfg",
    )
    make_option(
        "--with-cdecimal",
        action="store_true",
        dest="cdecimal",
        default=False,
        help="Monkeypatch the cdecimal library into Python 'decimal' "
        "for all tests",
    )
    make_option(
        "--include-tag",
        action="callback",
        callback=_include_tag,
        type=str,
        help="Include tests with tag <tag>",
    )
    make_option(
        "--exclude-tag",
        action="callback",
        callback=_exclude_tag,
        type=str,
        help="Exclude tests with tag <tag>",
    )
    make_option(
        "--write-profiles",
        action="store_true",
        dest="write_profiles",
        default=False,
        help="Write/update failing profiling data.",
    )
    make_option(
        "--force-write-profiles",
        action="store_true",
        dest="force_write_profiles",
        default=False,
        help="Unconditionally write/update profiling data.",
    )
    make_option(
        "--dump-pyannotate",
        type=str,
        dest="dump_pyannotate",
        help="Run pyannotate and dump json info to given file",
    )
    make_option(
        "--mypy-extra-test-path",
        type=str,
        action="append",
        default=[],
        dest="mypy_extra_test_paths",
        help="Additional test directories to add to the mypy tests. "
        "This is used only when running mypy tests. Multiple OK",
    )


def configure_follower(follower_ident):
    """Configure required state for a follower.

    This invokes in the parent process and typically includes
    database creation.

    """
    from sqlalchemy.testing import provision

    provision.FOLLOWER_IDENT = follower_ident


def memoize_important_follower_config(dict_):
    """Store important configuration we will need to send to a follower.

    This invokes in the parent process after normal config is set up.

    This is necessary as pytest seems to not be using forking, so we
    start with nothing in memory, *but* it isn't running our argparse
    callables, so we have to just copy all of that over.

    """
    dict_["memoized_config"] = {
        "include_tags": include_tags,
        "exclude_tags": exclude_tags,
    }


def restore_important_follower_config(dict_):
    """Restore important configuration needed by a follower.

    This invokes in the follower process.

    """
    global include_tags, exclude_tags
    include_tags.update(dict_["memoized_config"]["include_tags"])
    exclude_tags.update(dict_["memoized_config"]["exclude_tags"])


def read_config():
    global file_config
    file_config = configparser.ConfigParser()
    file_config.read(["setup.cfg", "test.cfg"])


def pre_begin(opt):
    """things to set up early, before coverage might be setup."""
    global options
    options = opt
    for fn in pre_configure:
        fn(options, file_config)


def set_coverage_flag(value):
    options.has_coverage = value


def post_begin():
    """things to set up later, once we know coverage is running."""
    # Lazy setup of other options (post coverage)
    for fn in post_configure:
        fn(options, file_config)

    # late imports, has to happen after config.
    global util, fixtures, engines, exclusions, assertions, provision
    global warnings, profiling, config, testing
    from sqlalchemy import testing  # noqa
    from sqlalchemy.testing import fixtures, engines, exclusions  # noqa
    from sqlalchemy.testing import assertions, warnings, profiling  # noqa
    from sqlalchemy.testing import config, provision  # noqa
    from sqlalchemy import util  # noqa

    warnings.setup_filters()


def _log(opt_str, value, parser):
    global logging
    if not logging:
        import logging

        logging.basicConfig()

    if opt_str.endswith("-info"):
        logging.getLogger(value).setLevel(logging.INFO)
    elif opt_str.endswith("-debug"):
        logging.getLogger(value).setLevel(logging.DEBUG)


def _list_dbs(*args):
    print("Available --db options (use --dburi to override)")
    for macro in sorted(file_config.options("db")):
        print("%20s\t%s" % (macro, file_config.get("db", macro)))
    sys.exit(0)


def _requirements_opt(opt_str, value, parser):
    _setup_requirements(value)


def _exclude_tag(opt_str, value, parser):
    exclude_tags.add(value.replace("-", "_"))


def _include_tag(opt_str, value, parser):
    include_tags.add(value.replace("-", "_"))


pre_configure = []
post_configure = []


def pre(fn):
    pre_configure.append(fn)
    return fn


def post(fn):
    post_configure.append(fn)
    return fn


@pre
def _setup_options(opt, file_config):
    global options
    options = opt


@pre
def _set_nomemory(opt, file_config):
    if opt.nomemory:
        exclude_tags.add("memory_intensive")


@pre
def _set_notimingintensive(opt, file_config):
    if opt.notimingintensive:
        exclude_tags.add("timing_intensive")


@pre
def _monkeypatch_cdecimal(options, file_config):
    if options.cdecimal:
        import cdecimal

        sys.modules["decimal"] = cdecimal


@post
def _init_symbols(options, file_config):
    from sqlalchemy.testing import config

    config._fixture_functions = _fixture_fn_class()


@post
def _set_disable_asyncio(opt, file_config):
    if opt.disable_asyncio or not py3k:
        from sqlalchemy.testing import asyncio

        asyncio.ENABLE_ASYNCIO = False


@post
def _engine_uri(options, file_config):

    from sqlalchemy import testing
    from sqlalchemy.testing import config
    from sqlalchemy.testing import provision

    if options.dburi:
        db_urls = list(options.dburi)
    else:
        db_urls = []

    extra_drivers = options.dbdriver or []

    if options.db:
        for db_token in options.db:
            for db in re.split(r"[,\s]+", db_token):
                if db not in file_config.options("db"):
                    raise RuntimeError(
                        "Unknown URI specifier '%s'.  "
                        "Specify --dbs for known uris." % db
                    )
                else:
                    db_urls.append(file_config.get("db", db))

    if not db_urls:
        db_urls.append(file_config.get("db", "default"))

    config._current = None

    expanded_urls = list(provision.generate_db_urls(db_urls, extra_drivers))

    for db_url in expanded_urls:
        log.info("Adding database URL: %s", db_url)

        if options.write_idents and provision.FOLLOWER_IDENT:  # != 'master':
            with open(options.write_idents, "a") as file_:
                file_.write(provision.FOLLOWER_IDENT + " " + db_url + "\n")

        cfg = provision.setup_config(
            db_url, options, file_config, provision.FOLLOWER_IDENT
        )
        if not config._current:
            cfg.set_as_current(cfg, testing)


@post
def _requirements(options, file_config):

    requirement_cls = file_config.get("sqla_testing", "requirement_cls")
    _setup_requirements(requirement_cls)


def _setup_requirements(argument):
    from sqlalchemy.testing import config
    from sqlalchemy import testing

    if config.requirements is not None:
        return

    modname, clsname = argument.split(":")

    # importlib.import_module() only introduced in 2.7, a little
    # late
    mod = __import__(modname)
    for component in modname.split(".")[1:]:
        mod = getattr(mod, component)
    req_cls = getattr(mod, clsname)

    config.requirements = testing.requires = req_cls()

    config.bootstrapped_as_sqlalchemy = bootstrapped_as_sqlalchemy


@post
def _prep_testing_database(options, file_config):
    from sqlalchemy.testing import config

    if options.dropfirst:
        from sqlalchemy.testing import provision

        for cfg in config.Config.all_configs():
            provision.drop_all_schema_objects(cfg, cfg.db)


@post
def _reverse_topological(options, file_config):
    if options.reversetop:
        from sqlalchemy.orm.util import randomize_unitofwork

        randomize_unitofwork()


@post
def _post_setup_options(opt, file_config):
    from sqlalchemy.testing import config

    config.options = options
    config.file_config = file_config


@post
def _setup_profiling(options, file_config):
    from sqlalchemy.testing import profiling

    profiling._profile_stats = profiling.ProfileStatsFile(
        file_config.get("sqla_testing", "profile_file"),
        sort=options.profilesort,
        dump=options.profiledump,
    )


def want_class(name, cls):
    if not issubclass(cls, fixtures.TestBase):
        return False
    elif name.startswith("_"):
        return False
    elif (
        config.options.backend_only
        and not getattr(cls, "__backend__", False)
        and not getattr(cls, "__sparse_backend__", False)
        and not getattr(cls, "__only_on__", False)
    ):
        return False
    else:
        return True


def want_method(cls, fn):
    if not fn.__name__.startswith("test_"):
        return False
    elif fn.__module__ is None:
        return False
    elif include_tags:
        return (
            hasattr(cls, "__tags__")
            and exclusions.tags(cls.__tags__).include_test(
                include_tags, exclude_tags
            )
        ) or (
            hasattr(fn, "_sa_exclusion_extend")
            and fn._sa_exclusion_extend.include_test(
                include_tags, exclude_tags
            )
        )
    elif exclude_tags and hasattr(cls, "__tags__"):
        return exclusions.tags(cls.__tags__).include_test(
            include_tags, exclude_tags
        )
    elif exclude_tags and hasattr(fn, "_sa_exclusion_extend"):
        return fn._sa_exclusion_extend.include_test(include_tags, exclude_tags)
    else:
        return True


def generate_sub_tests(cls, module):
    if getattr(cls, "__backend__", False) or getattr(
        cls, "__sparse_backend__", False
    ):
        sparse = getattr(cls, "__sparse_backend__", False)
        for cfg in _possible_configs_for_cls(cls, sparse=sparse):
            orig_name = cls.__name__

            # we can have special chars in these names except for the
            # pytest junit plugin, which is tripped up by the brackets
            # and periods, so sanitize

            alpha_name = re.sub(r"[_\[\]\.]+", "_", cfg.name)
            alpha_name = re.sub(r"_+$", "", alpha_name)
            name = "%s_%s" % (cls.__name__, alpha_name)
            subcls = type(
                name,
                (cls,),
                {"_sa_orig_cls_name": orig_name, "__only_on_config__": cfg},
            )
            setattr(module, name, subcls)
            yield subcls
    else:
        yield cls


def start_test_class_outside_fixtures(cls):
    _do_skips(cls)
    _setup_engine(cls)


def stop_test_class(cls):
    # close sessions, immediate connections, etc.
    fixtures.stop_test_class_inside_fixtures(cls)

    # close outstanding connection pool connections, dispose of
    # additional engines
    engines.testing_reaper.stop_test_class_inside_fixtures()


def stop_test_class_outside_fixtures(cls):
    engines.testing_reaper.stop_test_class_outside_fixtures()
    provision.stop_test_class_outside_fixtures(config, config.db, cls)
    try:
        if not options.low_connections:
            assertions.global_cleanup_assertions()
    finally:
        _restore_engine()


def _restore_engine():
    if config._current:
        config._current.reset(testing)


def final_process_cleanup():
    engines.testing_reaper.final_cleanup()
    assertions.global_cleanup_assertions()
    _restore_engine()


def _setup_engine(cls):
    if getattr(cls, "__engine_options__", None):
        opts = dict(cls.__engine_options__)
        opts["scope"] = "class"
        eng = engines.testing_engine(options=opts)
        config._current.push_engine(eng, testing)


def before_test(test, test_module_name, test_class, test_name):

    # format looks like:
    # "test.aaa_profiling.test_compiler.CompileTest.test_update_whereclause"

    name = getattr(test_class, "_sa_orig_cls_name", test_class.__name__)

    id_ = "%s.%s.%s" % (test_module_name, name, test_name)

    profiling._start_current_test(id_)


def after_test(test):
    fixtures.after_test()
    engines.testing_reaper.after_test()


def after_test_fixtures(test):
    engines.testing_reaper.after_test_outside_fixtures(test)


def _possible_configs_for_cls(cls, reasons=None, sparse=False):
    all_configs = set(config.Config.all_configs())

    if cls.__unsupported_on__:
        spec = exclusions.db_spec(*cls.__unsupported_on__)
        for config_obj in list(all_configs):
            if spec(config_obj):
                all_configs.remove(config_obj)

    if getattr(cls, "__only_on__", None):
        spec = exclusions.db_spec(*util.to_list(cls.__only_on__))
        for config_obj in list(all_configs):
            if not spec(config_obj):
                all_configs.remove(config_obj)

    if getattr(cls, "__only_on_config__", None):
        all_configs.intersection_update([cls.__only_on_config__])

    if hasattr(cls, "__requires__"):
        requirements = config.requirements
        for config_obj in list(all_configs):
            for requirement in cls.__requires__:
                check = getattr(requirements, requirement)

                skip_reasons = check.matching_config_reasons(config_obj)
                if skip_reasons:
                    all_configs.remove(config_obj)
                    if reasons is not None:
                        reasons.extend(skip_reasons)
                    break

    if hasattr(cls, "__prefer_requires__"):
        non_preferred = set()
        requirements = config.requirements
        for config_obj in list(all_configs):
            for requirement in cls.__prefer_requires__:
                check = getattr(requirements, requirement)

                if not check.enabled_for_config(config_obj):
                    non_preferred.add(config_obj)
        if all_configs.difference(non_preferred):
            all_configs.difference_update(non_preferred)

    if sparse:
        # pick only one config from each base dialect
        # sorted so we get the same backend each time selecting the highest
        # server version info.
        per_dialect = {}
        for cfg in reversed(
            sorted(
                all_configs,
                key=lambda cfg: (
                    cfg.db.name,
                    cfg.db.driver,
                    cfg.db.dialect.server_version_info,
                ),
            )
        ):
            db = cfg.db.name
            if db not in per_dialect:
                per_dialect[db] = cfg
        return per_dialect.values()

    return all_configs


def _do_skips(cls):
    reasons = []
    all_configs = _possible_configs_for_cls(cls, reasons)

    if getattr(cls, "__skip_if__", False):
        for c in getattr(cls, "__skip_if__"):
            if c():
                config.skip_test(
                    "'%s' skipped by %s" % (cls.__name__, c.__name__)
                )

    if not all_configs:
        msg = "'%s' unsupported on any DB implementation %s%s" % (
            cls.__name__,
            ", ".join(
                "'%s(%s)+%s'"
                % (
                    config_obj.db.name,
                    ".".join(
                        str(dig)
                        for dig in exclusions._server_version(config_obj.db)
                    ),
                    config_obj.db.driver,
                )
                for config_obj in config.Config.all_configs()
            ),
            ", ".join(reasons),
        )
        config.skip_test(msg)
    elif hasattr(cls, "__prefer_backends__"):
        non_preferred = set()
        spec = exclusions.db_spec(*util.to_list(cls.__prefer_backends__))
        for config_obj in all_configs:
            if not spec(config_obj):
                non_preferred.add(config_obj)
        if all_configs.difference(non_preferred):
            all_configs.difference_update(non_preferred)

    if config._current not in all_configs:
        _setup_config(all_configs.pop(), cls)


def _setup_config(config_obj, ctx):
    config._current.push(config_obj, testing)


class FixtureFunctions(ABC):
    @abc.abstractmethod
    def skip_test_exception(self, *arg, **kw):
        raise NotImplementedError()

    @abc.abstractmethod
    def combinations(self, *args, **kw):
        raise NotImplementedError()

    @abc.abstractmethod
    def param_ident(self, *args, **kw):
        raise NotImplementedError()

    @abc.abstractmethod
    def fixture(self, *arg, **kw):
        raise NotImplementedError()

    def get_current_test_name(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def mark_base_test_class(self):
        raise NotImplementedError()


_fixture_fn_class = None


def set_fixture_functions(fixture_fn_class):
    global _fixture_fn_class
    _fixture_fn_class = fixture_fn_class
