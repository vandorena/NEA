
class Boat:

    def __init__(self,name: str) -> None:
        self.data = {
            "name":name
        }

    def add_polar(self,filename:str):
        line_holding_array = []
        with open(filename,"r") as f:
