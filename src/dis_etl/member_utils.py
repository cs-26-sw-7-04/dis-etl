"""
Transform layer for dim_member:
Turn raw member row into the full set of attributes needed in dim_member
"""

UNKNOWN_YEAR = None

GENDER_MAP = {"M": "Male", "F": "Female", "U": "Unknown"}


def normalize_gender(raw_gender) -> str:
    """Returns normalised gender, if no gender -> Unknown"""
    if raw_gender is None:
        return "Unknown"
    return GENDER_MAP.get(raw_gender.strip().upper(), "Unknown")


def normalize_year(raw_year) -> int:
    """Returns normalised year, if no year or > 1975 -> None"""
    if raw_year is None:
        return UNKNOWN_YEAR
    if raw_year > 1975: # year before fklub start
        return UNKNOWN_YEAR 
    return raw_year


def decompose_member_row(row: dict) -> dict:
    """Uses decomposition procs to extract and transform member data
    ready for ingretion into dim_member"""
    return {
        'member_id': row['id'],
        'year_joined': normalize_year(row['year']),
        'gender': normalize_gender(row['gender']),
    }


def unknown_member_row() -> dict:
    """If the member is unknown for osme reason"""

    return {
        'member_id': 0,
        'year_joined': UNKNOWN_YEAR,
        'gender': 'Unknown',
    }
