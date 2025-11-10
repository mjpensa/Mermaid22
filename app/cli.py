import argparse
import sys
import json
from pdf_pipeline import process_pdf
from docx_pipeline import process_docx

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('--log-json')
    parser.add_argument('--dpi', type=int, default=300)
    parser.add_argument('--max-height-ratio', type=float, default=0.8)
    parser.add_argument('--skip-invalid', action='store_true')
    args = parser.parse_args()
    logs = []
    def log_callback(*args):
        logs.append(args)
    if args.input.endswith('.pdf'):
        process_pdf(args.input, args.output, log_callback)
    elif args.input.endswith('.docx'):
        process_docx(args.input, args.output, log_callback)
    if args.log_json:
        with open(args.log_json, 'w') as f:
            json.dump(logs, f)

if __name__ == '__main__':
    main()