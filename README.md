# RAG EXTRACTOR

A CLI tools for PDF data ingestion for RAG

This repository contains the code for extracting the text and table for RAG pipeline.
It handle the layout aware chunking strategy.

it extract page_no , layout box

./run.sh test
./run.sh run ./data/raw/myfile.pdf
./run.sh run ./data/raw/