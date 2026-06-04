# RAG EXTRACTOR

A CLI tools for PDF data ingestion for RAG

This repository contains the code for extracting the text and table for RAG pipeline.
It handle the layout aware chunking strategy.

it extract page_no , layout box

## To test 

```bash
# Help for CLI utility
./run.sh test
```

```bash
# Single pdf file
./run.sh run ./data/raw/myfile.pdf
```

```bash
# folder contaaining pdf
./run.sh run ./data/raw/
```


## Models used for embedding

* [bge-m3](https://ollama.com/library/bge-m3)
