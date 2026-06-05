import argparse
import os
from tqdm import tqdm
from transformers import AutoTokenizer
from transformers.models.gpt2.tokenization_gpt2 import bytes_to_unicode


parser = argparse.ArgumentParser(description="Tokenizer training script.")

parser.add_argument("--base_tokenizer", type=str, default="gpt2-medium", help="Base tokenizer.")
parser.add_argument("--txt_file_path", type=str, required=True, help="Path to the text file for training.")
parser.add_argument("--batch_size", type=int, default=300000, help="Batch size for training")
parser.add_argument("--vocab_size", type=int, default=2048, help="Vocabulary size for the tokenizer")
parser.add_argument("--new_tokenizer_path", type=str, required=True,  help="Name of new tokenizer")
parser.add_argument("--push_to_hub", action='store_true', help="Whether to push the tokenizer to Hugging Face's model hub.")

args = parser.parse_args()

print("Base Tokenizer:", args.base_tokenizer)
print("Text File Path:", args.txt_file_path)
print("Batch Size:", args.batch_size)
print("Vocabulary Size:", args.vocab_size)
print("New Tokenizer Path:", args.new_tokenizer_path)
print("Push to Hub:", args.push_to_hub)

# Iterator for Training
def batch_iterator():
    with open(args.txt_file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        for i in tqdm(range(0, len(lines), args.batch_size)):
        # for i in range(0, len(lines), args.batch_size):
            if i % 100000 == 0: print(i,'lines proceeded...')
            yield lines[i:i+args.batch_size]

# Load base tokenizer
tokenizer = AutoTokenizer.from_pretrained(args.base_tokenizer)
base_vocab = list(bytes_to_unicode().values())

# Train and save new tokenizer
new_tokenizer = tokenizer.train_new_from_iterator(
    batch_iterator(), vocab_size=args.vocab_size, initial_alphabet=base_vocab
)
new_tokenizer.save_pretrained(args.new_tokenizer_path, push_to_hub=args.push_to_hub)
