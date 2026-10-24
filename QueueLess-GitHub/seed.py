from datetime import datetime, timedelta
from app import create_app, db
from app.models import User, Service, QueueTicket, Appointment
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    db.create_all()

    if not User.query.filter_by(email="admin@queueless.local").first():
        db.session.add(User(
            full_name="QueueLess Administrator",
            email="admin@queueless.local",
            password_hash=generate_password_hash("Admin123!"),
            role="admin"
        ))

    if not User.query.filter_by(email="customer@queueless.local").first():
        db.session.add(User(
            full_name="Demo Customer",
            email="customer@queueless.local",
            password_hash=generate_password_hash("Demo123!"),
            role="customer"
        ))

    service_specs = [
        ("General Enquiry", "General questions and walk-in support.", 6),
        ("Document Support", "Document checking, printing and submission support.", 8),
        ("Account Support", "Help with account access, profile and login issues.", 10),
    ]

    services = []
    for name, description, avg in service_specs:
        service = Service.query.filter_by(name=name).first()
        if not service:
            service = Service(name=name, description=description, average_service_minutes=avg, is_open=True)
            db.session.add(service)
            db.session.flush()
        services.append(service)

    db.session.commit()

    demo_customer = User.query.filter_by(email="customer@queueless.local").first()

    # Add a completed demo ticket so waiting-time calculations have historical data.
    if not QueueTicket.query.filter_by(ticket_number="G001", status="completed").first():
        t = QueueTicket(
            ticket_number="G001",
            user_id=demo_customer.id,
            service_id=services[0].id,
            status="completed",
            joined_at=datetime.utcnow() - timedelta(days=1, minutes=18),
            called_at=datetime.utcnow() - timedelta(days=1, minutes=12),
            service_started_at=datetime.utcnow() - timedelta(days=1, minutes=10),
            completed_at=datetime.utcnow() - timedelta(days=1),
        )
        db.session.add(t)

    # Add one upcoming appointment for demo screenshots.
    if not Appointment.query.filter_by(user_id=demo_customer.id, status="booked").first():
        a = Appointment(
            user_id=demo_customer.id,
            service_id=services[1].id,
            appointment_date=(datetime.utcnow() + timedelta(days=2)).date(),
            appointment_time="10:30",
            status="booked",
        )
        db.session.add(a)

    db.session.commit()
    print("QueueLess database initialized and demo data seeded.")
    print("Admin: admin@queueless.local / Admin123!")
    print("Customer: customer@queueless.local / Demo123!")
