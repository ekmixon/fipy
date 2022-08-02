from __future__ import print_function
from distutils.core import Command
import os

__all__ = ["upload_products"]

class upload_products(Command):
    description = "upload FiPy compressed archives to website(s)"
    
    user_options = [('pdf', None, "upload the PDF variant of the documentation"),
                    ('html', None, "upload the HTML variant of the documentation"),
                    ('tarball', None, "upload the .tar.gz source distribution"),
                    ('winzip', None, "upload the .win32.zip distribution"),
                   ]

    def initialize_options (self):
        self.pdf = 0
        self.html = 0
        self.tarball = 0
        self.winzip = 0

    def finalize_options (self):
        pass

    def run(self):
        if self.pdf:
            fname = f'dist/fipy-{self.distribution.metadata.get_version()}.pdf'
            print("setting permissions of manual...")
            os.system('chmod -R g+w documentation/_build/latex/fipy.pdf')

            print("linking manual to `dist/`...")
            os.system('mkdir dist/')
            os.system(f'ln -f documentation/_build/latex/fipy.pdf {fname}')

            print("uploading pdf...")
            os.system(
                f"rsync -pgoDLC -e ssh {fname} {os.environ['FIPY_WWWHOST']}/download/"
            )


        if self.html:
            print("setting group and ownership of web pages...")
            os.system('chmod -R g+w documentation/_build/html/')

            print("uploading web pages...")
            # The -t flag (implicit in -a) is suddenly causing problems
            # os.system('rsync -aLC -e ssh %s %s'%('documentation/www/', os.environ['FIPY_WWWHOST']))
            os.system(
                f"rsync -rlpgoDLC -e ssh documentation/_build/html/ {os.environ['FIPY_WWWHOST']}"
            )


        if self.tarball:
            fname = f'dist/FiPy-{self.distribution.metadata.get_version()}.tar.gz'
            print(f"setting permissions for {fname} ...")
            os.system(f'chmod -R g+w {fname}')

            print("uploading tarball...")
            os.system(
                f"rsync -pgoDLC -e ssh {fname} {os.environ['FIPY_WWWHOST']}/download/"
            )


        if self.winzip:
            fname = f'dist/FiPy-{self.distribution.metadata.get_version()}.win32.zip'
            print(f"setting permissions for {fname} ...")
            os.system(f'chmod -R g+w {fname}')

            print("uploading winzip...")
            os.system(
                f"rsync -pgoDLC -e ssh {fname} {os.environ['FIPY_WWWHOST']}/download/"
            )


        print("activating web pages...")
        os.system(os.environ['FIPY_WWWACTIVATE'])
