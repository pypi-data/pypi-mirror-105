import argparse
import keyword
import os
import sys
from argparse import ArgumentParser
from typing import Optional, List, Dict, Callable
from warnings import warn

from hbreader import hbread
from jsonasobj2 import as_dict
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.formatutils import camelcase
from template_config_model.config_model import Config

# ================
#  DEFAULTS
# ================
default_keywords = [
    'linkml',
    'LOD',
    'Modeling',
    'Linked',
    'open',
    'data',
    'model']

default_classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Healthcare Industry',
    'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
]

default_template_directory = os.path.join(os.path.dirname(__file__), "templates")
default_output_directory = os.getcwd()

# Stuff to ignore in the template
skip_suffixes = [".pyc"]


class Configurator:
    """
    Process all files in the test_templates directory, processing it and saving the output in the targets directory.  If the
    file name appears in the "special processing" table, the special process is called first, and the output is then
    formatted using the using the variables in the configuration file.  Otherwise, the content of the file is handled
    directly

    """

    def __init__(self, conf_file_location: str, template_dir: str, target_dir: str, hard_reset: bool):
        """
        Set up a configuration run
        :param conf_file_location: Location of a file that conforms to the Config schema
        :param template_dir: Base directory of input test_templates to be processed
        :param target_dir: Base directory of where the template information goes
        :param hard_reset: True means we configure everything, even if a copy already exists
        """
        self.config: Config = yaml_loader.load(conf_file_location, Config)
        self.massage_config_file()
        self.config_dict: Dict = as_dict(self.config)
        self.template_dir = template_dir
        self.target_dir = target_dir
        self.hard_reset = hard_reset

    def massage_config_file(self) -> None:
        if not self.config.model_py_name:
            self.config.model_py_name = self.config.model_name.replace('-', '_')
        if not self.config.model_py_name.isidentifier():
            warn(f"model_py_name ({self.config.model_py_name}) is not a valid identifier")
        self.config.model_root_class = camelcase(self.config.model_root_class)
        if not self.config.model_description:
            self.config.model_description = self.config.model_synopsis
        if keyword.iskeyword(self.config.model_py_name):
            warn(f"model_py_name ({self.config.model_py_name}) is a python keyword")
        if not self.config.model_url:
            self.config.model_url = f"https://github.com/{self.config.model_organization}/{self.config.model_name}"
        if not self.config.classifiers:
            self.config.classifiers = default_classifiers
        if not self.config.keywords:
            self.config.keywords = default_keywords

    def build(self) -> None:
        """ Walk the template directory processing and transferring files """
        def do_process(fname) -> bool:
            for sfx in skip_suffixes:
                if fname.endswith(sfx):
                    return False
            return True

        for dirpath, _, fnames in os.walk(self.template_dir):
            for fname in fnames:
                if do_process(fname):
                    self.process(dirpath, fname)

    def process(self, dirpath: str, fname: str) -> None:
        """ Process dirpath/fname """
        template_file = os.path.join(dirpath, fname)
        target_file = os.path.join(self.target_dir, os.path.relpath(template_file, self.template_dir))
        rel_target = os.path.relpath(target_file, os.getcwd())
        if self.hard_reset or not os.path.exists(target_file):
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
            template_text = hbread(template_file)
            if fname in self.special_processing:
                template_text = self.special_processing[fname](self, template_text)
            else:
                template_text = template_text.format(**self.config_dict)
            with open(target_file, 'w') as f:
                f.write(template_text)
            print(f"{rel_target} written")
        else:
            print(f"{rel_target} skipped - copy already exists")

    @staticmethod
    def strip_config_comments(txt: str) -> str:
        return '\n'.join([line for line in txt.split('\n') if not line.startswith(';')])

    def proc_makefile(self, makefile_text: str) -> str:
        return makefile_text.format(generate_targets=' '.join([entry.code.text for entry in self.config.generate]),
                                    **self.config_dict)

    def proc_setup_cfg(self, setup_cfg_text: str) -> str:

        def build_data_files() -> str:
            template = "{model_py_name}/{{component}} = {model_py_name}/{{component}}/*".format(**self.config_dict)
            filelist = [template.format(component="model")]
            for entry in self.config.generate:
                filelist.append(template.format(component=entry.code.text))
            return '\n    '.join(filelist)

        def build_keywords() -> str:
            return '\n    ' + '\n    '.join(self.config.keywords)

        def build_classifiers() -> str:
            return '\n    ' + '\n    '.join(self.config.classifiers)

        return setup_cfg_text.format(data_files=build_data_files(),
                                     classifiers_=build_classifiers(),
                                     keywords_=build_keywords(),
                                     **self.config_dict)

    def build_httpd_rules(self) -> None:
        pass

    special_processing: Dict[str, Callable[["Configurator", str], str]] = {
        "Makefile": proc_makefile,
        "setup.cfg": proc_setup_cfg
    }


def genargs() -> ArgumentParser:
    """
    Generate an input string parser
    :return: parser
    """
    parser = ArgumentParser(prog="configure", description="Configure a LinkML model repository")
    parser.add_argument("configfile", help="Model configuration file", type=argparse.FileType('r'))
    parser.add_argument("--templatedir", help="Template source directory (Default: template_configurator/templates)",
                        default=default_template_directory)
    parser.add_argument("-t", "--targetdir", help="Output target directory (Default: current working directory",
                        default=os.getcwd())
    parser.add_argument("--reset", help="Hard reset -- regenerate all files from scratch", action="store_true")
    return parser


def main(argv: Optional[List[str]] = None) -> None:
    opts = genargs().parse_args(argv)
    if not os.path.isdir(opts.templatedir):
        raise NotADirectoryError(f"Template directory: {opts.templatedir} does not exist")
    if not os.path.isdir(opts.targetdir):
        raise NotADirectoryError(f"Target directory: {opts.targetdir} does not exist")
    Configurator(opts.configfile, opts.templatedir, opts.targetdir, opts.reset).build()


if __name__ == '__main__':
    main()
