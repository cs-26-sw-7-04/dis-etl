from pygrametl.tables import CachedDimension


def build_member(connection) -> CachedDimension:

    return CachedDimension(
    name="dim_member",
    key="id",
    attributes=["member_id",
               "year_joined",
               "gender"],  
    lookupatts=["member_id"],
    targetconnection=connection,
    )

def get_member_key(dim_member: CachedDimension, member_id: int) -> int:
    return dim_member.lookup({"member_id": member_id})
    
