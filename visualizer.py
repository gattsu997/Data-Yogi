from nl4dv import NL4DV
import altair as alt
from IPython.display import display

#####Should run whenever csv file is uploaded
data_url = "https://raw.githubusercontent.com/nl4dv/nl4dv/master/examples/assets/data/movies-w-year.csv"
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
response = nl4dv_instance.analyze_query("movie with highest worldwide gross")
#display(alt.display.html_renderer(response['visList'][0]['vlSpec']), raw=True)
image = (alt.display.html_renderer(response['visList'][0]['vlSpec']))
with open('visualization.html', 'w') as f:
    f.write(image['text/html'])

#####################################################

