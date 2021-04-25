# gnsstime.py
`gnsstime` is an extended datetime for the gnss analysis.

Requirements
------------
* Python 3.3 or later (not support 2.x)

History
-------
0.0.3 (2014-12-04)
* first release

0.0.4 (2014-12-07)
* bug fix

0.0.5 (2014-12-09)
* added 'gpscal' to the module function.

0.0.6 (2015-12-01)
* added a new leapsec.
* modified julian day (mjd) support.
  added 'mjd2date', 'from_mjd', and a property 'mjd'.

0.0.8 (2015-12-03)
* fix bug of 'gpst'.

0.0.9 (2021-04-25)
* fix the timezone problem.
  
Example
-------
::

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
    gpst    : 2011-01-01T00:00:15
    leapsec : -15
    mjd     : 55562.0

    >>> import datetime as dt
    >>> print("gt1 + dt.timedelta(days=2) :", (gt1 + dt.timedelta(days=2)).isoformat())
    >>> print("gt1 - dt.timedelta(days=2) :", (gt1 - dt.timedelta(days=2)).isoformat())
    gt1 + dt.timedelta(days=2) : 2011-01-03T00:00:00
    gt1 - dt.timedelta(days=2) : 2010-12-30T00:00:00
