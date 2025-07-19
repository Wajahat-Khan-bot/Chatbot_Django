from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
import openai
import json
from django.conf import settings
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
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
            return Response({"response": f"You said:{user_message}"}, status=status.HTTP_200_OK)

        except Exception as e:
            print("OpenAI Error:", e)
            return Response({"error": "Chatbot error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# @csrf_exempt
# def chat_response(request):

#     openai.api_key = settings.OPENAI_API_KEY
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_message = data.get('message', '')
#         business_id = data.get('business_id', '').strip()

#         if not user_message:
#             return JsonResponse({"error": "message is required"}, status=status.HTTP_400_BAD_REQUEST)
        
#         try:
#             business = Business.objects.get(identifier=business_id)
#         except Business.DoesNotExist:
#             return JsonResponse({"error": "Invalid business ID"}, status=status.HTTP_404_NOT_FOUND)
        
#         context = f"""
#             Company: {business.name}
#             Services: {business.services}
#             Location: {business.location}
#             Email: {business.email}
#             Phone: {business.phone}
#             """
#         try:
#             response=openai.ChatCompletion.create(
#                 model="gpt-4.1",
#                 messages=[
#                     {"role": "system", "content": "You are a helpful assistant for this business. Use the following info:\n" + context},
#                     {"role": "user", "content": user_message}
#                 ]
#             )
            
#             bot_reply = response["choices"][0]["message"]["content"]
#             print(f"bot_response: {bot_reply}")
#             return JsonResponse({"response": bot_reply})
#         except Exception as e:
#             print("OpenAI Error:", e)
#             return JsonResponse({"error": "Chatbot error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
#     return JsonResponse({"error": "Invalid request"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


