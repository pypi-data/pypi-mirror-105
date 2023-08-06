import pytz,pandas as pd, numpy as np,datetime as dt,pickle
from dorianUtils.configFilesD import ConfigDashTagUnitTimestamp
import subprocess as sp, os,re,glob
import psycopg3
from scipy import linalg
from scipy import integrate
pd.options.mode.chained_assignment = None  # default='warn'


class ConfigFilesSmallPower(ConfigDashTagUnitTimestamp):
    # ==========================================================================
    #                       INIT FUNCTIONS
    # ==========================================================================

    def __init__(self,folderPkl,pklMeteo=None,folderFig=None,folderExport=None,encode='utf-8'):
        self.appDir = os.path.dirname(os.path.realpath(__file__))
        self.filePLC = glob.glob(self.appDir +'/confFiles/' + '*PLC*')[0]
        super().__init__(folderPkl,self.filePLC,folderFig=folderFig,folderExport=folderExport)
        # self.typeGraphs = pd.read_csv('confFiles/typeGraph.csv',index_col=0)
        self.usefulTags = pd.read_csv(self.appDir+'/confFiles/predefinedCategories.csv',index_col=0)
        self.dfPLC      = self.__buildPLC()
        self.listUnits  = self.getUnitsdfPLC()
    def __buildPLC(self):
        return self.dfPLC[self.dfPLC.DATASCIENTISM==True]
