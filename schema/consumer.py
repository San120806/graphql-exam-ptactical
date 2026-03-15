"""
Consumer GraphQL Type
----------------------
Defines how Consumer data is exposed via GraphQL API

For Viva:
- This is the "contract" - tells clients what data they can query
- SQLAlchemyObjectType automatically converts DB model to GraphQL type
"""

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models.consumer import Consumer


class ConsumerObject(SQLAlchemyObjectType):
    """
    GraphQL representation of Consumer
    Automatically includes all fields from Consumer model
    """
    class Meta:
        model = Consumer


class ConsumerInput(graphene.InputObjectType):
    """
    Input type for creating/updating consumers
    InputObjectType is used for mutation arguments
    """
    name = graphene.String(required=True)
    address = graphene.String(required=True)
    connection_type = graphene.String(required=True)  # "residential" or "commercial"
    status = graphene.String()  # Optional
