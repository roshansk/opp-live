import json
import pickle
from django.http.response import JsonResponse
from io import BytesIO

from official_app.models import Offender,Offence
from OPP.FaceREC import get_offender_match

def search_offenders_by_image(request):
 
    if request.method == "POST" :
        if request.body :
            image = request.body
            result = get_offender_match(BytesIO(image))# Offence Id to avoid registered offenders
            print(result)

        return JsonResponse({'result':result})


def search_offenders_by_name(request):

    result = {
        'match':False,
        'offenders':[],
        'error':''
    }   

    if request.method == "POST" :
        body = json.loads(request.body)
        name = body["name"]
        names = name.split(' ')
        querysets = []         
        offender_objs = []   
        offenders = []

        for name in names :
            try : 
                querysets.append( Offender.objects.filter(name__icontains=name) )
            except Offender.DoesNotExist :
                result['error'] = "No Match Found"

        for offenders in querysets :
            if len(offenders) > 0 :
                for offender in offenders :
                    if offender not in offender_objs :
                        offender_objs.append(offender)

            if len(offender_objs) > 0 :
                for offender in offender_objs :
                    result['match'] = True
                    offences = Offence.objects.filter(offenders__id=offender.id)
                    offender = offender.get_offender()
                    offender['related_offences'] = []
                    for offence in offences :
                        offender['related_offences'].append(offence.get_offence())
                    result['offenders'].append(offender)
                    result['error'] = ""
            else :
                result['error'] = "No Match Found"


        return JsonResponse({ 'result' : result })


