#!/usr/bin/env python
import argparse
import sys
from cmsis_svd.parser import SVDParser
from svdconverter.generators.zinc_ioregs import ZincIoregsCodeGenerator


def build_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help="Path to SVD XML File")
    return parser


def main():
    args = build_arg_parser().parse_args()
    parser = SVDParser.for_xml_file(args.path)
    device = parser.get_device()
    generator = ZincIoregsCodeGenerator(device, sys.stdout)
    generator.generate()


if __name__ == '__main__':
    main()

