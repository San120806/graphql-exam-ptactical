"""
Root Query and Mutation Classes
---------------------------------
This is where we combine all queries and mutations

For Viva:
- Query class = all read operations
- Mutation class = all write operations
- This file is the "menu" - lists all available operations
"""

import graphene

# Import all types
from schema.consumer import ConsumerObject
from schema.meter import MeterObject
from schema.meter_reading import MeterReadingObject
from schema.bill import BillObject
from schema.payment import PaymentObject

# Import all mutations
from mutations.consumer import CreateConsumer, UpdateConsumer
from mutations.meter import CreateMeter, DeleteMeter
from mutations.meter_reading import RecordMeterReading
from mutations.bill import GenerateBill, CheckOverdueBills
from mutations.payment import RecordPayment

# Import models for filtering
from models.consumer import Consumer
from models.meter import Meter
from models.meter_reading import MeterReading
from models.bill import Bill, BillStatus
from models.payment import Payment
from database import db_session


class Query(graphene.ObjectType):
    """
    Root Query - all read operations
    Think: This is like a restaurant menu showing what you can order
    """
    # Query all consumers
    all_consumers = graphene.List(ConsumerObject)
    
    # Query single consumer by ID
    consumer = graphene.Field(ConsumerObject, id=graphene.Int(required=True))
    
    # Query all meters
    all_meters = graphene.List(MeterObject)
    
    # Query meters by consumer
    meters_by_consumer = graphene.List(MeterObject, consumer_id=graphene.Int(required=True))
    
    # Query all meter readings
    all_meter_readings = graphene.List(MeterReadingObject)
    
    # Query readings by meter
    readings_by_meter = graphene.List(
        MeterReadingObject,
        meter_id=graphene.Int(required=True)
    )
    
    # Query all bills
    all_bills = graphene.List(BillObject)
    
    # Query bills by consumer
    bills_by_consumer = graphene.List(BillObject, consumer_id=graphene.Int(required=True))
    
    # Query bills by status (for overdue handling)
    bills_by_status = graphene.List(BillObject, status=graphene.String(required=True))
    
    # Query single bill
    bill = graphene.Field(BillObject, id=graphene.Int(required=True))
    
    # Query all payments
    all_payments = graphene.List(PaymentObject)
    
    # Query payments by bill
    payments_by_bill = graphene.List(PaymentObject, bill_id=graphene.Int(required=True))
    
    
    # Resolvers - the actual code that fetches data
    # Resolver naming convention: resolve_<field_name>
    
    def resolve_all_consumers(self, info):
        """Get all consumers"""
        return db_session.query(Consumer).all()
    
    def resolve_consumer(self, info, id):
        """Get consumer by ID"""
        return db_session.query(Consumer).filter(Consumer.id == id).first()
    
    def resolve_all_meters(self, info):
        """Get all meters"""
        return db_session.query(Meter).all()
    
    def resolve_meters_by_consumer(self, info, consumer_id):
        """Get all meters for a specific consumer"""
        return db_session.query(Meter).filter(Meter.consumer_id == consumer_id).all()
    
    def resolve_all_meter_readings(self, info):
        """Get all meter readings"""
        return db_session.query(MeterReading).order_by(MeterReading.reading_date.desc()).all()
    
    def resolve_readings_by_meter(self, info, meter_id):
        """Get all readings for a specific meter"""
        return db_session.query(MeterReading).filter(
            MeterReading.meter_id == meter_id
        ).order_by(MeterReading.reading_date.desc()).all()
    
    def resolve_all_bills(self, info):
        """Get all bills"""
        return db_session.query(Bill).order_by(Bill.generated_date.desc()).all()
    
    def resolve_bills_by_consumer(self, info, consumer_id):
        """Get billing history for a consumer"""
        return db_session.query(Bill).filter(
            Bill.consumer_id == consumer_id
        ).order_by(Bill.generated_date.desc()).all()
    
    def resolve_bills_by_status(self, info, status):
        """Get bills by status (e.g., 'overdue', 'paid', 'generated')"""
        try:
            bill_status = BillStatus[status.upper()]
            return db_session.query(Bill).filter(Bill.status == bill_status).all()
        except KeyError:
            return []
    
    def resolve_bill(self, info, id):
        """Get bill by ID"""
        return db_session.query(Bill).filter(Bill.id == id).first()
    
    def resolve_all_payments(self, info):
        """Get all payments"""
        return db_session.query(Payment).order_by(Payment.payment_date.desc()).all()
    
    def resolve_payments_by_bill(self, info, bill_id):
        """Get all payments for a specific bill"""
        return db_session.query(Payment).filter(Payment.bill_id == bill_id).all()


class Mutation(graphene.ObjectType):
    """
    Root Mutation - all write operations
    """
    # Consumer mutations
    create_consumer = CreateConsumer.Field()
    update_consumer = UpdateConsumer.Field()
    
    # Meter mutations
    create_meter = CreateMeter.Field()
    delete_meter = DeleteMeter.Field()
    
    # Meter reading mutations
    record_meter_reading = RecordMeterReading.Field()
    
    # Bill mutations
    generate_bill = GenerateBill.Field()
    check_overdue_bills = CheckOverdueBills.Field()
    
    # Payment mutations
    record_payment = RecordPayment.Field()


# Create schema - this combines Query and Mutation
schema = graphene.Schema(query=Query, mutation=Mutation)
