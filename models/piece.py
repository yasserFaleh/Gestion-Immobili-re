class Piece:

    def __init__(self,  size, id=None, asset_id=None):
        self.id = id
        self.size = size
        self.asset_id = asset_id



    def to_json(self,):
        return {"id":self.id,"size":self.size,"asset_id":self.asset_id}       