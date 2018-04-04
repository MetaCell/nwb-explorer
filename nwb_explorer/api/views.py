from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import logging
import model as pygeppetto
from ..nwb_model_interpreter import NWBModelInterpreter

#curl -X POST http://localhost:8000/api/load
@api_view(['GET','POST'])
@permission_classes((AllowAny, ))
def load(request):
    if request.method == 'GET':
        # posts = Post.objects.all()
        # serializer = PostSerializer(posts, many=True)
        model_interpreter = NWBModelInterpreter()
        return Response(model_interpreter.importType("","","",""))
    elif request.method == 'POST':
        return Response("Post model")
    