import argparse
import importlib
from common import TimedValue, timed

def main(args: argparse.Namespace):
    try:
        with open(args.file) as f:
            contents = f.read().splitlines()
    except FileNotFoundError:
        print(f"File {args.file} does not exist, exiting...")
        exit(1)

    day_module = importlib.import_module(f"day{args.day}")
    part_one_sol: TimedValue = timed(day_module.solve_part_one)(contents) #type: ignore
    part_two_sol: TimedValue = timed(day_module.solve_part_two)(contents) #type: ignore

    print(f'Part 1: {part_one_sol.value} ({part_one_sol.elapsed_time*1000:.3f}ms)')
    print(f'Part 2: {part_two_sol.value} ({part_two_sol.elapsed_time*1000:.3f}ms)')


if (__name__ == '__main__'):
    data_dir = 'data/'
    parser = argparse.ArgumentParser()
    parser.add_argument('day', type=int, default=1, help='Day to run')
    parser.add_argument('-f', '--file', type=str, help=f'File to run. If not specified \'{data_dir}input\' for the day will be used')
    parser.add_argument('-t', '--test', action='store_true', help=f'Use \'{data_dir}inputTest\' file for the day if none specified')
    args = parser.parse_args()
    if (args.file is None):
        args.file = f'{data_dir}input{args.day}' if not args.test else f'{data_dir}input{args.day}Test'
    main(args)
