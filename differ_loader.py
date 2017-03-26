import rpmdiff
import dnf
import os

class Differ:
    """Abstract class for Differ inheritance"""

    def __init__(self, pkg1 = None, pkg2 = None):
        raise "This class is abstract and cannot make instances"

    def get_diff(self):
        raise "Method get_diff was not implemented"

class Rpm_Differ(Differ):
    def __init__(self, pkg1, pkg2):
        self.pkg1 = pkg1
        self.pkg2 = pkg2
        self.diff = None

    def _download_pkg():
        base = dnf.Base()

    def get_diff(self):
        text_diff = None
        rdir = os.getcwd()
        try:
            os.chdir("%s/rpms" % rdir)
            self.diff = rpmdiff.Rpmdiff(self.pkg1,
                                self.pkg2
                               )
            text_diff = self.diff.textdiff()
        finally:
            os.chdir(rdir)
        for r in self.diff.result:
            print(r)
        return text_diff

def load_differ(pkg1 = None, pkg2 = None, category = "RPM"):
    return Rpm_Differ(pkg1, pkg2)
