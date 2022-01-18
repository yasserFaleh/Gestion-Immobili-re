class Asset:

    def __init__(self, emailowner,  name=None, description=None, type=None,id=None, city=None, pieces=[]):
        self.id = id
        self.name = name
        self.emailowner = emailowner
        self.description = description
        self.type = type
        self.city = city 
        self.pieces = pieces

    def to_json(self,):
        pieces_json = [piece.to_json() for piece in self.pieces]
        return {"id":self.id,"name":self.name,"description":self.description,"type":self.type,"city":self.city,"emailowner":self.emailowner,"pieces":pieces_json}       

    #returns Piece if found by the id else it returns None
    def findPieceById(self, id):
        for piece in self.pieces:
            if piece.id == id:
                return piece
        
        return None