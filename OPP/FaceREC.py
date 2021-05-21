
import cv2
import face_recognition
import pickle

from ast import literal_eval

from numpy.core.multiarray import result_type
from official_app.models import Offence, Offender


def check_face(img):
    
    context = {
        'detected':False,
        'encoding':[],
        'error':''
    }

    face = face_recognition.load_image_file(img)
    face = cv2.cvtColor(face,cv2.COLOR_BGR2RGB)

    faceloc = face_recognition.face_locations(face)
    
    if len(faceloc) < 1 :
        context['error'] = 'No faces detected! upload VALID image'
        return context
    if len(faceloc) > 1 :
        context['error'] = 'Multiple faces detected! upload VALID image'
        return context
    if len(faceloc) == 1 : 
        encoding = face_recognition.face_encodings(face)[0]
        context['detected'] = True
        context['encoding'] = encoding
        return context
    

    
    
def show_face(img,context):

    face = face_recognition.load_image_file(img)
    face = cv2.cvtColor(face,cv2.COLOR_BGR2RGB)

    faceloc = face_recognition.face_locations(face)[0]

    cv2.rectangle(face,(faceloc[3],faceloc[0]),(faceloc[1],faceloc[2]),(0,255,0),3)

    cv2.namedWindow(context,cv2.WINDOW_NORMAL)
    cv2.imshow(context,face)
    cv2.waitKey(0)




def get_offender_match(image) :

    check_result = check_face(image)

    result = {
        'detected': check_result['detected'],
        'match':False,
        'offenders':[],
        'error':check_result['error'],
    }
    
    if result['detected'] == True :
        offenders = Offender.objects.all()

        if len(offenders) > 0 :
            for offender in offenders :           
                test_encoding = check_result['encoding']
                offender_encoding = pickle.loads(data=literal_eval(offender.face_obj))     
                face_distance = face_recognition.face_distance([offender_encoding],test_encoding)
                if face_distance < 0.6 :
                    result['match'] = True
                    offences = Offence.objects.filter(offenders__id=offender.id)
                    offender = offender.get_offender()
                    offender['related_offences'] = []
                    for offence in offences :
                        offender['related_offences'].append(offence.get_offence())
                        
                    result['offenders'].append(offender)
                else : 
                        result['error'] = 'No match found!'
        else :
            result['error'] = 'No match found!'


    return result
