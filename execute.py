import sys
import argparse
from poke_api.management import commands


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='◓ Pokermon api command line utils!! ◓',
        usage="python execute.py import_pokemon --path <path_to_csv_file>")

    parser.add_argument('command', metavar='command', type=str,
                        help="Available Commands: import_pokemon ")

    parser.add_argument('-p', '--path', type=str,
                        required='import_pokemon' in sys.argv, help='path to csv file containing pokemon data')

    args = parser.parse_args()

    if not args.command in commands.keys():
        raise Exception("Invalid command provided\nPlease use one of the following:\n"
                        + f" - {str(list(commands.keys()))}")

    commands[args.command](args)
