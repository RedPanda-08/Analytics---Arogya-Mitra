import enum
import uuid
from sqlalchemy import Column, String, Integer, DateTime, Date, ForeignKey, Boolean, Enum as SQLEnum, Float
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from .database import Base

#-- Enums ---- 

class AppointmentType(str, enum.Enum):
    ONLINE = "ONLINE"
    IN_PERSON = "IN_PERSON"

class AppointmentStatus(str, enum.Enum):
    BOOKED = "BOOKED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"

class InvoiceStatus(str, enum.Enum):
    PAID = "PAID"
    UNPAID = "UNPAID"
    PARTIAL = "PARTIAL"

# --- HOSPITAL MODEL ---
class Hospital(Base):
    __tablename__ = "hospitals"
    hospitalId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, name="hospital_id")
    name = Column(String(255), nullable=False)
    addressLine = Column(String(255), name="address_line")
    area = Column(String(100))
    city = Column(String(100))
    state = Column(String(100))
    pincode = Column(String(20))
    contactNumber = Column(String(20), name="contact_number")
    achievements = Column(ARRAY(String)) 
    establishedDate = Column(Date, name="established_date")
    totalBeds = Column(Integer, name="total_beds")
    createdAt = Column(DateTime, name="created_at")
    updatedAt = Column(DateTime, name="updated_at")

# --- PATIENT MODEL ---
class Patient(Base):
    __tablename__ = "patients"
    patientId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, name="patient_id")
    hospitalId = Column(UUID(as_uuid=True), ForeignKey("hospitals.hospital_id"), name="hospital_id", nullable=False)
    userId = Column(UUID(as_uuid=True), name="user_id", unique=True, nullable=False)
    
    fullName = Column(String(255), name="full_name", nullable=False)
    address = Column(String(255), name="address")
    phoneNumber = Column(String(20), name="phone_number")
    emergencyContact = Column(String(20), name="emergency_contact")
    bloodGroup = Column(String(20), name="blood_group")
    gender = Column(String(20), name="gender")
    dateOfBirth = Column(Date, name="date_of_birth")
    
    active = Column(Boolean, default=True, name="active")
    createdAt = Column(DateTime, name="created_at")
    updatedAt = Column(DateTime, name="updated_at")

# --- APPOINTMENT MODEL ---
class Appointment(Base):
    __tablename__ = "appointments"
    appointmentId = Column("appointment_id", UUID(as_uuid=True), primary_key=True)
    hospitalId = Column("hospital_id", UUID(as_uuid=True))
    date = Column("date", Date) # Use this for trends
    status = Column("status", String)
    createdAt = Column("created_at", DateTime)

class Invoice(Base):
    __tablename__ = "invoices"
    # Mapping Python attributes to your specific Supabase columns
    invoiceId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, name="invoice_id")
    hospitalId = Column(UUID(as_uuid=True), ForeignKey("hospitals.hospital_id"), name="hospital_id", nullable=False)
    patientId = Column(UUID(as_uuid=True), ForeignKey("patients.patient_id"), name="patient_id", nullable=False) 
    totalAmount = Column(Float, name="total_amount", default=0.0)
    status = Column(SQLEnum(InvoiceStatus), name="status")
    createdAt = Column(DateTime, name="created_at")
    items = relationship("InvoiceItem", back_populates="invoice")

# --- INVOICE ITEM MODEL ---
class InvoiceItem(Base):
    __tablename__ = "invoice_items"
    
    itemId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, name="item_id")
    invoiceId = Column(UUID(as_uuid=True), ForeignKey("invoices.invoice_id"), name="invoice_id", nullable=False)
    # referenceId could be an AppointmentID, LabRecordID, etc.
    referenceId = Column(UUID(as_uuid=True), name="reference_id") 
    referenceType = Column(String(50), name="reference_type") # e.g., 'BED', 'LAB'
    description = Column(String(255), name="description")
    cost = Column(Float, name="cost", default=0.0)
    invoice = relationship("Invoice", back_populates="items")

# --- INSURANCE CLAIMS MODEL ---
class InsuranceClaim(Base):
    __tablename__ = "insurance_claims"
    # Python Attribute : Database Column (snake_case)
    claimId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, name="claim_id")
    invoiceId = Column(UUID(as_uuid=True), ForeignKey("invoices.invoice_id"), name="invoice_id", nullable=False)
    providerName = Column(String(255), name="provider_name")
    policyNumber = Column(String(100), name="policy_number")
    claimAmount = Column(Float, name="claim_amount")
    status = Column(String(50), name="status") # 'SUBMITTED', 'REJECTED'
    
    # Optional: If your Java service also creates a created_at column here
    # createdAt = Column(DateTime, name="created_at")

