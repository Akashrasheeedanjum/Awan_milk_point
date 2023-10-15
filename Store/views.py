# Create your views here.
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from . models import *
from django.contrib.auth import authenticate, login,logout
from datetime import date
from decimal import Decimal
from django.contrib import messages
from django.db.models import Sum
import os

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# from twilio.rest import Client
# from django.conf import settings

# def send_sms(to, body):
#     client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
#     message = client.messages.create(
#         to=to,
#         from_=settings.TWILIO_PHONE_NUMBER,
#         body=body
#     )
#     return message


# def send_sms_view(request):
#     print("akash")
#     to_number = '+923014070721'  # Replace with the recipient's phone number
#     message_body = 'Hello, this is your SMS message!'
#     send_sms(to_number, message_body)
#     return HttpResponse('SMS sent successfully!')


def index(request):
    # Your view logic here
    return render(request, 'base.html')

def profile(request):
    username=request.user
    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        # Handle the case where the user does not exist (e.g., show an error page).
        return render(request, 'user_profile_not_found.html')

    context = {
        'user': user,
    }
    return render(request, 'manager/profile.html',context)






def index(request):
    branch_name = Branch.objects.all()

    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        branch = request.POST['branch']

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                if str(user.branch) == str(branch):
                    login(request, user)
                    messages.success(request, "Welcome User")
                    return redirect('manager_dashbord')
                else:
                    # Branch doesn't match
                    messages.error(request, "Invalid Branch")
            except Branch.DoesNotExist:
                # User has no associated branch
                messages.error(request, "User has no associated branch")
        else:
            # Invalid login credentials
            messages.error(request, "Invalid login credentials")

    # Your view logic here
    return render(request, 'main_login.html', {"branch": branch_name})




def render_pdf_view(request,pid):
    invice=MilkPurchase.objects.get(id=pid)
    template_path = 'pdf.html'
    context = {'invice':invice}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # for downlord 
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # foe view 
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def user_login(request):
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(request, username=username, password=password)
        print(username,password)
        print("/////")
        print(user)

        if user is not None:
            login(request, user)
            if user.user_type == 'manager':
                print("i am manager")
                return redirect('manager_dashbord')
            elif request.user.is_staff:
                print("i am Admin")
                return redirect('manager_dashbord')

            elif user.user_type == 'customer':
                return redirect('customer_dashboard')  # Redirect customers to their dashboard
        else:
            # Handle invalid login credentials
            # You can render a template with an error message or redirect to the login page again
            pass
    return render(request, 'login.html')

def signup(request):
    branch=request.user.branch
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        user_type = request.POST['user_type']
        phone = request.POST.get('phone', '')  # Optional field
        address = request.POST.get('address', '')  # Optional field
        date_of_birth = request.POST.get('date_of_birth', '')  # Optional field

        # Process and save the data (e.g., create a user object)
        CustomUser.objects.create_user(username=username,password=password,user_type=user_type,phone_number=phone,address=address,date_of_birth=date_of_birth,branch=branch)
        
        print("saved")

        return redirect('index')
    # Your view logic here
    return render(request, 'signup.html')

def signout(request):
    print("logout")
    logout(request)
    # messages.success(request,"Logout Successfully")
    return redirect("/")

# delect Functions

def deleteCenterMilk(request,id,pid):
    print('rining')
    print(id)

    inf = MilkPurchase.objects.get(id=id)
    inf.delete()
    return redirect(f'/view_center/{pid}')

def deleteCenter(request,id):
    print('rining')
    print(id)

    inf = Employee.objects.get(id=id)
    inf.delete()
    return redirect('center_details')

def deleteCenterPayment(request,id,pid):
    print('rining')
    print(id)

    inf = MakePayment.objects.get(id=id)
    inf.delete()
    return redirect(f'/view_center/{pid}')

def deleteCustomer(request,id):
    print('rining')
    print(id)

    inf = Employee.objects.get(id=id)
    inf.delete()
    return redirect('customer_details')

def deleteCustomerPayment(request,id,pid):
    print('rining')
    print(id)

    inf = ReceivedPayment.objects.get(id=id)
    inf.delete()
    return redirect(f'/view_customer/{pid}')

def deleteExpence(request,id,pid):
    print('rining')
    print(id)   

    inf = CustomerExpence.objects.get(id=id)
    inf.delete()
    return redirect(f'/view_customer/{pid}')

def deleteSalePayment(request,id,pid):
    print('rining')
    print(id)

    inf = MilkSale.objects.get(id=id)
    inf.delete()
    return redirect(f'/view_customer/{pid}')


# Edit Functions
#
def editCenterMilk(request,id,pid):

    edit_milk=MilkPurchase.objects.get(id=id)

    dd=str(edit_milk.purchase_date)




    if request.method == 'POST':
        # center_name = request.POST.get('milk_center', '')
        date_str = request.POST.get('date', '')
        print(date_str)
        volume = request.POST.get('volume', '')
        price = request.POST.get('price', '')
        lr = request.POST.get('LR', '')  # Corrected variable name
        fat = request.POST.get('Fat', '')  # Corrected variable name
        snf = request.POST.get('SNF', '') # Corrected variable name
        ts = request.POST.get('TS', '')  # Corrected variable name
        TsVolume = request.POST.get('TsVolume', '')
        total_price = request.POST.get('total_price', '')
        date = datetime.strptime(date_str, '%Y-%m-%d')
        print(date)

        # date=str(date)
        edit_milk=MilkPurchase.objects.get(id=id)

        # edit_milk.milk_center=milk_center,
        edit_milk.purchase_date=date,
        edit_milk.volume=volume,
        edit_milk.price_per_liter=price,
        edit_milk.LR=lr,
        edit_milk.Fat=fat,
        edit_milk.SNF=snf,
        edit_milk.price_on_TS=TsVolume,
        edit_milk.total_price=total_price

        edit_milk.save()





        return redirect(f'/view_center/{pid}')

    context={
        'edit_milk':edit_milk,
        'dd':dd
    }


    return render(request, 'manager/edit_purchase_milk.html',context)

