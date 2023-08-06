import sys,re,importlib,pandas as pd, numpy as np, time, datetime as dt
from dateutil import parser
from dash.dependencies import Input, Output, State
from pylab import cm

import dash, dash_bootstrap_components as dbc, dash_html_components as html, dash_core_components as dcc
import plotly.express as px
import matplotlib.colors as mtpcl
import configFiles, smallPowerDash
from libs import utils, dccExtended as dccE

importlib.reload(configFiles)
importlib.reload(smallPowerDash)
importlib.reload(utils)
importlib.reload(dccE)

readFolder = '/home/dorian/data/sylfenData/tempSmallPower/'
folderData = '/home/dorian/data/sylfenData/smallPower_pkl/'
confFile    = "/home/dorian/sylfen/exploreSmallPower/PLC_confg/SmallPower-10002-001-ConfigurationPLC.csv"
cfg = configFiles.ConfigFiles(folderData,confFile,'latin-1')
spd = smallPowerDash.SmallPowerDash(cfg)
utils = utils.Utils()
dccE = dccE.DccExtended()

listTags = ['SEH1.STB_STK_04.TT_04.HM05',
            ]
df = cfg.readSQLdataBase(listTags)
