import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ১. পেজ কনফিগারেশন
st.set_page_config(page_title="Hypertension Dashboard", layout="wide", page_icon="🫀")

# শিরোনাম এবং ডেসক্রিপশন
st.title("🫀 Interactive Hypertension Meta-Analysis")
st.markdown("""
Welcome to the advanced dashboard! Filter the data from the sidebar and explore the interactive tabs below.
""")

# ২. ডেটা লোড করা
@st.cache_data
def load_data():
    return pd.read_csv('Final_Remastered_Meta_Data.csv')

try:
    df = load_data()
    
    # ৩. সাইডবার ফিল্টার
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3004/3004451.png", width=100) # একটা সুন্দর আইকন
    st.sidebar.header("🔍 Filter Options")
    
    risk_factors = df['Standard_Risk_Factor'].dropna().unique().tolist()
    risk_factors.sort()
    
    selected_factor = st.sidebar.selectbox("Select a Risk Factor:", ["All"] + risk_factors)

    # ডেটা ফিল্টার করা
    if selected_factor == "All":
        filtered_df = df
    else:
        filtered_df = df[df['Standard_Risk_Factor'] == selected_factor]

    # ৪. Quick Stats (KPIs)
    st.markdown("### 💡 Quick Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total Studies/Papers", filtered_df['Study_ID'].nunique())
    col2.metric("Total Data Points", len(filtered_df))
    col3.metric("Average OR", round(filtered_df['OR'].mean(), 2))
    col4.metric("Max OR", round(filtered_df['OR'].max(), 2))
    
    st.markdown("---")

    # ৫. TABS তৈরি করা (ম্যাজিক শুরু!)
    tab1, tab2, tab3 = st.tabs(["📊 Main Analysis", "🌍 Demographics", "📋 Raw Data"])

    # ট্যাব ১: মেইন অ্যানালাইসিস (বার চার্ট)
    with tab1:
        st.subheader(f"📈 Odds Ratio for: {selected_factor}")
        chart_data = filtered_df.set_index('Author')[['OR']]
        st.bar_chart(chart_data, color="#FF4B4B") # চার্টের কালার সুন্দর করলাম

    # ট্যাব ২: ডেমোগ্রাফিক্স (নতুন পাই চার্ট এবং স্ক্যাটার প্লট)
    with tab2:
        col_pie, col_scatter = st.columns(2)
        
        with col_pie:
            st.subheader("Setting Distribution")
            # Matplotlib দিয়ে পাই চার্ট তৈরি
            setting_counts = filtered_df['Standard_Setting'].value_counts()
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            ax1.pie(setting_counts, labels=setting_counts.index, autopct='%1.1f%%', colors=sns.color_palette("Set2"), startangle=90)
            ax1.axis('equal')  
            st.pyplot(fig1)

        with col_scatter:
            st.subheader("Sample Size vs Odds Ratio")
            # Matplotlib দিয়ে স্ক্যাটার প্লট তৈরি
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            sns.scatterplot(data=filtered_df, x='Clean_Sample_Size', y='OR', hue='Standard_Setting', palette='viridis', ax=ax2)
            ax2.set_xlabel("Sample Size")
            ax2.set_ylabel("Odds Ratio (OR)")
            st.pyplot(fig2)

    # ট্যাব ৩: র ডেটা ভিউ (কালারফুল টেবিল)
    with tab3:
        st.subheader("📋 Dataset Explorer")
        # ডেটাফ্রেমকে স্টাইল করে শো করা (OR এর উপর ভিত্তি করে কালার গ্রেডিয়েন্ট)
        st.dataframe(
            filtered_df[['Author', 'Year', 'Standard_Setting', 'Clean_Sample_Size', 'OR', 'P_Value']]
            .style.background_gradient(subset=['OR'], cmap='Reds')
        )

except FileNotFoundError:
    st.error("⚠️ ডেটা ফাইলটি পাওয়া যাচ্ছে না!")
