import argparse
import os

from validation import *
from detection import MainDetector


def parse_args():
    parser = argparse.ArgumentParser(description='Run validation on directory or labels.csv. For one model provide '
                                                 'path to model and threshold. For app validation provide config '
                                                 '(only labels.csv). '
                                                 '')
    parser.add_argument('--threshold', default=0.9, help='Classification threshold [0-1]. Only for single model.)')
    required_named = parser.add_argument_group('Required keyword arguments')
    required_named.add_argument('--config_path', required=True, help='Path to model or config')
    required_named.add_argument('--eval_path', required=True, help='Path to labels.csv or \
                                 directory with unlabeled images - means no objects are present (only single model).')
    required_named.add_argument('--mode', required=True, help='\'single\' for single model, \'all\' for whole app.')
    args = vars(parser.parse_args())
    eval_path = args['eval_path']
    mode = args['mode']

    if mode not in ['single', 'all']:
        print('%s - unknown type! Use \'single\' or \'all\'' % mode)
        exit(1)

    if not eval_path.endswith('.csv') and not os.path.isdir(eval_path):
        print('%s is not a csv file or directory!' % eval_path)
        exit(1)

    if os.path.isdir(eval_path) and mode == 'all':
        print('Cannot use \'all\' mode with directory!')
        exit(1)

    return args


def main():
    args = parse_args()
    config_path, eval_path = args['config_path'], args['eval_path']
    threshold = float(args['threshold'])
    mode = args['mode']
    if mode == 'all':
        detector = MainDetector(config_path=config_path)
        validator = MainValidator(detector=detector)
    else:
        if eval_path.endswith('.csv'):
            validator = SingleValidator(path_to_model=config_path, threshold=threshold)
        else:
            validator = DirectoryValidator(path_to_model=config_path, threshold=threshold)

    validator.evaluate(eval_path)
    print(validator)


if __name__ == '__main__':
    main()
