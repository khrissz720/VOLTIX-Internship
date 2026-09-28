from pathlib import Path
import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.chart import BarChart, DoughnutChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.utils import get_column_letter

# Excel 16.0-compatible dashboard generator.
# Input: healthcare_noshows.csv
# Output: Healthcare_No_Shows_Dashboard.xlsx
BASE = Path(__file__).resolve().parent
INPUT = BASE / 'healthcare_noshows.csv'
OUTPUT = BASE / 'Healthcare_No_Shows_Dashboard.xlsx'

raw = pd.read_csv(INPUT)
raw.columns = raw.columns.str.strip()
df = raw.copy()
df['ScheduledDay'] = pd.to_datetime(df['ScheduledDay'], errors='coerce')
df['AppointmentDay'] = pd.to_datetime(df['AppointmentDay'], errors='coerce')
df['Gender'] = df['Gender'].astype(str).str.strip().str.upper()
df['Neighbourhood'] = df['Neighbourhood'].astype(str).str.strip().str.upper()
original_wait = pd.to_numeric(df['Date.diff'], errors='coerce')
df['Wait_Days'] = original_wait.clip(lower=0).astype(int)

df['Age_Group'] = pd.cut(df['Age'], [-1,17,29,44,59,74,np.inf], labels=['0-17','18-29','30-44','45-59','60-74','75+']).astype(str)
df['Appointment_Weekday'] = df['AppointmentDay'].dt.day_name()
df['Appointment_Month'] = df['AppointmentDay'].dt.strftime('%Y-%m')
df['Attendance_Status'] = np.where(df['Showed_up'], 'Attended', 'No-show')
df['SMS_Status'] = np.where(df['SMS_received'], 'Yes', 'No')
df['Scholarship_Status'] = np.where(df['Scholarship'], 'Yes', 'No')
df['Hypertension_Status'] = np.where(df['Hipertension'], 'Yes', 'No')
df['Diabetes_Status'] = np.where(df['Diabetes'], 'Yes', 'No')
df['Alcoholism_Status'] = np.where(df['Alcoholism'], 'Yes', 'No')
df['Handicap_Status'] = np.where(df['Handcap'], 'Yes', 'No')
df['Data_Quality_Flag'] = np.where(original_wait < 0, 'Adjusted negative wait time to 0', 'OK')

cols = ['PatientId','AppointmentID','Gender','ScheduledDay','AppointmentDay','Age','Age_Group','Neighbourhood','Scholarship_Status','Hypertension_Status','Diabetes_Status','Alcoholism_Status','Handicap_Status','SMS_Status','Showed_up','Attendance_Status','Wait_Days','Appointment_Weekday','Appointment_Month','Data_Quality_Flag']
data = df[cols]

# The workbook uses pre-calculated analysis tables and charts rather than modern Excel formulas.
# This makes the dashboard display correctly in Excel 16.0 immediately after opening.
wb = Workbook(); dash = wb.active; dash.title = 'Dashboard'; analysis = wb.create_sheet('Analysis'); clean = wb.create_sheet('Data_Cleaned'); readme = wb.create_sheet('Read_Me')
NAVY='17365D'; BLUE='2F75B5'; LIGHT='D9EAF7'; GRAY='F2F2F2'; WHITE='FFFFFF'; DARK='404040'; GREEN='70AD47'; ORANGE='ED7D31'; RED='C00000'; TEAL='00A6A6'
for row in data.itertuples(index=False, name=None): clean.append(row)
for c in clean[1]: c.font=Font(bold=True,color=WHITE); c.fill=PatternFill('solid',fgColor=NAVY); c.alignment=Alignment(horizontal='center')
tab=Table(displayName='HealthcareData',ref=f'A1:T{len(data)+1}'); tab.tableStyleInfo=TableStyleInfo(name='TableStyleMedium2',showRowStripes=True); clean.add_table(tab); clean.freeze_panes='A2'; clean.auto_filter.ref=f'A1:T{len(data)+1}'

