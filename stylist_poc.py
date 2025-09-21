import os
import chromadb
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import streamlit as st



wardrobe = [
    # Tops (6 items)
    {"name": "Floral Empire Waist Top", "description": "A white empire-waist top with a blue floral print.", "metadata": {"category": "top", "style": "casual", "color": "white/blue", "material": "cotton", "formality": 4, "fit": "relaxed", "properties": ["breathable", "lightweight"]}},
    {"name": "Black Peplum Top", "description": "A black top with a square neckline and a flared peplum waist.", "metadata": {"category": "top", "style": "smart-casual", "color": "black", "material": "crepe", "formality": 6, "fit": "tailored", "properties": ["lightweight", "drapes"]}},
    {"name": "Plaid Tunic Shirt", "description": "A women's plaid button-up shirt with a longer tunic length.", "metadata": {"category": "top", "style": "casual", "color": "plaid", "material": "flannel", "formality": 2, "fit": "relaxed", "properties": ["insulating", "soft"]}},
    {"name": "White Crop Tank Top", "description": "A simple white cropped tank top in a bralette style.", "metadata": {"category": "top", "style": "casual", "color": "white", "material": "cotton", "formality": 1, "fit": "slim", "properties": ["breathable", "stretch"]}},
    {"name": "Graphic Floral Sweater", "description": "A grey sweater with a distinct square graphic of flowers.", "metadata": {"category": "top", "style": "casual", "color": "grey", "material": "cotton-blend", "formality": 3, "fit": "relaxed", "properties": ["insulating", "soft"]}},
    {"name": "White Silk Shirt", "description": "An elegant collared button-down shirt made from silk.", "metadata": {"category": "top", "style": "elegant", "color": "white", "material": "silk", "formality": 8, "fit": "relaxed", "properties": ["breathable", "lightweight", "delicate"]}},
    # Bottoms (4 items)
    {"name": "Light Blue Boyfriend Jeans", "description": "Relaxed, straight-leg boyfriend fit jeans in a light blue wash.", "metadata": {"category": "bottom", "style": "casual", "color": "light blue", "material": "denim", "formality": 2, "fit": "relaxed", "properties": ["durable", "wind-resistant"]}},
    {"name": "Black Ankle-Length Jeans", "description": "Petite-fit straight-leg jeans in solid black.", "metadata": {"category": "bottom", "style": "casual", "color": "black", "material": "denim", "formality": 3, "fit": "slim", "properties": ["durable", "wind-resistant", "stretch"]}},
    {"name": "Black Palazzo Pants", "description": "Wide-leg, flowing palazzo pants in black.", "metadata": {"category": "bottom", "style": "smart-casual", "color": "black", "material": "viscose", "formality": 5, "fit": "relaxed", "properties": ["breathable", "lightweight", "drapes"]}},
    {"name": "Black A-Line Skirt", "description": "A classic black A-line skirt that ends at the knee.", "metadata": {"category": "bottom", "style": "smart-casual", "color": "black", "material": "polyester-blend", "formality": 6, "fit": "tailored", "properties": ["durable", "wrinkle-resistant"]}},
    # Dresses (2 items)
    {"name": "Green Sleeveless Maxi Dress", "description": "A sleeveless A-line maxi dress in a light green color.", "metadata": {"category": "dress", "style": "casual", "color": "green", "material": "linen", "formality": 3, "fit": "relaxed", "properties": ["breathable", "lightweight"]}},
    {"name": "Printed Kaftan", "description": "A large, flowy kaftan with a vibrant pink and orange print.", "metadata": {"category": "dress", "style": "bohemian", "color": "pink/orange", "material": "viscose", "formality": 4, "fit": "oversized", "properties": ["breathable", "lightweight"]}},
    # Outerwear (1 item)
    {"name": "Dark Blue Denim Jacket", "description": "A classic dark blue denim jacket with a waist-length cut.", "metadata": {"category": "outerwear", "style": "casual", "color": "dark blue", "material": "denim", "formality": 3, "fit": "relaxed", "properties": ["durable", "wind-resistant"]}},
    # Shoes (1 item)
    {"name": "White Nike Air Force 1", "description": "Classic white Nike Air Force 1 sneakers.", "metadata": {"category": "shoes", "style": "streetwear", "color": "white", "material": "leather", "formality": 1, "fit": "standard", "properties": ["durable", "water-resistant"]}},
]


