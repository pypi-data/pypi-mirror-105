import sys,re,importlib,pandas as pd, numpy as np, time, datetime as dt
from dateutil import parser
from pylab import cm

from dash.dependencies import Input, Output, State
import dash, dash_bootstrap_components as dbc, dash_html_components as html, dash_core_components as dcc
import plotly.express as px
import matplotlib.colors as mtpcl

import dorianUtils.configFilesD as cfd
importlib.reload(cfd)

import dorianUtils.utilsD as utd
importlib.reload(utd)
utils=utd.Utils()
#
# import dorianUtils.dccExtendedD as dccExtendedD
# importlib.reload(dccExtendedD)
# dccE = dccExtendedD.DccExtended()

baseFolder = '/home/dorian/sylfen/screeningBuilding/'
folderPkl = baseFolder + 'pkl/'
confFile    = baseFolder + "src/confFiles/screenBuilding-10001-001-ConfigurationPLC.csv"
cfgtu = cfd.ConfigDashTagUnitTimestamp(folderPkl,confFile,'latin-1')

from dorianUtils import templateDashD as tdd
importlib.reload(tdd)

import configFilesBuilding
importlib.reload(configFilesBuilding)

import screenBuildingDash
importlib.reload(screenBuildingDash)

cfg = configFilesBuilding.ConfigFilesBuilding(folderPkl,confFile)
sbd = screenBuildingDash.ScreenBuildingDash(cfg)

start=time.time()
timeRange = ['2021-05-01 00:10','2021-05-02 23:20']
meteoCsvs = '/home/dorian/data/sylfenData/archivesMeteo/'
monitoringCsvs = '/home/dorian/data/sylfenData/archivesMonitoring/'
meteoPkls = '/home/dorian/sylfen/screeningBuilding/pklMeteo/'
# utils.convert_csv2pkl(monitoringCsvs,folderPkl)
# utils.convert_csv2pkl(meteoCsvs,meteoPkls)

# dfM=cfg.loadFileMeteo('*04-21*')
# df =cfg.loadFileMonitoring('*04-24*')
# df = pd.concat([df,dfM],ignore_index=True)

tags = cfg.getTagsTU('','°C')
# tags = ['C00000001-A003-1-kWh-JTWH','SIS-01-TT-01-XM00']
df = cfg.loadDF_TimeRange_Tags(timeRange,tags,rs='auto',applyMethod='nanmean')
#
