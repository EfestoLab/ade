import argparse
import unittest

def arguments():
    parser = argparse.ArgumentParser(
        description='Command line for file system manager')
    parser.add_argument('-t', '--test', help='run test', action="store_false")
    parser.add_argument('-bp', '--build_path', help='Path to be checked')

    args = vars(parser.parse_args())
    return args


if __name__ == '__main__':
	args = arguments()
	if args.get('test'):
		testSuite = unittest.main('unit_test', verbosity=2)