# ==============================================================================
#                   functions compute new variables
# ==============================================================================

    def integrateDFTag(self,df,tagname,timeWindow=60,formatted=1):
        dfres = df[df.Tag==tagname]
        if not formatted :
            dfres = self.formatRawDF(dfres)
        dfres = dfres.sort_values(by='timestamp')
        dfres.index=dfres.timestamp
        dfres=dfres.resample('100ms').ffill()
        dfres=dfres.resample(str(timeWindow) + 's').mean()
        dfres['Tag'] = tagname
        return dfres

    def integrateDF(self,df,pattern,**kwargs):
        ts = time.time()
        dfs = []
        listTags = self.getTagsTU(pattern[0],pattern[1])[self.tagCol]
        # print(listTags)
        for tag in listTags:
            dfs.append(self.integrateDFTag(df,tagname=tag,**kwargs))
        print('integration of pattern : ',pattern[0],' finished in ')
        self.utils.printCTime(ts)
        return pd.concat(dfs,axis=0)

    def convertCur2Power(self,df,voltage):
        dfOut = df.copy()
        dfOut.value*=voltage #V
        dfOut.Tag=dfOut.Tag.str.replace('_IT_','_Power' + str(voltage) + 'V_')
        return df

    def computePower(self,df,group,timeWindow=60):
        pattern = self.dictPower[group]
        if len(pattern) == 3 :
            dfPowerGroup = self.integrateDF(df,pattern=pattern[:2],timeWindow=timeWindow)
            dfPowerGroup = self.convertCur2Power(dfPowerGroup,pattern[2])
        else :
            dfPowerGroup = self.integrateDF(df,pattern=pattern,timeWindow=timeWindow)
        return dfPowerGroup

    def getTagsUsedForPower(self):
        tagList,dfs = list(self.dictPower.keys())[:-1],[]
        for group in tagList:
            pat = self.dictPower[group]
            df = self.getTagsTU(pat[0],pat[1])
            df['group'] = group
            if len(pat)==3 :
                df['voltage'] = pat[2]
            else :
                df['voltage'] = np.nan
            dfs.append(df)
        res = pd.concat(dfs)
        res.to_csv('variableUsedToComputePower.csv')
        # self.utils.printDFSpecial(res)
        return res

    def getDFtypeGraph(self,df,typeGraph='Bilan système en puissance',**kwargs):
        dfTypeGraph = []
        if typeGraph == 'Bilan système en puissance':
            df=pd.concat([self.getDFsameCat(df,'A'),self.getDFsameCat(df,'W')])
            for group in list(self.dictPower.keys())[:-1]:
                print(group)
                dftmp = self.computePower(df,group,**kwargs)
                dftmp['groupPower'] = group
                dfTypeGraph.append(dftmp)
            dfTypeGraph = pd.concat(dfTypeGraph,axis=0)
            dfTypeGraph['timestamp'] = dfTypeGraph.index
            return dfTypeGraph

    # ==============================================================================
    #                   functions computation
    # ==============================================================================

    def prepareDFforFit(self,filename,ts=None,group='temperatures Stack 1',rs='30s'):
        df = self.loadFile(filename)
        a  = self.usefulTags[group]
        df = self.getDFTagsTU(df,a[0],a[1])
        df = self.pivotDF(df,resampleRate=rs)
        if not not ts :
            df= self.getDFTime(df,ts)
        return df

    def fitDataframe(self,df,func='expDown',plotYes=True,**kwargs):
        res = {}
        period = re.findall('\d',df.index.freqstr)[0]
        print(df.index[0].freqstr)
        for k,tagName in zip(range(len(df)),list(df.columns)):
             tmpRes = self.utils.fitSingle(df.iloc[:,[k]],func=func,**kwargs,plotYes=plotYes)
             res[tagName] = [tmpRes[0],tmpRes[1],tmpRes[2],
                            1/tmpRes[1]/float(period),tmpRes[0]+tmpRes[2]]
        res  = pd.DataFrame(res,index = ['a','b','c','tau(s)','T0'])
        return res

    # ==============================================================================
    #                   SQL SPARK FUNCTIONS
    # ==============================================================================
    def connectToDataBase(self,hostname = "192.168.1.44",port ="5434",
                            dbName = "Jules",username = "postgres",password = "SylfenBDD"):
        connReq = "host=" + hostname + " port=" + port + " dbname="+ dbName +" user="+ username + " password=" + password
        conn = psycopg3.connect(connReq,autocommit=True)
        return conn

    def readSQLdataBase(self,listTags,secs=60*30):
        t1 = dt.datetime.now()
        t0 = t1 - dt.timedelta(seconds=secs)
        timeRange = [t.strftime('%Y-%m-%d %H:%M:%S').replace('T',' ') for t in [t0,t1]]
        tsCol,tagCol = "timestampz","TAG"
        t0,t1 = timeRange[0], timeRange[1]
        conn = self.connectToDataBase()
        cur = conn.cursor()
        dfs = []
        if isinstance(listTags,str):listTags = [listTags]
        for Tag in listTags :
            start = time.time()
            Tag = "'" + Tag + "'"
            sqlQ = "select * from realtimedata where " + tsCol + " BETWEEN '" + t0 +"' AND '" + t1 + "' and  " + tagCol + " = " + Tag + ";"
            df = pd.read_sql_query(sqlQ,conn,parse_dates=[tsCol])
            df.columns=['Tag','value','timestamp']
            self.utils.printCTime(start)
            dfs.append(self.formatRawDF(df,True))
        df = pd.concat(dfs)
        df.timestamp = [k.tz_convert('Etc/GMT-2') for k in df.timestamp]
        conn.close()
        return df

    def readSQLdataBase_v2(self,patSql,secs=60*30):
        t1 = dt.datetime.now()
        t0 = t1 - dt.timedelta(seconds=secs)
        timeRange = [t.strftime('%Y-%m-%d %H:%M:%S').replace('T',' ') for t in [t0,t1]]
        t0,t1 = timeRange[0], timeRange[1]
        conn = self.connectToDataBase()
        cur = conn.cursor()
        start = time.time()
        sqlQ = "select * from realtimedata where " + tsCol + " BETWEEN '" + t0 +"' AND '" + t1 + "' and  " + tagCol + " like " + patSql + ";"
        df = pd.read_sql_query(sqlQ,conn,parse_dates=[tsCol])
        df.columns=['Tag','value','timestamp']
        self.utils.printCTime(start)
        dfs.append(self.formatRawDF(df,True))
        df = pd.concat(dfs)
        df.timestamp = [k.tz_convert('Etc/GMT-2') for k in df.timestamp]
        conn.close()
        return df

    def initSpark(self):# Set the job name
        import os, sys,time
        try: os.environ["JOB_NAME"]
        except: os.environ["JOB_NAME"] = "SylfenConsumer"
        # Set the home directories
        HOME = os.getenv("HOME")
        APPLICATION_HOME = os.getenv("APPLICATION_HOME")
        if (APPLICATION_HOME == None): # Home detection
            APPLICATION_HOME = os.path.abspath(os.getcwd())
            for i in range(0, 10): # Start home detection
                if (os.path.isdir(APPLICATION_HOME + "/bin") and os.path.exists(APPLICATION_HOME + "/bin")): break
                else: APPLICATION_HOME += "/.."
            if (not os.path.exists(APPLICATION_HOME + "/bin") or not os.path.isdir(APPLICATION_HOME + "/bin")):
                print("APPLICATION_HOME not found !") ; sys.exit()
            APPLICATION_HOME = os.path.realpath(APPLICATION_HOME)
            os.environ["APPLICATION_HOME"] = APPLICATION_HOME
        sys.path.append(APPLICATION_HOME + "/lib/init")
        # Init env
        from AppEnv_V1_3 import AppEnv
        appEnv = AppEnv(APPLICATION_HOME)
        # Init spark
        try: spark
        except: spark = None
        sc, spark = appEnv.initSpark(spark)
        # Set objects used by the developer
        cfgSys = appEnv.cfgSys; cfgProps = appEnv.cfgProps; cfgYaml = appEnv.cfgYaml
        log = appEnv.log; sdu = appEnv.utilSparkDf; sthu = appEnv.utilSparkThrift
        txtu = appEnv.utilString; ftpu = appEnv.utilFtp; smtp = appEnv.emailSmtp
        tika = appEnv.tika

    def loadSparkTimeDF(self,timeRange):
        basePath  =  HOME + "/share/localfs/ro/Gaston/products/SmallPower/10001/001/"
        basePath = '/home/dorian/data/sylfenData/share/sylfen/node0/ro/Gaston/products/SmallPower/10002/001/'
        datapathEnc =basePath + "EncodedData/"
        datapathAgg =basePath + "AggregatedData/"
        datapathPop =basePath + "PopulatedData/"
        datapathRef =basePath + "RefinedData/"
        # t0 =
        partitions = [
                "YEAR=2021/MONTH=3/DAY=28/HOUR={19,23}",
                "YEAR=2021/MONTH=3/DAY=29/HOUR={0,23}"
            ]
        df = sdu.loadParquet(inputDir=datapathEnc,partitions=partitions)
        df = sdu.organizeColumns(df, columns=["YEAR", "MONTH", "DAY", "HOUR", "MINUTE", "SECOND"], atStart=True)
        return df

    def getSparkTU(df,listTags=None):
        # listTags = cfg.getTagsTU('BLR','A').TAG
        start = time.time()
        for Tag in listTags:
            df2 = df.where("TAG == "+ "'" + Tag + "'")
            df3 = df2.select('TAG','VALUE','TIMESTAMP_UTC')
        pdf = df3.toPandas()
        self.utils.printCTime(start)
        return pdf
