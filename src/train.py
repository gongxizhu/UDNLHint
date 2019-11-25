import sys
import os
import argparse
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
from config import hparams
from model import argument_parser
import tensorflow as tf


def train():
    translator_parser = argparse.ArgumentParser()
    argument_parser.add_arguments(translator_parser)
    argument_parser.FLAGS, unparsed = translator_parser.parse_known_args(['--' + k + '=' + str(v) for k, v in hparams.items()])
    tf.app.run(main=argument_parser.main, argv=[os.getcwd() + "\\model\\argument_parser.py"] + unparsed)

if __name__ == "__main__":
    train()
