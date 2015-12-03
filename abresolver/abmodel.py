class BaseModel(object):
    """ Wrapper over the model P(t|a) """
    
    def __contains__(self, a):
        """ Checks if abbreviation is in the dictionary. """
        raise NotImplementedError()
    
    
    def get_expansions(self, a):
        raise NotImplementedError()
    
    
    def get_p_term_given_abbreviation(self, t, a):
        raise NotImplementedError()
    
    
class Model(BaseModel):
    """ Wrapper over the model P(t|a) """
    
    def __init__(self, df):
        self.df = df
    
    
    def __contains__(self, a):
        return self.df[self.df.a==a].shape[0] > 0
    
    
    def get_expansions(self, a):
        return self.df[self.df.a==a]['t'].unique().tolist()
    
    
    def get_p_term_given_abbreviation(self, t, a):
        return self.df[(self.df.a==a)&(self.df.t==t)]['P(t|a)'].iloc[0]