def add_vendor(request):
    if request.method == 'POST':
        try:
            # Assuming you have already authenticated the user and retrieved the branch
            branch=request.user.branch
            name = request.POST.get('name', '')
            phone = request.POST.get('phone', '')
            address = request.POST.get('address', '')
            balance = request.POST.get('balance', '')
            vendor_type = request.POST['vendor_type']
            print(vendor_type)

            # Create and save a new MilkCenter instance
            Vendor = Employee(name=name, phone_number=phone, address=address,opening_balance=balance, Employee_type=vendor_type, branch=branch)
            Vendor.save()
            messages.success(request, (vendor_type +" saved successfully"))
            return redirect('/manager_dashbord/')  # Redirect to the manager dashboard or the appropriate URL
        except Exception as e:
            print(f"Error saving Milk Center: {e}")
            messages.error(request, "Error")
            # Handle the error more gracefully, e.g., displaying an error message to the user
    return render(request, 'manager/add_vander.html')




def add_center(request):
    if request.method == 'POST':
        try:
            # Assuming you have already authenticated the user and retrieved the branch
            branch=request.user.branch
            name = request.POST.get('name', '')
            phone = request.POST.get('phone', '')
            address = request.POST.get('address', '')
            opening_balance = request.POST.get('price', '')

            # Create and save a new MilkCenter instance
            milk_center = Employee(name=name, phone_number=phone, address=address, opening_balance=opening_balance, branch=branch)
            milk_center.save()
            print("Milk Center saved successfully")
            return redirect('/manager_dashbord/')  # Redirect to the manager dashboard or the appropriate URL
        except Exception as e:
            print(f"Error saving Milk Center: {e}")
            # Handle the error more gracefully, e.g., displaying an error message to the user
    return render(request, 'manager/add_center.html')

def add_customer(request):
    if request.method == 'POST':
        # Assuming you have already authenticated the user
        branch=request.user.branch
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        opening_balance = 0


        try:
            # Create and save a new Customer instance
            customer = Employee(name=name, phone_number=phone, address=address,opening_balance=opening_balance, branch=branch)
            customer.save()
            print("Customer saved successfully")
            return redirect('/manager_dashbord/')  # Redirect to the manager dashboard or the appropriate URL
        except Exception as e:
            print(f"Error saving customer: {e}")
            # You may want to handle the error more gracefully, e.g., displaying an error message to the user
    return render(request, 'manager/add_customer.html')



def raw_purchase(request):
    from datetime import date
    today = date.today()
    branch=request.user.branch
    centers = Employee.objects.filter(branch=branch,Employee_type='supplier')
    purchase=MilkPurchase.objects.filter(purchase_date=today,branch=branch)

    if request.method == 'POST':
        if 'submit1' in request.POST:
            center_name = request.POST.get('milk_center', '')
            print(center_name)
            date = request.POST.get('date', '')
            print(date)
            volume = request.POST.get('volume', '')
            price = request.POST.get('price', '')
            total_price = request.POST.get('total_price', '')

            # Basic validation, you should add more robust validation
            if center_name and date and volume and price and total_price:
                # Get the MilkCenter instance
                try:
                    milk_center = Employee.objects.get(name=center_name)

                except MilkCenter.DoesNotExist:
                    milk_center = None

                if milk_center:
                    # Create a MilkPurchase instance and save it
                    MilkPurchase(
                        milk_center=milk_center,
                        purchase_date=date,
                        volume=volume,
                        price_per_liter=price,
                        LR=0,
                        Fat=0,
                        SNF=0,
                        price_on_TS=0,
                        total_price=total_price,
                        branch=branch
                    ).save()
                    milk_center.closing_balance+=Decimal(total_price)
                    milk_center.save()

                    print("Saved")
                    # stor, created = Stor.objects.get_or_create(id=1)

                    # if created:
                    #     stor.milk_storage = Decimal('0.0')  # Set an initial value for 'milk_storage'
                    # volume_decimal = Decimal(volume)
                    # X = stor.milk_storage
                    # print(X)
                    # X += volume_decimal
                    # print(X)
                    # stor.milk_storage = X
                    # stor.save()
                    purchase=MilkPurchase.objects.filter(purchase_date=today,branch=branch)
                    return redirect('/raw_purchase/')
                    # Redirect to a success page or do something else
                    # return redirect('success_page')  # Replace 'success_page' with your actual success page URL
                else:
                    # Handle the case where the MilkCenter with the given name doesn't exist
                    error_message = "Milk Center not found."
                    print("Milk Center not found.")
            else:
                # Handle the case where some fields are missing
                error_message = "Please fill in all fields."
                print("Please fill in all fields")

        elif 'submit2' in request.POST:
            date1 = request.POST.get('date', '')
            purchase=MilkPurchase.objects.filter(purchase_date=date1,branch=branch)
            print("thats is submit 2")
            return render(request, 'manager/raw_purchase.html', {'milk_center': centers,'purchase':purchase,"select_date":date1})

    # If it's not a POST request or there was an error, render the form page
    return render(request, 'manager/raw_purchase.html', {'milk_center': centers,'purchase':purchase,"select_date":today})

