from __future__ import print_function
import os
import sys

msg = "\nThe GDK rendering GTK matplotlib backend is missing or not installed properly.\n"
msg += "See http://matplotlib.org/faq/usage_faq.html#what-is-a-backend.\n"
msg += "Is the PYTHONPATH environment variable set correctly?\n"
msg += "Please verify your installation by running on the command line:\n"
msg += "python -c 'from matplotlib.backends import backend_gdk'\n"
msg += "\n"
msg += "This module is optional and required in order to use "
msg += "ASE's simple GUI (ase-gui).\n"
msg += "If you don't wish to use ase-gui ignore this error, otherwise\n"
msg += "please install the matplotlib package containing the missing backend\n"
msg += "using your distribution package manager, i.e.:\n"
msg += "\n"
msg += "  Debian/Ubuntu: sudo apt-get python-matplotlib\n"
msg += "\n"
msg += "  OpenSUSE: yast -i python-matplotlib\n"
msg += "\n"
msg += "  Red Hat/Fedora: yum install python-matplotlib\n"
msg += "\n"
msg += "or perform manual installation, preferably as non-root user,\n"
msg += "following http://matplotlib.sourceforge.net/users/installing.html\n"
msg += "after installing the http://www.pygtk.org/downloads.html dependency first."

if locals().get('display'):
    try:
        import matplotlib.backends as b
        f = os.path.join(os.path.dirname(b.__file__), '_backend_gdk.so')
        open(f).close()
        from matplotlib.backends import backend_gdk
    except ImportError:
        print(msg, file=sys.stderr)
        raise
    except IOError:
        print(("\nThe backend file %s does not exist.\n" % f) + msg, file=sys.stderr)
        raise
