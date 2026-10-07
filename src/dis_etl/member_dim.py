"""
dim_member setup and load logic.
"""

from pygrametl.tables import CachedDimension


def build_dim_member(connection) -> CachedDimension:
    """
    a pygrametl.ConnectionWrapper wrapping a psycopg2 connection to the fklubdw database
    """
    return CachedDimension(
        name="dim_member",
        key="id",
        attributes=["member_id", "year_joined", "gender"],
        lookupatts=["member_id"],
        targetconnection=connection,
    )


def get_member_key(dim_member: CachedDimension, member_id: int) -> int:
    """Return a members id based on the member_id"""
    return dim_member.lookup({"member_id": member_id})
