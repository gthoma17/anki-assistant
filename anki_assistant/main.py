import argparse
import json

from args.Face import Face
from args.Gender import Gender
from args.Operation import Operation


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("output_folder", help="The Anki deck folder", type=str)
    parser.add_argument('--language', '-l',
                        help="language code (any BCP-47 compliant language code should work, but only en-US and ja-JP "
                             "have been tested)",
                        type=str,
                        default='en-US'
                        )
    parser.add_argument('--gender', '-g',
                        help="gender for the voice to speak with (don't read this as an author's opinion on gender -- "
                             "this is an API limitation ;-))",
                        type=Gender,
                        choices=list(Gender),
                        default=Gender.neutral)
    parser.add_argument('--face', '-f',
                        help="Which face of the card should we apply the operation to (default front)",
                        type=Face,
                        choices=list(Face),
                        default=Face.front)
    parser.add_argument('--unspoken_separator', '-s',
                        help="A substring after which text should be ignored and not sent to the cloud for "
                             "text-to-speech (useful for hints or notes)",
                        type=str,
                        default="<br />")
    parser.add_argument('--operation', '-o',
                        help="What operation the script should perform (adding or removing)",
                        type=Operation,
                        choices=list(Operation),
                        default=Operation.add_speech)

    return parser.parse_args()


def main():
    args = get_args()

    with open(f"{args.output_folder}/deck.json", 'r') as deck_file:
        deck = json.load(deck_file)

    args.operation.get_method()(deck, args)

    with open(f"{args.output_folder}/deck.json", 'w') as deck_file:
        json.dump(deck, deck_file)


if __name__ == '__main__':
    main()
