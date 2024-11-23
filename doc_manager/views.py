from django.http import HttpResponse
from django.shortcuts import render
from .models import Document, Request
from django.contrib.auth.decorators import login_required
from .dec_utils import decrypt_and_verify_document
from django.core.mail import send_mail

# Create your views here.
@login_required
def actor_Dashboard_with_all_docs(request):
    # Ensure the user is a shipper
    if request.user.user_type != 4:
        return HttpResponse("Unauthorized", status=403)

    # Fetch all documents along with their exporters
    documents = Document.objects.select_related("exporter").all()

    return render(request, "user/actor_dashboard.html", {"documents": documents})


@login_required
def request_document_access(request, document_id):
    document = Document.objects.get(id=document_id)
    # Ensure the user is a Actor
    if request.user.user_type == 4:
        Request.objects.create(shipper=request.user, document=document)
        return HttpResponse("Request sent to admin.")
    else:
        return HttpResponse("Unauthorized", status=403)
    

@login_required
def admin_dashboard(request):
    # Ensure the user is an admin
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=403)

    # Fetch pending requests
    pending_requests = Request.objects.filter(status="Pending")

    if request.method == "POST":
        request_id = request.POST.get("request_id")
        action = request.POST.get("action")
        req = Request.objects.get(id=request_id)

        if action == "verify":
            # Perform forgery check
            metadata_key = req.document.s3_metadata_key
            encrypted_key = req.document.s3_encrypted_key
            try:
                decrypt_and_verify_document(encrypted_key, metadata_key)
                req.status = "Forgery Check Passed"
                req.save()
                return HttpResponse("Forgery check passed.")
            except Exception as e:
                return HttpResponse(f"Forgery check failed: {str(e)}")

        elif action == "approve":
            # Approve request and send email to the shipper
            req.status = "Approved"
            req.save()

            # Decrypt the document
            decrypted_path = decrypt_and_verify_document(
                req.document.s3_encrypted_key, req.document.s3_metadata_key
            )

            # Send the document to the shipper
            send_mail(
                "Document Access Approved",
                "Your request to access the document has been approved. Please find the document attached.",
                "admin@exportease.com",
                [req.shipper.email],
                fail_silently=False,
                # Attach the decrypted document
                files=[decrypted_path],
            )
            return HttpResponse("Request approved and document sent.")

        elif action == "reject":
            # Reject the request
            req.status = "Rejected"
            req.save()
            return HttpResponse("Request rejected.")

    return render(request, "user/admin_dashboard.html", {"pending_requests": pending_requests})