@st.cache_resource
def load_resources():
    """Load and set up all the necessary AI models and database connections."""
    client = chromadb.Client()
    collection = client.get_or_create_collection(name="wardrobe_v2_collection")

   
    documents_to_embed = []
    metadata_list = []
    ids = []
    for i, item in enumerate(wardrobe):
        metadata = item['metadata'].copy()
        if isinstance(metadata.get('properties'), list):
            metadata['properties'] = ', '.join(metadata['properties'])
        item['metadata'] = metadata
        
        full_description = (
            f"Item Name: {item['name']}. "
            f"Description: {item['description']}. "
            f"Style: {item['metadata']['style']}. "
            f"Category: {item['metadata']['category']}. "
            f"Material: {item['metadata']['material']}. "
            f"Fit: {item['metadata']['fit']}. "
            f"Properties: {', '.join(item['metadata']['properties'])}."
        )
        documents_to_embed.append(full_description)
        metadata_list.append(item['metadata'])
        ids.append(str(i + 1))

    collection.add(
        documents=documents_to_embed,
        metadatas=metadata_list,
        ids=ids
    )
    

    if "OPENAI_API_KEY" not in os.environ:
        st.error("FATAL ERROR: Please set the OPENAI_API_KEY environment variable.")
        return None, None
    
    llm_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    return collection, llm_client



def get_outfit_suggestion(collection, llm_client, user_query, weather_context):

    print(f"\nReceived query: '{user_query}' with weather: '{weather_context}'")
    
    # Part A: Retrieval
    print("Retrieving relevant items from the wardrobe...")
    retrieved_items = collection.query(
        query_texts=[f"{user_query} suitable for {weather_context}"],
        n_results=7 # Retrieve a few more items to give the LLM more options
    )
    
    retrieved_clothes_list = []
    for doc in retrieved_items['documents'][0]:
        retrieved_clothes_list.append(f"- {doc}")
    
    retrieved_clothes_str = "\n".join(retrieved_clothes_list)
    print(f"Found relevant items:\n{retrieved_clothes_str}")

    # Part B: Generation with the new "Reasoning Prompt"
    print("\nAsking the AI Stylist (LLM) for a reasoned outfit suggestion...")


    system_prompt = (
        "You are an expert fashion stylist with a deep understanding of how fabric materials "
        "and clothing properties perform in various weather conditions. Your task is to create a complete, "
        "stylish outfit that is practical and comfortable for the user's specific request and weather."
    )

    user_prompt = (
        f"User Request: '{user_query}'\n\n"
        f"Current Weather Context: '{weather_context}'\n\n"
        "Here are the most relevant items from my wardrobe that might fit this request, along with their properties:\n"
        f"{retrieved_clothes_str}\n\n"
        "Please suggest one complete outfit. Your reasoning MUST be based on both the style "
        "and the functional properties of the items (e.g., breathable, insulating, wind-resistant) "
        "as they relate to the weather. Explain your final choice."
        f"If a crucial item (like shoes or a bottom) is missing from the retrieved list, you can state that, but try to make a good outfit from what is provided"
    )

    try:
        response = llm_client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.5 # Lower temperature for more focused, logical reasoning
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred with the OpenAI API: {e}"



st.title("AI Fashion Stylist ✨")
st.write("Welcome! Describe the occasion and the weather, and I'll suggest an outfit from our wardrobe.")

# Load the AI resources using our new cached function
collection, llm_client = load_resources()


# Check if resources loaded successfully before building the rest of the UI
if collection and llm_client:
    # Create the text input fields for the user
    user_query = st.text_input(
        "What's the occasion?", 
        "A casual weekend brunch with friends"
    )
    weather_context = st.text_input(
        "What's the weather like?", 
        "Cool, windy, and overcast, around 55°F (13°C)"
    )
    
    if st.button("Get Outfit Suggestion"):
        with st.spinner("Styling the perfect outfit for you..."):
            suggestion = get_outfit_suggestion(collection, llm_client, user_query, weather_context)
            st.markdown("---")
            st.subheader("Here's your outfit suggestion:")
            st.markdown(suggestion)
else:
    st.warning("AI resources could not be loaded. Please check your configuration.")