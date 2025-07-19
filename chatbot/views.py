from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
import openai
from django.conf import settings
from django.http import HttpResponseForbidden
from .models import Business

def index(request, identifier):
    token = request.GET.get("token")

    try:
        business = Business.objects.get(identifier=identifier, access_token = token)
        print(f"business: {business}")
        return render(request, "index.html", {"business_id": business})
    except Business.DoesNotExist:
        return HttpResponseForbidden("Invalid business")

class ChatResponse(APIView):
    def post(self, request):
        openai.api_key = settings.OPENAI_API_KEY

        user_message = request.data.get("message", "").strip()
        business_id = request.data.get("business_id", "").strip()

        if not user_message or not business_id:
            return Response(
                {"error": "Missing message or business_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            business = Business.objects.get(identifier=business_id)
        except Business.DoesNotExist:
            return Response(
                {"error": "Invalid business ID"},
                status=status.HTTP_404_NOT_FOUND
            )

        context = f"""
        Company: {business.name}
        Services: {business.services}
        Location: {business.location}
        Email: {business.email}
        Phone: {business.phone}
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for this business. Use the following info:\n" + context},
                    {"role": "user", "content": user_message}
                ]
            )

            bot_reply = response["choices"][0]["message"]["content"]
            return Response({"response": bot_reply}, status=status.HTTP_200_OK)

        except Exception as e:
            print("OpenAI Error:", e)
            return Response({"error": "Chatbot error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)