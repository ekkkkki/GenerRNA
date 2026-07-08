# GenerRNA: A Generative Language Model for *de novo* RNA Design

[![Hugging Face Model](https://img.shields.io/badge/%F0%9F%A4%97%20Model-pfnet%2FGenerRNA-yellow)](https://huggingface.co/pfnet/GenerRNA)
[![Paper (PLOS ONE)](https://img.shields.io/badge/Paper-PLOS%20ONE%202024-orange)](https://doi.org/10.1371/journal.pone.0310814)
[![Preprint (bioRxiv)](https://img.shields.io/badge/Preprint-bioRxiv-red)](https://doi.org/10.1101/2024.02.01.578496)
[![Project page](https://img.shields.io/badge/Project-Page-2ea44f)](https://ekkkkki.github.io/GenerRNA/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

> 🤗 **The model weights are hosted on Hugging Face → [`pfnet/GenerRNA`](https://huggingface.co/pfnet/GenerRNA).**
> This repository mirrors the **code and documentation**. To download or run the model, get the weights from Hugging Face (see [Quickstart](#quickstart)).

**GenerRNA is a generative pre-trained language model for *de novo* RNA sequence design.** It is a Transformer (decoder-only, GPT-style) model that learns the "language" of RNA from millions of natural sequences and can generate novel, realistic RNA sequences **without any structural input, functional label, or sequence alignment**. To our knowledge, GenerRNA is the first application of a generative language model to RNA generation.

With GenerRNA you can:

- **Generate RNA in a zero-shot manner** to explore the RNA sequence space, or
- **Fine-tune on your own dataset** to generate RNAs belonging to a particular family or possessing specific characteristics (e.g., high binding affinity to a target protein).

> Introduced in the peer-reviewed paper *PLOS ONE* (2024): [GenerRNA: A generative pre-trained language model for *de novo* RNA design](https://doi.org/10.1371/journal.pone.0310814).

## Links

- 🤗 **Model & weights (Hugging Face):** https://huggingface.co/pfnet/GenerRNA
- 🌐 **Project page:** https://ekkkkki.github.io/GenerRNA/
- 📄 **Paper (PLOS ONE):** https://doi.org/10.1371/journal.pone.0310814
- 📝 **Preprint (bioRxiv):** https://doi.org/10.1101/2024.02.01.578496

## Table of Contents

- [Model Summary](#model-summary)
- [Key Features](#key-features)
- [Model Details](#model-details)
- [Intended Use & Use Cases](#intended-use--use-cases)
- [Requirements](#requirements)
- [Quickstart](#quickstart)
- [Training & Fine-tuning](#training--fine-tuning)
- [Repository Structure](#repository-structure)
- [Training Data](#training-data)
- [Limitations](#limitations)
- [FAQ](#faq)
- [Citation](#citation)
- [License](#license)

## Model Summary

GenerRNA is a **Transformer decoder-only (GPT-style) language model** trained on RNA nucleotide sequences. By treating RNA as a sequence of tokens, it learns statistical and structural regularities of RNA directly from data and can then **sample entirely new sequences**. GenerRNA was pre-trained on ~16 million RNA sequences (16.09M), encompassing ~17.4 billion nucleotides. Generated RNAs are novel (distinct from training sequences) yet fold into stable secondary structures, and the model can be fine-tuned to design functional RNAs such as protein binders — all without requiring prior structural knowledge.

## Key Features

- 🧬 **De novo RNA generation** — create novel RNA sequences from scratch; no structure, label, or alignment required.
- 🎯 **Zero-shot or fine-tuned** — explore RNA space out of the box, or specialize the model for a target family or function.
- 🔬 **Structurally plausible outputs** — generated sequences fold into stable secondary structures (low minimum free energy).
- 🧩 **Transformer / GPT architecture** — a familiar, scalable decoder-only design (~350M parameters).
- ⚡ **Two checkpoints on Hugging Face** — an updated long-context model and the original historical model.
- 📖 **Open & reproducible** — MIT-licensed code, tokenizer, and the data behind the paper's figures.

## Model Details

|  |  |
|---|---|
| **Model type** | Generative language model (decoder-only Transformer, GPT-style) |
| **Domain** | RNA / nucleotide sequences |
| **Parameters** | 350M (24 transformer layers, model dimension 1280) |
| **Context window** | 1024 tokens (~4000 nucleotides) |
| **Tokenizer** | Byte-Pair Encoding (BPE), vocabulary size 1024 |
| **Weights** | Hosted on Hugging Face: [`pfnet/GenerRNA`](https://huggingface.co/pfnet/GenerRNA) |
| **Framework** | PyTorch (≥ 2.0) |
| **License** | MIT |
| **Paper** | *PLOS ONE* 19(10):e0310814 (2024) · [doi:10.1371/journal.pone.0310814](https://doi.org/10.1371/journal.pone.0310814) |
## Intended Use & Use Cases

GenerRNA is intended for **research in RNA biology, synthetic biology, and RNA-based therapeutics / drug discovery**. Typical use cases include:

- Exploring the diversity of the RNA sequence space.
- Generating candidate RNAs from a target family by fine-tuning on family-specific data.
- Designing RNAs with desired functional properties, such as aptamers/binders with high affinity to a target protein (demonstrated for the RNA-binding proteins **ELAVL1** and **SRSF1** in the paper).
- Serving as a pre-trained backbone for downstream RNA modeling and design tasks.

## Requirements

A CUDA environment with a minimum of **8 GB VRAM** is required.

```
torch>=2.0
numpy
transformers==4.33.0.dev0
datasets==2.14.4
tqdm
```

## Quickstart

```bash
# 1. Get the code (this repository)
git clone https://github.com/ekkkkki/GenerRNA
cd GenerRNA
pip install torch numpy transformers==4.33.0.dev0 datasets==2.14.4 tqdm

# 2. Download the model weights from Hugging Face (weights live there, not on GitHub)
pip install -U "huggingface_hub[cli]"
huggingface-cli download pfnet/GenerRNA model_updated.pt --local-dir .

# 3. Generate RNA de novo (the BPE tokenizer is included in this repo under tokenizer/)
python sampling.py \
    --out_path generated.txt \
    --max_new_tokens 256 \
    --ckpt_path model_updated.pt \
    --tokenizer_path tokenizer
```

> The original (historical) model is also on Hugging Face as split files under `experiment_data/historical_version/`; recombine with `cat model.pt.part-* > model.pt` and use its dedicated tokenizer. See the [Hugging Face model card](https://huggingface.co/pfnet/GenerRNA) for details.

## Training & Fine-tuning

**1. Tokenize your sequences** (one sequence per line, no header):

```bash
python tokenization.py \
    --data_dir {path_to_directory_containing_sequence_data} \
    --file_name {file_name_of_sequence_data} \
    --tokenizer_path tokenizer \
    --out_dir {directory_to_save_tokenized_data} \
    --block_size 256
```

**2. Create a config** based on `configs/example_pretraining.py` (training from scratch) or `configs/example_finetuning.py` (fine-tuning).

**3. Train / fine-tune:**

```bash
python train.py --config {path_to_your_config_file}
```

### Train your own tokenizer (optional)

```bash
python train_BPE.py \
    --txt_file_path {path_to_training_file_one_sequence_per_line} \
    --vocab_size 50256 \
    --new_tokenizer_path {directory_to_save_trained_tokenizer}
```

## Repository Structure

```
.
├── LICENSE
├── README.md
├── CITATION.cff               # machine-readable citation metadata
├── docs/
│   └── index.html             # project landing page (served via GitHub Pages)
├── model.py                   # model architecture (decoder-only Transformer)
├── sampling.py                # generate sequences from a trained model
├── tokenization.py            # tokenize sequence data for training
├── train.py                   # pre-training / fine-tuning entry point
├── train_BPE.py               # train a new BPE tokenizer
├── tokenizer/                 # BPE tokenizer (vocabulary size 1024)
├── configs/
│   ├── example_pretraining.py
│   └── example_finetuning.py
└── experiment_data/           # data underlying the paper's figures
    └── pretraining_data.sh    # how the pre-training corpus was built (RNAcentral + MMseqs2)
```

> **Model weights** (`model_updated.pt` and the historical split model) are **hosted on Hugging Face**: https://huggingface.co/pfnet/GenerRNA

## Training Data

GenerRNA was pre-trained on RNA sequences from **[RNAcentral](https://rnacentral.org/)** (release 22, which aggregates 51 expert databases). Starting from **34.39 million** raw sequences, deduplication with **[MMseqs2](https://github.com/soedinglab/MMseqs2)** at **80% sequence identity** yielded a pre-training corpus of **~16 million sequences (16.09M), encompassing ~17.4 billion nucleotides**. GenerRNA has a context window of **1024 tokens (~4000 nucleotides)**. The pre-processing pipeline is in [`experiment_data/pretraining_data.sh`](experiment_data/pretraining_data.sh), and the data underlying the paper's figures is in `experiment_data/`. See the [paper](https://doi.org/10.1371/journal.pone.0310814) for full dataset details.

## Limitations

- GenerRNA models RNA **sequence**; it does not explicitly predict tertiary structure or function. Validate candidates with downstream structure/function tools and wet-lab experiments.
- A CUDA GPU is required for generation and training as provided.
- Zero-shot outputs reflect the natural distribution of the training data; targeting a specific family or property generally requires fine-tuning.
- Generated sequences are computational hypotheses and should be experimentally validated before any real-world application.

## FAQ

**What is GenerRNA?**
GenerRNA is a generative, pre-trained language model (a decoder-only Transformer) that designs novel RNA sequences *de novo*, without requiring structural information, functional labels, or sequence alignments.

**How is GenerRNA different from other RNA models?**
Most RNA models are *discriminative* — they predict structure or properties from a given sequence. GenerRNA is *generative*: it samples entirely new sequences. To our knowledge, it is the first application of a generative language model to RNA generation.

**Where are the model weights?**
On Hugging Face: [`pfnet/GenerRNA`](https://huggingface.co/pfnet/GenerRNA). This GitHub repository hosts the code and documentation only.

**Do I need RNA structure or alignments as input?**
No. GenerRNA generates sequences directly from its learned distribution; no structure or alignment is needed.

**Can I generate RNAs from a specific family or with a specific function?**
Yes. Fine-tune GenerRNA on a family- or function-specific dataset. The paper demonstrates designing RNAs with high binding affinity to the proteins ELAVL1 and SRSF1.

**Which checkpoint should I use?**
Use `model_updated.pt` (longer context, trained on deduplicated data). The original split model is kept under `experiment_data/historical_version/` on Hugging Face for reproducibility.

**How do I cite GenerRNA?**
See [Citation](#citation) below.

## Citation

If you use GenerRNA, its checkpoints, or this repository in your research, please cite:

```bibtex
@article{zhao2024generrna,
  title     = {GenerRNA: A generative pre-trained language model for de novo RNA design},
  author    = {Zhao, Yichong and Oono, Kenta and Takizawa, Hiroki and Kotera, Masaaki},
  journal   = {PLOS ONE},
  volume    = {19},
  number    = {10},
  pages     = {e0310814},
  year      = {2024},
  doi       = {10.1371/journal.pone.0310814},
  publisher = {Public Library of Science}
}
```

**Plain text:** Zhao Y, Oono K, Takizawa H, Kotera M (2024) GenerRNA: A generative pre-trained language model for *de novo* RNA design. PLOS ONE 19(10): e0310814. https://doi.org/10.1371/journal.pone.0310814

**First author:** [Yichong Zhao / Eric Zhao](https://ekkkkki.github.io/) — AI engineer at Preferred Networks.

## License

The source code is licensed under the **MIT License** — see [`LICENSE`](LICENSE). © 2024 Yichong Zhao / Eric Zhao, Masaaki Kotera, Kenta Oono, Hiroki Takizawa.
