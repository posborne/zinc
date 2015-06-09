#!/usr/bin/env python
import argparse
from svdconverter.parser import SVDParser


def build_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help="Path to SVD XML File")
    return parser

def main():
    args = build_arg_parser().parse_args()
    parser = SVDParser.for_xml_file(args.path)
    device = parser.get_device()
    import pprint
    pprint.pprint(device.__dict__)



if __name__ == '__main__':
    main()

