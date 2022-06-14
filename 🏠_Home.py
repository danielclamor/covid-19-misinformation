import streamlit as st
from PIL import Image

if __name__ == '__main__':
    st.set_page_config(page_title='COVID-19 Misinfo Tweets',
                       layout='wide',
                       page_icon='😷')

    st.title('COVID-19 Misinformation Tweets: Identification and Analysis')

    pandemic_text = '''
                    The COVID-19 pandemic started after the first casualty outside China, 
                    in the Philippines, and inflicted a lasting impact on the lives of many people. 
                    COVID-19 or Coronavirus disease is caused by the newfound coronavirus, 
                    SARS-CoV-2 virus, that is transmissible through saliva droplets or nose discharge.
                    '''

    infodemic_text = '''
                     With the pandemic, an "infodemic" or information outbreak has started and 
                     it contains both true and false information according to the 
                     World Health Organization.
                     '''

    col1, col2, col3 = st.columns(3)
    with col1:
        image = Image.open('data-res/files-needed/sars-cov-2.png')
        st.image(image,
                 caption='SARS-CoV-2 virus image from Wikimedia Commons')

    with col2:
        st.subheader('The Pandemic')
        st.markdown('''
                    <p>{text}</p>
                    '''.format(text=pandemic_text),
                    unsafe_allow_html=True)
        st.subheader('The Infodemic')
        st.markdown('''
                    <p>{text}</p>
                    '''.format(text=infodemic_text),
                    unsafe_allow_html=True)

    with col3:
        st.subheader('About')
        st.markdown('''This research project tackled three main tasks:''')
        st.markdown('1. Identification of COVID-19-related health misinformation tweets')
        st.markdown('2. Extract common topics from identified misinformation tweets')
        st.markdown('3. Visualize the spread of misinformation on Twitter')