def purchase_milk(request):


    from datetime import date
    today = date.today()
    branch=request.user.branch
    centers = Employee.objects.filter(branch=branch,Employee_type='supplier')
    purchase=MilkPurchase.objects.filter(purchase_date=today,branch=branch)

    if request.method == 'POST':
        if 'submit1' in request.POST:
            center_name = request.POST.get('milk_center', '')
            date = request.POST.get('date', '')
            print(date)
            volume = request.POST.get('volume', '')
            price = request.POST.get('price', '')
            lr = request.POST.get('LR', '')  # Corrected variable name
            fat = request.POST.get('Fat', '')  # Corrected variable name
            snf = request.POST.get('SNF', '') # Corrected variable name
            ts = request.POST.get('TS', '')  # Corrected variable name
            TsVolume = request.POST.get('TsVolume', '')
            total_price = request.POST.get('total_price', '')

            # Basic validation, you should add more robust validation
            if center_name and date and volume and price and lr and fat and snf and ts and total_price:
                # Get the MilkCenter instance
                try:
                    milk_center = Employee.objects.get(name=center_name)

                except MilkCenter.DoesNotExist:
                    milk_center = None

                if milk_center:
                    # Create a MilkPurchase instance and save it
                    MilkPurchase(
                        milk_center=milk_center,
                        purchase_date=date,
                        volume=volume,
                        price_per_liter=price,
                        LR=lr,
                        Fat=fat,
                        SNF=snf,
                        price_on_TS=TsVolume,
                        total_price=total_price,
                        branch=branch
                    ).save()
                    milk_center.closing_balance+=Decimal(total_price)
                    milk_center.save()

                    print("Saved")
                    # stor, created = Stor.objects.get_or_create(id=1)

                    # if created:
                    #     stor.milk_storage = Decimal('0.0')  # Set an initial value for 'milk_storage'
                    # volume_decimal = Decimal(volume)
                    # X = stor.milk_storage
                    # print(X)
                    # X += volume_decimal
                    # print(X)
                    # stor.milk_storage = X
                    # stor.save()
                    purchase=MilkPurchase.objects.filter(purchase_date=today,branch=branch)
                    return redirect('/purchase_milk/')
                    # Redirect to a success page or do something else
                    # return redirect('success_page')  # Replace 'success_page' with your actual success page URL
                else:
                    # Handle the case where the MilkCenter with the given name doesn't exist
                    error_message = "Milk Center not found."
                    print("Milk Center not found.")
            else:
                # Handle the case where some fields are missing
                error_message = "Please fill in all fields."
                print("Please fill in all fields")

        elif 'submit2' in request.POST:
            date1 = request.POST.get('date', '')
            purchase=MilkPurchase.objects.filter(purchase_date=date1,branch=branch)
            print("thats is submit 2")
            return render(request, 'manager/purchase.html', {'milk_center': centers,'purchase':purchase,"select_date":date1})

    # If it's not a POST request or there was an error, render the form page
    return render(request, 'manager/purchase.html', {'milk_center': centers,'purchase':purchase,"select_date":today})


def purchase_invice(request,pid):
    invice=MilkPurchase.objects.get(id=pid)
    template_path = 'pdf.html'
    context = {'invice':invice}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # for downlord 
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # foe view 
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



def raw_sale(request):
    
    from datetime import date
    today = date.today()
    branch=request.user.branch
    customers = Employee.objects.filter(branch=branch,Employee_type='customer')
    sales=MilkSale.objects.filter(purchase_date=today,branch=branch)


    if request.method == 'POST':
        if 'submit1' in request.POST:
            customer = request.POST.get('customer_name', '')
            date2 = request.POST.get('date', '')
            volume = request.POST.get('volume', '')
            price = request.POST.get('price', '')
            # lr = request.POST.get('LR', '')  # Corrected variable name
            # fat = request.POST.get('Fat', '')  # Corrected variable name
            # snf = request.POST.get('SNF', '') # Corrected variable name
            # ts = request.POST.get('TS', '')  # Corrected variable name
            total_price = request.POST.get('total_price', '')
            print(customer,date2,date2,price,total_price)

            # Basic validation, you should add more robust validation
            if customer and date2 and volume and price and total_price:
                # Get the MilkCenter instance
                try:
                    milk_center = Employee.objects.get(name=customer)
                except Customer.DoesNotExist:
                    milk_center = None

                if milk_center:
                    # Create a MilkPurchase instance and save it
                    MilkSale(
                        customer=milk_center,
                        purchase_date=date2,
                        volume=volume,
                        price_per_liter=price,
                        LR=0,
                        Fat=0,
                        SNF=0,
                        price_on_TS=0,
                        total_price=total_price,branch=branch
                    ).save()
                    print("Saved")
                    milk_center.closing_balance+=Decimal(total_price)
                    milk_center.save()

                    sales=MilkSale.objects.filter(purchase_date=today,branch=branch)
                    return redirect('/raw_sale/')
                    # Redirect to a success page or do something else
                    # return redirect('success_page')  # Replace 'success_page' with your actual success page URL
                else:
                    # Handle the case where the MilkCenter with the given name doesn't exist
                    error_message = "Milk Center not found."
                    print("Milk Center not found.")
            else:
                # Handle the case where some fields are missing
                error_message = "Please fill in all fields."
                print("Please fill in all fields")

        
        elif 'submit2' in request.POST:
            date1 = request.POST.get('date', '')
            sales=MilkSale.objects.filter(purchase_date=date1,branch=branch)
            print("thats is submit 2")
            return render(request, 'manager/raw_sale.html', {'customers': customers, 'sales': sales,"select_date":date1})

    # If it's not a POST request or there was an error, render the form page
    return render(request, 'manager/raw_sale.html', {'customers': customers, 'sales': sales,"select_date":today})



