from validation.main_validator import MainValidator
from detection.main_detector import MainDetector

import time
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Run validation on directory or labels.csv. Uses only one model.')
    required_named = parser.add_argument_group('Required keyword arguments')
    required_named.add_argument('--config_path', required=True, help='Path to config')
    required_named.add_argument('--eval_path', required=True, help='Path to labels.csv')

    args = vars(parser.parse_args())
    eval_path = args['eval_path']
    if not eval_path.endswith('.csv'):
        print('%s is not a csv file!' % eval_path)
        exit(1)

    return args


def main():
    args = parse_args()
    config_path, labels_path = args['config_path'], args['eval_path']
    detector = MainDetector(config_path)
    validator = MainValidator(detector)
    t1 = time.time()
    validator.evaluate(labels_path)
    print("Time taken: %f" % (time.time()-t1))
    print(validator)


if __name__ == '__main__':
    main()