att=(df.Attendance_Status=='Attended').sum(); nos=(df.Attendance_Status=='No-show').sum(); total=len(df)
gender=pd.crosstab(df.Gender,df.Attendance_Status).reindex(columns=['Attended','No-show'],fill_value=0); gender['Total']=gender.sum(axis=1); gender['No-show Rate']=gender['No-show']/gender['Total']
age=pd.crosstab(df.Age_Group,df.Attendance_Status).reindex(['0-17','18-29','30-44','45-59','60-74','75+'],fill_value=0).reindex(columns=['Attended','No-show'],fill_value=0); age['Total']=age.sum(axis=1); age['No-show Rate']=age['No-show']/age['Total']
sms=pd.crosstab(df.SMS_Status,df.Attendance_Status).reindex(['Yes','No'],fill_value=0).reindex(columns=['Attended','No-show'],fill_value=0); sms['Total']=sms.sum(axis=1); sms['No-show Rate']=sms['No-show']/sms['Total']
days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']; weekday=pd.crosstab(df.Appointment_Weekday,df.Attendance_Status).reindex(days,fill_value=0).reindex(columns=['Attended','No-show'],fill_value=0); weekday['Total']=weekday.sum(axis=1); weekday['No-show Rate']=weekday['No-show']/weekday['Total']

# Dashboard KPIs
for pos,label,val,fmt,color in [('A5','TOTAL APPOINTMENTS',total,'#,##0',BLUE),('D5','ATTENDED',att,'#,##0',GREEN),('G5','NO-SHOWS',nos,'#,##0',RED),('J5','NO-SHOW RATE',nos/total,'0.0%',ORANGE)]:
    c=dash[pos]; sc=c.column; sr=c.row; dash.merge_cells(start_row=sr,start_column=sc,end_row=sr,end_column=sc+2); dash.merge_cells(start_row=sr+1,start_column=sc,end_row=sr+2,end_column=sc+2); dash.cell(sr,sc,label).font=Font(bold=True,color=WHITE); dash.cell(sr,sc).fill=PatternFill('solid',fgColor=color); dash.cell(sr+1,sc,val).font=Font(size=22,bold=True,color=NAVY); dash.cell(sr+1,sc).fill=PatternFill('solid',fgColor=LIGHT); dash.cell(sr+1,sc).number_format=fmt; dash.cell(sr+1,sc).alignment=Alignment(horizontal='center')

dash.merge_cells('A1:N2'); dash['A1']='HEALTHCARE NO-SHOWS'; dash['A1'].font=Font(size=24,bold=True,color=WHITE); dash['A1'].fill=PatternFill('solid',fgColor=NAVY); dash['A1'].alignment=Alignment(horizontal='center',vertical='center')
dash.merge_cells('A3:N3'); dash['A3']='Appointment Attendance & No-show Analysis | Excel 16.0 Compatible'; dash['A3'].alignment=Alignment(horizontal='center')

# Analysis tables and charts are generated from fixed values for reliable rendering.
def put(frame,row,col,title):
    analysis.cell(row,col,title).font=Font(bold=True,color=WHITE); analysis.cell(row,col).fill=PatternFill('solid',fgColor=NAVY)
    for j,h in enumerate(frame.columns,col): analysis.cell(row+1,j,h).font=Font(bold=True,color=WHITE); analysis.cell(row+1,j).fill=PatternFill('solid',fgColor=BLUE)
    for i,(idx,r) in enumerate(frame.iterrows(),row+2):
        analysis.cell(i,col,str(idx))
        for j,v in enumerate(r,col+1): analysis.cell(i,j,float(v) if isinstance(v,(float,np.floating)) else int(v) if isinstance(v,(int,np.integer)) else v)
    return row+1,row+1+len(frame)

put(pd.DataFrame({'Count':[att,nos]},index=['Attended','No-show']),1,1,'Attendance')
put(gender[['Attended','No-show','Total','No-show Rate']],1,5,'Gender')
put(age[['Attended','No-show','Total','No-show Rate']],1,11,'Age Group')
put(sms[['Attended','No-show','Total','No-show Rate']],10,1,'SMS Received')
put(weekday[['Attended','No-show','Total','No-show Rate']],10,7,'Weekday')

