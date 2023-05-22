from nl4dv import NL4DV
import altair as alt
from IPython.display import display
import streamlit as st
import streamlit.components as components

from bokeh.models import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import *
from bokeh.io import curdoc
from bokeh.io import show
from PIL import Image
im=Image.open('illus.png')
st.set_page_config(page_title="Handsfree Database Visualization",page_icon = im)

st.markdown('<h1 style="text-align:center;color:white;font-weight:bolder;font-size:100px;">Data Yogi</h1>',unsafe_allow_html=True)
st.image('illus.png',width=300)


st.write('## 1. Drop CSV file :wink:')
f = st.file_uploader('pdf file', type='csv', key='pdf_file', disabled=False, on_change=None, label_visibility="collapsed")
if f is not None:
            path = f.name
           

#solutions= toggle button, add timer, add stop button
# st.header('headers')

stt_button = Button(label="Speak",button_type="danger")
stt_button.js_on_click(CustomJS(code = "console.log('button: You have clicked on the button!')"))


stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    console.log('inner code');
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.start();
    

    """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)


if result:
    if "GET_TEXT" in result:
        a=result.get("GET_TEXT")
        st.write(result.get("GET_TEXT"))
# show(stt_button)
# curdoc().add_root(stt_button)
# st.bokeh_chart(curdoc().to_json())


            
#####Should run whenever csv file is uploaded
data_url = path
label_attribute = None
dependency_parser_config = {"name": "spacy", "model": "en_core_web_sm", "parser": None}

nl4dv_instance = NL4DV(verbose=False, 
                       debug=True, 
                       data_url=data_url, 
                       label_attribute=label_attribute, 
                       dependency_parser_config=dependency_parser_config
                       )
####################################


###########Should run whenever query is asked
response = nl4dv_instance.analyze_query("Show the average budget of movies per genre")
#display(alt.display.html_renderer(response['visList'][0]['vlSpec']), raw=True)
image = (alt.display.html_renderer(response['visList'][0]['vlSpec']))
if st.button('get answer',  type='primary', use_container_width=True):
    st.write("done 	:+1: ")
with open('visualization.html', 'w') as f:
    f.write(image['text/html'])
pf=open("F:/code/mistrel/nl4dv/visualization.html",'r')
components.html(pf.read(),width=400,height=400,scrolling=True)


#####################################################

