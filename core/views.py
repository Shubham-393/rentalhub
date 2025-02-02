from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse , HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Tool, Category, Rental, Review

from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.core.mail import send_mail

import razorpay
from django.conf import settings

from django.contrib.auth import get_user_model # assuming you have a registration form

User = get_user_model()  # Get the custom User model


import google.generativeai as genai

from django.views.decorators.csrf import csrf_exempt
import json 

# Configure Gemini AI
genai.configure(api_key=settings.GEMINI_API_KEY)
flash_model = genai.GenerativeModel("gemini-1.5-flash")
pro_model = genai.GenerativeModel("gemini-1.5-pro")

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").lower()

            if not user_message:
                return JsonResponse({"error": "No message provided"}, status=400)

            # Tool Availability Check
            if "available" in user_message or "rent" in user_message:
                tools = Tool.objects.filter(availability_status=True)
                tool_names = [tool.name for tool in tools]
                if tool_names:
                    return JsonResponse({"reply": f"Available tools: {', '.join(tool_names)}"})
                else:
                    return JsonResponse({"reply": "No tools are available for rent right now."})

            # Rental Cost Check
            elif "price" in user_message or "cost" in user_message:
                tool_name = extract_tool_name(user_message)
                if tool_name:
                    tool = Tool.objects.filter(name__icontains=tool_name).first()
                    if tool:
                        return JsonResponse({"reply": f"The rental cost for {tool.name} is ₹{tool.rental_price} per day."})
                return JsonResponse({"reply": "Please specify the tool name to check the price."})

            # User Booking Status
            elif "my booking" in user_message or "rented" in user_message:
                user_rentals = Rental.objects.filter(renter=request.user)
                if user_rentals.exists():
                    response = "Your current bookings:\n"
                    for rental in user_rentals:
                        response += f"- {rental.tool.name}: {rental.rental_start_date} to {rental.rental_end_date}\n"
                    return JsonResponse({"reply": response})
                else:
                    return JsonResponse({"reply": "You have no active bookings."})
            else:                 
                # prompt = f"""You are a chatbot for an online tool rental marketplace. The user asks: {user_message}.You can only respond to queries related to tool , rentals, availability, pricing, bookings, and general information related to tools, online rental marketplace. If the query is not related to these topics, tell the user: 'Sorry, I can only assist with rental and tool-related queries.' Please provide a clear and concise , short.Answer as specifically as possible regarding rental and tools.Use bullet point to make good reply"""
                 
                 # **2. Use AI for general tool-related questions**
                prompt = f"""
            You are a chatbot for an online tool rental marketplace. Your job is to provide expert advice on tools and their best use cases.Please provide a clear, concise, short  and specific answers.Use bullet points, lists, and examples to make good reply.
            The user asks: {user_message}.
            - If the question is about tool usage, maintenance, or recommendations, provide a helpful answer.
            - If the question is about tool availability, rental price, or user bookings, inform the user that they should check the website.
            - If the question is unrelated to tools or rentals, politely respond: 'I'm here to assist with tools and rentals. Let me know if you have any questions about our available tools or their usage!'.
            """
            
                response = flash_model.generate_content(prompt)  # Use Flash for quick responses
                bot_reply = response.text
                print(bot_reply)
                return JsonResponse({"reply": bot_reply})

            # If the message is vague, use AI but **ONLY for rental-related responses**
            # prompt = f"You are a chatbot for an online tool rental marketplace. The user asks: {user_message}. Answer only based on rental-related knowledge."
                
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


def extract_tool_name(user_message):
    """Extracts tool name from user query using simple keyword matching."""
    tool_names = [tool.name.lower() for tool in Tool.objects.all()]
    for word in user_message.split():
        if word in tool_names:
            return word.capitalize()
    return None


# Homepage view
def index(request):
    
    categories = Category.objects.all()
    featured_tools = Tool.objects.filter(availability_status=True).order_by('-created_at')[:3]

    query = request.GET.get('q')
    # if query:
    #     try:
    #         category = Category.objects.get(name=query)
    #         return redirect('category_listing', category_id=category.id)
    #     except Category.DoesNotExist:
    #         try:
    #             tool = Tool.objects.get(name=query)
    #             return redirect('tool_details', tool_id=tool.id)
    #         except Tool.DoesNotExist:
    #             messages.error(request, "No results found for your query.")
    #             return render(request, 'index.html', {
    #     'categories': categories,
    #     'featured_tools': featured_tools
    # })

    if query:
        
        query_lower = query.lower()
        categories = Category.objects.filter(name__icontains=query_lower)
        tools = Tool.objects.filter(name__icontains=query_lower)
        if categories:
            return redirect('category_listing', category_id=categories[0].id)
        elif tools:
            return redirect('tool_details', tool_id=tools[0].id)
        else:
            messages.error(request, "No results found for your query.")
                 
            return render(request, 'index.html', {'categories': categories,  'featured_tools': featured_tools})
    

    return render(request, 'index.html', {
        'categories': categories,
        'featured_tools': featured_tools
    })

