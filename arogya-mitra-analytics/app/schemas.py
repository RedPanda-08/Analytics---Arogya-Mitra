from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from uuid import UUID
from datetime import datetime, date
from typing import Optional, List

class BaseSchema(BaseModel):
    # Automatically handles snake_case to camelCase conversion
    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel, populate_by_name=True)

class HospitalRead(BaseSchema):
    hospitalId: UUID
    name: str
    addressLine: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    totalBeds: int
    contactNumber: Optional[str] = None
    establishedDate: Optional[date] = None
    createdAt: Optional[datetime] = None

class PatientBase(BaseSchema):
    fullName: str
    address: Optional[str] = None
    phoneNumber: Optional[str] = None
    emergencyContact: Optional[str] = None
    bloodGroup: Optional[str] = None
    gender: Optional[str] = None
    dateOfBirth: Optional[date] = None
    active: bool = True

class PatientRead(PatientBase):
    patientId: UUID
    hospitalId: UUID
    userId: UUID
    createdAt: Optional[datetime] = None

class AppointmentBase(BaseSchema):
    date: date
    timeSlot: str
    type: str
    status: str

class AppointmentRead(AppointmentBase):
    appointmentId: UUID
    hospitalId: UUID
    patientId: UUID
    doctorId: UUID
    createdAt: Optional[datetime] = None

class InvoiceItemRead(BaseSchema):
    itemId: UUID
    referenceType: Optional[str] = None
    description: Optional[str] = None
    cost: float

class InvoiceBase(BaseSchema):
    totalAmount: float
    status: str

class InvoiceRead(InvoiceBase):
    invoiceId: UUID
    hospitalId: UUID
    patientId: UUID
    createdAt: Optional[datetime] = None
    items: List[InvoiceItemRead] = []

class InsuranceClaimRead(BaseSchema):
    claimId: UUID
    invoiceId: UUID
    providerName: Optional[str] = None
    policyNumber: Optional[str] = None
    claimAmount: float
    status: str

class TreatmentRecordRead(BaseSchema):
    recordId: UUID
    treatmentId: UUID
    performedAt: Optional[datetime] = None
    outcome: Optional[str] = None

class LabResultRead(BaseSchema):
    id: UUID
    testId: UUID
    description: Optional[str] = None
    resultData: Optional[str] = None
    uploadedAt: Optional[datetime] = None
    uploadedBy: Optional[UUID] = None

class MedicineRead(BaseSchema):
    id: UUID
    name: str
    dosageForm: Optional[str] = None
    strength: Optional[str] = None
    manufacturer: Optional[str] = None

class PharmacyRead(BaseSchema):
    id: UUID
    name: str
    address: Optional[str] = None
    affiliatedHospitalId: UUID

class BedRead(BaseSchema):
    bedId: UUID
    hospitalId: UUID
    bedType: str
    status: str
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

class DepartmentRead(BaseSchema):
    departmentId: UUID
    hospitalId: UUID
    deptName: str

class DepartmentTreatmentRead(BaseSchema):
    departmentId: UUID
    treatmentName: str

class AmbulanceRead(BaseSchema):
    ambulanceId: UUID
    hospitalId: UUID
    vehicleNumber: str
    driverName: Optional[str] = None
    location: Optional[str] = None
    available: bool

class DiagnosticCentreRead(BaseSchema):
    id: UUID
    name: str
    location: Optional[str] = None
    rating: float
    affiliatedHospital: UUID