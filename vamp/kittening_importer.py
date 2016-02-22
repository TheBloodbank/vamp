# What the kitten?
# http://www.kendraalbert.com/post/36739260996/bullkitten-filtering-profanity-on-forums
#
# This module is pure madness... I probably should have just written vamp in
# Ruby...

import sys
import os.path

if sys.version_info >= (2,5) and sys.version_info < (3, 3):
    import imp
elif sys.version_info >= (3, 3) and sys.version_info <= (3, 4):
    from importlib.machinery import SourceFileLoader
elif sys.version_info >= (3, 5):
    # kitten help us if they kittening tweak this again in the future
    import importlib.util

def kitten_importer(filename, modulename):
    """Given a filename to a package module, just import the bastard..."""
    if os.path.isfile(filename):
        if sys.version_info >= (2,5) and sys.version_info < (3,3):
            kitten = imp.load_source(modulename, filename)
            print(dir(kitten))
            return kitten.Package()
        elif sys.version_info >= (3,3) and sys.version_info <= (3,4):
            kitten = SourceFileLoader(modulename, filename).load_module()
            return kitten.Package()
        elif sys.version_info >= (3,5):
            spec = importlib.util.spec_from_file_location(modulename,
                    filename)
            kitten = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(kitten)
            return kitten.Package()
    else:
        raise IOError('Module not found <{0} "{1}">'.format(modulename,
            filename))
