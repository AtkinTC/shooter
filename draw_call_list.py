import draw_call
class Draw_Call_List:
    def __init__(self):
        self.dict = {}

    def append(self, calls):
        for call in calls:
            if self.dict.has_key(call.depth):
                self.dict[call.depth].append(call)
            else:
                self.dict[call.depth] = [call]

    def draw(self):
        for k in self.dict.keys():
            for call in self.dict[k]:
                call.run_draw_call()
