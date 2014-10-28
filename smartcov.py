from importlib import import_module

import coverage
import pytest


__version__ = '0.1'


def pytest_addoption(parser):
    parser.addoption(
        '--no-cov',
        action='store_false',
        dest='coverage',
        default=True,
    )


@pytest.mark.tryfirst
def pytest_load_initial_conftests(early_config, parser, args):
    paths_hook = _get_paths_hook(
        early_config.inicfg.get('smartcov_paths_hook', ''))
    ns = parser.parse_known_args(args)
    cov_paths = paths_hook(ns.file_or_dir)
    if ns.coverage and cov_paths:
        plugin = CoveragePlugin(cov_paths)
        plugin.start()
        early_config.pluginmanager.register(plugin, '_coverage')


def _null_paths_hook(paths):
    return []


def _get_paths_hook(hook_import_path):
    if not hook_import_path:
        return _null_paths_hook
    module_path, funcname = hook_import_path.rsplit('.', 1)
    module = import_module(module_path)
    return getattr(module, funcname)


class CoveragePlugin(object):
    def __init__(self, cov_source):
        self.cov_source = cov_source
        self.cov_config = '.coveragerc'
        self.cov_data_file = '.coverage'

        self.cov = None

    def start(self):
        self.cov = coverage.coverage(
            source=self.cov_source,
            data_file=self.cov_data_file,
            config_file=self.cov_config,
        )
        self.cov.erase()
        self.cov.start()

    def stop(self):
        self.cov.stop()
        self.cov.save()

    def report(self, stream):
        stream.sep('-', 'coverage')
        pct = int(
            self.cov.report(file=FilteredStream(stream), ignore_errors=True))
        stream.write("Overall test coverage: %s%%\n" % pct)
        if pct < 100:
            self.cov.html_report(ignore_errors=True)
            stream.write(
                "Coverage HTML written to %s dir\n" % self.cov.config.html_dir)

    def pytest_sessionfinish(self):
        self.stop()

    def pytest_terminal_summary(self, terminalreporter):
        self.report(terminalreporter._tw)


class FilteredStream(object):
    """Filter the coverage terminal report to lines we are interested in."""
    def __init__(self, stream):
        self.stream = stream
        self._interesting = False
        self._buffered = []

    def line_is_interesting(self, line):
        """Return True, False, or None.

        True means always output, False means never output, None means output
        only if there are interesting lines.

        """
        if line.startswith('Name'):
            return None
        if line.startswith('--------'):
            return None
        if line.startswith('TOTAL'):
            return None
        if '100%' in line:
            return False
        return True

    def write(self, msg):
        is_interesting = self.line_is_interesting(msg)
        if is_interesting:
            if not self._interesting:
                for line in self._buffered:
                    self.stream.write(line)
                self._interesting = True
            self.stream.write(msg)
        elif is_interesting is None:
            if not self._interesting:
                self._buffered.append(msg)
            else:
                self.stream.write(msg)
