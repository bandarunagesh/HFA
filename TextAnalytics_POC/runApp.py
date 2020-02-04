import os
import sys
from flask import Flask, render_template, request,make_response
from werkzeug import secure_filename
from fileRead import *
from wordclouds import *
from DescriptiveAnalysis import *
from sentimentTag import sentimentPredict,visuals
from Topic_Models_Visualisations import *
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

path = os.getcwd()

flist=[]
dfList = []
app = Flask(__name__,template_folder='templates')

@app.route('/')
def upload_html():
    return render_template('upload.html')

@app.route('/dataanalysis',methods=['GET','POST'])
def analyzeFile():
    if request.method == 'POST':
        f = request.files['file']
        flist.append(f)
        f.save(secure_filename(f.filename))
        if not f:
            return ('No file found')
        allowedExtensions = ['csv','txt','xlsx']
        if f.filename.strip().split('.')[1] not in allowedExtensions:
            return ('Please upload a file of .csv/.xlsx/.txt extensions')
        if f.filename.strip().split('.')[1] in allowedExtensions:
            if f.filename.strip().split('.')[1] == 'csv':
                df = csvRead(f.filename)
                dfList.append(df)
            elif f.filename.strip().split('.')[1] == 'xlsx':
                df = xlsxRead(f.filename)
                dfList.append(df)
            elif f.filename.strip().split('.')[1] == 'txt':
                df = txtRead(f.filename)
                dfList.append(df)
            return (render_template('upload.html',data=str(df.shape)))
              
@app.route('/structanalysis',methods=['GET','POST'])
def analysis():
    return (render_template('analysis.html'))

@app.route('/ngramanalysis',methods=['GET','POST'])
def ngramAnalysis():
    if request.method == "POST":
        ngramvalue = int(request.values.get("ngram_value"))
        print (ngramvalue)
        if ngramvalue == 2:
            number_of_entities = int(request.values.get('entities'))
            print (number_of_entities)
            wordCloud_Visuals(dfList[0],path,ngramvalue,
                              number_of_entities)
            image_file = 'WordCloud_Bigrams_Frequent.png'
            image_file = image_file.split('.')[0] + '_' + str(number_of_entities) + '.' + image_file.split('.')[1]
            return render_template('analysis.html',userimage = image_file)
        elif ngramvalue == 3:
            number_of_entities = int(request.values.get('entities'))
            print (number_of_entities)
            wordCloud_Visuals(dfList[0],path,ngramvalue,
                              number_of_entities)
            image_file = 'WordCloud_Trigrams_Frequent.png'
            image_file = image_file.split('.')[0] + '_' + str(number_of_entities) + '.' + image_file.split('.')[1]
            return render_template('analysis.html',userimage = image_file)
        
@app.route('/summaryanalysis',methods=['GET','POST'])
def summaryAnalysis():
    if request.method == "POST":
        report,total_summary,plans = descriptiveAnalyze(dfList[0])
        response = make_response(report.to_csv())
        response.headers["Content-Disposition"] = "attachment; filename=Summary.csv"
        response.headers["Content-Type"] = "text/csv"
        return (response)
    
@app.route('/detailedsummary',methods=['GET','POST'])
def detailedSummary():
    if request.method=='POST':
        report,total_summary,plans = descriptiveAnalyze(dfList[0])
        response = make_response(total_summary.to_csv())
        response.headers["Content-Disposition"] = "attachment; filename=detailed_summary.csv"
        response.headers["Content-Type"] = "text/csv"
        return (response)
    
@app.route('/downloadsentiments',methods=['GET','POST'])
def storeSentiments():
    if request.method == 'POST':
        dfList.append(sentimentPredict(dfList[0]))
        response = make_response(dfList[1].to_csv())
        response.headers["Content-Disposition"] = "attachment; filename=Sentiments_Mapped.csv"
        response.headers['Content-Type'] = "text/csv"
        return (response)
        
@app.route('/sentimentanalysis',methods=['GET','POST'])
def sentimentAnalysis():
    if request.method == 'POST':
        result_sentiments = sentimentPredict(dfList[0])
        filtervalue = request.values.get("filterSentiment")
        fullPath = visuals(result_sentiments,filtervalue)
        chartFile = os.path.split(fullPath)[1]
        return render_template('charts.html',myimage=chartFile)
                    
@app.route("/topicmodeling",methods=['GET','POST'])
def topicModeling():
    if request.method == 'POST':
        filterQuarter = str(request.values.get("filterQuarter"))
        filterRegion = str(request.values.get("filterRegion"))
        if ((filterQuarter == 'NULL') & (filterRegion != 'NULL')):
            mydf = dfList[0]
            df = mydf[mydf['region']==filterRegion]
            myvisuals = topicVisuals(df)
            return (render_template(myvisuals))
        elif ((filterQuarter != 'NULL') & (filterRegion == 'NULL')):
            mydf = dfList[0]
            df = mydf[mydf['rptqtr']==filterQuarter]
            myvisuals = topicVisuals(df)
            return (render_template(myvisuals))
        elif ((filterQuarter != 'NULL') & (filterRegion != 'NULL')):
            mydf = dfList[0]
            df = mydf[(mydf['rptqtr']==filterQuarter) & (mydf['region']==filterRegion)]
            myvisuals = topicVisuals(df)
            return (render_template(myvisuals))
        else:
            mydf = dfList[0]
            myvisuals = topicVisuals(mydf)
            return (render_template(myvisuals))
        
        
         
if __name__ == '__main__':
    app.run(debug = True)