def sale_milk (request):
    from datetime import date
    today = date.today()
    branch=request.user.branch
    customers = Employee.objects.filter(branch=branch,Employee_type='customer')
    sales=MilkSale.objects.filter(purchase_date=today,branch=branch)


    if request.method == 'POST':
        if 'submit1' in request.POST:
            customer = request.POST.get('customer_name', '')
            date2 = request.POST.get('date', '')
            volume = request.POST.get('volume', '')
            price = request.POST.get('price', '')
            lr = request.POST.get('LR', '')  # Corrected variable name
            fat = request.POST.get('Fat', '')  # Corrected variable name
            snf = request.POST.get('SNF', '') # Corrected variable name
            ts = request.POST.get('TS', '')  # Corrected variable name
            total_price = request.POST.get('total_price', '')
            print(customer,date2,date2,price,lr,fat,snf,ts,total_price)

            # Basic validation, you should add more robust validation
            if customer and date2 and volume and price and lr and fat and snf and ts and total_price:
                # Get the MilkCenter instance
                try:
                    milk_center = Employee.objects.get(name=customer)
                except Customer.DoesNotExist:
                    milk_center = None

                if milk_center:
                    # Create a MilkPurchase instance and save it
                    MilkSale(
                        customer=milk_center,
                        purchase_date=date2,
                        volume=volume,
                        price_per_liter=price,
                        LR=lr,
                        Fat=fat,
                        SNF=snf,
                        price_on_TS=ts,
                        total_price=total_price,branch=branch
                    ).save()
                    print("Saved")
                    milk_center.closing_balance+=Decimal(total_price)
                    milk_center.save()
                    # stor, created = Stor.objects.get_or_create(id=1)

                    # if created:
                    #     stor.milk_storage = Decimal('0.0')  # Set an initial value for 'milk_storage'
                    # volume_decimal = Decimal(volume)
                    # X = stor.milk_storage
                    # print(X)
                    # X -= volume_decimal
                    # print(X)
                    # stor.milk_storage = X
                    # stor.save()
                    sales=MilkSale.objects.filter(purchase_date=today,branch=branch)
                    return redirect('/sale_milk/')
                    # Redirect to a success page or do something else
                    # return redirect('success_page')  # Replace 'success_page' with your actual success page URL
                else:
                    # Handle the case where the MilkCenter with the given name doesn't exist
                    error_message = "Milk Center not found."
                    print("Milk Center not found.")
            else:
                # Handle the case where some fields are missing
                error_message = "Please fill in all fields."
                print("Please fill in all fields")

        
        elif 'submit2' in request.POST:
            date1 = request.POST.get('date', '')
            sales=MilkSale.objects.filter(purchase_date=date1,branch=branch)
            print("thats is submit 2")
            return render(request, 'manager/sale_milk.html', {'customers': customers, 'sales': sales,"select_date":date1})

    # If it's not a POST request or there was an error, render the form page
    return render(request, 'manager/sale_milk.html', {'customers': customers, 'sales': sales,"select_date":today})

def sale_invoice(request,pid):
    invice=MilkSale.objects.get(id=pid)
    template_path = 'manager/sale_pdf.html'
    context = {'invice':invice}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # for downlord 
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # foe view 
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def make_payment_invoice(request,pid):
    invoice=MakePayment.objects.get(id=pid)
    template_path = 'manager/make_payment_invoice.html'
    context = {'invoice':invoice}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # for downlord 
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # foe view 
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response





def make_payment (request):
    from datetime import date
    today = date.today()
    branch=request.user.branch
    from django.db.models import Q

    centers = Employee.objects.filter(Q(branch=branch, Employee_type='supplier') | Q(branch=branch, Employee_type='employee'))
    
    payment_info=MakePayment.objects.filter(branch=branch,payment_date=today)
    # print("akaka",payment_info)
    if request.method == 'POST':
        if 'submit1' in request.POST:

            center_name = request.POST.get('center_name', '')
            amount = request.POST.get('amount', '')
            payment_date = request.POST.get('date', '')
            payment_method = 'Cash or ATM'
            notes= request.POST.get('node', '')
            print(center_name,amount,payment_date,payment_method,notes)

            if center_name and amount and payment_date and payment_method and notes:
                # Get the MilkCenter instance
                try:
                    milk_center = Employee.objects.get(name=center_name)
                except MilkCenter.DoesNotExist:
                    milk_center = None

                if milk_center:
                    # Create a MilkPurchase instance and save it
                    milk_center.closing_balance-=Decimal(amount)
                    milk_center.save()
                    balance=milk_center.closing_balance
                    MakePayment(milk_center=milk_center,amount=amount,payment_date=payment_date,payment_method=payment_method,notes=notes,balance=balance,branch=branch).save()

                    
                    print("Saved")
                    # purchase=MilkPurchase.objects.filter(purchase_date=today)
                    return redirect('/make_payment/')
                    # Redirect to a success page or do something else
                    # return redirect('success_page')  # Replace 'success_page' with your actual success page URL
                else:
                    # Handle the case where the MilkCenter with the given name doesn't exist
                    error_message = "Milk Center not found."
                    print("Milk Center not found.")
            else:
                # Handle the case where some fields are missing
                error_message = "Please fill in all fields."
                print("Please fill in all fields")
            
        elif 'submit2' in request.POST:
            date1 = request.POST.get('date', '')
            print(date1)
            payment_info=MakePayment.objects.filter(branch=branch,payment_date=date1)
            return render(request, 'manager/Make_payment.html',{'center_name':centers,"payment_info":payment_info})


    return render(request, 'manager/Make_payment.html',{'center_name':centers,"payment_info":payment_info})



def receive_payment_invoice(request,pid):
    invoice=ReceivedPayment.objects.get(id=pid)
    template_path = 'manager/receive_payment_invoice.html'
    context = {'invoice':invoice}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # for downlord 
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # foe view 
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response










