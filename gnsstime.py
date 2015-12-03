"""gnsstime

extended datetime module to handle dates related to the GNSS analysis.
Supports addition of timedelta, subtraction of a datetime.

2014/12/04 Created by Satoshi Kawamoto
2014/12/09 Added 'gpscal' to the module function.
2015/01/14 Added 'from_gpsw'.
2015/01/21 Added 'gpswsec'.
2015/08/21 Added a new leapsec.
2015/11/11 Added 'mjd2date'.
2015/12/01 Added 'from_mjd' and a property 'mjd'.
2015/12/03 Fixed bug of 'gpst'. The plus-minus sign was incorrect.  

methods:
    gpscal        : return a tuple (doy, gpsw, gpswd).
    ymd2date      : return a datetime from a string of 'yyyy/mm/dd'.
    mjd2date      : return a datetime from a modified Julian day.
    from_datetime : return a gnsstime from a datetime.
    to_datetime   : return a datetime from a gnsstime.
    from_gpsw     : return a gnsstime from a gps week.
    from_doy      : return a gnsstime from a set of yyyy, doy.
    from_mjd      : return a gnsstime from a modified julian day.

properties:
    gpsw          : GPS week from 1980/1/6.
    gpswd         : GPS weekday [0:Sunday .. 6:Saturday].
    gpswsec       : the second-of-week.
    doy           : day of the year [1-366].
    leapsec       : leap seconds for GPS time.
    gpst          : GPS time.
    mjd           : modified julian day.

Example:

>>> import gnsstime as gt
>>> gt1 = gt.gnsstime(2011, 1, 1)
>>> print("gpscal: show gps calendar (doy, gpsw, gpswd)")
>>> print("gpscal()                        -> ", gt1.gpscal())
>>> print("gpscal(2013,12,31)              -> ", gt1.gpscal(2013, 12, 31))
>>> print("gpscal(ymd='2013/12/31')        -> ", gt1.gpscal(ymd="2013/12/31"))
>>> print("gpscal(dt.datetime(2013,12,31)) -> ", gt1.gpscal(dt.datetime(2013, 12, 31)))
>>> print("gpscal(year=2013, month=12, day=31) -> ", gt.gpscal(year=2013, month=12, day=31))
gpscal()                        ->  (1, 1616, 6)
gpscal(2013,12,31)              ->  (365, 1773, 2)
gpscal(ymd='2013/12/31')        ->  (365, 1773, 2)
gpscal(dt.datetime(2013,12,31)) ->  (365, 1773, 2)
gpscal(year=2013, month=12, day=31) ->  (365, 1773, 2)
gpscal(mjd=56657)               ->  (365, 1773, 2)

>>> print("date    :", gt1.isoformat())
>>> print("doy     :", gt1.doy)
>>> print("gpsw    :", gt1.gpsw)
>>> print("gpswd   :", gt1.gpswd)
>>> print("gpst    :", gt1.gpst.isoformat())
>>> print("leapsec :", gt1.leapsec)
>>> print("mjd     :", gt1.mjd)
date    : 2011-01-01T00:00:00
doy     : 1
gpsw    : 1616
gpswd   : 6
gpst    : 2010-12-31T23:59:45
leapsec : -15
mjd     : 55562.0

>>> import datetime as dt
>>> print("gt1 + dt.timedelta(days=2) :", (gt1 + dt.timedelta(days=2)).isoformat())
>>> print("gt1 - dt.timedelta(days=2) :", (gt1 - dt.timedelta(days=2)).isoformat())
gt1 + dt.timedelta(days=2) : 2011-01-03T00:00:00
gt1 - dt.timedelta(days=2) : 2010-12-30T00:00:00
"""

import datetime as dt
from datetime import timedelta

DT_MJD0 = dt.datetime(1858,11,17)

