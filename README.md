# Workaround Brainstormer

## ℹ️ Description
Workaround Brainstormer is a web application designed to facilitate the identification of workarounds based on a process description or bpmn diagram in an interactive way.

It`s a generative AI approach that helps to identify workarounds in situations where no process data is available for process mining.

> [!NOTE]  
> The tool was created as part of the [Change.WorkAROUND](https://www.changeworkaround.de) research project by the [viadee](https://www.viadee.de) Data & AI-Team. The project Change.WorkAROUND is supported by the German [BMBF](https://www.bmbf.de/) since 2023 in the ["Zukunft der Wertschöpfung"](https://www.zukunft-der-wertschoepfung.de) program with the goal to improve the abiblity to adapt and innovate in a dynamic context. 

## ⭐ Features
- LLM based workaround generation
- Visual representation of the workarounds as a network graph
- Control mechanisms to facilitate the generation process

The tool contains the [CWA Corpus](rag/workarounds_corpus.csv), i.e. a list auf workarounds found in real industry processes and described in a structured way. This corpus is used to guide an LLM when creating plausible workarounds in new processes through few-shot examples.

Both the [CWA Corpus](rag/workarounds_corpus.csv) and the software tool are licensed under the [BSD 3-Clause License](LICENSE).

## How it works

https://github.com/user-attachments/assets/cb4db8b1-3041-4e84-a225-20d2dee6df62



# Getting Started

## Installation

1. Clone this repository and create a python virtual environment
2. Install the requirements.txt
``` 
    pip install -r requirements.txt
``` 
3. Create a .env file based on the .envtemplate and set you variables

4. Run the flask server for development
``` 
    python run.py
``` 
5. Or run a production server
``` 
    pip install uwsgi
   
    uwsgi --http 0.0.0.0:5000 --module run:app --master --processes 4 --threads 2
``` 
    
# Acknowledgements

The first implementation of the concept was created by [Fresh-P](https://github.com/Fresh-P) as part of his master thesis in cooperation with the University of Münster and viadee in 2024.

