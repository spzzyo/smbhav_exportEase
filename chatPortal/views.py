from django.shortcuts import render, redirect
from django.conf import settings
from .models import Messages
import os
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from django.http import JsonResponse



def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    
    # Retrieve query parameters
    carrier_name = request.GET.get('carrier_name')
    pol = request.GET.get('pol')
    pod = request.GET.get('pod')
    transit_time = request.GET.get('transit_time')
    vessel_id = request.GET.get('vessel_id')
    departure_date = request.GET.get('departure_date')

    summary = get_messages_and_summarize()
    
    # Add these parameters to the context dictionary
    context = {
        'carrier_name': carrier_name,
        'pol': pol,
        'pod': pod,
        'transit_time': transit_time,
        'vessel_id': vessel_id,
        'departure_date': departure_date,
        'summary': summary,
    }



    # Render the chatPage.html with the context
    return render(request, "chat/chatPage.html", context)



def comparison(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    if request.user.user_type == 2:
        return render(request, "carriers/carriers_exporter.html", context)

    return render(request, "carriers/carriers_shipper.html", context)





def get_messages_and_summarize():
    system_prompt = (
        "You are an AI assistant. Summarize the following chat conversation in a clear and concise manner. "
        "Focus on the main points discussed and avoid unnecessary details. Keep it focused on negotiation parameters "
        "discussed between the exporter and the shipping carrier service."
    )

    try:
        
        messages = Messages.objects.filter(roomId="saket_MSC").order_by('timestamp').values('username', 'message')
        if not messages.exists():
            return "No messages found in the chat room."

     
        all_messages = "\n".join([f"{message['username']}: {message['message']}" for message in messages])
    except Exception as e:
        return f"Error fetching messages: {str(e)}"

  
    try:
        api_key = settings.API_KEY  
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

        
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"{system_prompt}\n\n{all_messages}"
                        }
                    ]
                }
            ]
        }

        headers = {
            "Content-Type": "application/json",
        }

       
        response = requests.post(url, headers=headers, json=payload, params={"key": api_key})
        response_data = response.json()

        summary = (
            response_data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
            .strip()
        )

        if not summary:
            summary = "Failed to generate a summary. Please check the API response."
    except Exception as e:
        summary = f"Error summarizing messages: {str(e)}"

    context = {"summary": summary}

  
    return summary






def make_protected_call(request):
    if request.method == "POST":
        try:
            

            # Respond with success and call SID
            return JsonResponse({"status": "success", "call_sid": call.sid})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request method"})