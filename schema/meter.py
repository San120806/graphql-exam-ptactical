"""
Meter GraphQL Type
-------------------
Defines how Meter data is exposed via GraphQL API
"""

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models.meter import Meter


class MeterObject(SQLAlchemyObjectType):
    """GraphQL representation of Meter"""
    class Meta:
        model = Meter


class MeterInput(graphene.InputObjectType):
    """Input type for creating meters"""
    consumer_id = graphene.Int(required=True)
    meter_number = graphene.String(required=True)
    status = graphene.String()  # Optional: "active", "inactive", "faulty"
