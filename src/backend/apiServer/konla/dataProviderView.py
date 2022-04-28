from . import store

def provideWholeSummarisation(request):
    try:
        paper_id=request.session["paperFingerprint"]
    except KeyError:
        return {
            "current_status": 0,
            "errors": ["No file uploaded!"],
            "messages": [],
            "result": {}
        }
    if store.get(paper_id, "initialized")==None:
        return {
            "current_status": 0,
            "errors": ["No file uploaded!"],
            "messages": [],
            "result": {}
        }
    elif store.get(paper_id, "featureTable")["enableWholeSummarisation"]==False:
        return {
            "current_status": 0,
            "errors": ["Whole summarisation is disabled!"],
            "messages": [],
            "result": {}
        }
    
    elif store.get(paper_id, "initialized")==False:
        return {
            "current_status": -1,
            "errors": ["System initializing, analysis did not start yet!"],
            "messages": [],
            "result": {}
        }
    elif store.get(paper_id, "whole_completed") == False:
        return {
            "current_status": -1,
            "errors": ["Whole summarisation is in progress!"],
            "messages": [],
            "result": {}
        }
    elif store.get(paper_id, "whole_completed") == True:
        result=store.get(paper_id, "whole")
        response={
            "current_status": 1,
            "errors": [],
            "messages": [],
            "result": {"whole_summarisation":result}
        }
        return response
    else:
        return {
            "current_status": 0,
            "errors": ["Unknown error!"],
            "messages": [],
            "result": {}
        }

def providePartialSummarisation(request):
    try:
        paper_id=request.session["paperFingerprint"]
    except KeyError:
        return {
            "current_status": 0,
            "errors": ["No file uploaded!"],
            "messages": [],
            "result": {}
        }
    if store.get(paper_id, "initialized")==None:
        return {
            "current_status": 0,
            "errors": ["No file uploaded!"],
            "messages": [],
            "result": {}
        }
    elif store.get(paper_id, "featureTable")["enablePartialSummarisation"]==False:
        return {
            "current_status": 0,
            "errors": ["Partial summarisation is disabled!"],
            "messages": [],
            "result": {}
        }
    
    elif store.get(paper_id, "initialized")==False:
        return {
            "current_status": -1,
            "errors": ["System initializing, analysis did not start yet!"],
            "messages": [],
            "result": {}
        }
    elif store.get(paper_id, "partial_completed") == False:
        return {
            "current_status": -1,
            "errors": ["Partial summarisation is in progress!"],
            "messages": [],
            "result": {}
        }
    elif store.get(paper_id, "partial_completed") == True:
        result=store.get(paper_id, "partial")
        response={
            "current_status": 1,
            "errors": [],
            "messages": [],
            "result": {"partial_summarisation":result}
        }
        return response
    else:
        return {
            "current_status": 0,
            "errors": ["Unknown error!"],
            "messages": [],
            "result": {}
        }


def provideKeywords(request):
    try:
        paper_id=request.session["paperFingerprint"]
    except KeyError:
        return {
            "current_status": 0,
            "errors": ["No file uploaded!"],
            "messages": [],
            "result": {}
        }
    if store.get(paper_id, "initialized")==None: # avoid key error
        return {
            "current_status": 0,
            "errors": ["No file uploaded!"],
            "messages": [],
            "result": {}
        }
    elif store.get(paper_id, "featureTable")["enableKeywords"]==False:
        return {
            "current_status": 0,
            "errors": ["Keywords analysis is disabled!"],
            "messages": [],
            "result": {}
        }
    elif store.get(paper_id, "initialized")==False:
        return {
            "current_status": -1,
            "errors": ["System initializing, analysis did not start yet!"],
            "messages": [],
            "result": {}
        }
    elif store.get(paper_id, "keywords_completed") == False:
        return {
            "current_status": -1,
            "errors": ["Keywords analysis is in progress!"],
            "messages": [],
            "result": {}
        }
    elif store.get(paper_id, "keywords_completed") == True:
        result=store.get(paper_id, "keywords")
        if request.GET.get("max") != None:
            maxNum=int(request.GET.get("max"))
        else:
            maxNum=100
        ignoreCase=True if request.GET.get("ignorecase") == "1" else False
        extractLemma=True if request.GET.get("extractlemma") == "1" else False
        provisionalResult={}
        if extractLemma:
            provisionalResult=result["lemma"]
        elif ignoreCase:
            provisionalResult=result["ignoreCase"]
        else:
            provisionalResult=result["normal"]
        finalResultKey=sorted(provisionalResult,key=lambda x:provisionalResult[x],reverse=True)[:maxNum]
        finalResult={}
        for i in finalResultKey:
            finalResult[i]=provisionalResult[i]
        
        response={
            "current_status": 1,
            "errors": [],
            "messages": [],
            "result": {"keywords":finalResult}
        }
        return response
    else:
        return {
            "current_status": 0,
            "errors": ["Unknown error!"],
            "messages": [],
            "result": {}
        }


