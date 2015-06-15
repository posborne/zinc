#!/usr/bin/env python
import argparse
import sys
import click
from cmsis_svd.parser import SVDParser
from svdconverter.generators.zinc_ioregs import ZincIoregsCodeGenerator


@click.group("svdconvert")
def svdconvert():
    """Perform conversions from CMSIS SVD input files"""


@svdconvert.command()
@click.argument("path")
@click.option("--output", "-o", default=None)
def ioregs(path, output):
    """Perform conversion to an ioregs register description module"""
    parser = SVDParser.for_xml_file(path)
    device = parser.get_device()

    # NOTE: output file will be closed when it goes out of scope and
    # is garbage collected
    if output is not None:
        output_stream = open(output, "w")
    else:
        output_stream = sys.stdout

    generator = ZincIoregsCodeGenerator(device, output_stream)
    generator.generate()


if __name__ == '__main__':
    svdconvert()
