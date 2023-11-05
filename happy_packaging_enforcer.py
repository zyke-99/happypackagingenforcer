import argparse
import os.path
import sys

import javalang
from javalang import parse

VERSION = '0.0.1'
EXIT_CODES = {
    0: "Success! No constraint violations found",
    1: "Invalid target path provided",
    2: "Constraints violated"
}
TECHNICAL_PACKAGE_NAMES = [
    'util',
    'tools',
    'config',
    'internal',
    'impl',
    'framework',
    'api',
    'lib',
    'test',
    'helper',
    'adapter',
    'proxy',
    'model',
    'dto',
    'service',
    'manager',
    'controller',
    'repository',
    'factory',
    'handler',
    'interceptor',
    'listener',
    'filter',
    'builder',
    'configuration'
]


def exit_with_code(exit_code):
    print("{1}. Exiting with code {0}.".format(exit_code, EXIT_CODES.get(exit_code)))
    sys.exit(exit_code)


def init_cli():
    parser = argparse.ArgumentParser(prog='happy_packaging_enforcer',
                                     description='Welcome to HappyPackagingEnforcer v. {0}!\n\nThis tool was built '
                                                 'for ensuring a Java project package structure '
                                                 'adheres to the following constrains: \n1. Packages should never '
                                                 'depend on sub-packages\n2. Sub-packages should not introduce new '
                                                 'concepts, just more details\n3. Packages should reflect '
                                                 'business-concepts, not technical ones.'.format(VERSION),
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-v', '--version', action='version',
                        version='happy_packaging_enforcer version {0}'.format(VERSION))
    parser.add_argument('-t', '--target', help='Specify the path to Java sources which are to be checked',
                        required=True)
    parser.add_argument('-ff', '--fail-fast', help='Fail on first constraint violation occurrence', action='store_true')
    # For version 0.0.2
    # parser.add_argument('-s', '--skip-naming-check', help='Skips checks for non-business-concept package names', action='store_true')
    # parser.add_argument('-add', '--additional-violation-names', help='Path to a .txt file with comma delimited '
    #                                                                  'package names which violate the naming constraint')
    return parser


def perform_arg_checks(args):
    if not os.path.isdir(args.target):
        exit_with_code(1)


def sub_package_check():
    return None


def get_package_names(directory_path):
    package_declarations = []

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as java_file:
                    java_source_code = java_file.read()
                    tree = parse.parse(java_source_code)

                    # Extract the package declaration
                    for path, node in tree.filter(javalang.tree.PackageDeclaration):
                        package_declaration = node.name
                        package_declarations.append(package_declaration)

    return list(set(package_declarations))


def naming_check(target):
    package_names = get_package_names(target)
    for package_name in package_names:
        #placeholder
        yield None


def run():
    parser = init_cli()
    args = parser.parse_args()
    perform_arg_checks(args)
    naming_check(args.target)
    exit_with_code(0)


if __name__ == '__main__':
    run()
