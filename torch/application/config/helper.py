import os
import subprocess
import logging
import sys
from enum import Enum

class LIFECYCLE_ACTIONS(Enum):
    DEPLOY = 'deploy'
    TEARDOWN = 'teardown'
    RELEASE = 'release' # Reserved for future

class LIFECYCLE_COMMANDS(Enum):
    DEPLOY = ('init', 'plan', 'apply')
    TEARDOWN = ('init', 'plan', 'destroy')
    RELEASE = () # Reserved for future

class BuildMetaData():

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.src_folder = os.getcwd()
        self.platform_folder = os.path.normpath(os.path.join(self.src_folder, 'platform'))
        self.deployments_folder = os.path.normpath(os.path.join(self.src_folder, 'deployments'))
        self.build_spec_folder = os.path.normpath(os.path.join(self.deployments_folder, 'buildspec'))
        self.builds_folder = os.path.normpath(os.path.join(self.deployments_folder, 'builds'))
        self.current_build = None
        self.current_build_folder = None

    def set_folders_for_build(self):
        try:
            if not os.path.exists(self.platform_folder):
                raise FileNotFoundError("Missing folder: {}".format(self.platform_folder))
            if not os.path.exists(self.deployments_folder):
                os.makedirs(self.deployments_folder)
            if not os.path.exists(self.build_spec_folder):
                os.makedirs(self.build_spec_folder)
            if not os.path.exists(self.builds_folder):
                os.makedirs(self.builds_folder)
        except FileNotFoundError as fn:
            self.logger.error("Missing required folder - {}".format(self.platform_folder))
            sys.exit(1)
        except FileExistsError as fe:
            self.logger.error("Folder exists - {}".format(self.platform_folder))
            sys.exit(1)
        except NotADirectoryError as nd:
            self.logger.error("Not a directory - {}".format(self.platform_folder))
            sys.exit(1)
        except PermissionError as pe:
            self.logger.error("Permission issue - {}".format(self.platform_folder))
            sys.exit(1)

    def set_current_build(self):
        try:
            current_build_spec = os.path.normpath(os.path.join(self.build_spec_folder, 'currentBuild'))
            if os.path.exists(current_build_spec):
                with open(current_build_spec, 'r+') as f:
                    self.current_build = int(f.read()) + 1
                    f.seek(0)
                    f.write(str(self.current_build))
                    f.truncate()
            else:
                with open(current_build_spec, 'w') as f:
                    self.current_build = 1
                    f.write(str(self.current_build))
            self.current_build_folder = os.path.normpath(os.path.join(self.builds_folder, str(self.current_build)))
            self.set_current_build_folder()
        except Exception as e:
            self.logger.error('Issue while setting the current build number : {}'.format(e))
            sys.exit(1)

    def set_current_build_folder(self):
        try:
            if not os.path.exists(self.current_build_folder):
                os.makedirs(self.current_build_folder)
        except Exception as e:
            self.logger.error('Issue while creating the current build folder : {}'.format(e))
            sys.exit(1)

def set_context_for_build():
    build_meta_data = BuildMetaData()
    build_meta_data.set_folders_for_build()
    build_meta_data.set_current_build()

def build_acid(*args, **kwargs):
    # Build ACID
    pass
