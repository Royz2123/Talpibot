import datetime
from random import shuffle

from Docs.DocsManager import DocsManager
from Calendar.quickstart import CalManager

INF = 1000

class DochManager:
    def __init__(self):
        self._cal_manager = CalManager()
        self._docs_manager = DocsManager()

    """
    Creates the cleaning week
    """
    def create_event_list(self):
        # Get the doch1 event list
        list = self._docs_manager.get_doch_list()
                
        # Send all the events (Dovner)
        self._cal_manager.send_events(list)
  

    


def main():
    # create cleaning manager
    cleaning_manager = DochManager()

    # create the cleaning schedule for the upcoming week
    cleaning_manager.create_event_list()



if __name__ == "__main__":
    main()


