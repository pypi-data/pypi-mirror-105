import pytz,pandas as pd
from dorianUtils.templateDashD import TemplateDashTagsUnit

class ScreenBuildingDash(TemplateDashTagsUnit):
    # ==========================================================================
    #                       INIT FUNCTIONS
    # ==========================================================================

    def __init__(self,cfg,baseNameUrl='/monitoringBuilding/',skipEveryHours=120,port=45103):
        super().__init__(cfg,baseNameUrl=baseNameUrl,title='Monitoring buildings',
                            port=port,cacheRedis=False)
        self.skipEveryHours = skipEveryHours
