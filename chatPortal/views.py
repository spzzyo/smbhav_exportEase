from django.shortcuts import render, redirect
from django.conf import settings
from .models import Messages
import os
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.rest import Client
from django.http import JsonResponse
import matplotlib.pyplot as plt

# Directory for saving the chart
CHART_DIR = "static/charts"


def calculate_import_charges_view(request):
    if request.method == "POST":
        # Gather input from the form
        product_value = float(request.POST.get("product_value", 0))
        shipping_cost = float(request.POST.get("shipping_cost", 0))
        insurance_cost = float(request.POST.get("insurance_cost", 0))

        # Specific rates for furniture imports from Germany to India
        import_duty_rate = 25.0  # Example: Furniture typically has 25% import duty
        IGST_rate = 18.0  # Integrated GST for furniture is 18% in India

        # Perform calculations
        import_duty = (product_value * import_duty_rate) / 100
        taxable_base = product_value + shipping_cost + insurance_cost + import_duty
        IGST = (taxable_base * IGST_rate) / 100
        total_cost = product_value + shipping_cost + insurance_cost + import_duty + IGST

        # Calculate percentages for each category
        percentages = {
            "Product Value": round((product_value / total_cost) * 100, 2),
            "Shipping Cost": round((shipping_cost / total_cost) * 100, 2),
            "Insurance Cost": round((insurance_cost / total_cost) * 100, 2),
            "Import Duty": round((import_duty / total_cost) * 100, 2),
            "IGST": round((IGST / total_cost) * 100, 2),
        }

        # Return JSON response with data
        return JsonResponse({
            "breakdown": {
                "Product Value": product_value,
                "Shipping Cost": shipping_cost,
                "Insurance Cost": insurance_cost,
                "Import Duty": import_duty,
                "IGST": IGST,
                "Total Cost": total_cost,
            },
            "percentages": percentages,
        })

    return render(request, "estimator/index.html")


def packreco(request):
    return render(request, "packaging/packaging_rec.html")

def logistics(request):
    return render(request, "logistics/logistic.html")

def doc_buddy(request):
    return render(request, "docBuddy/doc.html")

def landing(request):
    return render(request, "landing.html")
def shiptrack(request):
    return render(request,"user/shipment_tracking.html")

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
        
        messages = Messages.objects.filter(roomId="exporter_MSC").order_by('timestamp').values('username', 'message')
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
            # Twilio credentials
            account_sid = "AC53ccbc7b90c6e3e019895efadc19e6d3"
            auth_token = "6c62feb76465fe2ae69713867dfaa2e9"
            client = Client(account_sid, auth_token)

            # Create the call
            call = client.calls.create(
                method="GET",
                status_callback_method="POST",
                url="http://demo.twilio.com/docs/voice.xml",
                to="+919833914068", 
                from_="+12406604030",
            )

            # Respond with success and call SID
            return JsonResponse({"status": "success", "call_sid": call.sid})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request method"})