class gnsstime(dt.datetime):
    """
    gnsstime(year, month, day[, hour[, minute[, second[, microsecond]]]])
    """
    # datetime at the reference of GPST, MJD
    dt_gpst0 = dt.datetime(1980, 1, 6)
    dt_mjd0  = dt.datetime(1858,11,17)
    leaps    = []

    # leap seconds for GPST
    class leapsec:
        __slots__ = ['date', 'sec']
        def __init__(self, yyyy, mm, dd, sec=0):
            self.date = dt.datetime(yyyy, mm, dd)
            self.sec  = sec
            return

    leaps.append(leapsec(2015, 7, 1, sec=-17))
    leaps.append(leapsec(2012, 7, 1, sec=-16))
    leaps.append(leapsec(2009, 1, 1, sec=-15))
    leaps.append(leapsec(2006, 1, 1, sec=-14))
    leaps.append(leapsec(1999, 1, 1, sec=-13))
    leaps.append(leapsec(1997, 7, 1, sec=-12))
    leaps.append(leapsec(1996, 1, 1, sec=-11))
    leaps.append(leapsec(1994, 7, 1, sec=-10))
    leaps.append(leapsec(1993, 7, 1, sec= -9))
    leaps.append(leapsec(1992, 7, 1, sec= -8))
    leaps.append(leapsec(1991, 1, 1, sec= -7))
    leaps.append(leapsec(1990, 1, 1, sec= -6))
    leaps.append(leapsec(1988, 1, 1, sec= -5))
    leaps.append(leapsec(1985, 7, 1, sec= -4))
    leaps.append(leapsec(1983, 7, 1, sec= -3))
    leaps.append(leapsec(1982, 7, 1, sec= -2))
    leaps.append(leapsec(1981, 7, 1, sec= -1))

    @staticmethod
    def ymd2date(ymd):
        """
        Return a datetime from ymd string e.g. "2011/1/1"
        """
        yyyy, mm, dd = ymd.strip().split('/')
        return dt.datetime(int(yyyy), int(mm), int(dd))

    @staticmethod
    def mjd2date(mjd):
        """
        Return a datetime from a modified Julian day.
        """
        return DT_MJD0 + timedelta(mjd)

    @classmethod
    def from_datetime(cls, datetime_object):
        """
        Convert a datetime to a gnsstime.
        """
        dto = datetime_object
        return cls(dto.year, dto.month, dto.day, dto.hour, dto.minute,
                   dto.second, dto.microsecond)

    @classmethod
    def from_mjd(cls, mjd):
        """
        Convert a mjd (modified julian date) to a gnsstime.
        """
        dto = cls.mjd2date(mjd)
        return cls(dto.year, dto.month, dto.day, dto.hour, dto.minute,
                   dto.second, dto.microsecond)

    @classmethod
    def from_gpsw(cls, gpsw, gpswd=None, tow=None, nrollover=0):
        """
        Convert a gps week to a gnsstime.
        """
        # 4 def calgps(gpsw, gpswd=None, tow=None, doy=None):
        #gt0 = cls(1980, 1, 6)
        seconds = 0.

        if gpswd is None:
            if tow is not None:
                gpswd = int(tow/86400.)
                seconds = tow - gpswd*86400.
            else:
                gpswd = 0.

        return cls.dt_gpst0 + dt.timedelta(days=1024*nrollover+gpsw*7+gpswd, seconds=seconds)

    @classmethod
    def from_doy(cls, year, doy):
        """
        Convert a date with year and doy to a gnsstime.
        """
        if year < 100:
            if year < 80:
                year += 2000
            else:
                year += 1900
        if doy < 1:
            print("error: doy must be positive. doy={:}".format(doy))
            return None
        return cls(year, 1, 1) + dt.timedelta(days=doy-1)

    def to_datetime(self):
        return dt.datetime(self.year, self.month, self.day, self.hour,
                           self.minute, self.second, self.microsecond)

    def _arg2date(self, *args, date, year, month, day, ymd, mjd):
        """
        Convert arguments to a gnsstime instance.
        args could be one of:
        1. year, month, day, [hour, minute, second, microsecond]
        2. datetime or gnsstime
        3. ymd string e.g. "2011/1/1"
        """
        if len(args) == 1:
            if isinstance(args[0], dt.datetime):
                tmpdate = self.from_datetime(args[0])     # datetime object
            elif isinstance(args[0], str):
                tmpdate = self.ymd2date(args[0])  # "yyyy/mm/dd"
        elif len(args) >= 3:
            # yyyy, mm, dd, [HH, MM, SS, microsec]
            tmpdate = self.from_datetime(dt.datetime(*args))
        else:
            # do not modify date
            tmpdate = self.from_datetime(self)

        if date is not None:
            tmpdate = self.from_datetime(date)
        elif year is not None and month is not None and day is not None:
            tmpdate = tmpdate.replace(year=year, month=month, day=day)
        elif ymd is not None:
            tmpdate = self.from_datetime(self.ymd2date(ymd))
        elif mjd is not None:
            tmpdate = self.from_datetime(self.mjd2date(mjd))

        return tmpdate

    def gpscal(self, *args, date=None, year=None, month=None, day=None, ymd=None, mjd=None):
        """
        return doy, GPS Week (from 1980/1/6), GPS weekday [0:Sunday .. 6:Saturday].

        doy, gpsw, gpswd = gnsstime.gpscal(date = dt.datetime.utcnow())
        doy, gpsw, gpswd = gnsstime.gpscal(year=2013, month=1, day=1)
        doy, gpsw, gpswd = gnsstime.gpscal(ymd="2013/01/01")
        doy, gpsw, gpswd = gnsstime.gpscal(2013, 1, 1)

        example:
        doy, gpsw, gpswd = gnsstime.gpscal(year=2013, month=1, day=1)
        """
        date = self._arg2date(*args, date=date, year=year, month=month,
                            day=day, ymd=ymd, mjd=mjd)
        return date.doy, date.gpsw, date.gpswd

    @property
    def gpsw(self):
        """
        return GPS Week from 1980/1/6.
        """
        return int((self-self.dt_gpst0).days/7.0)

    @property
    def gpswd(self):
        """
        return GPS weekday [0:Sunday .. 6:Saturday].
        """
        return self.isoweekday() % 7 # sunday is 0 for GPS week day, instead of 7.

    @property
    def gpswsec(self):
        """
        return GPS second-of-week.
        """
        return self.gpswd*86400. + self.hour*3600. + self.minute*60. + self.second

    @property
    def weekday(self):
        """
        return Weekday [0:Monday .. 6:Sunday].
        """
        #return date.isoweekday()  # wrong!
        return super(gnsstime, self).weekday()

    @property
    def doy(self):
        """
        return day of the year [1-366].
        """
        return self.timetuple().tm_yday

    @property
    def leapsec(self):
        """
        leap seconds for GPST.
        """
        # search leap seconds
        for leap in self.leaps:
            if self >= leap.date:
                return leap.sec

        # return 0 sec before 1981/7/1
        return 0

    @property
    def gpst(self):
        """
        Return the gps time.
        """
        return self - timedelta(seconds=self.leapsec)

    @property
    def mjd(self):
        """
        Return the modified julian date.
        """
        return (self - DT_MJD0).total_seconds()/86400.

    # timedelta support
    def __add__(self, other):
        """
        Add a gnsstime and timedelta.
        """
        return self.from_datetime(self.to_datetime() + other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        """
        Subtract a gnsstime and a gnsstime, or a timedelta.
        """
        if isinstance(other, dt.datetime) or isinstance(other, gnsstime):
            dday = self.toordinal() - other.toordinal()
            sec1 = self.hour*3600 + self.minute*60 + self.second
            sec2 = other.hour*3600 + other.minute*60 + other.second
            dsec = sec1 - sec2
            dmicrosec = other.microsecond - other.microsecond
            return dt.timedelta(dday, dsec, dmicrosec)
        elif isinstance(other, dt.timedelta):
            return self + -other

# gpscal for static method
gpscal = gnsstime(1980, 1, 6).gpscal

def test():
    gt = gnsstime(2011, 1, 1)
    print("--- gpscal test ---")
    print("gpscal: show gps calendar (doy, gpsw, gpswd)")
    print("gpscal()                        -> ", gt.gpscal())
    print("gpscal(2013,12,31)              -> ", gt.gpscal(2013, 12, 31))
    print("gpscal(ymd='2013/12/31')        -> ", gt.gpscal(ymd="2013/12/31"))
    print("gpscal(dt.datetime(2013,12,31)) -> ", gt.gpscal(dt.datetime(2013, 12, 31)))
    print("gpscal(year=2013, month=12, day=31) -> ", gt.gpscal(year=2013, month=12, day=31))
    print("gpscal(mjd=56657)               -> ", gt.gpscal(mjd=56657))

    print("--- properties ---")
    print("date    :", gt.isoformat())
    print("doy     :", gt.doy)
    print("gpsw    :", gt.gpsw)
    print("gpswd   :", gt.gpswd)
    print("gpst    :", gt.gpst.isoformat())
    print("leapsec :", gt.leapsec)
    print("mjd     :", gt.mjd)

    print("--- timedelta support ---")
    print("gt :", gt.isoformat())
    print("gt + dt.timedelta(days=2) :", (gt + dt.timedelta(days=2)).isoformat())
    print("gt - dt.timedelta(days=2) :", (gt - dt.timedelta(days=2)).isoformat())

if __name__ == "__main__":
    test()
