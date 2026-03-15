"""
Consumer Mutations
-------------------
Actions to create and update consumers

For Viva:
- Mutation = action that changes data
- Resolver (mutate method) = the actual code that executes
"""

import graphene
from models.consumer import Consumer, ConnectionType, ConsumerStatus
from schema.consumer import ConsumerObject, ConsumerInput
from database import db_session


class CreateConsumer(graphene.Mutation):
    """
    Mutation to create a new consumer
    Think: Customer registration form
    """
    class Arguments:
        input = ConsumerInput(required=True)
    
    # What this mutation returns
    consumer = graphene.Field(lambda: ConsumerObject)
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(self, info, input):
        """
        The actual logic that executes when mutation is called
        """
        try:
            # Convert string to enum
            connection_type = ConnectionType[input.connection_type.upper()]
            
            # Create new consumer object
            consumer = Consumer(
                name=input.name,
                address=input.address,
                connection_type=connection_type,
                status=ConsumerStatus.ACTIVE
            )
            
            # Save to database
            db_session.add(consumer)
            db_session.commit()
            db_session.refresh(consumer)
            
            return CreateConsumer(
                consumer=consumer,
                success=True,
                message=f"Consumer {consumer.name} created successfully"
            )
        except Exception as e:
            db_session.rollback()
            return CreateConsumer(
                consumer=None,
                success=False,
                message=f"Error: {str(e)}"
            )


class UpdateConsumer(graphene.Mutation):
    """Mutation to update consumer details"""
    class Arguments:
        id = graphene.Int(required=True)
        input = ConsumerInput(required=True)
    
    consumer = graphene.Field(lambda: ConsumerObject)
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(self, info, id, input):
        try:
            consumer = db_session.query(Consumer).filter(Consumer.id == id).first()
            
            if not consumer:
                return UpdateConsumer(
                    consumer=None,
                    success=False,
                    message="Consumer not found"
                )
            
            # Update fields
            consumer.name = input.name
            consumer.address = input.address
            consumer.connection_type = ConnectionType[input.connection_type.upper()]
            
            if input.status:
                consumer.status = ConsumerStatus[input.status.upper()]
            
            db_session.commit()
            db_session.refresh(consumer)
            
            return UpdateConsumer(
                consumer=consumer,
                success=True,
                message="Consumer updated successfully"
            )
        except Exception as e:
            db_session.rollback()
            return UpdateConsumer(
                consumer=None,
                success=False,
                message=f"Error: {str(e)}"
            )
