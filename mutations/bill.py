"""
Bill Mutations
---------------
Actions to generate bills

Important business logic:
- Auto-calculates units from meter readings
- Prevents duplicate bill generation for same cycle
- Calculates amount based on connection type
"""

import graphene
from models.bill import Bill, BillStatus
from models.consumer import Consumer, ConnectionType
from models.meter import Meter
from models.meter_reading import MeterReading
from schema.bill import BillObject, BillInput
from database import db_session
from datetime import datetime, timedelta


# Rate card (price per unit)
RATES = {
    ConnectionType.RESIDENTIAL: 7.5,  # ₹7.5 per unit
    ConnectionType.COMMERCIAL: 12.0   # ₹12 per unit
}


class GenerateBill(graphene.Mutation):
    """
    Mutation to generate a bill for a consumer
    Think: Monthly bill generation
    
    Key features:
    1. Prevents duplicate bills for same billing cycle
    2. Auto-calculates units from meter readings
    3. Applies different rates for residential vs commercial
    """
    class Arguments:
        input = BillInput(required=True)
    
    bill = graphene.Field(lambda: BillObject)
    success = graphene.Boolean()
    message = graphene.String()
    
    def mutate(self, info, input):
        try:
            # Get consumer
            consumer = db_session.query(Consumer).filter(
                Consumer.id == input.consumer_id
            ).first()
            
            if not consumer:
                return GenerateBill(
                    bill=None,
                    success=False,
                    message="Consumer not found"
                )
            
            # Check for duplicate bill (same consumer + same billing cycle)
            existing_bill = db_session.query(Bill).filter(
                Bill.consumer_id == input.consumer_id,
                Bill.billing_cycle == input.billing_cycle
            ).first()
            
            if existing_bill:
                return GenerateBill(
                    bill=None,
                    success=False,
                    message=f"Bill already generated for cycle {input.billing_cycle}"
                )
            
            # Get all meters for this consumer
            meters = db_session.query(Meter).filter(
                Meter.consumer_id == input.consumer_id
            ).all()
            
            if not meters:
                return GenerateBill(
                    bill=None,
                    success=False,
                    message="No meters found for this consumer"
                )
            
            # Calculate total units consumed across all meters
            total_units = 0
            
            for meter in meters:
                # Get latest 2 readings for this meter
                readings = db_session.query(MeterReading).filter(
                    MeterReading.meter_id == meter.id
                ).order_by(MeterReading.reading_date.desc()).limit(2).all()
                
                if len(readings) >= 2:
                    # Calculate units: latest - previous
                    units = readings[0].reading_value - readings[1].reading_value
                    total_units += units
                elif len(readings) == 1:
                    # Only one reading, use it as total
                    total_units += readings[0].reading_value
            
            # Calculate amount based on connection type
            rate = RATES.get(consumer.connection_type, 7.5)
            amount = total_units * rate
            
            # Create bill
            bill = Bill(
                consumer_id=input.consumer_id,
                billing_cycle=input.billing_cycle,
                total_units=total_units,
                amount=amount,
                status=BillStatus.GENERATED,
                generated_date=datetime.utcnow(),
                due_date=datetime.utcnow() + timedelta(days=15)  # 15 days to pay
            )
            
            db_session.add(bill)
            db_session.commit()
            db_session.refresh(bill)
            
            return GenerateBill(
                bill=bill,
                success=True,
                message=f"Bill generated: {total_units} units × ₹{rate} = ₹{amount}"
            )
        except Exception as e:
            db_session.rollback()
            return GenerateBill(
                bill=None,
                success=False,
                message=f"Error: {str(e)}"
            )


class CheckOverdueBills(graphene.Mutation):
    """
    Mutation to scan all GENERATED bills and mark them OVERDUE
    if their due date has passed.

    For Viva: In a real system, this would run as a scheduled/cron job daily.
    Here we call it manually to trigger the overdue logic.
    """
    updated_count = graphene.Int()
    overdue_bills = graphene.List(lambda: BillObject)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info):
        try:
            now = datetime.utcnow()

            # Find all GENERATED bills whose due date has passed
            overdue = db_session.query(Bill).filter(
                Bill.status == BillStatus.GENERATED,
                Bill.due_date < now
            ).all()

            for bill in overdue:
                bill.status = BillStatus.OVERDUE

            db_session.commit()

            return CheckOverdueBills(
                updated_count=len(overdue),
                overdue_bills=overdue,
                success=True,
                message=f"{len(overdue)} bill(s) marked as OVERDUE"
            )
        except Exception as e:
            db_session.rollback()
            return CheckOverdueBills(
                updated_count=0,
                overdue_bills=[],
                success=False,
                message=f"Error: {str(e)}"
            )
