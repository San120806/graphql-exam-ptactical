"""
Bill GraphQL Type
------------------
Defines how Bill data is exposed via GraphQL API
"""

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models.bill import Bill


class BillObject(SQLAlchemyObjectType):
    """GraphQL representation of Bill"""
    class Meta:
        model = Bill


class BillInput(graphene.InputObjectType):
    """Input type for generating bills"""
    consumer_id = graphene.Int(required=True)
    billing_cycle = graphene.String(required=True)  # e.g., "2024-01"
    # total_units and amount will be calculated automatically
