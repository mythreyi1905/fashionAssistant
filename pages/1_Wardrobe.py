import streamlit as st
from database import SessionLocal, User, WardrobeItem


st.set_page_config(page_title="My Wardrobe", layout="wide")

st.title("My Wardrobe 👚👖")
def get_user_wardrobe(user_id):
        """Fetches all clothing items for a specific user."""
        db = SessionLocal()
        wardrobe = db.query(WardrobeItem).filter(WardrobeItem.owner_id == user_id).all()
        db.close()
        return wardrobe

def add_clothing_item(user_id, name, metadata):
    """Adds a new clothing item to the database for a specific user."""
    db = SessionLocal()
    new_item = WardrobeItem(owner_id=user_id, name=name, item_metadata=metadata)
    db.add(new_item)
    db.commit()
    db.close()


if not st.session_state.get("authentication_status"):
    st.warning("Please log in on the Home page to access your wardrobe.")
else:
         
    db = SessionLocal()
    current_user = db.query(User).filter(User.username == st.session_state["name"]).first()
    db.close()
    
    st.header("My Clothing Items")

   
    user_wardrobe = get_user_wardrobe(current_user.id)

    if not user_wardrobe:
        st.info("Your wardrobe is empty! Add some items using the form below.")
    else:
        for i in range(0, len(user_wardrobe), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(user_wardrobe):
                    item = user_wardrobe[i+j]
                    with cols[j]:
                        with st.expander(f"{item.name}"):
                            print("=====================================================================")
                            print(f"Item Metadata: {item.metadata}")
                            print(item.item_metadata)
                            print("=====================================================================")
                            st.write(f"**Category:** {item.item_metadata.get('category', 'N/A')}")
                            st.write(f"**Style:** {item.item_metadata.get('style', 'N/A')}")
                            st.write(f"**Properties:** {', '.join(item.item_metadata.get('properties', []))}")


    st.markdown("---")
    st.header("Add a New Clothing Item")

    # The form to add new items
    with st.form("add_item_form", clear_on_submit=True):
        item_name = st.text_input("Item Name", placeholder="e.g., Blue Denim Jacket")
        
        col1, col2 = st.columns(2)
        with col1:
            item_category = st.selectbox("Category", ["top", "bottom", "dress", "outerwear", "shoes"])
            item_style = st.text_input("Style", placeholder="e.g., casual, elegant")
            item_fit = st.selectbox("Fit", ["slim", "relaxed", "oversized", "tailored"])
            
        with col2:
            item_color = st.text_input("Color", placeholder="e.g., blue, black, plaid")
            item_material = st.text_input("Material", placeholder="e.g., denim, cotton, silk")
            item_formality = st.slider("Formality (1=Casual, 10=Formal)", 1, 10, 3)

        item_properties = st.multiselect(
            "Properties",
            ["breathable", "insulating", "water-resistant", "wind-resistant", "durable", "lightweight", "stretch"],
        )
        
        submitted = st.form_submit_button("Add Item to Wardrobe")

        if submitted:
            if not item_name:
                st.error("Please enter an item name.")
            else:
                metadata = {
                    "category": item_category, "style": item_style, "color": item_color,
                    "material": item_material, "formality": item_formality, "fit": item_fit,
                    "properties": item_properties
                }
                add_clothing_item(current_user.id, item_name, metadata)
                
                st.success(f"Successfully added '{item_name}' to your wardrobe!")
   