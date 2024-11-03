# Vector Store

This repository is a vector store based on FAISS using the `nomic-embed-text-v1.5` model. The project's status is "early in development," so expect changes and potential improvements over time.

## Overview

This project enables k-NN similarity search on vector encodings stored in FAISS. It's currently a work in progress for a Retrieval-Augmented Generation (RAG) Project.

## Requirements

Before you get started, you will need a Nomic API key. Make sure to have it ready before proceeding with the steps below. Ensure the key is available through the path:

## Usage

1. **Clone the Project**

   Start by cloning the repository:
   ```bash
   git clone <repository-url>
   ```

2. **Navigate to the Source Directory**

   Use the following command to navigate to the project's source directory:
   ```bash
   cd <source-directory>
   ```

   Running `ls` (or `dir` on Windows) should show you `build_index.py` and `cached_faiss.py`.

3. **Set Up the Input Directory**

   If an input directory doesn't exist, create one using:
   ```bash
   mkdir input

   And put a text based document inside of it. Or "copy *.py to ./input"
   to embed the source code.
   ```

4. **Build the Index**

   Run the following command to build the FAISS index:
   ```bash
   python build_index.py
   ```

5. **Cache FAISS**

   Once the index is built, cache it using:
   ```bash
   python cached_faiss.py
   ```

6. **Edit the Search Query**

   Manually edit the search string in `load_store.py`. As of now, it can be found on line 72, although this might change frequently as the project develops:

   ```python
   result = similarity_search("What is faiss?", CONFIG['DB'], 3)
   ```

7. **Perform a Search**

   Finally, execute the following command to perform a search against the indexed FAISS vector store using the predefined query:
   ```bash
   python load_store.py
   ```

   This will search the vector store with the hardcoded "What is faiss?" query.

## Notes

- This README is primarily for personal use but feedback and contributions are always welcome.
- Ensure that your directory structure and scripts are correctly set up as this project is still evolving, expect potential changes in the workflow.

## Contributing

Since this is a personal project primarily for self-use, contributions aren't actively sought. However, if you're interested in collaborating, feel free to fork the repo and open a pull request.

---

*This repository is still in its early stages, so expect iterative improvements and potential restructuring.*