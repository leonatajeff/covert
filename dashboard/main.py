import streamlit as st
import pandas as pd
import scraper  # Importing your scraper.py

def main():
    st.set_page_config(page_title="M9 Tiger Tooth Tracker", page_icon="🐅", layout="wide")
    
    st.title("🐅 M9 Bayonet | Tiger Tooth Tracker")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("Controls")
        if st.button("🔄 Fetch Latest Prices", type="primary"):
            with st.spinner("Scraping CSFloat..."):
                # Call the function from scraper.py
                raw_data = scraper.fetch_listings()
                
                if raw_data:
                    # Convert to DataFrame for easier handling
                    df = pd.DataFrame(raw_data)
                    st.session_state['data'] = df
                    st.success(f"Fetched {len(df)} listings!")
                else:
                    st.error("No data found or API error.")

    # Main Display Area
    if 'data' in st.session_state:
        df = st.session_state['data']

        # 1. Key Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Floor Price", f"${df['price'].min():,.2f}")
        with col2:
            st.metric("Best Float", f"{df['float_value'].min():.6f}")
        with col3:
            avg_top_10 = df['price'].mean()
            st.metric("Avg Price (Top 10)", f"${avg_top_10:,.2f}")

        st.divider()

        # 2. Detailed Table
        st.subheader("Listing Details")
        
        # Configure column display
        st.dataframe(
            df,
            column_config={
                "price": st.column_config.NumberColumn("Price", format="$%.2f"),
                "float_value": st.column_config.NumberColumn("Float", format="%.6f"),
                "paint_seed": "Seed",
                "id": "Listing ID",
                "inspect_link": st.column_config.LinkColumn("Inspect Link", display_text="Inspect in Game"),
                "image": st.column_config.ImageColumn("Icon")
            },
            column_order=["image", "price", "float_value", "paint_seed", "inspect_link", "id"],
            width='stretch',
            hide_index=True
        )
    else:
        st.info("👈 Click 'Fetch Latest Prices' in the sidebar to start.")

if __name__ == "__main__":
    main()
