"""
MeterReading Mutations
-----------------------
Actions to record meter readings

This is the most important mutation - it records electricity consumption
"""

import graphene
from models.meter_reading import MeterReading
from models.meter import Meter
from schema.meter_reading import MeterReadingObject, MeterReadingInput
from database import db_session
from datetime import datetime, timedelta


class RecordMeterReading(graphene.Mutation):
    """
    Mutation to record a new meter reading
    Think: Monthly meter reading by electricity board employee
    
    Important: Prevents duplicate readings within same day
    """
    class Arguments:
        input = MeterReadingInput(required=True)
    
    meter_reading = graphene.Field(lambda: MeterReadingObject)
    success = graphene.Boolean()
    message = graphene.String()
    units_consumed = graphene.Float()  # Extra info for user
    
    def mutate(self, info, input):
        try:
            # Validate meter exists
            meter = db_session.query(Meter).filter(Meter.id == input.meter_id).first()
            if not meter:
                return RecordMeterReading(
                    meter_reading=None,
                    success=False,
                    message="Meter not found",
                    units_consumed=0
                )
            
            # ✅ DUPLICATE READING CHECK — prevents two readings on same day
            today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            existing_reading = db_session.query(MeterReading).filter(
                MeterReading.meter_id == input.meter_id,
                MeterReading.reading_date >= today_start
            ).first()
            
            if existing_reading:
                return RecordMeterReading(
                    meter_reading=None,
                    success=False,
                    message="Reading already recorded today. Cannot duplicate.",
                    units_consumed=0
                )
            
            # Get previous reading to calculate units consumed
            previous_reading = db_session.query(MeterReading).filter(
                MeterReading.meter_id == input.meter_id
            ).order_by(MeterReading.reading_date.desc()).first()
            
            units_consumed = 0
            if previous_reading:
                # Validate: new reading should be greater than previous
                if input.reading_value < previous_reading.reading_value:
                    return RecordMeterReading(
                        meter_reading=None,
                        success=False,
                        message="Invalid reading: New reading is less than previous reading",
                        units_consumed=0
                    )
                units_consumed = input.reading_value - previous_reading.reading_value
            else:
                # First reading for this meter
                units_consumed = input.reading_value
            
            # Create new reading
            new_reading = MeterReading(
                meter_id=input.meter_id,
                reading_value=input.reading_value,
                reading_date=datetime.utcnow()
            )
            
            db_session.add(new_reading)
            db_session.commit()
            db_session.refresh(new_reading)
            
            return RecordMeterReading(
                meter_reading=new_reading,
                success=True,
                message=f"Reading recorded. Units consumed: {units_consumed}",
                units_consumed=units_consumed
            )
        except Exception as e:
            db_session.rollback()
            return RecordMeterReading(
                meter_reading=None,
                success=False,
                message=f"Error: {str(e)}",
                units_consumed=0
            )
