from nl4dv import *
import nl4dv
import altair as alt
from IPython.display import display
import streamlit as st
import streamlit.components.v1 as components

from bokeh.models import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import *
from bokeh.io import curdoc
from bokeh.io import show
from PIL import Image


col1, col2 = st.columns(2)
with col1:
    st.image('im.png',width=300)
with col2:
    st.markdown('<h1 style="text-align:center;color:white;font-weight:bolder;font-size50px;">Data Guru</h1>',unsafe_allow_html=True)

url = st.text_input('enter URL')
if url:
    data_url = url
    label_attribute = None
    dependency_parser_config = {"name": "spacy",
                                "model": "en_core_web_sm", "parser": None}
    nl4dv_instance = NL4DV(verbose=False,
                           debug=True,
                           data_url=data_url,
                           label_attribute=label_attribute,
                           dependency_parser_config=dependency_parser_config
                           )
    

stt_button = Button(label="Speak", button_type="danger")
stt_button.js_on_click(
    CustomJS(code="console.log('button: You have clicked on the button!')"))


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
        a = result.get("GET_TEXT")
        st.write(result.get("GET_TEXT"))
        try:
            response = nl4dv_instance.analyze_query(a)
            image = (alt.display.html_renderer(response['visList'][0]['vlSpec']))

            with open('visualization.html', 'w') as f:
                f.write(image['text/html'])

            pf = open("F:/code/mistrel/nl4dv/visualization.html", 'r')
            components.html(pf.read(), width=900, height=900, scrolling=True)
        except Exception:
            st.markdown('Something is wrong with query,Try agin !!🫠')

    #display(alt.display.html_renderer(response['visList'][0]['vlSpec']), raw=True)
        
# show(stt_button)
# curdoc().add_root(stt_button)
# st.bokeh_chart(curdoc().to_json())