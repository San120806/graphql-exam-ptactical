"""
MeterReading GraphQL Type
--------------------------
Defines how MeterReading data is exposed via GraphQL API
"""

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models.meter_reading import MeterReading


class MeterReadingObject(SQLAlchemyObjectType):
    """GraphQL representation of MeterReading"""
    class Meta:
        model = MeterReading


class MeterReadingInput(graphene.InputObjectType):
    """Input type for recording meter readings"""
    meter_id = graphene.Int(required=True)
    reading_value = graphene.Float(required=True)
