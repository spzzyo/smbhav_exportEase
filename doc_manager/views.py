from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Document, Request
from django.contrib.auth.decorators import login_required
from .dec_utils import decrypt_and_verify_document
from django.core.mail import send_mail


from PIL import Image, ImageDraw, ImageFont
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import os

def add_watermark(file_path, output_path, watermark_text="ExportEase"):
    """Adds a diagonal watermark to both PDFs and images."""
    # Detect file type
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == ".pdf":
        # Watermark a PDF
        reader = PdfReader(file_path)
        writer = PdfWriter()

        for page in reader.pages:
            # Get the page size
            page_width = float(page.mediabox.width)
            page_height = float(page.mediabox.height)

            # Create a temporary watermark PDF
            watermark_buffer = io.BytesIO()
            c = canvas.Canvas(watermark_buffer, pagesize=(page_width, page_height))
            c.setFont("Helvetica-Bold", 50)
            c.setFillColorRGB(0.7, 0.7, 0.7, alpha=0.3)  # Light grey with transparency
            c.rotate(45)  # Rotate text diagonally

            # Calculate center position
            text_width = c.stringWidth(watermark_text, "Helvetica-Bold", 50)
            x = (page_width - text_width) / 2
            y = page_height / 2

            # Draw watermark at the center
            c.drawString(x, y, watermark_text)
            c.save()
            watermark_buffer.seek(0)
            watermark_pdf = PdfReader(watermark_buffer).pages[0]

            # Apply watermark to the current page
            page.merge_page(watermark_pdf)
            writer.add_page(page)

        # Save the output PDF
        with open(output_path, "wb") as f:
            writer.write(f)

    elif file_extension in [".png", ".jpg", ".jpeg"]:
        # Watermark an image
        img = Image.open(file_path).convert("RGBA")
        txt = Image.new("RGBA", img.size, (255, 255, 255, 0))

        # Initialize drawing context
        draw = ImageDraw.Draw(txt)
        font_size = int(min(img.size) * 0.05)  # Adjust font size based on image size
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        # Calculate the size of the watermark text using getbbox()
        text_width, text_height = draw.textbbox((0, 0), watermark_text, font=font)[2:]

        # Draw the diagonal watermark
        for x in range(0, img.size[0], text_width + 100):
            for y in range(0, img.size[1], text_height + 100):
                draw.text((x, y), watermark_text, fill=(119, 119, 119, 128), font=font)

        watermarked = Image.alpha_composite(img, txt)
        watermarked.save(output_path, "PNG")

    else:
        raise ValueError("Unsupported file type. Please provide a PDF or an image file.")



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
    

from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.http import HttpResponse
from doc_manager.models import Request
from django.conf import settings

@login_required
def admin_dashboard(request):
    # Fetch pending requests that passed forgery checks
    pending_requests = Request.objects.filter(status="Forgery Check Passed")

    if request.method == "POST":
        request_id = request.POST.get("request_id")
        action = request.POST.get("action")
        req = Request.objects.get(id=request_id)

        if action == "approve":
            # Approve request
            req.status = "Approved"
            req.save()

            # Send the document to the shipper using EmailMessage
            document_path = req.document.original_file.path  # Ensure this is the correct file path
            watermarked_path = os.path.join(
                os.path.dirname(document_path), f"watermarked_{os.path.basename(document_path)}"
            )

            try:
                # Add a watermark to the document
                add_watermark(document_path, watermarked_path, watermark_text="ExportEase")

                # Send the email with the watermarked file
                email = EmailMessage(
                    "Document Access Approved",
                    "Your request to access the document has been approved. Please find the document attached.",
                    settings.EMAIL_HOST_USER,
                    [req.shipper.email],
                )
                email.attach_file(watermarked_path)
                email.send(fail_silently=False)

                # Optionally, clean up the watermarked file after sending
                os.remove(watermarked_path)

                return HttpResponse("Request approved and watermarked document sent.")
            except Exception as e:
                return HttpResponse(f"Failed to send email: {str(e)}", status=500)

        elif action == "reject":
            # Reject the request
            req.status = "Rejected"
            req.save()
            return HttpResponse("Request rejected.")

    return render(request, "user/admin_dashboard.html", {"pending_requests": pending_requests})


@login_required
def process_forgery_checks(request):
    # Automatically approve forgery checks
    pending_requests = Request.objects.filter(status="Pending")

    for req in pending_requests:
        req.status = "Forgery Check Passed"
        req.save()

    # Redirect to the admin dashboard after processing forgery checks
    return redirect("user:admin-dashboard")  # Use the correct namespace and name