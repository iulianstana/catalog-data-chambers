import logging


_LEGS = {2016, 2012, 2008, 2004, 2000, 1996, 1992, 1990}

def __log_error_failed_parse(string):
    logger = logging.getLogger(__name__)
    logger.error('Failed to parse {string}, the available legislatures are '
                 '{legs}.'.format(string, _LEGS))


def __log_warning_failed_range(integer):
    logger = logging.getLogger(__name__)
    logger.warning('{integer} is not avaialbe as a legislature. The available '
                   'legislatures are {legs}.'.format(integer, _LEGS))


def expand_legs_str(legs_str):
    logger = logging.getLogger(__name__)

    if legs_str:
        requested_legs = set() 
        try:
            legs_int = set(map(int, 
                               legs_str.split()))
            for leg in legs_int:
                if leg in _LEGS:
                    requested_legs.add(leg)
                else:
                    __log_warning_failed_range(leg)
        except ValueError:
            _log_error_failed_parse(legs_str)
            raise
        return requested_legs
    else:
        return _LEGS
