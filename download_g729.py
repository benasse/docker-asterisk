#!/usr/bin/env python3

"""Script that download and setup codecs from asterisk.hosting.lv

The code for this script is contained in a single file and is
self-documented. With ``--help``, you can get the purpose of the
script as well as the options it accepts.

"""

import argparse
import logging
import logging.handlers
import os
import sys
import requests

logger = logging.getLogger(os.path.splitext(os.path.basename(sys.argv[0]))[0])


class CustomFormatter(argparse.RawDescriptionHelpFormatter,
                      argparse.ArgumentDefaultsHelpFormatter):
    pass


def parse_args(args=sys.argv[1:]):
    """Parse arguments."""
    parser = argparse.ArgumentParser(
        description=sys.modules[__name__].__doc__,
        formatter_class=CustomFormatter)

    g = parser.add_mutually_exclusive_group()
    g.add_argument("--debug", "-d", action="store_true",
                   default=False,
                   help="enable debugging")
    g.add_argument("--silent", "-s", action="store_true",
                   default=False,
                   help="don't log")

    g = parser.add_argument_group("settings")
    g.add_argument("--codecs", nargs=' ',
                   default=['g729','g723'],
                   type=list,
                   help="Codec to install")
    g.add_argument("--asterisk-version",
                   default='13',
                   type=str,
                   help="The version of asteirsk")
    g.add_argument("--binary-type",
                   default='gcc4-glibc-x86_64-pentium4',
                   type=str,
                   help="The version of asteirsk")
    g.add_argument("--asterisk-module-path",
                   default='/usr/lib/asterisk/modules/',
                   type=str,
                   help="Module folder of asterisk")
    g.add_argument("--remove", "-r", action="store_true",
                   default=False,
                   help="Remove codecs")

    return parser.parse_args(args)

def setup_logging(options):
    """Configure logging."""
    root = logging.getLogger("")
    root.setLevel(logging.WARNING)
    logger.setLevel(options.debug and logging.DEBUG or logging.INFO)
    if not options.silent:
        if not sys.stderr.isatty():
            facility = logging.handlers.SysLogHandler.LOG_DAEMON
            sh = logging.handlers.SysLogHandler(address='/dev/log',
                                                facility=facility)
            sh.setFormatter(logging.Formatter(
                "{0}[{1}]: %(message)s".format(
                    logger.name,
                    os.getpid())))
            root.addHandler(sh)
        else:
            ch = logging.StreamHandler()
            ch.setFormatter(logging.Formatter(
                "%(levelname)s[%(name)s] %(message)s"))
            root.addHandler(ch)

def download_binary(codec,ast_version,binary_type,module_path):
    # NOTE won't work with asterisk 1.8
    url = 'http://asterisk.hosting.lv/bin/codec_' + codec + '-ast' + str(ast_version) + '0-' + binary_type + '.so'
    logger.info("Download url: {}".format(url))
    r = requests.get(url, allow_redirects=True)
    open( module_path + 'codec_' + codec + '.so', 'wb').write(r.content)

def delete_binary(codec,module_path):
    logger.info('Remove :' + module_path + 'codec_' + codec + '.so')
    os.remove( module_path + 'codec_' + codec + '.so')

def main(options):
    """print args"""
    logger.debug(options)
    for codec in options.codecs:
        if options.remove:
            delete_binary(codec, options.asterisk_module_path)
        else:
            download_binary(codec, options.asterisk_version, options.binary_type, options.asterisk_module_path)

if __name__ == "__main__":
    options = parse_args()
    setup_logging(options)

    try:
        print("\n".join(main(options)))
    except Exception as e:
        logger.exception("%s", e)
        sys.exit(1)
    sys.exit(0)
