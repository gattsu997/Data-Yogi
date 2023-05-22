import json
from nl4dv import NL4DV
import sys
sys.path.append("K:/MistralHack/NL4DV/venv/Lib/site-packages")
import streamlit as st
import os
import altair as alt
import streamlit as st
# from altair import vega, vegalite
# vega.renderers.enable('colab')
# vegalite.renderers.enable('colab')
from IPython.display import display


def update_csv(path):
    data_url = path
    label_attribute = None
    dependency_parser_config = {"name": "spacy", "model": "en_core_web_sm", "parser": None}
    nl4dv_instance = NL4DV(verbose=False, 
                        debug=True, 
                        data_url=data_url, 
                        label_attribute=label_attribute, 
                        dependency_parser_config=dependency_parser_config
                        )
    return nl4dv_instance

def query_ans(query,inst):
    response = inst.analyze_query(query)
    #display(alt.display.html_renderer(response['visList'][0]['vlSpec']), raw=True)
    image = (alt.display.html_renderer(response['visList'][0]['vlSpec']))

    with open('visualization.html', 'w') as f:
        f.write(image['text/html'])
        
    # pf=open("visualisation.html",'r')
    # components.html(pf.read(),widht=400,height=400,scrolling=True)


def main():
    print("data set url/path")
    url = input("enter the url")
    inst = update_csv(url)
    while(True):
        print('enter your query---')
        query = input()
        query_ans(query,inst)       

main()