def bc(title, col, catcol, start, end, anchor, typ='bar'):
    ch=BarChart(); ch.type=typ; ch.title=title; ch.height=7; ch.width=11; ch.style=10; ch.add_data(Reference(analysis,min_col=col,min_row=start,max_row=end),titles_from_data=True); ch.set_categories(Reference(analysis,min_col=catcol,min_row=start+1,max_row=end)); dash.add_chart(ch,anchor)

ch=DoughnutChart(); ch.add_data(Reference(analysis,min_col=2,min_row=2,max_row=3),titles_from_data=False); ch.set_categories(Reference(analysis,min_col=1,min_row=2,max_row=3)); ch.title='Attendance vs No-show'; ch.height=7; ch.width=11; ch.dataLabels=DataLabelList(); ch.dataLabels.showPercent=True; dash.add_chart(ch,'A13')
bc('No-shows by Gender',7,5,2,4,'G13')
bc('No-shows by Age Group',13,11,2,8,'A28','col')
bc('No-shows by Appointment Weekday',9,7,11,18,'G28','col')
bc('No-shows by SMS Received',3,1,11,13,'M13')

dash.merge_cells('M28:N28'); dash['M28']='ACTIONABLE FINDINGS'; dash['M28'].font=Font(bold=True,color=WHITE); dash['M28'].fill=PatternFill('solid',fgColor=NAVY); dash.merge_cells('M29:N36')
top_age=age['No-show Rate'].idxmax(); top_day=weekday['No-show Rate'].idxmax(); top_sms=sms['No-show Rate'].idxmax(); top_gender=gender['No-show Rate'].idxmax()
dash['M29']=(f'• Overall no-show rate: {nos/total:.1%}.\n• Highest age-group rate: {top_age} ({age.loc[top_age,"No-show Rate"]:.1%}).\n• Highest weekday rate: {top_day} ({weekday.loc[top_day,"No-show Rate"]:.1%}).\n• Highest gender rate: {top_gender} ({gender.loc[top_gender,"No-show Rate"]:.1%}).\n• Highest SMS-group rate: {top_sms} ({sms.loc[top_sms,"No-show Rate"]:.1%}).\n• Investigate these segments using the filters in Data_Cleaned.')
dash['M29'].alignment=Alignment(wrap_text=True,vertical='top'); dash['M29'].fill=PatternFill('solid',fgColor=GRAY)
dash.merge_cells('A43:N45'); dash['A43']='INTERACTION: Data_Cleaned is an Excel Table with AutoFilter enabled. Filter Gender, SMS_Status, Age_Group, Neighbourhood, Attendance_Status and other fields using the dropdown arrows. Dashboard charts are pre-calculated so they display immediately in Excel 16.0.'; dash['A43'].alignment=Alignment(wrap_text=True,vertical='center'); dash['A43'].fill=PatternFill('solid',fgColor=GRAY)
for c in range(1,15): dash.column_dimensions[get_column_letter(c)].width=13
dash.sheet_view.showGridLines=False; analysis.sheet_view.showGridLines=False

readme['A1']='TASK 8 — HEALTHCARE NO-SHOWS'; readme['A1'].font=Font(size=18,bold=True,color=WHITE); readme['A1'].fill=PatternFill('solid',fgColor=NAVY); readme.merge_cells('A1:F1')
items=[('Purpose','Analyze appointment attendance and identify patterns associated with no-shows.'),('Source records',total),('Missing cells',int(data.isna().sum().sum())),('Duplicate rows',int(data.duplicated().sum())),('Corrected negative wait records',int((data.Data_Quality_Flag!='OK').sum())),('Compatibility','Designed for Excel 16.0; no modern Excel functions are required.'),('Interaction','Use AutoFilter on Data_Cleaned for detailed exploration.'),('Sheets','Dashboard = presentation; Analysis = supporting data; Data_Cleaned = cleaned records.')]
for i,(a,b) in enumerate(items,3): readme.cell(i,1,a).font=Font(bold=True,color=NAVY); readme.cell(i,2,b); readme.merge_cells(start_row=i,start_column=2,end_row=i,end_column=6); readme.cell(i,2).alignment=Alignment(wrap_text=True)
readme.column_dimensions['A'].width=38
wb.save(OUTPUT)
print(f'Created: {OUTPUT}')
