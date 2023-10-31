from rest_framework.response import Response
from rest_framework.views import APIView

from common.decorator import mandatories, optionals


class QueryTestView(APIView):
    @mandatories("name", "age")
    def get(self, request, m):
        response_data = {"name": m["name"], "age": m["age"]}
        return Response(response_data)

    @optionals({"city": "New York", "occupation": "Engineer"})
    def post(self, request, o):
        response_data = {"city": o["city"], "occupation": o["occupation"]}
        return Response(response_data)
