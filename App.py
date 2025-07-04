from lead_generator import Google_maps_lead_scraper
import streamlit as st
import csv
import os

if 'data_ready' not in st.session_state:
    st.session_state.data_ready = False
st.title('✉️🌏Global business Lead scraper',anchor=False)
search_header = st.header("🔍 Search Details:",anchor=False)
with st.sidebar:
    with st.popover('How does it work ?'):
      st.markdown("""
1.Enter the Business Type & City\n
Start by typing the type of business you're targeting (e.g. Dentist, Gym, Lawyer) and the city you're interested in.

2.The Bot Scans Google Maps\n
Once you start the process, the bot automatically opens Google Maps, searches for businesses matching your criteria, and clicks through each result.

3.Scrapes Key Business Details\n
For each business, it extracts essential info like:

°Name

°Phone number

°Website

°Review score & number of reviews

°Street address & city

4.Data Exported to CSV\n
After gathering the data, a clean, ready-to-use spreadsheet is generated for download so you can use the leads in your marketing or outreach tools.

  """)
col1,col2= st.columns(2)
with col1:
    Business_input = st.text_input(label='Enter the type of business',placeholder='e.g, ("Dentist")')
with col2:
    City_input = st.text_input(label='Enter the city', placeholder='e.g, ("New York")')

run_bot_header =st.header("🏃‍♂️Run the bot ",anchor=False)
run_bot = st.button(label='Run bot')
if run_bot:
    if not Business_input or not City_input:
        st.error("Please enter both the business type and the city before running the bot")
        st.stop()
    else:
        with st.status(f'Running bot for {Business_input} in {City_input}...',expanded=True) as status:
            lead_scraper = Google_maps_lead_scraper()
            lead_scraper.input_business_and_location(f'{Business_input} in {City_input}')
            st.write('Scrolling the page')
            lead_scraper.scroll(5)
            st.write('Getting business names....')
            lead_scraper.scrape_business_name()
            st.write('Getting business reviews....')
            lead_scraper.scrape_business_review()
            st.write('Getting businesses personal information...')
            lead_scraper.press_on_each_business_link_and_scrape_details()
            st.write('Exporting the data to a csv...')
            lead_scraper.clean_lists()
            lead_scraper.export_to_csv()
            lead_scraper.export_to_spreadsheet()
            status.update(label='Scraping complete',state='complete',expanded=False)
            st.session_state.data_ready= True
if st.session_state.data_ready == True :
    col3,col4= st.columns(2)

    with col3:
        with open("Lead_Data.csv", "rb") as f:
            st.download_button("Download csv", data=f, file_name="Lead_Data.csv", mime="text/csv",icon=':material/download:')
        with open('Lead_Data.xlsx','rb') as file :
            st.download_button(label='Download Spreadsheet',data= file,file_name='Lead_Data.xlsx',mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',icon=':material/download:')
    with col4:
        csv_file_path = "Lead_Data.csv"
        if st.button("Delete CSV file"):
            if os.path.exists(csv_file_path):
                os.remove(csv_file_path)
                st.success("CSV file deleted!")