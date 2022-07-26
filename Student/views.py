from datetime import datetime
import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import serial
import time
import schedule
import json

from .forms import StudentForm
from .models import StudentModel

import pyfirmata2

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

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def fetch_sensor_values_ajax(request):
    data={}

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        com_port = request.GET.get('id', None)
        sensor_val = ''
        ser = serial.Serial(com_port, 115200, timeout=1)
        time.sleep(2)
        line = ser.readline()
        sensor_data=[]
        now=datetime.now()
        ok_date=str(now.strftime('%Y-%m-%d %H:%M:%S'))
        ser.close()
        try:
            if line:
                string = line.decode()
                num = int(string)

                sensor_val = str(num(''.join(line[:])))
                if (sensor_val):
                    sensor_data.append(str(sensor_val)+','+ok_date)
                else:
                    sensor_data.append(str(sensor_val)+','+ok_date)
        except Exception as e:
                sensor_data.append(str(sensor_val)+','+ok_date)
        data['result']=sensor_data
    else:
        data['result']='Not Ajax'
    return JsonResponse(data)