class TreatmentRecord(Base):
    __tablename__ = "treatment_records"
    
    # Mapping to your specific Supabase columns
    recordId = Column(UUID(as_uuid=True), primary_key=True, name="record_id")
    treatmentId = Column(UUID(as_uuid=True), name="treatment_id", nullable=False)
    
    # Using 'performed_at' for temporal analytics (trends over time)
    performedAt = Column(DateTime, name="performed_at")
    
    # 'outcome' allows us to calculate clinical success rates
    outcome = Column(String(100), name="outcome") # e.g., 'SUCCESS', 'RECOVERY', 'CRITICAL'

class LabResult(Base):
    __tablename__ = "lab_result"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, name="id")
    testId = Column(UUID(as_uuid=True), name="test_id", nullable=False)
    
    # 'uploaded_at' is perfect for calculating average report delivery time
    uploadedAt = Column(DateTime, name="uploaded_at")
    uploadedBy = Column(UUID(as_uuid=True), name="uploaded_by") # Typically a Doctor or Lab Tech ID
    
    description = Column(String(255), name="description")
    resultData = Column(String, name="result_data") # Stores the actual finding or summary

class Medicine(Base):
    __tablename__ = "medicine"
    
    # Mapping to your specific Supabase columns
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, name="id")
    name = Column(String(255), name="name", nullable=False)
    
    # 'dosage_form' (e.g., Tablet, Syrup) and 'strength' (e.g., 500mg) 
    # are key for precise inventory categorization
    dosageForm = Column(String(100), name="dosage_form")
    strength = Column(String(100), name="strength")
    manufacturer = Column(String(255), name="manufacturer")

class Pharmacy(Base):
    __tablename__ = "pharmacy"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    affiliatedHospitalId = Column("affiliated_hospital_id", String) # String type

class Bed(Base):
    __tablename__ = "beds"
    
    # Mapping to your specific Supabase columns
    bedId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, name="bed_id")
    hospitalId = Column(UUID(as_uuid=True), ForeignKey("hospitals.hospital_id"), name="hospital_id")
    
    bedType = Column(String(50), name="bed_type") # e.g., 'ICU', 'General'
    status = Column(String(50), name="status") # e.g., 'OCCUPIED', 'AVAILABLE'
    
    # Temporal columns for turnover analytics
    createdAt = Column(DateTime, name="created_at")
    updatedAt = Column(DateTime, name="updated_at")

class Department(Base):
    __tablename__ = "departments"
    
    # Mapping to your specific Supabase columns
    departmentId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, name="department_id")
    hospitalId = Column(UUID(as_uuid=True), ForeignKey("hospitals.hospital_id"), name="hospital_id")
    
    deptName = Column(String(255), name="dept_name", nullable=False)

class DepartmentTreatment(Base):
    __tablename__ = "department_treatments_offered"
    
    # Using an autoincrement ID as a primary key for SQLAlchemy requirements
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Mapping to your specific column: department_department_id
    departmentId = Column(
        UUID(as_uuid=True), 
        ForeignKey("departments.department_id"), 
        name="department_department_id"
    )
    
    # Mapping to your specific column: treatments_offered
    treatmentName = Column(String(255), name="treatments_offered")
    
    # Relationship to easily pull department names in analytics
    department = relationship("Department")

class Ambulance(Base):
    __tablename__ = "ambulances"
    
    # Mapping to your specific Supabase columns
    ambulanceId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, name="ambulance_id")
    hospitalId = Column(UUID(as_uuid=True), ForeignKey("hospitals.hospital_id"), name="hospital_id")
    
    vehicleNumber = Column(String(20), name="vehicle_number")
    driverName = Column(String(255), name="driver_name")
    location = Column(String(255), name="location") # Current GPS or base location
    
    # This boolean is critical for real-time availability analytics
    available = Column(Boolean, default=True, name="available")

class DiagnosticCentre(Base):
    __tablename__ = "diagnostic_centre"
    id = Column(String, primary_key=True)
    affiliatedHospital = Column("affiliated_hospital", String) # String type
    name = Column(String, nullable=False)
    location = Column(String)
    rating = Column(Float) # double precision