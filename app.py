import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="Hypertension Dashboard", layout="wide", page_icon="🫀")


st.title("🫀 Interactive Hypertension Meta-Analysis")
st.markdown("""
Welcome to the advanced dashboard! Filter the data from the sidebar and explore the interactive tabs below.
""")


@st.cache_data
def load_data():
    return pd.read_csv('Final_Remastered_Meta_Data.csv')

try:
    df = load_data()
    

    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3004/3004451.png", width=100) 
    st.sidebar.header("🔍 Filter Options")
    
    risk_factors = df['Standard_Risk_Factor'].dropna().unique().tolist()
    risk_factors.sort()
    
    selected_factor = st.sidebar.selectbox("Select a Risk Factor:", ["All"] + risk_factors)

  
    if selected_factor == "All":
        filtered_df = df
    else:
        filtered_df = df[df['Standard_Risk_Factor'] == selected_factor]

   
    st.markdown("### 💡 Quick Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total Studies/Papers", filtered_df['Study_ID'].nunique())
    col2.metric("Total Data Points", len(filtered_df))
    col3.metric("Average OR", round(filtered_df['OR'].mean(), 2))
    col4.metric("Max OR", round(filtered_df['OR'].max(), 2))
    
    st.markdown("---")

  
    tab1, tab2, tab3 = st.tabs(["📊 Main Analysis", "🌍 Demographics", "📋 Raw Data"])

  
    with tab1:
        st.subheader(f"📈 Odds Ratio for: {selected_factor}")
        chart_data = filtered_df.set_index('Author')[['OR']]
        st.bar_chart(chart_data, color="#FF4B4B") 


    with tab2:
        col_pie, col_scatter = st.columns(2)
        
        with col_pie:
            st.subheader("Setting Distribution")
          
            setting_counts = filtered_df['Standard_Setting'].value_counts()
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            ax1.pie(setting_counts, labels=setting_counts.index, autopct='%1.1f%%', colors=sns.color_palette("Set2"), startangle=90)
            ax1.axis('equal')  
            st.pyplot(fig1)

        with col_scatter:
            st.subheader("Sample Size vs Odds Ratio")
           
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            sns.scatterplot(data=filtered_df, x='Clean_Sample_Size', y='OR', hue='Standard_Setting', palette='viridis', ax=ax2)
            ax2.set_xlabel("Sample Size")
            ax2.set_ylabel("Odds Ratio (OR)")
            st.pyplot(fig2)

 
    with tab3:
        st.subheader("📋 Dataset Explorer")
       
        st.dataframe(
            filtered_df[['Author', 'Year', 'Standard_Setting', 'Clean_Sample_Size', 'OR', 'P_Value']]
            .style.background_gradient(subset=['OR'], cmap='Reds')
        )

except FileNotFoundError:
    st.error("⚠️ ডেটা ফাইলটি পাওয়া যাচ্ছে না!")
