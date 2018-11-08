import datetime
from random import shuffle

from Docs.DocsManager import DocsManager
from Calendar.quickstart import CalManager

INF = 1000

class Manager:

    SHIFT_CLEANERS = 4
    MORNING_CLEANERS = SHIFT_CLEANERS * 5
    EVENING_CLEANERS = SHIFT_CLEANERS * 5
    WEEKLY_CLEANERS = MORNING_CLEANERS + EVENING_CLEANERS

    def __init__(self, week_num):
        self._first_day = self._next_sunday()
        self._week_num = week_num

        self._cal_manager = CalManager()
        self._docs_manager = DocsManager(self._week_num, self._first_day)

    def _next_sunday(self):
        today = datetime.date.today()
        days_to_add = (6 - today.weekday()) % 7 # MON = 0, SUN = 6 -> SUN = 0 .. SAT = 6
        next_sunday = today + datetime.timedelta(days_to_add)
        return next_sunday #.strftime('%d/%m/%Y')

    """
    Creates the cleaning week
    """
    def create_week(self):
        # Create the scouting list for the week
        cleaning_list = self._docs_manager.get_list()
        original_order = [cleaner for cleaner in cleaning_list]

        # choose the weekly workers
        weekly_cleaners = self.choose_cleaners(cleaning_list)

        # Update all of the docs's
        self.set_documents(weekly_cleaners, original_order)

    """
    Get the cleaning list and decide based on set of rules who needs to clean now
    """
    def choose_cleaners(self, cleaning_list):
        # decide who needs to scout based on who cleaned the least
        cleaning_list.sort(key=lambda x: x["cleans"])
        weekly_cleaners = cleaning_list[:Manager.WEEKLY_CLEANERS]
        shuffle(weekly_cleaners)

        # Document the new workers
        for cleaner in weekly_cleaners:
            cleaner["cleans"] = str(int(cleaner["cleans"]) + 1)

        # Put them into the schedule
        evening_cleaners = []
        morning_cleaners = []
        for cleaner in weekly_cleaners:
            if cleaner["only_evening"] != "X" or len(morning_cleaners) == Manager.MORNING_CLEANERS:
                evening_cleaners.append(cleaner)
            else:
                morning_cleaners.append(cleaner)

        # Split into days
        weekly_cleaners = []
        for cleaner_type in (morning_cleaners, evening_cleaners):
            weekly_cleaners.append([
                cleaner_type[i:i+Manager.SHIFT_CLEANERS]
                for i in range(0, len(cleaner_type), Manager.SHIFT_CLEANERS)
            ])

        # return the weekly cleaners
        return weekly_cleaners

    """
    Set all the docs that need to updated:
    New List <- cleaning_list
    New Schedule <- weekly_cleaners
    New events <- weekly_cleaners
    """
    def set_documents(self, weekly_cleaners, cleaning_list):
        # Update the cleaning list (Margolis)
        self._docs_manager.set_list(cleaning_list)

        # Update the schedule (Margolis)
        self._docs_manager.set_schedule(weekly_cleaners)

        # Send all the events (Dovner)
        self._cal_manager.send_events(weekly_cleaners, self._first_day)




def main():
    # create cleaning manager
    cleaning_manager = Manager(2)

    # create the cleaning schedule for the upcoming week
    cleaning_manager.create_week()



if __name__ == "__main__":
    main()


