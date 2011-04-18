"""
.. automodule:: model.database
"""

def load_model(classes):
    o = {}
        
    for i in classes:
        a = i()
        if a.key in o:
            o[a.key].update(a.read())
        else:
            o[a.key] = a.read()
            
    return o
    