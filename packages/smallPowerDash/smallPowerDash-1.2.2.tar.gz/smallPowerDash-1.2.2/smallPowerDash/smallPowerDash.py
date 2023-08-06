import os,re,pandas as pd
import dash, dash_core_components as dcc, dash_html_components as html, dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px, plotly.graph_objects as go
import matplotlib.pyplot as plt, matplotlib.colors as mtpcl
from pylab import cm
import datetime as dt, pickle, time
from libs.templateDash import TemplateDashMaster
from libs.dccExtended import DccExtended

class SmallPowerDash(TemplateDashMaster):
    # extSheets = [dbc.themes.BOOTSTRAP]
    # ==========================================================================
    #                       INIT FUNCTIONS
    # ==========================================================================

    def __init__(self,cfg,skipEveryHours=120,port=45103,refreshSeconds=60):
        super().__init__(cfg,baseNameUrl='/smallPowerDash/',
                            title='small Power Dash',port=port,extSheets='bootstrap',cacheRedis=False)
        self.skipEveryHours = skipEveryHours
        self.formatTime     = '%Y-%m-%d %H:%M'
        self.refreshSeconds = refreshSeconds

    # ==========================================================================
    #                       BASIC FUNCTIONS
    # ==========================================================================

    def exportDFOnClick(self,df,timeRange,folder=None,baseName='smallPower'):
        timeRange = [re.findall('\d{4}-\d{2}-\d{2} \d{2}:\d{2}',k)[0] for k in timeRange]
        timeRange = [re.sub('[: ]','_',k) for k in timeRange]
        filename = baseName +  '_' + timeRange[0] + ' ' + timeRange[1]
        if not folder : folder = self.cfg.folderExport
        df.to_csv(folder + filename + '.txt')

    def buildLayout(self,listWidgets,baseId,widthG=80,nbGraphs=1,nbCaches=0):
        widgetLayout,dicLayouts = [],{}
        for widgetId in listWidgets:
            if 'dd_listFiles' in widgetId  :
                widgetObj = self.dccE.dropDownFromList(baseId+widgetId,self.cfg.listFilesPkl,'Select your File : ',
                    labelsPattern='\d{4}-\d{2}-\d{2}-\d{2}',defaultIdx=-1)


            elif 'dd_Tag' in widgetId:
                widgetObj = self.dccE.dropDownFromList(baseId+widgetId,list(self.cfg.getTagsRegexp('',ds=True).TAG),
                'Select type graph : ',defaultIdx=0,multi=True,
                style={'fontsize':'20 px','height': '40px','min-height': '1px',},optionHeight=20)

            elif 'dd_cmap' in widgetId:
                widgetObj = self.dccE.dropDownFromList(baseId+widgetId,self.cfg.cmaps[0],
                                                'select the colormap : ',value='jet')

            elif 'in_step' in widgetId:
                widgetObj = [html.P('skip points : '),
                dcc.Input(id=baseId+widgetId,placeholder='skip points : ',type='number',min=1,step=1,value=20)]

            elif 'in_roll' in widgetId:
                widgetObj = [html.P('time resolution : '),
                dcc.Input(id=baseId+widgetId,placeholder='time resolution : ',type='text',value='60s')]

            elif 'btn_legend' in widgetId:
                widgetObj = [html.Button('description',id=baseId+widgetId, n_clicks=1)]

            elif 'btn_export' in widgetId:
                widgetObj = [html.Button('export .txt',id=baseId+widgetId, n_clicks=0)]

            elif 'btn_style' in widgetId:
                widgetObj = [html.Button('lines+markers',id=baseId+widgetId, n_clicks=0)]

            elif 'btn_Update' in widgetId:
                widgetObj = [html.Button(children='recompute',id=baseId+widgetId, n_clicks=0)]

            elif 'dd_Units' in widgetId :
                widgetObj = self.dccE.dropDownFromList(baseId+widgetId,self.cfg.listUnits,'Select units graph : ',value='A')

            elif 'in_patternTag' in widgetId  :
                widgetObj = [html.P('pattern with regexp on tag : '),
                dcc.Input(id=baseId+widgetId,type='text',value='BLR')]

            elif 'dd_typeTags' in widgetId:
                widgetObj = self.dccE.dropDownFromList(baseId+widgetId,list(self.cfg.usefulTags.index),
                            'Select type graph : ',defaultIdx=0,
                            style={'fontsize':'20 px','height': '40px','min-height': '1px',},optionHeight=20)

            elif 'dd_patternCat' in widgetId:
                widgetObj = self.dccE.dropDownFromList(baseId+widgetId,self.cfg.allPatterns,
                            'Select regExpPattern : ',defaultIdx=0,
                            style={'fontsize':'20 px','height': '40px','min-height': '1px',},optionHeight=20)

            elif 'dd_multiPattern' in widgetId:
                widgetObj = self.dccE.dropDownFromList(baseId+widgetId,self.cfg.allPatterns,
                                            style={'fontsize':'20 px','height': '40px','min-height': '1px',},
                                            multi=True,optionHeight=20)

            elif 'rs_time' in widgetId:
                widgetObj = self.dccE.timeRangeSlider(baseId+widgetId)

            elif 'in_time' in widgetId:
                t1 = dt.datetime.now()
                t1 = t1 - dt.timedelta(hours=t1.hour+1)
                t0 = t1 - dt.timedelta(days=3)
                t0,t1 = [d.strftime(self.formatTime) for d in [t0,t1]]
                widgetObj = [
                html.Div([
                    dbc.Row([dbc.Col(html.P('select start and end time : '))]),
                    dbc.Row([dbc.Col(dcc.Input(id = baseId + widgetId + 'Start',type='text',value = t0,size='13',style={'font-size' : 13})),
                            dbc.Col(dcc.Input(id = baseId + widgetId + 'End',type='text',value = t1,size='13',style={'font-size' : 13}))])
                ])]

            elif 'pdr_time' in widgetId :
                tmax = dt.datetime.now()
                tmax = dt.datetime(2021,4,19)
                t1 = tmax - dt.timedelta(hours=tmax.hour+1)
                t0 = t1 - dt.timedelta(days=3)

                widgetObj = [
                html.Div([
                    dbc.Row([dbc.Col(html.P('select start and end time : ')),
                        dbc.Col(html.Button(id  = baseId + widgetId + 'Btn',children='update Time'))]),

                    dbc.Row([dbc.Col(dcc.DatePickerRange( id = baseId + widgetId + 'Pdr',
                                min_date_allowed = dt.date(2021, 3, 15),max_date_allowed = tmax, initial_visible_month = t0.date(),
                                display_format = 'MMM D, YY',minimum_nights=0,
                                start_date = t0.date(), end_date   = t1.date()))]),

                    dbc.Row([dbc.Col(dcc.Input(id = baseId + widgetId + 'Start',type='text',value = '07:00',size='13',style={'font-size' : 13})),
                            dbc.Col(dcc.Input(id = baseId + widgetId + 'End',type='text',value = '21:00',size='13',style={'font-size' : 13}))])
                ])]

            elif 'in_axisSp' in widgetId  :
                widgetObj = [html.P('select the space between axis : '),
                dcc.Input(id=baseId+widgetId,type='number',value=0.1,max=1,min=0,step=0.02)]

            elif 'int_RT' in widgetId :
                widgetObj = [dcc.Interval(
                    id=baseId+widgetId,
                    interval=self.refreshSeconds*1000, # in milliseconds
                    n_intervals=0
                )]

            for widObj in widgetObj:
                widgetLayout.append(widObj)

        dicLayouts['widgetLayout'] = html.Div(widgetLayout,
                                    style={"width": str(100-widthG) + "%", "float": "left"})

        dicLayouts['cacheLayout']= html.Div([html.Div(id=baseId+'fileInCache' + str(k)) for k in range(1,nbCaches+1)],
                                    style={"display": "none"})

        dicLayouts['graphLayout']= html.Div([dcc.Graph(id=baseId+'graph' + str(k)) for k in range(1,nbGraphs+1)],
                                    style={"width": str(widthG) + "%", "display": "inline-block"})


        layout = html.Div(list(dicLayouts.values()))
        return layout

    def updateLegend(self,df,fig,legendType,pivoted=False,breakLine=None,addUnit=False):
        if legendType%3==1: # description name
            dfDes       = self.cfg.getTagDescription(df,pivoted,2)
            newNames    = dfDes[self.cfg.descriptCol]
            dictNames   = dict(zip(dfDes[self.cfg.tagCol],newNames))
            fig         = self.cfg.utils.customLegend(fig,dictNames,breakLine=breakLine)
        elif legendType%3==2: # unvisible
            fig.update_layout(showlegend=False)
        return fig

    def saveImage(self,fig,figname,w=1500,h=400):
        fig.write_image(self.cfg.folderFig + figname + '.png',width=w,height=h)

    def computeDataFrame(self,date0,date1,t0,t1,toJson=True):
        df = self.cfg.loadDFTimeRange([date0+' '+t0,date1+' '+t1],'',self.skipEveryHours)
        print('======================================='),print('dataframe reading finished'),print('=======================================')
        if toJson : df=df.to_json(date_format='iso', orient='split')
        return df

    def preparePivotedData(self,df,tags,rs='1s'):
        df = self.cfg.getDFfromTagList(df,tags)
        df = self.cfg.pivotDF(df,rs)
        return df

    # ==========================================================================
    #                           DASH LAYOUTS
    # ==========================================================================

    def singleCatGraphLayout(self,idBase,widthG=80,heightGraph=900):
        listWidgets = ['dd_listFiles','dd_Units','dd_patternCat','dd_multiPatternSubCat',
                        'btn_legend','in_step','dd_cmap']

        SCG_html=self.buildLayout(listWidgets,idBase,widthG=widthG,cacheFile=self.cacheRedis)

        def loadDataFrame(filename,tagPattern,unit):
            return self.cfg.getDFTagsTU(self.cfg.loadFile(filename),tagPattern,unit)

        @self.app.callback(
        Output(idBase + 'btn_legend', 'children'),Input(idBase + 'btn_legend','n_clicks'))
        def updateBtnState(legendType):return self.changeLegendBtnState(legendType)

        @self.app.callback(
        Output(idBase+'dd_multiPatternSubCat','options'),
        Input(idBase+'dd_Units','value'),Input(idBase+'dd_patternCat','value'))
        def updateDropDownCat(unitName,pattern):
            return [{'label': i, 'value': i} for i in self.cfg.getCatsFromUnit(unitName,pattern)]

        dictOptsGraph = {k : 'value' for k in ['fileInCache','in_step','dd_cmap']}
        dictOptsGraph['btn_legend'] = 'n_clicks'

        if self.cacheRedis :
            @self.cache.memoize()
            def storeDF(value):
                return loadDataFrame(value[0],value[1],value[2])

            @self.app.callback(
            Output(idBase + 'fileInCache', 'children'),
            Input(idBase + 'dd_listFiles','value'),Input(idBase + 'dd_Units','value'),
            Input(idBase + 'dd_multiPatternSubCat','value'))
            def computeDf(filename,unitName,subCats):
                value = [filename,subCats,unitName]
                storeDF(value)
                return value

            @self.app.callback(
                Output(idBase + 'graph1', 'figure'),
                [Input(idBase+k,v) for k,v in dictOptsGraph.items()])
            def update_SCGgraph(cacheVal,step,cmapName,legendType):
                df = storeDF(cacheVal).iloc[::step]
                title = self.cfg.utils.makeFigureName(cacheVal[0],'_Small',[cacheVal[1],cacheVal[2]])
                fig = self.updateTUGraph(cacheVal[0],cacheVal[2],cacheVal[1],step,cmapName,legendType,
                                        heightGraph=900,df=df,figname=title,breakLine=None)
                return fig
        else:
            dictOptsGraph = {k : 'value' for k in ['dd_listFiles','dd_Units','dd_multiPatternSubCat','in_step','dd_cmap']}
            dictOptsGraph['btn_legend'] = 'n_clicks'

            @self.app.callback(
            Output(idBase + 'graph1', 'figure'),
            [Input(idBase+k,v) for k,v in dictOptsGraph.items()])
            def update_SCGgraph(filename,unit,tagPattern,step,cmapName,legendType):
                df = loadDataFrame(filename,tagPattern,unit).iloc[::step]
                print(tagPattern)
                title = self.cfg.utils.makeFigureName(filename,'_Small',[unit])
                fig = self.updateTUGraph(filename,tagPattern,unit,step,cmapName,legendType,
                                        heightGraph=900,df=df,figname=title,breakLine=None)
                return fig
        return SCG_html
