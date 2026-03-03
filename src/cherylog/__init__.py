from cherylog import bootstrap
from cherylog import config_provider
from cherylog import common
from cherylog import units
from cherylog import log_formatter

def main():
    container = bootstrap.Container()
    bootstrapper = bootstrap.Bootstrapper(container)
    bootstrapper.run()

__all__ = [
    'bootstrap',
    'config_provider',
    'common',
    'units',
    'log_formatter',

    'main'
]