def recive_payment (request):
    from datetime import date
    today = date.today()
    branch=request.user.branch
    customers=Employee.objects.filter(branch=branch,Employee_type='customer')
    payment_info=ReceivedPayment.objects.filter(branch=branch,payment_date=today)



    if request.method == 'POST':
        if 'submit1' in request.POST:
            customer = request.POST.get('customer_name', '')
            amount_received = request.POST.get('amount', '')
            payment_date = request.POST.get('date', '')
            payment_method = 'Cash or ATM'
            notes= request.POST.get('node', '')
            print(customer,amount_received,payment_date,payment_method,notes)

            if customer and amount_received and payment_date and payment_method and notes:
                # Get the MilkCenter instance
                try:
                    milk_center = Employee.objects.get(name=customer)
                except Customer.DoesNotExist:
                    milk_center = None

                if milk_center:
                    # Create a MilkPurchase instance and save it
                    milk_center.closing_balance-=Decimal(amount_received)
                    milk_center.save()
                    balance=milk_center.closing_balance
                    ReceivedPayment(customer=milk_center,amount_received=amount_received,payment_date=payment_date,payment_method=payment_method,notes=notes,balance=balance,branch=branch).save()
                    print("Saved")
                    # purchase=MilkPurchase.objects.filter(purchase_date=today)
                    return redirect('/recive_payment/')
                    # Redirect to a success page or do something else
                    # return redirect('success_page')  # Replace 'success_page' with your actual success page URL
                else:
                    # Handle the case where the MilkCenter with the given name doesn't exist
                    error_message = "Milk Center not found."
                    print("Milk Center not found.")
            else:
                # Handle the case where some fields are missing
                error_message = "Please fill in all fields."
                print("Please fill in all fields")

        elif 'submit2' in request.POST:
            date1 = request.POST.get('date', '')
            print(date1)
            payment_info=ReceivedPayment.objects.filter(branch=branch,payment_date=date1)

            return render(request, 'manager/recive_payment.html',{"customers":customers,"payment_info":payment_info})

    # Your view logic here
    return render(request, 'manager/recive_payment.html',{"customers":customers,"payment_info":payment_info})

def manager_dashbord (request):
    from datetime import date
    today = date.today()
    from datetime import datetime
    branch=request.user.branch
    customers=Employee.objects.filter(branch=branch,Employee_type='customer').count()
    centers=Employee.objects.filter(branch=branch,Employee_type='supplier').count()
    employee=Employee.objects.filter(branch=branch,Employee_type='employee').count()
    total_volume = MilkPurchase.objects.filter(purchase_date=today,branch=branch).aggregate(Sum('volume'))['volume__sum'] or 0
    total_price = MilkPurchase.objects.filter(purchase_date=today,branch=branch).aggregate(Sum('total_price'))['total_price__sum'] or 0
    sale_volume= MilkSale.objects.filter(purchase_date=today,branch=branch).aggregate(Sum('volume'))['volume__sum'] or 0
    sale_price=MilkSale.objects.filter(purchase_date=today,branch=branch).aggregate(Sum('total_price'))['total_price__sum'] or 0
    # storage=Stor.objects.get(id=1)

    T_p = MilkPurchase.objects.filter(branch=branch).aggregate(Sum('volume'))['volume__sum'] or 0
    T_s= MilkSale.objects.filter(branch=branch).aggregate(Sum('volume'))['volume__sum'] or 0
    total=T_p-T_s

    if request.method == 'POST':
        selected_date=request.POST.get('date', '')
        # Parse the selected_date string to a datetime object
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d')
        today=selected_date
        # Query the database to get the total volume and total price for the selected date
        total_volume = MilkPurchase.objects.filter(purchase_date=selected_date,branch=branch).aggregate(Sum('volume'))['volume__sum'] or 0
        total_price = MilkPurchase.objects.filter(purchase_date=selected_date,branch=branch).aggregate(Sum('total_price'))['total_price__sum'] or 0
        sale_volume= MilkSale.objects.filter(purchase_date=selected_date,branch=branch).aggregate(Sum('volume'))['volume__sum'] or 0
        sale_price=MilkSale.objects.filter(purchase_date=selected_date,branch=branch).aggregate(Sum('total_price'))['total_price__sum'] or 0
        T_p = MilkPurchase.objects.filter(branch=branch).aggregate(Sum('volume'))['volume__sum'] or 0
        T_s= MilkSale.objects.filter(branch=branch).aggregate(Sum('volume'))['volume__sum'] or 0
        total=T_p-T_s


    # Your view logic here
    context={
        'today':today,
        "sale_price":sale_price,
        "sale_volume":sale_volume,
        'customers':customers,
        "centers":centers,
        'storage':total,
        'total_volume': total_volume,
            'total_price': total_price,
            'employee':employee

    }
    return render(request, 'manager/manager_content.html',context)

def customer_details (request):
    branch=request.user.branch
    customers=Employee.objects.filter(branch=branch,Employee_type='customer')
    
    # Your view logic here
    return render(request, 'manager/customer_details.html',{'customers':customers})

def center_details (request):
    branch=request.user.branch
    
    centers=Employee.objects.filter(branch=branch,Employee_type='supplier')
    # Your view logic here
    return render(request, 'manager/center_details.html',{'centers':centers})

