class Asset:

    def __init__(self, name):
        self.name=name
        self.factors = {}
    
    def add_factor(self, factor_name, factor_list):
        self.factors[factor_name] = factor_list
        
    def get_factor(self, factor_name):
        if(self.factors.__contains__(factor_name)):
            return self.factors[factor_name]
        else:
            return None
        
    def list_factors(self):
        return self.factors.keys()