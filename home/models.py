from django.db import models
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class GatePass(models.Model):
    allowing_entry = models.CharField(max_length=10, choices=[('Yes', 'Hazardous Area'), ('No', 'Non Hazardous Area')])
    id = models.AutoField(primary_key=True)
    cardNo                       = models.CharField(max_length=250,blank=False,null=False)
    date                         = models.DateField(null=True, blank=True)
    name                         = models.CharField(max_length=250,blank=True, null=True)
    company                      = models.CharField(max_length=250,blank=True, null=True)
    address                      = models.CharField(max_length=250,blank=True,null=True)
    mobile                       = models.CharField(max_length=250,blank=True, null=True)
    vehicleNo                    = models.CharField(max_length=250,blank=True, null=True)
    purpose                      = models.TextField()
    visitor_name                      = models.TextField()
    noOfPerson                   = models.CharField(max_length=250,blank=True,null=True)
    idNo                         = models.CharField(max_length=250,blank=True,null=True)
    typeOf                       = models.CharField(max_length=250,blank=True,null=True)
    govt_id                      = models.CharField(max_length=250,blank=True,null=True)
    govtno                       = models.CharField(max_length=250,blank=True,null=True)
    personToMeet                 = models.CharField(max_length=250,blank=True,null=True)
    inTime                       = models.CharField(max_length=250,blank=True,null=True)
    outTime                      = models.CharField(max_length=250,blank=True,null=True)
    permittedBy                  = models.CharField(max_length=250,blank=True,null=True)
    carringGadget                = models.CharField(max_length=250,blank=True,null=True)
    passNo                       = models.CharField(max_length=250,blank=True,null=True)
    image                        = models.ImageField(upload_to="gatepass_images/", default="default.jpg")
    remarks = models.TextField(blank=True, null=True) 
    valid_from                   = models.DateTimeField(null=True, blank=True)
    valid_to                     = models.DateTimeField(null=True, blank=True)
    renew_remarks=models.TextField(max_length=250,blank=True,null=True)
    createdAt                    = models.DateField(null=True, blank=True)
    updatedAt                    = models.DateField(null=True, blank=True)
    status                       = models.CharField(max_length=250, default='true')
    def __str__(self):
            return f"GatePass {self.id}"
    class Meta:
        db_table = 'GatePass'
class MachineMast(models.Model):
    id = models.AutoField(primary_key=True)
    MachineNo = models.CharField(max_length=50)
    RDRNO = models.CharField(max_length=50)
    PortNo = models.CharField(max_length=50)
    Password = models.CharField(max_length=100)
    con_status = models.CharField(max_length=50)
    Site = models.CharField(max_length=50)
    MachineType = models.TextField()
    SRNO = models.CharField(max_length=100, unique=True)
    RDRNAME = models.TextField()
    IPAddress = models.TextField()
    IO=models.CharField(max_length=50)
    LastConnected = models.DateTimeField(null=True, blank=True)
    Response = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.SRNO
    class Meta:
        db_table = 'Machines'

class EnrollMast(models.Model):
    id = models.AutoField(primary_key=True)
    enrollid = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey('DepartMast', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return str(self.id)
    class Meta:
        db_table = 'EnrollMast'

class EmpMast(models.Model): 
    id = models.BigAutoField(primary_key=True)
    empcode = models.CharField(max_length=100)
    enrollid = models.ForeignKey(EnrollMast, on_delete=models.CASCADE, null=True)
    Cardno = models.CharField(max_length=50)
    Name = models.TextField(blank=True, null=True)
    department = models.ForeignKey('DepartMast', on_delete=models.CASCADE, null=True,to_field='id')
    company = models.ForeignKey('CompanyMast', on_delete=models.CASCADE, null=True,to_field='id')
    designation = models.ForeignKey('DesMast', on_delete=models.CASCADE, null=True,to_field='id')
    Cardstatus = models.BooleanField(default=True)
    Shift = models.CharField(max_length=50)
    CatName = models.TextField(null=True, blank=True)
    STATUS_E = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return str(self.empcode)
    class Meta:
        db_table = 'EmpMast'

class MonitorData(models.Model):
    id = models.BigAutoField(primary_key=True)
    SRNO = models.CharField(max_length=50)
    EnrollID = models.CharField(max_length=100)
    PunchDate = models.DateTimeField()
    TRID = models.CharField(max_length=50)

    SEND_SERVER = models.CharField(max_length=50, null=True, blank=True)
    RESEND_SERVER = models.CharField(max_length=50, null=True, blank=True)

    Errorstatus = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.SRNO

    class Meta:
        db_table = 'MonitorDataTbl'



class CompanyMast(models.Model):
	id = models.AutoField(primary_key=True)
	Company = models.TextField()
	Address = models.TextField()

	def __str__(self):
		return self.CompanyId
    



class DepartMast(models.Model):
	id = models.AutoField(primary_key=True)
	DepartName = models.TextField(null=True, blank=True)
	Status = models.TextField(default=True)

	def __str__(self):
		return f"{self.DepartName}"

class DesMast(models.Model):

	id = models.AutoField(primary_key=True)
	department = models.ForeignKey(DepartMast, on_delete=models.CASCADE, null=True, blank=True,to_field='id')
	Designation = models.TextField()

	def __str__(self):
		return self.Desgid
      
class ReportLog(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()  
    addedon = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    Status = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.date}"

class License(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