def center_invoice(request,pid):
    selecting_date = request.session.get('Purchase_SD', None)
    ending_date = request.session.get('Purchase_ED', None)

    if request.method == 'POST':
        if 'submit2' in request.POST:
            selecting_date = request.POST.get('from')
            ending_date = request.POST.get('to')
            print(selecting_date, ending_date)

    branch = request.user.branch
    customer = get_object_or_404(Employee, id=pid)

    if selecting_date is not None and ending_date is not None:
        milk_purchases = MilkPurchase.objects.filter(milk_center__id=pid, purchase_date__range=[selecting_date, ending_date])
        payments = MakePayment.objects.filter(milk_center__id=pid, payment_date__range=[selecting_date, ending_date])
        expences = CustomerExpence.objects.filter(customer__id=pid,date__range=[selecting_date, ending_date])
        
    else:
        milk_purchases = MilkPurchase.objects.filter(milk_center__id=pid)
        payments = MakePayment.objects.filter(milk_center__id=pid)
        expences = CustomerExpence.objects.filter(customer__id=pid)

    milk_purchases = milk_purchases.annotate(source=models.Value('MilkPurchase', output_field=models.CharField()))
    payments = payments.annotate(source=models.Value('MakePayment', output_field=models.CharField()))
    expences = expences.annotate(source=models.Value('Expences', output_field=models.CharField()))
    combined_data = list(milk_purchases) + list(payments)+ list(expences)
    # combined_data.sort(key=lambda x: x.purchase_date if x.source == 'MilkPurchase' else x.payment_date)

    opening_balance = customer.opening_balance  # Get the opening balance from the employee model

    balance = opening_balance  # Initialize balance with the opening balance

    for entry in combined_data:
        if entry.source == 'MilkPurchase':
            balance += entry.total_price
        elif entry.source == 'Expences':
            balance -= entry.expense_amount
        else:
            balance -= entry.amount

        entry.balance = balance

    context = {
        'pid':pid,
        'opening_balance':opening_balance,
        'combined_data': combined_data,
        'customer': customer,
           "selecting_date":selecting_date, 
           "ending_date":ending_date # Pass the customer object to the template
    }
    template_path = 'manager/center_pdf.html'
    # context =request.session.get('context')
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # for downlord 
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # foe view 
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def view_center(request, pid):
    selecting_date = None
    ending_date = None

    if request.method == 'POST':
        if 'submit2' in request.POST:
            selecting_date = request.POST.get('from')
            ending_date = request.POST.get('to')
            print(selecting_date, ending_date)

    branch = request.user.branch
    customer = get_object_or_404(Employee, id=pid)

    if selecting_date is not None and ending_date is not None:
        milk_purchases = MilkPurchase.objects.filter(milk_center__id=pid, purchase_date__range=[selecting_date, ending_date])
        payments = MakePayment.objects.filter(milk_center__id=pid, payment_date__range=[selecting_date, ending_date])
        expences = CustomerExpence.objects.filter(customer__id=pid,date__range=[selecting_date, ending_date])
        
    else:
        milk_purchases = MilkPurchase.objects.filter(milk_center__id=pid)
        payments = MakePayment.objects.filter(milk_center__id=pid)
        expences = CustomerExpence.objects.filter(customer__id=pid)

    milk_purchases = milk_purchases.annotate(source=models.Value('MilkPurchase', output_field=models.CharField()))
    payments = payments.annotate(source=models.Value('MakePayment', output_field=models.CharField()))
    expences = expences.annotate(source=models.Value('Expences', output_field=models.CharField()))
    combined_data = list(milk_purchases) + list(payments)+ list(expences)
    # combined_data.sort(key=lambda x: x.purchase_date if x.source == 'MilkPurchase' else x.payment_date)

    opening_balance = customer.opening_balance  # Get the opening balance from the employee model

    balance = opening_balance  # Initialize balance with the opening balance

    for entry in combined_data:
        if entry.source == 'MilkPurchase':
            balance += entry.total_price
        elif entry.source == 'Expences':
            balance -= entry.expense_amount
        else:
            balance -= entry.amount

        entry.balance = balance

    context = {
        'pid': pid,
        'combined_data': combined_data,
        'customer': customer,
        'opening_balance': opening_balance,
    }

    request.session['Purchase_SD'] = selecting_date
    request.session['Purchase_ED'] = ending_date

    return render(request, 'manager/view_center.html', context)


def customer_invoice(request,pid):
    starting_date = request.session.get('Sale_SD', None)
    ending_date = request.session.get('Sale_ED', None)

    if request.method == 'POST':
        if 'submit2' in request.POST:
            starting_date = request.POST.get('from')
            ending_date = request.POST.get('to')
            print(starting_date,ending_date)
    
    customer = get_object_or_404(Employee, id=pid)
    # Use the date range filter if dates are provided, otherwise, retrieve all data
    if starting_date is not None and ending_date is not None:
        milk_sale = MilkSale.objects.filter(customer__id=pid,purchase_date__range=[starting_date, ending_date])
        payments = ReceivedPayment.objects.filter(customer__id=pid,payment_date__range=[starting_date, ending_date])
        expences = CustomerExpence.objects.filter(customer__id=pid,date__range=[starting_date, ending_date])
    else:
        milk_sale = MilkSale.objects.filter(customer__id=pid)
        payments = ReceivedPayment.objects.filter(customer__id=pid)
        expences = CustomerExpence.objects.filter(customer__id=pid)
    # Add a field to each query to identify the source (MilkPurchase or MakePayment)
    milk_sale = milk_sale.annotate(source=models.Value('MilkPurchase', output_field=models.CharField()))
    expences = expences.annotate(source=models.Value('Expences', output_field=models.CharField()))
    payments = payments.annotate(source=models.Value('MakePayment', output_field=models.CharField()))

    # Combine and order the two querysets by datetime
    combined_data = list(milk_sale)+ list(expences) + list(payments)
    # combined_data.sort(key=lambda x: x.purchase_date if x.source == 'MilkPurchase' else x.payment_date)
    def get_record_date(record):
        if record.source == 'MilkPurchase':
            return record.purchase_date
        elif record.source == 'MakePayment':
            return record.payment_date
        elif record.source == 'Expences':
            return record.date  # Assuming there is an 'expense_date' field in the Expenses model

# Sort the combined_data list based on the date using the get_record_date function
    combined_data.sort(key=get_record_date)

    opening_balance = customer.opening_balance  # Get the opening balance from the employee model

    balance = opening_balance  # Initialize balance with the opening balance
    for entry in combined_data:
        if entry.source == 'MilkPurchase':
            balance += entry.total_price
        elif entry.source=='Expences':
            balance+=entry.expence_amount
        else:
            balance -= entry.amount_received

        # Add a 'balance' attribute to each entry
        entry.balance = balance

    context = {
        'pid':pid,
        'opening_balance':opening_balance,
        'combined_data': combined_data,
        'customer': customer,  # Pass the customer object to the template
        "selecting_date":starting_date, 
        "ending_date":ending_date
    }
    template_path = 'manager/customer_pdf.html'
    # context =request.session.get('context')
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # for downlord 
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # foe view 
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



