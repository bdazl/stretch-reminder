from balloon import balloon_tip
import time
import argparse
import sys

parser = argparse.ArgumentParser(description='Reminds user/coder to stretch.')
parser.add_argument('-m', '--minutes', type=int, default=30,
                    help='Show notification with a specified minute interval.')                    
parser.add_argument('-c', '--count', type=int, default=sys.maxsize,
                    help='How many notifications will be shown (default to intmax)')
parser.add_argument('-t', '--title', default='Stretch reminder',
                    help='The title of the tooltip window.')
parser.add_argument('-M', '--message', default='Stand up!',
                    help='The message of the tooltip window.')

args = parser.parse_args()

for i in range(args.count):
    print('Waiting {} minutes for tooltip {} / {}'.format(args.minutes, i+1, args.count))
    time.sleep(60 * args.minutes)
    balloon_tip(title=args.title, msg=args.message)