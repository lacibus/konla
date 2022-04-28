from . import store

from .form import selectionForm

from .PaperProcessor.PaperProcessor import PaperProcessor
from threading import Thread
# COMP0016-Team6-Minyi Lei

def startProcessing(request):
    try:
        if request.method=="POST":
            form=selectionForm(request.POST)
            if not form.is_valid():
                raise Exception("Invalid form!")

        featureTable={
            "enableWholeSummarisation":True if form.cleaned_data["whole"] == 1 else False,
            "enablePartialSummarisation":True if form.cleaned_data["partial"] == 1 else False,
            "enableKeywords":True if form.cleaned_data["keywords"] == 1 else False,
            "enableRefs":True if form.cleaned_data["refs"] == 1 else False,
            "enableMeta":True if form.cleaned_data["metadata"] == 1 else False,
            "enableMetrics":True if form.cleaned_data["metrics"] == 1 else False
        }
        if "paperFingerprint" not in request.session:
            raise Exception("No file uploaded! Session data missing!")
        paper_id=request.session["paperFingerprint"]
        store.put(paper_id, "featureTable",featureTable)
        threadMain=Thread(target=mainThread,args=(request.session["uploadedFile"],paper_id,featureTable))
        threadMain.start()

        response={
            "current_status": 1,
            "errors": [],
            "messages": [],
            "result": {}
        }

    except Exception as e:
        response={
            "current_status": 0,
            "errors": [str(e)],
            "messages": [],
            "result": {}
        }
    finally:
        return response

def mainThread(path,paper_id,featureTable):
    store.put(paper_id,"initialized",False)
    pp=PaperProcessor(path)

    if featureTable["enableWholeSummarisation"]:
        whole=Thread(target=wholeSummarisationThread,args=(prefix,pp))
        store.put(paper_id,"whole_completed",False)
        whole.start()
    if featureTable["enablePartialSummarisation"]:
        partial=Thread(target=partialSummarisationThread,args=(prefix,pp))
        store.put(paper_id,"partial_completed",False)
        partial.start()
    if featureTable["enableKeywords"]:
        keyword=Thread(target=keywordThread,args=(prefix,pp))
        store.put(paper_id,"keywords_completed",False) # 0: in progress, 1: completed, -1: disabled
        keyword.start()

    if featureTable["enableRefs"]:
        refs=Thread(target=referencesThread,args=(prefix,pp))
        store.put(paper_id,"refs_completed",False)
        refs.start()
    
    if featureTable["enableMeta"]:
        meta=Thread(target=metadataThread,args=(prefix,pp))
        store.put(paper_id,"meta_completed",False)
        meta.start()
    
    if featureTable["enableMetrics"]:
        metrics=Thread(target=metricsThread,args=(prefix,pp))
        store.put(paper_id,"metrics_completed",False)
        metrics.start()
    
    store.put(paper_id,"initialized",True)

def wholeSummarisationThread(prefix,paperProcessor):
    summary=paperProcessor.summarize_whole()
    store.put(paper_id,"whole",summary)
    store.put(paper_id,"whole_completed",True)

def partialSummarisationThread(prefix,paperProcessor):
    summary=paperProcessor.summarize_partial()
    store.put(paper_id,"partial",summary)
    store.put(paper_id,"partial_completed",True)

def keywordThread(prefix,paperProcessor):
    normalResult=paperProcessor.wordFrequency(max=100,ignoreCase=False,useLemma=False)
    ignoreCaseResult=paperProcessor.wordFrequency(max=100,ignoreCase=True,useLemma=False)
    lemmaResult=paperProcessor.wordFrequency(max=100,ignoreCase=False,useLemma=True)
    result={
        "normal": normalResult,
        "ignoreCase": ignoreCaseResult,
        "lemma": lemmaResult
    }
    #time.sleep(60)
    store.put(paper_id,"keywords",result)
    store.put(paper_id,"keywords_completed",True) # -1 means feature disabled, 0 means feature in progress, 1 means feature completed

def referencesThread(prefix,paperProcessor):
    refs=paperProcessor.references()
    store.put(paper_id,"refs",refs)
    store.put(paper_id,"refs_completed",True)

def metadataThread(prefix,paperProcessor):
    meta=paperProcessor.metaData()
    store.put(paper_id,"meta",meta)
    store.put(paper_id,"meta_completed",True)

def metricsThread(prefix,paperProcessor):
    metrics=paperProcessor.metrics()
    store.put(paper_id,"metrics",metrics)
    store.put(paper_id,"metrics_completed",True)


