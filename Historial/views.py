from django.shortcuts import render, redirect
from .models import Historial_usuario
from django.contrib.auth.decorators import permission_required 
from django.contrib.auth.decorators import login_required 
from django.core.paginator import Paginator  
from urllib.parse import urlencode

def listHistU(request): 

    ListAllHU= Historial_usuario.objects.all().order_by('Id_historial')  
    ListAllHU22= Historial_usuario.objects.all().count()

    paginator= Paginator(ListAllHU, 20)
    Page_number= request.GET.get('page') 
    page_objt= paginator.get_page(Page_number)

    List={'HistU': page_objt, 
          'Conter' : ListAllHU22 } 
    return render (request,'templates_historial_usuario/historial_usuario.html',List) 


def BusqHistorial (request): 

    HistEmp= request.GET.get('HistEmp') 
    HistMovimientos= request.GET.get('HistMovimientos')  
    HistModulo= request.GET.get('HistModulo') 
    HistFecha= request.GET.get('HistFecha') 

    if not any([HistEmp, HistMovimientos, HistModulo, HistFecha]): 
        
        return redirect("HistorialU")
    
    if HistEmp: 

        sql_Busqueda3= "SELECT historial_usuario.*, Empleados_user_empleados.* from historial_usuario join Empleados_user_empleados on historial_usuario.id_usuario = Empleados_user_empleados.id WHERE Empleados_user_empleados.first_name= %s" 

        BUsqhist= Historial_usuario.objects.raw(sql_Busqueda3,[HistEmp])

    if HistMovimientos: 

        sql_Busqueda3= "SELECT historial_usuario.*, Empleados_user_empleados.* from historial_usuario join Empleados_user_empleados on historial_usuario.id_usuario = Empleados_user_empleados.id WHERE historial_usuario.TIpo_Movimiento= %s" 
        
        BUsqhist= Historial_usuario.objects.raw(sql_Busqueda3,[HistMovimientos]) 

    if HistModulo: 

        sql_Busqueda3= "SELECT historial_usuario.*, Empleados_user_empleados.* from historial_usuario join Empleados_user_empleados on historial_usuario.id_usuario = Empleados_user_empleados.id WHERE historial_usuario.Modulo= %s" 
        
        BUsqhist= Historial_usuario.objects.raw(sql_Busqueda3,[HistModulo])  

    if HistFecha: 

        sql_Busqueda3= "SELECT historial_usuario.*, Empleados_user_empleados.* from historial_usuario join Empleados_user_empleados on historial_usuario.id_usuario = Empleados_user_empleados.id WHERE historial_usuario.Fecha_y_hora= %s" 
        
        BUsqhist= Historial_usuario.objects.raw(sql_Busqueda3,[HistFecha])   

    if HistEmp and HistMovimientos: 

        sql_Busqueda3= "SELECT historial_usuario.*, Empleados_user_empleados.* from historial_usuario join Empleados_user_empleados on historial_usuario.id_usuario = Empleados_user_empleados.id WHERE Empleados_user_empleados.first_name= %s and historial_usuario.TIpo_Movimiento= %s" 
        
        BUsqhist= Historial_usuario.objects.raw(sql_Busqueda3,[HistEmp, HistMovimientos])   

    if HistModulo and HistFecha: 

        sql_Busqueda3= "SELECT historial_usuario.*, Empleados_user_empleados.* from historial_usuario join Empleados_user_empleados on historial_usuario.id_usuario = Empleados_user_empleados.id WHERE historial_usuario.Modulo= %s and historial_usuario.Fecha_y_hora= %s"

        BUsqhist= Historial_usuario.objects.raw(sql_Busqueda3,[HistModulo, HistFecha])    


    if HistMovimientos and HistModulo:

        sql_Busqueda3= "SELECT historial_usuario.*, Empleados_user_empleados.* from historial_usuario join Empleados_user_empleados on historial_usuario.id_usuario = Empleados_user_empleados.id WHERE historial_usuario.TIpo_Movimiento= %s and historial_usuario.Modulo= %s" 

        BUsqhist= Historial_usuario.objects.raw(sql_Busqueda3,[HistMovimientos, HistModulo])    


    if HistEmp and HistFecha: 

        sql_Busqueda3= "SELECT historial_usuario.*, Empleados_user_empleados.* from historial_usuario join Empleados_user_empleados on historial_usuario.id_usuario = Empleados_user_empleados.id WHERE Empleados_user_empleados.first_name= %s and historial_usuario.Fecha_y_hora= %s"  

        BUsqhist= Historial_usuario.objects.raw(sql_Busqueda3,[HistEmp, HistFecha])   
        
    if HistEmp and HistMovimientos and HistModulo: 

        sql_Busqueda3= "SELECT historial_usuario.*, Empleados_user_empleados.* from historial_usuario join Empleados_user_empleados on historial_usuario.id_usuario = Empleados_user_empleados.id WHERE Empleados_user_empleados.first_name= %s and historial_usuario.TIpo_Movimiento= %s and historial_usuario.Modulo= %s"  

        BUsqhist= Historial_usuario.objects.raw(sql_Busqueda3,[HistEmp, HistMovimientos, HistModulo])  

    if HistEmp and HistMovimientos and HistFecha: 

        sql_Busqueda3= "SELECT historial_usuario.*, Empleados_user_empleados.* from historial_usuario join Empleados_user_empleados on historial_usuario.id_usuario = Empleados_user_empleados.id WHERE Empleados_user_empleados.first_name= %s and historial_usuario.TIpo_Movimiento= %s and historial_usuario.Fecha_y_hora= %s"   

        BUsqhist= Historial_usuario.objects.raw(sql_Busqueda3,[HistEmp, HistMovimientos, HistFecha])  

    if HistEmp and HistModulo and HistFecha: 

        sql_Busqueda3= "SELECT historial_usuario.*, Empleados_user_empleados.* from historial_usuario join Empleados_user_empleados on historial_usuario.id_usuario = Empleados_user_empleados.id WHERE Empleados_user_empleados.first_name= %s and historial_usuario.Modulo= %s and historial_usuario.Fecha_y_hora= %s"    

        BUsqhist= Historial_usuario.objects.raw(sql_Busqueda3,[HistEmp, HistModulo, HistFecha])  
    
    if HistMovimientos and HistModulo and HistFecha: 

        sql_Busqueda3= "SELECT historial_usuario.*, Empleados_user_empleados.* from historial_usuario join Empleados_user_empleados on historial_usuario.id_usuario = Empleados_user_empleados.id WHERE historial_usuario.TIpo_Movimiento= %s and historial_usuario.Modulo= %s and and historial_usuario.Fecha_y_hora= %s"  

        BUsqhist= Historial_usuario.objects.raw(sql_Busqueda3,[HistMovimientos, HistModulo, HistFecha])   

    if HistEmp and HistMovimientos and HistModulo and HistFecha: 

        sql_Busqueda3= "SELECT historial_usuario.*, Empleados_user_empleados.* from historial_usuario join Empleados_user_empleados on historial_usuario.id_usuario = Empleados_user_empleados.id WHERE Empleados_user_empleados.first_name= %s and historial_usuario.TIpo_Movimiento= %s and historial_usuario.Modulo= %s and historial_usuario.Fecha_y_hora= %s"  

        BUsqhist= Historial_usuario.objects.raw(sql_Busqueda3,[HistEmp, HistMovimientos, HistModulo, HistFecha])  

    collector= list(BUsqhist)
    Limite= Paginator(collector, 20) 
    Page_number= request.GET.get('page') 
    page_objt= Limite.get_page(Page_number)  

    params = {k: v for k, v in request.GET.items() if k != 'page' and v != ''}
    querystring = '&' + urlencode(params) if params else ''

    ListAllHU22= Historial_usuario.objects.all().count()

    Ackerman={ 
        'Filter' : page_objt,  
        'querystring' : querystring, 
        'Conter' : ListAllHU22
    }  

    return render(request, 'templates_historial_usuario/historial_usuario.html', Ackerman)