"""
dim_member setup and load logic.
"""

from pygrametl.tables import CachedDimension

from dis_etl.member_utils import decompose_member_row, unknown_member_row


def build_dim_member(connection) -> CachedDimension:
    """
    a pygrametl.ConnectionWrapper wrapping a psycopg2 connection to the fklubdw database
    """
    dim_member = CachedDimension(
        name="dim_member",
        key="id",
        attributes=["member_id", "year_joined", "gender"],
        lookupatts=["member_id"],
        targetconnection=connection,
    )
    # We want to ensure that there exitst a "Unknown member" row
    # before any sales facts reference them (member_id=0) are loaded!
    # This is done with pygrametl `ensure`.
    dim_member.ensure(unknown_member_row())
    return dim_member


def get_member_key(dim_member: CachedDimension, raw_row: dict) -> int:
    """Transform a raw typed member row, and ensure it has a matching
    dim_member row, returning a surrugate key"""
    return dim_member.ensure(decompose_member_row(raw_row))


def lookup_member_key(dim_member, member_id: int) -> int:
    """Lookup member by id"""
    key = dim_member.lookup({'member_id': member_id})
    if key is None:
        # member_id not seen before (and not the unknown-member row) —
        # fall back to the unknown member rather than failing the load
        key = dim_member.lookup({'member_id': 0})
    return key
