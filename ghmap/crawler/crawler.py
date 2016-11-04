#!/usr/bin/env python3

import json
import argparse
import configparser

import github

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()

    if args.config:
        config = configparser.ConfigParser()
        config.read(args.config)

    output = args.output if args.output else 'location.json'

    github.crawl(output=output)