def view_customer(request, pid):

    starting_date=None
    ending_date=None

    if request.method == 'POST':
        if 'submit2' in request.POST:
            starting_date = request.POST.get('from')
            ending_date = request.POST.get('to')
            print(starting_date,ending_date)
    
    customer = get_object_or_404(Employee, id=pid)
    # Use the date range filter if dates are provided, otherwise, retrieve all data
    if starting_date is not None and ending_date is not None:
        milk_sale = MilkSale.objects.filter(customer__id=pid,purchase_date__range=[starting_date, ending_date])
        payments = ReceivedPayment.objects.filter(customer__id=pid,payment_date__range=[starting_date, ending_date])
        expences = CustomerExpence.objects.filter(customer__id=pid,date__range=[starting_date, ending_date])
    else:
        milk_sale = MilkSale.objects.filter(customer__id=pid)
        payments = ReceivedPayment.objects.filter(customer__id=pid)
        expences = CustomerExpence.objects.filter(customer__id=pid)
    # Add a field to each query to identify the source (MilkPurchase or MakePayment)
    milk_sale = milk_sale.annotate(source=models.Value('MilkPurchase', output_field=models.CharField()))
    expences = expences.annotate(source=models.Value('Expences', output_field=models.CharField()))
    payments = payments.annotate(source=models.Value('MakePayment', output_field=models.CharField()))

    # Combine and order the two querysets by datetime
    combined_data = list(milk_sale)+ list(expences) + list(payments)
    # combined_data.sort(key=lambda x: x.purchase_date if x.source == 'MilkPurchase' else x.payment_date)
    def get_record_date(record):
        if record.source == 'MilkPurchase':
            return record.purchase_date
        elif record.source == 'MakePayment':
            return record.payment_date
        elif record.source == 'Expences':
            return record.date  # Assuming there is an 'expense_date' field in the Expenses model

# Sort the combined_data list based on the date using the get_record_date function
    combined_data.sort(key=get_record_date)

    opening_balance = customer.opening_balance  # Get the opening balance from the employee model

    balance = opening_balance  # Initialize balance with the opening balance
    for entry in combined_data:
        if entry.source == 'MilkPurchase':
            balance += entry.total_price
        elif entry.source=='Expences':
            balance+=entry.expence_amount
        else:
            balance -= entry.amount_received

        # Add a 'balance' attribute to each entry
        entry.balance = balance

    context = {
        'pid':pid,
        'opening_balance':opening_balance,
        'combined_data': combined_data,
        'customer': customer,  # Pass the customer object to the template
        
    }
    request.session['Sale_SD'] = starting_date
    request.session['Sale_ED'] = ending_date

    return render(request, 'manager/view_customers.html', context)


def register_customer_ex (request):
    branch=request.user.branch
    if request.method=='POST':
        expence_name=request.POST.get('expence_name', '')
        branch=request.user.branch
        Expence(expense_name=expence_name,branch=branch).save()
        print("expence saved")

    # Your view logic here
    return render(request, 'manager/register_customer_ex.html')


def add_customer_ex (request):
    branch=request.user.branch
    expences=Expence.objects.filter(branch=branch)
    customers=Employee.objects.filter(branch=branch,Employee_type='customer')
   
    print(customers)

    if request.method=='POST':
        date=request.POST.get('date', '')
        customer_name=request.POST.get('customer_name', '')
        expence_type=request.POST.get('expence_type', '')
        expence_amount=request.POST.get('expence_amount', '')


        name = Customer.objects.get(name=customer_name)
        CustomerExpence(customer=name,date=date,expense_type=expence_type,expense_amount=expence_amount,branch=branch).save()
        print("expence saved")

    context={
        'expences':expences,
        'customers':customers
    }
    # Your view logic here
    return render(request, 'manager/add_customer_ex.html',context)


def add_center_ex(request):
    branch=request.user.branch
    expences=Expence.objects.filter(branch=branch)
    customers=Employee.objects.filter(branch=branch,Employee_type='supplier')
   
    print(customers)

    if request.method=='POST':
        date=request.POST.get('date', '')
        customer_name=request.POST.get('customer_name', '')
        expence_type=request.POST.get('expence_type', '')
        expence_amount=request.POST.get('expence_amount', '')


        name = Employee.objects.get(name=customer_name,Employee_type='supplier')
        CustomerExpence(customer=name,date=date,expense_type=expence_type,expense_amount=expence_amount,branch=branch).save()
        print("expence saved")

    context={
        'expences':expences,
        'customers':customers
    }
    # Your view logic here
    return render(request, 'manager/add_customer_ex.html',context)


from decimal import Decimal  # Import Decimal

from django.db.models import Sum
from datetime import date, datetime


