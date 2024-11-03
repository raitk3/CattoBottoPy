class Queue:
    def __init__(self, owner, queue = []):
        self.owner = owner
        self.queue = queue

    def get_as_dictionary_object(self):
        return {
            "owner": self.owner, 
            "queue": self.queue
            }