import streamlit as st
import streamlit.components.v1 as components
pf=open("F:/code/mistrel/nl4dv/visualization.html",'r')
components.html(pf.read(),width=400,height=400,scrolling=True)