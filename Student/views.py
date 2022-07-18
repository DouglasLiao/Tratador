from datetime import datetime
import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import serial
import time
import schedule

from .forms import StudentForm
from .models import StudentModel





def add_student(request, template_name='student_add.html'):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        # return  HttpResponse("ok saved")
        return redirect('Student:student_manage')
    return render(request, template_name, {'form':form})


def student_manage(request, template_name='student_manage.html'):
    std_data = StudentModel.objects.all() ###   select * from Student(table)
    data = {}
    data['object_list'] = std_data
    return render(request, template_name, data)


def student_edit(request, pk, template_name='student_add.html'):
    book= get_object_or_404(StudentModel, pk=pk)### select * from student where id=pk(parameterized id),pk means primary key
    form = StudentForm(request.POST or None, instance=book)
    if form.is_valid():
        form.save()
        return redirect('Student:student_manage')
    return render(request, template_name, {'form':form})

def delete_student(request, pk):
    obj = get_object_or_404(StudentModel, pk=pk)
    obj.delete()
    return redirect('Student:student_manage')



def show_graph(request,template_name='live_graph.html'):
    return render(request,template_name)


def fetch_sensor_values_ajax(request):
    data={}
    if request.is_ajax():
            com_port = request.GET.get('id', None)
            # sensor_val=random.random() # auto random value if sendor is not connected , you can remove this line
            sensor_data=[]
            now=datetime.now()
            ok_date=str(now.strftime('%Y-%m-%d %H:%M:%S'))
            try:

                sr=serial.Serial("COM9",9600)
                sr=serial.Serial(com_port,9600)
                st=list(str(sr.readline(),'utf-8'))
                sr.close()
                sensor_val=str(''.join(st[:]))
                if(sensor_val):
                    sensor_data.append(str(sensor_val)+','+ok_date)
                else:
                    sensor_data.append(str(sensor_val)+','+ok_date)
            except Exception as e:
                    sensor_data.append(str(sensor_val)+','+ok_date)
            data['result']=sensor_data
    else:
        data['result']='Not Ajax'
    return JsonResponse(data)

def main_func(request):
    arduino = serial.Serial('com3', 9600)
    print('Established serial connection to Arduino')
    arduino_data = arduino.readline()

    decoded_values = str(arduino_data[0:len(arduino_data)].decode("utf-8"))
    list_values = decoded_values.split('x')

    for item in list_values:
        list_in_floats.append(float(item))

    print(f'Collected readings from Arduino: {list_in_floats}')

    arduino_data = 0
    list_in_floats.clear()
    list_values.clear()
    arduino.close()
    print('Connection closed')
    print('<----------------------------->')


# ----------------------------------------Main Code------------------------------------
# Declare variables to be used
list_values = []
list_in_floats = []

print('Program started')

# Setting up the Arduino
schedule.every(10).seconds.do(main_func)

while True:
    schedule.run_pending()
    time.sleep(1)