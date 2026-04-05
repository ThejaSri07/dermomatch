import streamlit as st
import pandas as pd

# -------------------------------
# Load Dataset
# -------------------------------
df = pd.read_csv("datasheet.csv")
print(df.columns)
# Fill missing values safely
df = df.copy()
df['afterUse'] = df['afterUse'].fillna("")

# -------------------------------
# Define Tags
# -------------------------------

positive_tags = [
    'Good For Oily Skin', 'Skin Texture', 'Reduces Large Pores',
    'Anti-Aging', 'Brightening', 'Redness Reducing',
    'Reduces Irritation', 'Acne Fighting',
    'Scar Healing', 'Hydrating'
]

negative_tags = [
    'Drying', 'Acne Trigger', 'Irritating',
    'Rosacea', 'May Worsen Oily Skin',
    'Eczema', 'Dark Spots'
]

# Deal breakers for personalization
DEAL_BREAKERS = {
    "Eczema": ["Irritating", "Drying", "Acne Trigger"],
    "Oily": ["May Worsen Oily Skin"],
    "Sensitive": ["Irritating", "Rosacea"]
}

# -------------------------------
# Function: Score calculation
# -------------------------------

def calculate_score(text, user_profile):
    if pd.isna(text):
        return 0

    tags = [t.strip() for t in str(text).split(',')]

    score = 0

    # Positive points
    for t in tags:
        if t in positive_tags:
            score += 2

    # Negative points
    for t in tags:
        if t in negative_tags:
            score -= 2

    # Deal breaker penalty
    for condition in user_profile:
        if condition in DEAL_BREAKERS:
            for bad in DEAL_BREAKERS[condition]:
                if bad in tags:
                    score -= 5

    return score

# -------------------------------
# STREAMLIT UI
# -------------------------------

st.title("DermoMatch - Skincare Recommender")

st.write("Select your skin concerns:")

user_profile = st.multiselect(
    "Choose your skin type / issues",
    ["Oily", "Eczema", "Sensitive", "Acne"]
)

# Button to run recommendation
if st.button("Find My Products"):

    if len(user_profile) == 0:
        st.warning("Please select at least one skin concern")
    else:
        df['score'] = df['afterUse'].apply(lambda x: calculate_score(x, user_profile))

        # Sort best products
        top_products = df.sort_values(by='score', ascending=False).head(10)

        st.subheader("✨ Top Recommended Products")

        st.dataframe(top_products[['brand', 'name', 'score']])