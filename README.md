# AI Fashion Stylist POC

This project is an interactive AI-powered fashion stylist built with Streamlit. It uses a curated wardrobe, a vector database for semantic search, and OpenAI's GPT models to suggest stylish, weather-appropriate outfits based on user input.

## Features

- **Curated Wardrobe**: A sample wardrobe with detailed metadata for each item (category, style, material, fit, properties, etc.).
- **Semantic Search**: Uses ChromaDB and sentence embeddings to retrieve the most relevant wardrobe items for a user's request and weather context.
- **AI Reasoning**: Leverages OpenAI's GPT-4-turbo to generate outfit suggestions, reasoning about materials, weather, and style.
- **Streamlit UI**: Simple web interface for users to describe the occasion and weather, and receive a personalized outfit suggestion.

## How It Works

1. **Wardrobe Definition**: The wardrobe is defined as a list of Python dictionaries, each with detailed metadata.
2. **Vector Database Setup**: Wardrobe items are embedded and stored in ChromaDB for fast semantic retrieval.
3. **User Input**: The user enters the occasion and weather conditions via the Streamlit app.
4. **Retrieval & Generation**: Relevant wardrobe items are retrieved and passed to the OpenAI LLM, which generates a reasoned outfit suggestion.
5. **Display**: The suggested outfit and reasoning are displayed in the Streamlit app.

## Setup Instructions

### Prerequisites

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [ChromaDB](https://docs.trychroma.com/)
- [sentence-transformers](https://www.sbert.net/)
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- An OpenAI API key with access to `gpt-4-turbo` or `gpt-3.5-turbo`

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/mythreyi1905/fashionAssistant.git
    cd fashionAssistant
    ```

2. **Install dependencies:**
    ```bash
    pip install streamlit chromadb sentence-transformers openai
    ```

3. **Set your OpenAI API key:**
    ```bash
    export OPENAI_API_KEY=sk-...
    ```

### Running the App

```bash
streamlit run stylist_poc.py
```

Open the provided local URL in your browser to use the app.

## Usage

1. Enter the occasion (e.g., "A casual weekend brunch with friends").
2. Enter the weather context (e.g., "Cool, windy, and overcast, around 55°F (13°C)").
3. Click **Get Outfit Suggestion**.
4. View the AI-generated outfit and reasoning.

## Notes

- If you see an error about the OpenAI API key, ensure you have set the `OPENAI_API_KEY` environment variable.
- If you get a model access error, try changing the model name in the code to one you have access to (e.g., `gpt-3.5-turbo`).


