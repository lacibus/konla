import json
import requests
import vdlpy.vdl as vdl

def __init__(self):
    global source
    global auth
    global attributes
    source = None
    auth = None
    attributes = {
            'fingerprint', (vdl.NamedItm(source, 'paper_fingerprint'), False),
            'initialized', (vdl.NamedItm(source, 'paper_initialized'), False),
            'featureTable', (vdl.NamedItm(source, 'paper_featureTable'), True),
            'whole_completed', (vdl.NamedItm(source, 'paper_whole_completed'), False),
            'whole', (vdl.NamedItm(source, 'paper_whole'), False),
            'partial_completed', (vdl.NamedItm(source, 'paper_partial_completed'), False),
            'partial', (vdl.NamedItm(source, 'paper_partial'), False),
            'keywords_completed', (vdl.NamedItm(source, 'paper_keywords_completed'), False),
            'keywords', (vdl.NamedItm(source, 'paper_keywords'), True),
            'refs_completed', (vdl.NamedItm(source, 'paper_refs_completed'), False),
            'refs', (vdl.NamedItm(source, 'paper_refs'), False),
            'meta_completed', (vdl.NamedItm(source, 'paper_meta_completed'), False),
            'meta', (vdl.NamedItm(source, 'paper_meta'), False),
            'metrics_completed', (vdl.NamedItm(source, 'paper_metrics_completed'), False),
            'metrics', (vdl.NamedItm(source, 'paper_metrics'), False)
        }
    
def init(api_url, source_nr, credential_id, key):
    global source
    global auth
    source = source_nr
    vdl.set_api(api_url)
    auth = (vdl.Itm(credential_id), key)

def add():
    global source
    global auth
    return vdl.update(vdl.CreateItem('Paper', source), auth)['Paper'].itemid

def get(paper_id, attribute_name):
    global attributes
    global auth
    if attribute_name not in attributes: 
        raise StoreException("Unknown attribute: " + attribute_name)
    solutions = vdl.query([
            (vdl.Itm(paper_id), attrributes[attribute_name][0], vdl.Unknown('val'))
        ], auth)
    l = len(solutions)
    if l > 1: raise StoreException('Multiple values for attribute: ' + attribute_name)
    elif l == 0: return None
    else:
        val = solutions[0]['val']
        if attrributes[attribute_name][1]: return json.loads(val)
        else: return val
    

def put(paper_id, attribute_name, value):
    global attributes
    global auth
    if attribute_name not in attributes: 
        raise StoreException("Unknown attribute: " + attribute_name)
    if attrributes[attribute_name][1]: val = json.dumps(value)
    else: val = value
    vdl.update(vdl.SetUniqueObject(
        vdl.Itm(paper_id), attrributes[attribute_name], val), auth)            
            
class StoreException(RuntimeError):
    '''
    A run-time exception occurring during a store operation.
    '''
    def __init__(self, *messages):
        super().__init__(*messages)
       
