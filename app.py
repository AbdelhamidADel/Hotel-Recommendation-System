
import streamlit as st
import base64
import nltk
nltk.download('wordnet')
nltk.download('punkt')
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from streamlit_folium import folium_static
import folium
# ------------------------data---------------------------
df = pd.read_csv("short_Hotel_data.csv")
# ------------------------------------------------------
def recommend_hotel(location, description):
    description = description.lower()
    word_tokenize(description)
    stop_words = stopwords.words('english')
    lemm = WordNetLemmatizer()
    filtered  = {word for word in description if not word in stop_words}
    filtered_set = set()
    for fs in filtered:
        filtered_set.add(lemm.lemmatize(fs))

    country = df[df['countries']==location.lower()]
    country = country.set_index(np.arange(country.shape[0]))
    list1 = []
    list2 = []
    cos = []
    for i in range(country.shape[0]):
        temp_token = word_tokenize(country["Tags"][i])
        temp_set = [word for word in temp_token if not word in stop_words]
        temp2_set = set()
        for s in temp_set:
            temp2_set.add(lemm.lemmatize(s))
        vector = temp2_set.intersection(filtered_set)
        cos.append(len(vector))
    country['similarity']=cos
    country = country.sort_values(by='similarity', ascending=False)
    country.drop_duplicates(subset='Hotel_Name', keep='first', inplace=True)
    country.sort_values('Average_Score', ascending=False, inplace=True)
    country.reset_index(inplace=True)
    return country[["Hotel_Address","Average_Score","Hotel_Name","lat","lng"]].head(5)

# ------------------------------------------------------
st.set_page_config(layout="centered",page_icon="🛎️",page_title="Hotel Recommendation System")

streamlit_style = """
			<style>
			@import url('https://fonts.googleapis.com/css2?family=Staatliches&display=swap');

			html, body, [class*="css"]  {
			font-family: 'Staatliches', cursive;
			}
			</style>
			"""
st.markdown(streamlit_style, unsafe_allow_html=True)
#----------------------------------------------------------------
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
set_background('cover_hotel.jpg')
# ---------------------------------------------------------------

# ---------------------------------------------------------------
button_styl="""<style>

<!-- HTML !-->
<button class="button-27" role="button">Button 27</button>

/* CSS */
button {
  appearance: none;
  background-color: #000000;
  border: 2px solid #1A1A1A;
  border-radius: 15px;
  box-sizing: border-box;
  color: #FFFFFF;
  cursor: pointer;
  display: inline-block;
  font-family: Roobert,-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol";
  font-size: 16px;
  font-weight: 600;
  line-height: normal;
  margin: 0;
  min-height: 60px;
  min-width: 0;
  outline: none;
  padding: 16px 24px;
  text-align: center;
  text-decoration: none;
  transition: all 300ms cubic-bezier(.23, 1, 0.32, 1);
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
  width: 100%;
  will-change: transform;
}

button:disabled {
  pointer-events: none;
}

button:hover {
  box-shadow: rgba(0, 0, 0, 0.25) 0 8px 15px;
  transform: translateY(-2px);
}

button:active {
  box-shadow: none;
  transform: translateY(0);
}
        </style>"""
st.markdown(button_styl, unsafe_allow_html=True) 

#----------------------------------------------------------------

st.markdown("<h2 style='text-align: center; color: white;'>W  e  l  c  o  m  e<br/>to<br/>Hotel Recommendation System </h2>", unsafe_allow_html=True)
# ---------------------------------------------------------------

# ----------------------------------------------------------------
country = st.selectbox(
    'what is your destination?',
    ('Netherlands','UK','France','Spain','Italy','Austria'))
description = st.text_area('', placeholder='''
    type what is the purpose of your trip and room specifications ...
    ''')

if st.button('Recommend'):
  result1=recommend_hotel(country,description)
 
  m = folium.Map(location=[result1.iloc[0]['lat'], result1.iloc[0]['lng']], zoom_start=7)

    # add marker for Liberty Bell
  for i in range(0,len(result1)):
    folium.Marker(
        location=[result1.iloc[i]['lat'], result1.iloc[i]['lng']],
        popup=f"Hotel Score: {result1.iloc[i]['Average_Score']} <br> Hotel Address: {result1.iloc[i]['Hotel_Address']}"
        , tooltip=result1.iloc[i]['Hotel_Name'],icon=folium.Icon(icon="hotel",  color="red", prefix="fa")
      ).add_to(m)

    # call to render Folium map in Streamlit
  
  folium_static(m)




  
footer="""<style>
a:link , a:visited{
color: white;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
text-shadow: 2px 2px 8px black;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;

text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤ by <a style='display: block; text-align: center;' href="https://github.com/AbdelhamidADel" target="_blank">Abdelhamid Adel</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                  
                    header {visibility: hidden;}
                    </style>
                    """
st.markdown(hide_st_style, unsafe_allow_html=True)
# ------------------------------------------------
