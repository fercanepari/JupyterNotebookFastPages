# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 16:15:18 2021

@author: CanepariF
"""

import streamlit as st
import requests

base_url = 'https://fercanepari.pythonanywhere.com/notes'

# Define callbacks to handle button clicks.
def handle_click(i, j):
    button_pressed = i
    print("Se presionó:")
    print(button_pressed)
    url = base_url + '/' + button_pressed
    
    response = requests.delete(
                url 
                #data=json.dumps(payload), 
                #headers=headers,
                #auth=HTTPBasicAuth(toggl_token, 'api_token')
                )
    print(response)


st.title("Llamada a flask API. Creacion de Notas")

st.write("Blog y otras apps: [link](http://fercanepari.com.ar/)")
st.write("Flask API: [link](https://fercanepari.pythonanywhere.com/notes)")

#Form
with st.form(key='insertform'):
    nav1, nav2, nav3 = st.columns([2,3,1])
    
    st.subheader("Nueva Nota")
    
    with nav1:
        title_text = st.text_input(label='title')
    with nav2:
        description_text = st.text_area(label='description')
    with nav3:
        st.text("Insertar")
        submit_insert = st.form_submit_button(label='Guardar')

        

if submit_insert:
    new_note = {'title': title_text,
                    'description': description_text,
                    'uploadDate': '20210924'}
    resp = requests.post(base_url,data = new_note)
    #st.success("Nota insertada!")    
    #st.balloons()

NOTE_HTML_TEMPLATE = """
<div>
    ---------------------------------------------------------------------------------------
    <h6>NoteID:{}</h6>
    <h4>Titulo:{}</h4>
    <h4>Descripcion:{}</h4>
    <h6>Creado:{}</h6>
</div>
"""

# Call API
response = requests.get(base_url)
r_dictionary = response.json()

#Parse json
for i in response.json():
    print(i)
    note_tile, note_description, note_uploadDate = "","",""
    for j in r_dictionary[i]:
        #print(j)
        if j=='title':
            note_tile = r_dictionary[i][j]
        if j=='description':
            note_description = r_dictionary[i][j]
        if j=='uploadDate':
            note_uploadDate = r_dictionary[i][j]
        
    st.markdown(NOTE_HTML_TEMPLATE.format(i, note_tile, note_description, note_uploadDate), 
                                          unsafe_allow_html=True)    
      
    st.button(
                'Eliminar',
                key=f"{i}",
                on_click=handle_click,
                args=(i, j),
            )





