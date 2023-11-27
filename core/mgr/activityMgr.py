import sys
from typing import TYPE_CHECKING


_hoshizora = sys.modules["Makiyui_Hoshizora"]("ActivityMgr")
hoshizora = _hoshizora.Teraseru

if TYPE_CHECKING:
    from ..db.entity.activity import Activity as GameActivity
    from .activity.gachaActivityMgr import GachaActivityMgr
else:
    GameActivity = sys.modules["GameActivity"]
    GachaActivityMgr = sys.modules["ActivityMgr:GachaActivityMgr"]


class ActivityMgr:
    def __init__(self) -> None:
        # init
        GameActivity.initActivitys()

        # ins
        self.gachaMgr = GachaActivityMgr()

    def fetchActivityList(self, toData: bool = False, activeOnly: bool = True):
        """Fetch activity list."""
        return GameActivity.getAll(toData, activeOnly)
    
    def newActivity(self, activity_id: int, start_time: int = 0, end_time: int = 1999999999, _type: str = "unset"):
        activity = self.getActivity(activity_id)
        if activity is None:
            activity = GameActivity(-1, activity_id, start_time, end_time, _type)
        activity.start_time = start_time
        activity.end_time = end_time
        activity._type = _type
        return activity


    def getActivity(self, activity_id: int):
        """Get activity."""
        activity = GameActivity.get(activity_id)
        return activity

    def removeActivity(self, activity_id: int):
        """Remove activity."""
        activitys = self.fetchActivityList(activeOnly=False)
        for i in activitys:
            if isinstance(i, GameActivity):
                if i.activity_id == activity_id:
                    i.delete()
                    hoshizora(f"Delete activity [green]#{i._id}[/] with activity_id [green]{activity_id}[/]")
                
