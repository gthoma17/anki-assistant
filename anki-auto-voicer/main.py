import sys
from google_cloud_speech_client import text_to_speech


def get_args():
	if(len(sys.argv) < 2):
		print_help()
		exit(1)
	return {
		'output_folder': sys.argv[1]
	}

def print_help():
	print("Usage...")
	print("python main.py <anki deck folder>")

def main():
	args = get_args()
	text_to_speech("Hello World", f"{args['output_folder']}/test")

if __name__ == '__main__':
	main()
