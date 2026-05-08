import os
from datetime import datetime
from django.template.loader import render_to_string
from django.core.management import call_command
from .models import MonitorData, MachineMast, EmpMast, EnrollMast, ReportLog,CompanyMast, DepartMast, DesMast
from django.conf import settings
from datetime import timedelta
from django.db.models import Count
from collections import defaultdict
# Try to import pisa
try:
    from xhtml2pdf import pisa
except ImportError:
    pisa = None

def generate_report_for_date(report_date):
    livedatas = MonitorData.objects.filter(PunchDate__date=report_date)
    monitor_data = MonitorData.objects.filter(PunchDate__date=report_date)
    data = []
    hazard_in_count = hazard_out_count = 0
    non_hazard_in = non_hazard_out = 0
    non_hazard_total = hazard_total = 0
    for live in monitor_data:
        # Calculate counts for non-hazard and hazard data
        if live.TRID in ['7']:
           non_hazard_in += 1
        elif live.TRID in ['8']:
           non_hazard_out += 1
        if live.TRID in ['1', '3','5']:
            hazard_in_count += 1
        elif live.TRID in ['2', '4','6']:
            hazard_out_count += 1
    
    srnos = monitor_data.values_list('SRNO', flat=True)
    machines = MachineMast.objects.filter(SRNO__in=srnos)
    enrollids = monitor_data.values_list('EnrollID', flat=True)
    enrolls = EnrollMast.objects.filter(enrollid__in=enrollids).select_related('department')
    employees = EmpMast.objects.filter(enrollid__in=enrolls)
    # Lookup dictionaries
    machine_dict = {machine.SRNO: machine for machine in machines}
    enroll_dict = {enroll.enrollid: enroll for enroll in enrolls}

    non_hazardous_departments = defaultdict(int)
    hazardous_departments = defaultdict(int)

# Define all departments to ensure departments with 0 data are included
    all_departments = [dept.DepartName for dept in DepartMast.objects.all()]

# Calculate department-wise counts for Non-Hazardous and Hazardous areas
    for record in monitor_data:
        machine = machine_dict.get(record.SRNO)
        enroll = enroll_dict.get(record.EnrollID)

        if not machine or not enroll or not enroll.department:
            continue

        department_name = enroll.department.DepartName

        if machine.MachineNo in ['7']:  # Non-hazard In
          non_hazardous_departments[department_name] += 1
            
        elif machine.MachineNo in ['8']:  # Non-hazard Out
          non_hazardous_departments[department_name] -= 1
            
        if machine.MachineNo in ['1', '3','5']:  # Hazard In
             hazardous_departments[department_name] += 1
           
        elif machine.MachineNo in ['2', '4','6']:  # Hazard Out
             hazardous_departments[department_name] -= 1
 
    non_hazardous_data = [
           {"Department": dept, "HeadCount": max(0, non_hazardous_departments.get(dept, 0))}
            for dept in all_departments
        ]

    hazardous_data = [
             {"Department": dept, "HeadCount": max(0, hazardous_departments.get(dept, 0))}
             for dept in all_departments
         ]
   
    total_non_hazard_head_count = non_hazard_in - non_hazard_out
    total_hazard_head_count = hazard_in_count - hazard_out_count
    if livedatas.exists():
        srnos = livedatas.values_list('SRNO', flat=True)
        enrollids = livedatas.values_list('EnrollID', flat=True)
        sorted_livedatas = livedatas.order_by('EnrollID', 'PunchDate')
        machines = MachineMast.objects.filter(SRNO__in=srnos)
        enrolls = EnrollMast.objects.filter(enrollid__in=enrollids)
        employees = EmpMast.objects.select_related('department', 'company', 'designation', 'enrollid').filter(enrollid__in=enrolls)
        machine_dict = {m.SRNO: m for m in machines}
        enroll_dict = {e.enrollid: e for e in enrolls}
        employee_dict = {e.enrollid_id: e for e in employees}
        for idx, live in enumerate(sorted_livedatas, start=1):  # add serial numbers
            machine = machine_dict.get(live.SRNO)
            if not machine:
                continue
            enroll = enroll_dict.get(live.EnrollID)
            emp_data = employee_dict.get(enroll.id) if enroll else None
            data.append({
                'srno': idx,   # add srno here
                'monitor': live,
                'machine': machine,
                'employee': emp_data
            })
    context = {
        "non_hazardous": non_hazardous_data,
        "hazardous": hazardous_data,
        'hazard_in_count': hazard_in_count,
        'hazard_out_count': hazard_out_count,
        'hazard_total': total_hazard_head_count,
        'non_hazard_in': non_hazard_in,
        'non_hazard_out': non_hazard_out,
        'non_hazard_total': total_non_hazard_head_count,
        'data': data,
        'selected_date': report_date,
        'total': len(data)
    }
    html = render_to_string('pages/report_pdf.html', context)
    output_dir = 'D:/headcountreport/'
    os.makedirs(output_dir, exist_ok=True)
    pdf_file_path = os.path.join(output_dir, f'report_{report_date}.pdf')
    if pisa:
        with open(pdf_file_path, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(html, dest=pdf_file)
        if pisa_status.err:
            print(f"PDF error on {report_date}")
        else:
            ReportLog.objects.create(date=report_date, Status=1)
    else:
        # fallback: save the HTML if PDF lib is not available
        fallback_html_path = os.path.join(output_dir, f'report_{report_date}.html')
        with open(fallback_html_path, "w", encoding="utf-8") as f:
            f.write(html)
        ReportLog.objects.create(date=report_date, Status=1)
        print(f"xhtml2pdf not installed. Saved as HTML: {fallback_html_path}")
def auto_backup_if_required(days=15):
    backup_dir = os.path.join(settings.BASE_DIR, 'db_backups')
    if not os.path.exists(backup_dir):
        return
    backup_files = [
        f for f in os.listdir(backup_dir)
        if f.endswith('_db.sqlite3')
    ]
    if not backup_files:
        call_command('backup_old_monitordata')
        return

    def extract_date(filename):
        date_str = filename.split('_')[0]
        return datetime.strptime(date_str, '%d-%m-%Y')

    latest_file = max(backup_files, key=extract_date)
    last_backup_date = extract_date(latest_file)

    diff_days = (datetime.now() - last_backup_date).days

    if diff_days >= days:
        call_command('backup_old_monitordata')

