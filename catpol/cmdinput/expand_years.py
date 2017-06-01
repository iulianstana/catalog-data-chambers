import logging

def __log_error_failed_parse(years, correct):
    logger = logging.getLogger(__name__)
    logger.error(
        'Failed to parse {}, an year must be one of {}.'.format(years, correct)
    )

def __log_error_failed_range(year, correct):
    logger = logging.getLogger(__name__)
    logger.error(
        '{} is not one of {}.'.format(year, correct)
    )

def expand_years(after, years):
    logger = logging.getLogger(__name__)
    all_years = {2016, 2012, 2008, 2004, 2000, 1996, 1992, 1990}
    all_years_str = ', '.join(map(str, sorted(list(all_years))))

    after_int = None
    years_int = None

    if after:
        try:
            after_int = int(after)
        except:
            _log_error_failed_parse(after, all_years)
    if years:
        try:
            years_int = set(map(int, years.split()))
        except ValueError:
            _log_error_failed_parse(years, all_years)
    if years_int:
        for year in years_int:
            if year not in all_years:
                __log_error_failed_range(year, all_years_str)
        years_int = {year for year in years_int if year in all_years}
        if after_int:
            return {year for year in years_int if year >= after_int}
        else:
            return {year for year in years_int}
    else:
        if after_int:
            return {year for year in all_years if year >= after_int}
        else:
            return all_years
