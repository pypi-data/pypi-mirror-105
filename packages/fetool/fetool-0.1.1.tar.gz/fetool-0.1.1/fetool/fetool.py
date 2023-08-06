#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2021 4Paradigm
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
from version import version
from csv_to_parquet import csv_to_parquet_args
from sample_parquet import sample_parquet_args
from inspect_parquet import inspect_parquet_args
from check_skew import check_skew_args
from benchmark import benchmark_args


def main():
    parser = argparse.ArgumentParser(prog="fetool")
    subparsers = parser.add_subparsers()

    version_command = subparsers.add_parser("version", help="Print the version of fetool")
    version_command.set_defaults(func=version)

    csv_to_parquet_command = subparsers.add_parser("csv_to_parquet", help="csv_to_parquet $input_csv_path $output_parquet_path")
    csv_to_parquet_command.add_argument("input_csv_path", type=str, help="The path of input CSV files")
    csv_to_parquet_command.add_argument("output_parquet_path", type=str, help="The path of output parquet files")
    csv_to_parquet_command.set_defaults(func=csv_to_parquet_args)

    sample_parquet_command = subparsers.add_parser("sample_parquet", help="sample_parquet $parquet_path")
    sample_parquet_command.add_argument("parquet_path", type=str, help="The path of parquet files")
    sample_parquet_command.set_defaults(func=sample_parquet_args)

    inspect_parquet_command = subparsers.add_parser("inspect_parquet", help="inspect_parquet $parquet_path")
    inspect_parquet_command.add_argument("parquet_path", type=str, help="The path of parquet files")
    inspect_parquet_command.set_defaults(func=inspect_parquet_args)

    check_skew_command = subparsers.add_parser("check_skew", help="check_skew $parquet_path")
    check_skew_command.add_argument("parquet_path", type=str, help="The path of parquet files")
    check_skew_command.set_defaults(func=check_skew_args)

    benchmark_command = subparsers.add_parser("benchmark", help="benchmark $command")
    benchmark_command.add_argument("command", type=str, help="The path of parquet files")
    benchmark_command.set_defaults(func=benchmark_args)

    args = parser.parse_args()
    if getattr(args, "func", None):
        args.func(args)
    else :
        # Print help messing if not passing any argument
        parser.print_help()    


if __name__ == "__main__":
    main()

    