# Tool details view
def tool_details(request, tool_id):
    tool = get_object_or_404(Tool, pk=tool_id)
    reviews = tool.reviews.all()
    average_rating = reviews.aggregate(Avg('rating')).get('rating__avg', 0)
    return render(request, 'tool_details.html', {
        'tool': tool,
        'reviews': reviews,
        'average_rating': average_rating
    })

# Rental booking view
# @login_required
# def book_tool(request, tool_id):
#     tool = get_object_or_404(Tool, pk=tool_id, availability_status=True)
#     print("Tool object retrieved:", tool)
#     print("Tool owner:", tool.owner)
#     print("Request user:", request.user)

#     if request.method == 'POST':
#         if request.user == tool.owner:
#             print("Owner trying to book their own tool!")
#             messages.error(request, "You cannot book your own tool!")
#             return redirect('index')
        
#         rental_start_date = request.POST.get('rental_start_date')
#         rental_end_date = request.POST.get('rental_end_date')
#         total_price = float(request.POST.get('total_price'))

#         rental = Rental.objects.create(
#             tool=tool,
#             renter=request.user,
#             rental_start_date=rental_start_date,
#             rental_end_date=rental_end_date,
#             total_price=total_price,
#             status='Pending'
#         )
#         tool.availability_status = False
#         tool.save()
#         # Add a success message
#         messages.success(request, "Booking completed successfully! Enjoy your tool.")
        
#         return redirect('index')
        

#     return render(request, 'book_tool.html', {'tool': tool})


@login_required
def book_tool(request, tool_id):
    tool = get_object_or_404(Tool, pk=tool_id, availability_status=True)

    if request.method == 'POST':
        if request.user == tool.owner:
            messages.error(request, "You cannot book your own tool!")
            return redirect('index')

        rental_start_date = request.POST.get('rental_start_date')
        rental_end_date = request.POST.get('rental_end_date')
        total_price = float(request.POST.get('total_price'))
        email = request.POST.get('email')

        # Razorpay Client
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # Create Razorpay Order
        order_data = {
            "amount": int(total_price * 100),  # Amount in paise
            "currency": "INR",
            "payment_capture": "1"
        }
        order = client.order.create(data=order_data)

        # Store order details in session (temporary)
        request.session['rental_details'] = {
            "tool_id": tool.id,
            "rental_start_date": rental_start_date,
            "rental_end_date": rental_end_date,
            "total_price": total_price,
            "order_id": order["id"]
        }

        # Pass order details to payment page
        return render(request, 'payment_page.html', {
            "order_id": order["id"],
            "amount": total_price,
            "key": settings.RAZORPAY_KEY_ID,
            "email": email
        })

    return render(request, 'book_tool.html', {'tool': tool})

@login_required
def payment_success(request):
    if request.method == "POST":
        payment_id = request.POST.get("razorpay_payment_id")
        order_id = request.POST.get("razorpay_order_id")
        signature = request.POST.get("razorpay_signature")
        user_email = request.POST.get("email")

        # Retrieve rental details from session
        rental_details = request.session.get('rental_details', {})
        if not rental_details:
            return JsonResponse({"status": "error", "message": "Session expired"})

        tool = get_object_or_404(Tool, pk=rental_details["tool_id"])
        renter = request.user

        # Verify payment signature
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature
            })

            # Create the rental record
            rental = Rental.objects.create(
                tool=tool,
                renter=renter,
                rental_start_date=rental_details["rental_start_date"],
                rental_end_date=rental_details["rental_end_date"],
                total_price=rental_details["total_price"],
                status='Completed'
            )

            # Mark tool as unavailable
            tool.availability_status = False
            tool.save()

            # Email details
            # user_email = request.user.email
            subject = f"Booking Confirmation - {tool.name}"
    
            message = f"""
            Dear {request.user.username},
            Your booking for '{ tool.name}' has been successfully confirmed!

            📅 Rental Period: {rental.rental_start_date} to {rental.rental_end_date}
            

            Thank you for renting with us!

            Best Regards,
            Rental Hub Team
            """
            print(message)
            send_mail(subject, message, "khotshubham393@gmail.com", [user_email])
            print("email sent")
            print(user_email)
            

            # Clear session data
            del request.session['rental_details']

            messages.success(request, "Booking successful! Enjoy your tool.[Check your email for more details]")
            return redirect('index')

        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({"status": "failure", "message": "Payment verification failed"})

    return JsonResponse({"status": "error", "message": "Invalid request"})



# Category listing view
def category_listing(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    tools = category.tools.filter(availability_status=True)
    return render(request, 'category_listing.html', {
        'category': category,
        'tools': tools
    })

# Add a review view
@login_required
def add_review(request, tool_id):
    tool = get_object_or_404(Tool, pk=tool_id)
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')

        Review.objects.create(
            tool=tool,
            user=request.user,
            rating=rating,
            comment=comment
        )

        return JsonResponse({'message': 'Review added successfully!'})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def register(request):
    if (request.method=='POST'):
        form = UserRegistrationForm(request.POST)
        if form.is_valid() :
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('index')
        
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Send email to admin
        send_mail(
            subject,
            message,
            "khotshubham393+rentalhub@gmail.com",
            ['khotshubham393@gmail.com'],
            fail_silently=False,
        )

        messages.success(request, 'Your message has been sent successfully!')
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')