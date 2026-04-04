from ..exceptions import InvalidSort, InvalidTimeFrame

def sort_validation(sort) -> bool:
    if sort not in ('latest', 'popular', 'liked'):
        raise InvalidSort
    return True

def timeframe_validation(timeframe) -> bool:
    if timeframe not in ('24h', '1w', '1m', '1y', 'all'):
        raise InvalidTimeFrame
    return True