import rpmdiff
import dnf
import os
from shutil import copyfile

class Differ:
    """Abstract class for Differ inheritance"""

    def __init__(self, pkg1 = None, pkg2 = None):
        raise Exception("This class is abstract and cannot make instances")

    def get_diff(self):
        raise Exception("Method get_diff was not implemented")

class Rpm_Differ(Differ):
    def __init__(self, pkg1, pkg2, additional):
        self._pkg1 = (pkg1, additional[0], additional[1])
        self._pkg2 = (pkg2, additional[2], additional[3])
        self.base = None
        self.diff = None

    def __get_package_path(self, pkg):
        repodir = "{release}-{arch}".format(
                                      release=pkg[1],
                                      arch=pkg[2]
                                    )
        for entity in os.listdir("cachedir"):
            if entity.startswith(repodir) and not (entity.endswith(".solvx") or entity.endswith(".solv")):
                print("dir: ", entity)
                repodir = entity

        repodir = "cachedir/{repodir}/packages/".format(repodir=repodir)

        for entity in os.listdir(repodir):
            print("pkg: ", entity)
            if entity.startswith(pkg[0]):
                pkg_name = entity
        return os.path.join(repodir, pkg_name)

    def _download_pkg(self, pkg):
        reponame = "{release}-{arch}".format(
                                            release=pkg[1],
                                            arch=pkg[2]
                                        )
        print("Release:%s\nArch:%s" % (pkg[1], pkg[2]))
        baseurl = "https://mirrors.nic.cz/fedora/linux/releases/{release}/Everything/{arch}/os/".format(
                                                                                                     release=pkg[1],
                                                                                                     arch=pkg[2]
                                                                                                )
        #self.base = dnf.Base()
        with dnf.Base() as self.base:
            conf = self.base.conf
            conf.cachedir = "cachedir"
            self.base.repos.add_new_repo(reponame,
                                    conf,
                                    baseurl=(baseurl,)
                                   )
            self.base.fill_sack()
            q = self.base.sack.query()
            q = q.available()
            q = q.filter(name=pkg[0])
            for package in q:
                print(package)
            self.base.download_packages(q)
            path = self.__get_package_path(pkg)
            pkgID = pkg[0] + "." + pkg[1] + "." + pkg[2]
            copyfile(path, "rpms/"+ pkgID +".rpm")
            return pkgID

    def get_diff(self):
        to_download = (self._pkg1, self._pkg2)
        pkgIDs = []
        for i, pkg in enumerate(to_download):
            pkgID = self._download_pkg(pkg)
            print("ID: " + pkgID)
            pkgIDs.append(pkgID)

        self.diff = rpmdiff.Rpmdiff("rpms/" + pkgIDs[0] + ".rpm",
                                    "rpms/" + pkgIDs[1] + ".rpm"
                                    )
        return self.diff.result

def load_differ(pkg1, pkg2, category, additional = None):
    if category == "RPM":
        return Rpm_Differ(pkg1, pkg2, additional)
    return None
