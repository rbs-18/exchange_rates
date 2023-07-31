from datetime import datetime, timedelta


class Days:
    DAY_BEFORE_YESTERDAY = 'day_before_yesterday'
    YESTERDAY = 'yesterday'
    TODAY = 'today'

    DATE_FORMAT = '%Y-%m-%d'

    def __init__(self):
        self._today = datetime.now()
        self._yesterday = self._today - timedelta(days=1)
        self._day_before_yesterday = self._today - timedelta(days=2)

    @property
    def today(self) -> str:
        return self._today.strftime(self.DATE_FORMAT)

    @property
    def yesterday(self) -> str:
        return self._yesterday.strftime(self.DATE_FORMAT)

    @property
    def day_before_yesterday(self) -> str:
        return self._day_before_yesterday.strftime(self.DATE_FORMAT)
