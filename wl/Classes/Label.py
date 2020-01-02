class Label:
    """Class for creating and managing water labels"""
    parameters = {}
    def __init__(self,id_gestore,aliasLoc,data,parms):
        self.data = data
        self.id_gestore = id_gestore
        self.aliasLoc = aliasLoc
        self.row_parms = parms
        import resource.Parametri as sp
        self.parameters = {sp.getSTDParm(k): v for k, v in self.row_parms.items()}

    def getAlias(self):
            return self.aliasLoc

    def addParameter(self,parm,value):
        """ Adding new parm"""
        __doc__ = 'addParameter(parm,value)'
        self.label[parm] = value
    
    def getParameters(self):
        return self.parameters
        
    def __str__(self):
        """Template printing"""
        return str(self.label)