"""
Meter Mutations
----------------
Actions to create and manage meters
"""

import graphene
from models.meter import Meter, MeterStatus
from schema.meter import MeterObject, MeterInput
from database import db_session


class CreateMeter(graphene.Mutation):
    """
    Mutation to create a new meter
    Think: Installing a new meter at customer's location
    """
    class Arguments:
        input = MeterInput(required=True)
    
    meter = graphene.Field(lambda: MeterObject)
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(self, info, input):
        try:
            # Check if meter number already exists (duplicate prevention)
            existing_meter = db_session.query(Meter).filter(
                Meter.meter_number == input.meter_number
            ).first()
            
            if existing_meter:
                return CreateMeter(
                    meter=None,
                    success=False,
                    message=f"Meter number {input.meter_number} already exists"
                )
            
            # Create new meter
            meter = Meter(
                consumer_id=input.consumer_id,
                meter_number=input.meter_number,
                status=MeterStatus.ACTIVE
            )
            
            db_session.add(meter)
            db_session.commit()
            db_session.refresh(meter)
            
            return CreateMeter(
                meter=meter,
                success=True,
                message="Meter created successfully"
            )
        except Exception as e:
            db_session.rollback()
            return CreateMeter(
                meter=None,
                success=False,
                message=f"Error: {str(e)}"
            )


class DeleteMeter(graphene.Mutation):
    """Mutation to delete a meter and all its readings"""
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        try:
            meter = db_session.query(Meter).filter(Meter.id == id).first()
            if not meter:
                return DeleteMeter(success=False, message="Meter not found")

            db_session.delete(meter)
            db_session.commit()
            return DeleteMeter(success=True, message=f"Meter {id} deleted successfully")
        except Exception as e:
            db_session.rollback()
            return DeleteMeter(success=False, message=f"Error: {str(e)}")
