from __future__ import print_function
import sys
import tempfile
import shutil
from vamp.config import Config
from vamp.bank import Bank
from vamp.manifest import Manifest
from vamp.in_a_world import ensure_path

class PackageBase:
    """The base definition of a package class."""

    # User-friendly name of the package
    name = None

    # Package name, as it will be known by vamp
    package_name = None

    # Simple requirements array. Should contain a list of packages this
    # package requires
    requires = []

    def __init__(self):
        pass

    def check_system_requirements(self):
        """Check the system requirements.

        When called, this should check to see if the necessary things are
        present on the system for this package to be installed and run.

        Returns True if they are met or False if they are not."""
        pass

    def install(self, workdir, installdir, verbose=False):
        """Installs a package.

        'workdir' is the working directory the installer should use. It's
        temporary, existing only during the installation. Packages shouldn't
        worry about cleaning it up, as the package hander will do that for them.

        'installdir' is the directroy where the package should install to.

        'verbose' indicates whether the package installer should be verbose or
        not.

        This install method should return an array that contains the absolute
        paths to each of the binary executables it installed or 'None' if
        there was a problem (the script can also bail if there's a problem,
        just be sure to print useful information to the user as to why it
        failed).
        """
        pass

class PackageHandler:
    __borg_state = {}

    def __init__(self, force=False):
        self.__dict__ = self.__borg_state

        self.c = Config()
        self.force = force
        self.b = Bank()
        self.m = Manifest()
        self.cache = {}
        self._installed = {}
        self._working_dirs = set()

    def _check_deps(self, pkg):
        """Checks that the dependencies are installed for a package."""
        all_deps = True
        for dep in pkg.requires:
            if dep not in self.m.get('PackageHandler', 'installed'):
                print("!! Error, dependency '{0}' not found for package" +
                " '{1}'!".format(dep, pkg.name))
                all_deps = False

        if not pkg.check_system_requirements():
            print("!! Error, system requirements not satisfied for" +
            " '{0}'!".format(pkg.name))
            all_deps = False

        return all_deps

    def _get_package(self, package):
        """Returns a package object, either loading as needed or from cache."""
        if package in self.cache:
            return self.cache[package]
        else:
            p = self.b.get_package(package)
            self.cache[package] = p
            return p

    def _cleanup(self, directory):
        """Given a directory, clean it up without prejudice.

        Will only clean up directries in the vamp infrastructure."""
        if directory in self._working_dirs:
            shutil.rmtree(directory)
            self._working_dirs.remove(directory)
        else:
            raise OSError("Error! Attempt to remove directory outside of vamp" + \
                    "infrastructure! '{0}'".format(directory))

    def _get_workdir(self, package):
        """Given a package name, get a working directory for it."""
        wdir = tempfile(prefix=package)
        self._working_dirs.add(wdir)
        ensure_path(wdir)
        return wdir

    def _get_installdir(self, package):
        """Given a package name, get the installation directory for it."""
        indir = "{0}/{1}".format(self.c.get('paths', 'install', True), package)
        self._working_dirs.add(indir)
        ensure_path(indir)
        return indir

    def _install(self, package):
        """Installs a package."""
        pkg = self._get_package(package)
        if pkg is None:
            print("Error! Unable to find package '{0}'!".format(package))
            sys.exit(1)

        if self._check_deps(pkg):
            print("> Installing '{0}'...".format(pkg.name))
            working_dir = self._get_workdir(package)
            install_dir = self._get_installdir(package)
            bins = pkg.install(working_dir, install_dir, self.c.get('globals',
                'verbose'))
            if bins is None:
                print("!! Error installing package '{0}'!".format(package))
                self._cleanup(working_dir)
                self._cleanup(install_dir)
            else:
                self._cleanup(working_dir)
        else:
            print("!! Error installing package '{0}'".format(package) + \
                    ", problem with dependencies!")
            sys.exit(1)

    def _find_build_deps(self, pkg):
        """Internal, recursive, function for finding the build deps of a
        package."""
        deps = []
        deps.append(pkg.package_name)
        for req in pkg.requires:
            if req not in self._installed:
                deppkg = self._get_package(req)
                deps.extend(self._find_build_deps(deppkg))
        return deps

    def build_deps(self, package):
        """Given a package, build the dependencies needed to install it."""
        pkg = self._get_package(package)
        # Pre-cache the installed packages
        self._installed = self.m.get('PackageHandler', 'installed')
        return list(set(self._find_build_deps(pkg)))

    def install(self, packages):
        """Given a list of packages, install them.

        If the list is not dependency resolved, you will probably get errors
        on install."""
        for p in packages:
            self._install(p)
