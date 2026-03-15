"""
Payment Mutations
------------------
Actions to record payments against bills

Updates bill status when fully paid
"""

import graphene
from models.payment import Payment, PaymentStatus
from models.bill import Bill, BillStatus
from schema.payment import PaymentObject, PaymentInput
from database import db_session
from datetime import datetime


class RecordPayment(graphene.Mutation):
    """
    Mutation to record a payment
    Think: Customer paying their electricity bill
    
    Features:
    - Records payment
    - Updates bill status to PAID if fully paid
    - Marks bill as OVERDUE if past due date
    """
    class Arguments:
        input = PaymentInput(required=True)
    
    payment = graphene.Field(lambda: PaymentObject)
    success = graphene.Boolean()
    message = graphene.String()
    remaining_amount = graphene.Float()
    
    def mutate(self, info, input):
        try:
            # Get bill
            bill = db_session.query(Bill).filter(Bill.id == input.bill_id).first()
            
            if not bill:
                return RecordPayment(
                    payment=None,
                    success=False,
                    message="Bill not found",
                    remaining_amount=0
                )
            
            # Check if bill is already paid
            if bill.status == BillStatus.PAID:
                return RecordPayment(
                    payment=None,
                    success=False,
                    message="Bill is already paid",
                    remaining_amount=0
                )
            
            # Calculate total paid so far
            existing_payments = db_session.query(Payment).filter(
                Payment.bill_id == input.bill_id,
                Payment.status == PaymentStatus.SUCCESS
            ).all()
            
            total_paid = sum(p.amount for p in existing_payments) + input.amount
            remaining = bill.amount - total_paid
            
            # Validate payment amount
            if total_paid > bill.amount:
                return RecordPayment(
                    payment=None,
                    success=False,
                    message=f"Payment exceeds bill amount. Bill: ₹{bill.amount}, Already paid: ₹{sum(p.amount for p in existing_payments)}",
                    remaining_amount=remaining
                )
            
            # Create payment record
            payment = Payment(
                bill_id=input.bill_id,
                amount=input.amount,
                payment_date=datetime.utcnow(),
                status=PaymentStatus.SUCCESS
            )
            
            db_session.add(payment)
            
            # Update bill status
            if remaining <= 0:
                bill.status = BillStatus.PAID
                message = "Payment recorded. Bill fully paid!"
            else:
                # Check if overdue
                if datetime.utcnow() > bill.due_date:
                    bill.status = BillStatus.OVERDUE
                    message = f"Partial payment recorded. Remaining: ₹{remaining}. Status: OVERDUE"
                else:
                    message = f"Partial payment recorded. Remaining: ₹{remaining}"
            
            db_session.commit()
            db_session.refresh(payment)
            
            return RecordPayment(
                payment=payment,
                success=True,
                message=message,
                remaining_amount=max(remaining, 0)
            )
        except Exception as e:
            db_session.rollback()
            return RecordPayment(
                payment=None,
                success=False,
                message=f"Error: {str(e)}",
                remaining_amount=0
            )
