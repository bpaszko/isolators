import argparse
import os

from validation.directory_validator import Validator


def parse_args():
    parser = argparse.ArgumentParser(description='Run validation on directory or labels.csv. Uses only one model.')
    parser.add_argument('--threshold', default=0.9, help='Classification threshold (between 0 and 1)')
    required_named = parser.add_argument_group('Required keyword arguments')
    required_named.add_argument('--model_path', required=True, help='Path to model')
    required_named.add_argument('--eval_path', required=True, help='Path to labels.csv or \
                                 directory with unlabeled images - means no objects are present.')
    args = vars(parser.parse_args())
    eval_path = args['eval_path']
    if not eval_path.endswith('.csv') and not os.path.isdir(eval_path):
        print('%s is not a csv file or directory!' % eval_path)
        exit(1)

    return args


def main():
    args = parse_args()
    path_to_model, eval_path = args['model_path'], args['eval_path']
    threshold = float(args['threshold'])
    validator = Validator(path_to_model, threshold)
    if eval_path.endswith('.csv'):
        validator.evaluate([eval_path])
    else:
        validator.evaluate_directory(eval_path)
    print(validator)


if __name__ == '__main__':
    main()