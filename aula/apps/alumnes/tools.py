# This Python file uses the following encoding: utf-8
from aula.apps.alumnes.models import Alumne, Grup
from django.db.models import Q
from aula.apps.incidencies.models import Incidencia, Expulsio, Sancio
from aula.apps.presencia.models import ControlAssistencia
from aula.apps.tutoria.models import Actuacio, SeguimentTutorial
from aula.apps.avaluacioQualitativa.models import AvaluacioQualitativa,\
    RespostaAvaluacioQualitativa
from aula.apps.usuaris.models import Accio, LoginUsuari
from datetime import date 
import datetime


def fusiona_alumnes_by_pk( pk , credentials = None):
    a = Alumne.objects.get( pk = pk )

    q_mateix_cognom = Q(                             
                    cognoms = a.cognoms  )
    q_mateix_nom = Q( 
                    nom = a.nom,
                      )            
    q_mateix_neixement = Q(
                    data_neixement = a.data_neixement
                        )
    q_mateixa_altres = Q(
                    adreca = a.adreca,
                    telefons = a.telefons,
                    localitat = a.localitat,
                    centre_de_procedencia = a.centre_de_procedencia,
                    adreca__gte= u""                             
                        )
    
    condicio1 = q_mateix_nom & q_mateix_cognom & q_mateix_neixement
    condicio2 = q_mateix_nom & q_mateix_cognom & q_mateixa_altres
    condicio3 = q_mateix_nom & q_mateixa_altres & q_mateix_neixement
    
    
    alumne_grup = Alumne.objects.filter(  
                                    condicio1 | condicio2 | condicio3
                                           ).exclude( pk = pk ).order_by( 'data_alta' )
    
    fusiona_alumnes( a, list( alumne_grup ), credentials )



    
def fusiona_alumnes( a_desti, a_fusionar , credentials = None ):
    '''
       el destí ha de ser el més vell (és baixa) perquè rebrà les dades dels nous 
    '''
    
    controls_desti = a_desti.controlassistencia_set.values_list('impartir__pk', flat=True)
    
    for a in a_fusionar:
        
        if a.data_baixa is None:
            a_desti.data_baixa = None
        a_desti.nom = a.nom
        a_desti.cognoms = a.cognoms
        a_desti.data_neixement = a.data_neixement
        
        if bool( a.correu_relacio_familia_pare ) :
            a_desti.correu_relacio_familia_pare = a.correu_relacio_familia_pare
        
        if bool( a.correu_relacio_familia_mare ):
            a_desti.correu_relacio_familia_mare = a.correu_relacio_familia_mare
        
        Incidencia.objects.filter( alumne = a ).update( alumne = a_desti  )
        Expulsio.objects.filter( alumne = a ).update( alumne = a_desti )
                
        controls = ControlAssistencia.objects.filter( alumne = a ).exclude( impartir__pk__in = controls_desti ).values_list( 'pk', flat = True)
        for i in controls:
            ControlAssistencia.objects.filter( pk = i ).update( alumne = a_desti )

        ControlAssistencia.objects.filter( alumne = a ).delete()

        Sancio.objects.filter( alumne = a ).update( alumne = a_desti )

        Actuacio.objects.filter( alumne = a ).update( alumne = a_desti )
        
        for x in RespostaAvaluacioQualitativa.objects.filter( alumne = a ):
            x.alumne = a_desti 
            x.credentials = credentials
            try:
                x.save()
            except:
                pass

        if a.get_user_associat():
            if  a_desti.get_user_associat():
                Accio.objects.filter( usuari = a.get_user_associat() ).update( usuari = a_desti.get_user_associat() )
                LoginUsuari.objects.filter( usuari = a.get_user_associat() ).update( usuari = a_desti.get_user_associat() )
            else:
                Accio.objects.filter( usuari = a.get_user_associat() ).delete()
                LoginUsuari.objects.filter( usuari = a.get_user_associat() ).delete()
            a.get_user_associat().delete()

        if SeguimentTutorial.objects.filter( alumne = a ).exists():
            SeguimentTutorial.objects.filter( alumne = a_desti ).delete()                
            SeguimentTutorial.objects.filter( alumne = a ).update( alumne = a_desti )
                        
        Alumne.objects.filter( pk = a.pk  ).delete()
        
    a_desti.save()
        
        
def crea_alumne(nom, cognoms, dataNaixement, grup):
    # Exemple d'ús: crea_alumne "Josep" "Serra Xoriguera(d)" 08-12-2001 2DAM

    #Cal fer comprovacions dels paràmetres.
    a=Alumne()
    a.nom = nom
    a.cognoms = cognoms
    a.data_neixement = datetime.datetime.strptime(dataNaixement, "%d-%m-%Y").date()
    descripcioGrup = str(grup)
    grup = Grup.objects.get(descripcio_grup=descripcioGrup)
    a.grup = grup
    a.estat_sincronitzacio = 'MAN'
    a.data_alta = date.today()
    a.motiu_bloqueig = u'No sol·licitat'
    a.tutors_volen_rebre_correu = False
    a.save()

