"""
Payment GraphQL Type
---------------------
Defines how Payment data is exposed via GraphQL API
"""

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models.payment import Payment


class PaymentObject(SQLAlchemyObjectType):
    """GraphQL representation of Payment"""
    class Meta:
        model = Payment


class PaymentInput(graphene.InputObjectType):
    """Input type for recording payments"""
    bill_id = graphene.Int(required=True)
    amount = graphene.Float(required=True)
    status = graphene.String()  # Optional: "success", "pending", "failed"