def provideRefs(request):
    try:
        paper_id=request.session["paperFingerprint"]
    except KeyError:
        return {
            "current_status": 0,
            "errors": ["No file uploaded!"],
            "messages": [],
            "result": {}
        }
    if store.get(paper_id, "initialized")==None:
        return {
            "current_status": 0,
            "errors": ["No file uploaded!"],
            "messages": [],
            "result": {}
        }
    elif store.get(paper_id, "featureTable")["enableRefs"]==False:
        return {
            "current_status": 0,
            "errors": ["References extraction is disabled!"],
            "messages": [],
            "result": {}
        }
    
    elif store.get(paper_id, "initialized")==False:
        return {
            "current_status": -1,
            "errors": ["System initializing, analysis did not start yet!"],
            "messages": [],
            "result": {}
        }
    elif store.get(paper_id, "refs_completed") == False:
        return {
            "current_status": -1,
            "errors": ["References extraction is in progress!"],
            "messages": [],
            "result": {}
        }
    elif store.get(paper_id, "refs_completed") == True:
        result=store.get(paper_id, "refs")
        response={
            "current_status": 1,
            "errors": [],
            "messages": [],
            "result": {"refs":result}
        }
        return response
    else:
        return {
            "current_status": 0,
            "errors": ["Unknown error!"],
            "messages": [],
            "result": {}
        }






def provideMeta(request):
    try:
        paper_id=request.session["paperFingerprint"]
    except KeyError:
        return {
            "current_status": 0,
            "errors": ["No file uploaded!"],
            "messages": [],
            "result": {}
        }
    if store.get(paper_id, "initialized")==None:
        return {
            "current_status": 0,
            "errors": ["No file uploaded!"],
            "messages": [],
            "result": {}
        }
    elif store.get(paper_id, "featureTable")["enableMeta"]==False:
        return {
            "current_status": 0,
            "errors": ["Metadata extraction is disabled!"],
            "messages": [],
            "result": {}
        }
    
    elif store.get(paper_id, "initialized")==False:
        return {
            "current_status": -1,
            "errors": ["System initializing, analysis did not start yet!"],
            "messages": [],
            "result": {}
        }
    elif store.get(paper_id, "meta_completed") == False:
        return {
            "current_status": -1,
            "errors": ["Metadata extraction is in progress!"],
            "messages": [],
            "result": {}
        }
    elif store.get(paper_id, "meta_completed") == True:
        result=store.get(paper_id, "meta")
        response={
            "current_status": 1,
            "errors": [],
            "messages": [],
            "result": {"metadata":result}
        }
        return response
    else:
        return {
            "current_status": 0,
            "errors": ["Unknown error!"],
            "messages": [],
            "result": {}
        }






def provideMetric(request):
    try:
        paper_id=request.session["paperFingerprint"]
    except KeyError:
        return {
            "current_status": 0,
            "errors": ["No file uploaded!"],
            "messages": [],
            "result": {}
        }
    if store.get(paper_id, "initialized")==None:
        return {
            "current_status": 0,
            "errors": ["No file uploaded!"],
            "messages": [],
            "result": {}
        }
    elif store.get(paper_id, "featureTable")["enableMetrics"]==False:
        return {
            "current_status": 0,
            "errors": ["Metrics is disabled!"],
            "messages": [],
            "result": {}
        }
    
    elif store.get(paper_id, "initialized")==False:
        return {
            "current_status": -1,
            "errors": ["System initializing, Metrics did not start yet!"],
            "messages": [],
            "result": {}
        }
    elif store.get(paper_id, "metrics_completed") == False:
        return {
            "current_status": -1,
            "errors": ["Metrics extraction is in progress!"],
            "messages": [],
            "result": {}
        }
    elif store.get(paper_id, "metrics_completed") == True:
        result=store.get(paper_id, "metrics")
        response={
            "current_status": 1,
            "errors": [],
            "messages": [],
            "result": {"metrics":result}
        }
        return response
    else:
        return {
            "current_status": 0,
            "errors": ["Unknown error!"],
            "messages": [],
            "result": {}
        }