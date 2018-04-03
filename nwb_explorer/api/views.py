from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

#curl -X POST http://localhost:8000/api/people
@api_view(['GET','POST'])
@permission_classes((AllowAny, ))
def people(request):
    if request.method == 'GET':
        # posts = Post.objects.all()
        # serializer = PostSerializer(posts, many=True)
        people = [
            {"name": "Matteo", "surname": "Cantarelli", "occupation": "Philisopher"},
            {"name": "Adrian", "surname": "Quintana", "occupation": "Guru"},
            {"name": "Giovanni", "surname": "Idilli", "occupation": "The Boss"},
        ]
        return Response(people)
    elif request.method == 'POST':
        return Response("Post person")
    