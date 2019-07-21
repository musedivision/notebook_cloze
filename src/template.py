# card template

NBC_CARD_NAME = "Notebook Cloze"

NBC_FLDS = {
    'is': u"Instructions",
    'lk': u"Notebook link",
    'an': u"Answer Cloze" 
}

NBC_FLD_IDS = [ 'is', 'lk', 'an' ]  

nbc_card_front = """\
{{%(instruction)s}}
<a href="{{%(notebook_link)s}}"> notebook </a>
""" % \
{'instruction': NBC_FLDS['is'],
 'notebook_link': NBC_FLDS['lk']}

nbc_card_back = """\
{{%(answer)s}}
""" % \
{'answer': NBC_FLDS['an']}

nbc_card_css = """\
.body {
    background: "red"
}
"""

def add_nbc_model(col):
    models = col.models
    nbc_model = models.new(NBC_CARD_NAME)
    
    for i in NBC_FLD_IDS:
        fld = models.newField(NBC_FLDS[i])
        models.addField(nbc_model, fld)
    # add Template
    template = models.newTemplate(NBC_CARD_NAME)
    template['qfmt'] = nbc_card_front
    template['afmt'] = nbc_card_back
    nbc_model['css'] = nbc_card_css

    models.addTemplate(nbc_model, template)
    models.add(nbc_model)

    return nbc_model