def PNL(request):
    # Get the current date
    today = date.today()
    
    branch=request.user.branch

    # Initialize selected_date to None
    selected_date = None

    # Process form input if the request method is POST
    if request.method == 'POST':
        selected_date_str = request.POST.get('date', '')
        try:
            # Parse the selected_date string to a datetime object
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d')
        except ValueError:
            # Handle invalid date format gracefully
            selected_date = None

    # If selected_date is still None, default it to today
    if selected_date is None:
        selected_date = today

    # Query the database to get total volume and total price for purchases and sales
    total_volume_purchase = MilkPurchase.objects.filter(purchase_date=selected_date,branch=branch).aggregate(Sum('volume'))['volume__sum'] or 0
    t_v = MilkPurchase.objects.filter(branch=branch).aggregate(Sum('volume'))['volume__sum'] or 0

    # Convert total_price_purchase to a Decimal if it's a string
    total_price_purchase = Decimal(MilkPurchase.objects.filter(purchase_date=selected_date,branch=branch).aggregate(Sum('total_price'))['total_price__sum'] or 0)
    formatted_total_price_purchase = "{:.2f}".format(total_price_purchase)

    total_volume_sale = MilkSale.objects.filter(purchase_date=selected_date,branch=branch).aggregate(Sum('volume'))['volume__sum'] or 0
    t_s= MilkSale.objects.filter(branch=branch).aggregate(Sum('volume'))['volume__sum'] or 0

    # Convert total_price_sale to a Decimal if it's a string
    total_price_sale = Decimal(MilkSale.objects.filter(purchase_date=selected_date,branch=branch).aggregate(Sum('total_price'))['total_price__sum'] or 0)
    formatted_total_price_sale = "{:.2f}".format(total_price_sale)
    # Calculate remaining milk, average price, estimated price, and other metrics
     # Calculate the total customer expenses for the selected date and branch
    total_customer_expenses = CustomerExpence.objects.filter(
        date=selected_date, branch=branch
    ).aggregate(Sum('expense_amount'))['expense_amount__sum'] or Decimal('0')

    # Calculate the profit including customer expenses
    # profit = total_sale_price - total_purchase_price - total_expense - total_customer_expenses

    remaining_milk = t_v - t_s
    average_price = round(total_price_purchase / total_volume_purchase if total_volume_purchase != 0 else Decimal('0'),3)
    # average_price = "{:.2f}".format(average_price)
    estimated_price = round(remaining_milk * average_price,3)
    total_purchase_price = total_price_purchase
    total_purchase_price = round(total_purchase_price, 2)
    total_expense = total_customer_expenses  # Adjust this if you have expenses to consider
    total_sale_price = round(total_price_sale + estimated_price,3)
    profit = total_sale_price - total_purchase_price - total_expense
    profit = round(profit, 2)

    # Prepare the context dictionary
    context = {
        'today': today,
        'selected_date': selected_date,
        'remaining_milk': remaining_milk,
        'average_price': average_price,
        'estimated_price': estimated_price,
        'total_purchase_price': total_purchase_price,
        'total_expense': total_expense,
        'total_sale_price': total_sale_price,
        'profit': profit,
        'total_volume_purchase': total_volume_purchase,
        'total_price_purchase': formatted_total_price_purchase,
        'total_volume_sale': total_volume_sale,
        'total_price_sale': formatted_total_price_sale,
    }

    # Render the HTML template and return it as an HTTP response
    return render(request, 'manager/PNL.html', context)




from datetime import datetime
from decimal import Decimal


def BetweenPNL(request):
    # Initialize default values for variables
    branch=request.user.branch
    total_volume_purchase = 0
    total_price_purchase = 0
    total_volume_sale = 0
    total_price_sale = 0
    total_customer_expenses=0

    # Set a default value for total_price_sale
    total_price_sale = 0

    # Process form input if the request method is POST
    if request.method == 'POST':
        selecting_date = request.POST.get('selecting_date', '')
        ending_date = request.POST.get('ending_date', '')
        print(selecting_date)
        print("111")


        # Parse the selected_date and ending_date strings to datetime objects
        selecting_date = datetime.strptime(selecting_date, '%Y-%m-%d')
        ending_date = datetime.strptime(ending_date, '%Y-%m-%d')

        # Query the database to get total volume and total price for purchases and sales
        purchase_query = MilkPurchase.objects.filter(purchase_date__range=[selecting_date, ending_date],branch=branch)
        sale_query = MilkSale.objects.filter(purchase_date__range=[selecting_date, ending_date],branch=branch)

        total_volume_purchase = purchase_query.aggregate(Sum('volume'))['volume__sum'] or 0
        print(total_volume_purchase)
        total_volume_sale = sale_query.aggregate(Sum('volume'))['volume__sum'] or 0
        print(total_volume_sale)
        # Convert total_price_purchase and total_price_sale to Decimals if they're strings
        total_price_purchase = Decimal(purchase_query.aggregate(Sum('total_price'))['total_price__sum'] or 0)
        total_price_sale = Decimal(sale_query.aggregate(Sum('total_price'))['total_price__sum'] or 0)

        # total_price_purchase = "{:.2f}".format(total_price_purchase)
        # total_price_sale = "{:.2f}".format(total_price_sale)
        print("total_price_purchase")
        total_customer_expenses = CustomerExpence.objects.filter(date__range=[selecting_date, ending_date], branch=branch).aggregate(Sum('expense_amount'))['expense_amount__sum'] or Decimal('0')


    # Calculate remaining milk, average price, estimated price, and other metrics
    remaining_milk = total_volume_purchase - total_volume_sale
    average_price =round( total_price_purchase / total_volume_purchase if total_volume_purchase != 0 else Decimal('0'),3)
    estimated_price =round( remaining_milk * average_price,3)
    total_purchase_price = total_price_purchase
    total_expense = total_customer_expenses  # Adjust this if you have expenses to consider
    total_sale_price = round(total_price_sale + estimated_price,3)
    profit = round(total_sale_price - total_purchase_price - total_expense, 2)

    # Prepare the context dictionary
    context = {
        'remaining_milk': remaining_milk,
        'average_price': average_price,
        'estimated_price': estimated_price,
        'total_purchase_price': total_purchase_price,
        'total_expense': total_expense,
        'total_sale_price': total_sale_price,
        'profit': profit,
        'total_volume_purchase': total_volume_purchase,
        'total_price_purchase': total_price_purchase,
        'total_volume_sale': total_volume_sale,
        'total_price_sale': total_price_sale,
    }

    # Render the HTML template and return it as an HTTP response
    return render(request, 'manager/BetweenPNL.html', context)

