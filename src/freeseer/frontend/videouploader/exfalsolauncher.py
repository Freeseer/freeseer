'''
Created on Dec 9, 2011

@author: jord
'''

_is_available = False
EXPECTED_VERSION_TUPLE = [(2, 3, 2), (2, 3, 1)]

try:
#    global _is_available
    from quodlibet import const
    for version in EXPECTED_VERSION_TUPLE:
        if (version[0] == const.VERSION_TUPLE[0] and
            version[1] == const.VERSION_TUPLE[1] and
            version[2] == const.VERSION_TUPLE[2]):
            _is_available = True
            break
except ImportError as e:
    pass
except Exception as e:
    # might get an index error
    pass

from multiprocessing.process import Process

def is_available():
    return _is_available

# http://code.google.com/p/quodlibet/source/browse/quodlibet/exfalso.py?name=quodlibet-2.3.1
# http://code.google.com/p/quodlibet/source/browse/quodlibet/exfalso.py?name=quodlibet-2.3.2

#def run_in_new_process(path):
#    p = Process(target=run, name="exfalso", args=(str(path),))
#    p.start()

def run(path):
    import quodlibet
    from quodlibet import config
    config.init(const.CONFIG)
    backend, library, player = quodlibet.init(icon="exfalso", backend="nullbe")

    from quodlibet.qltk.exfalsowindow import ExFalsoWindow
    from quodlibet import widgets
    widgets.main = ExFalsoWindow(library, path)
    quodlibet.main(widgets.main)
    quodlibet.quit((backend, library, player))
    config.write(const.CONFIG)
    
    