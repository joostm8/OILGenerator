from XMLparser import *
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filename", help="filename of xml file to convert to oil", metavar="FILE")
args = parser.parse_args()
oil_file_generator = SimulinkToOIL(args.filename)
oil_file_generator.generate_files()