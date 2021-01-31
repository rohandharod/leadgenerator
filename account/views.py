from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import auth
from .models import CustomUser
from django.contrib import messages
from django.conf import settings 
from django.core.mail import send_mail 
from django.core.mail import EmailMessage
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import token_generator
from django.contrib.auth.base_user import BaseUserManager
from .models import Leads
from django.db.models import Case, When
from django.http import FileResponse, Http404
# def random_password(size=8):
#     return BaseUserManager().make_random_password(size)
from leadgenerator.settings import EMAIL_HOST_USER

def register(request):
    if request.method == 'POST':
        
        fname = request.POST['fname']
        Email = request.POST['email']
        phone = request.POST['phone']
        alt_phone = request.POST['alt_phone']
        designation = request.POST['designation']
        if(designation == "Other"):
            designation = request.POST['other']
        address = request.POST['address']
        role = "Referral Partner"
        mapped_to = "admin"
        mapped_to_nm = "admin"
        by_online = "yes"

        if CustomUser.objects.filter(email=Email).exists():
            messages.info(request, 'Email Taken')
            return redirect('register')
        else:
            
            user = CustomUser.objects.create_user(username=Email, password="", email=Email, first_name=fname, phone=phone, alt_phone=alt_phone, designation=designation, address=address, role = role, mapped_to = mapped_to, mapped_to_name = mapped_to_nm, by_online = by_online)
            user.is_active = False
            user.save()
            ini = ""
            if user.designation == "Salaried":
                ini += "SAL"
            elif user.designation == "Self Employed":
                ini += "SE"
            elif user.designation == "Freelancer":
                ini += "FL"
            elif user.designation == "Student":
                ini += "ST"
            elif user.designation == "Home Maker":
                ini += "HM"
            elif user.designation == "DSA":
                ini += "DSA"
            elif user.designation == "Insurance Agent":
                ini += "IA"
            elif user.designation == "Chartered Accountant":
                ini += "CA"
            elif user.designation == "Tax Consultants":
                ini += "TC"
            elif user.designation == "Banker":
                ini += "BNK"
            elif user.designation == "Company Secretary":
                ini += "CS"
            elif user.designation == "Real Estate Agent":
                ini += "REA"
            elif user.designation == "Builder":
                ini += "BLD"
            else:
                ini+="O"

            if user.role == "Referral Partner":
                ini += "RP"

            num = '{:04d}'.format(user.id)
            newusername = ini+num
            user.username = newusername
            user.save()


            # if user.role == "Referral Partner":
            #     ini = "ORP"
            #     num = '{:03d}'.format(user.id)
            #     newusername = ini+num
            #     user.username = newusername
            #     user.save()
            

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user)})
            activate_url = "http://"+domain+link
            email_body = 'Hi ' + user.first_name + ' Please use this link to verify your account\n'+ activate_url
            email = EmailMessage(
                'Activate your account',
                email_body,
                'rohan@gmail.com',
                [Email],
            )
            email.send(fail_silently=False)


            message="this is test mail"
            subject="terms and conditions"
            mail_id=request.POST.get('email','')
            # mail_id="daghariddhi12@gmail.com"
    
            email=EmailMessage(subject,message, EMAIL_HOST_USER, [mail_id,])
            email.content_subtype='html'

            # file2=open("abcd.txt","r")
            # file=open("manage.py","r")
            # email.attach("abcd.txt",file2.read(),'text/plain')
            # email.attach("manage.py",file.read(), 'text/plain')
            email.attach_file('terms.pdf')

            email.send()
            # return render(request, 'account/terms.html')
            
            
        #else:
            #messages.info(request, 'Password did not match')
            #return redirect('register')

            return redirect('email_ver_msg')


        #else:
            #messages.info(request, 'Password did not match')
            #return redirect('register')
    else:    
        return render(request, 'account/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('uname_pw_gen')
            user.is_active = True
            password = BaseUserManager().make_random_password(10)
            user.set_password(password)
            user.save()
            email_body = 'Hi ' + user.first_name+' \n Your username: '+ user.username+ '\n Your Password: '+password
            email = EmailMessage(
                'Account Activated',
                email_body,
                'rohan@gmail.com',
                [user.email],
            )
            email.send(fail_silently=False)
            

            messages.success(request, 'Account activated successfully')
            return redirect('uname_pw_gen')

        except Exception as ex:
            pass

        return redirect('uname_pw_gen')

def email_ver_msg(request):
    return render(request, 'account/email_ver_msg.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            
            auth.login(request, user)
            if user.role == "Admin":
                return redirect('dashboard')
            elif user.role == "Referral Partner":
                return redirect('base')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login')

    else:
        return render(request, 'account/login.html')

def logout(request):
    auth.logout(request)
    return redirect('home')

def forgot_uname(request):
    if request.method == 'POST':
        email = request.POST['email']
        if CustomUser.objects.filter(email=email).exists():
            p = CustomUser.objects.raw('SELECT * FROM account_customuser WHERE email = %s', [email])
            subject = 'Request for username'
            message = f'Hi Your Username is: {p[0].username}'
            email_from = settings.EMAIL_HOST_USER 
            recipient_list = [email, ] 
            send_mail( subject, message, email_from, recipient_list ) 
            return redirect('login')
        else:
            messages.info(request, 'Email not registered')
            return redirect('forgot_uname')
    else:
        return render(request, 'account/forgot_uname.html')

def uname_pw_gen(request):
    return render(request, 'account/uname_pw_gen.html')
    
    
def add_leads(request):
    if request.method == 'POST':
        name = request.POST['name']
        ref = request.POST['ref']
        #username = request.POST['username']
        email = request.POST['email']
        #password1 = request.POST['password1']
        #password2 = request.POST['password2']
        product = request.POST['pdt']
        loan_amt = request.POST['amt']
        address = request.POST['address']
        phone = request.POST['phone']
        alt_phone = request.POST['alt_phone']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        country = request.POST['country']
        added_by = request.user.id
        user = request.user

        lead = Leads(name = name, phone = phone, alt_phone = alt_phone, email = email, reference = ref, product = product, loan_amt = loan_amt, address = address, pincode = pincode, country = country, state = state, city= city, added_by = added_by )
        lead.save()

        if user.role == "Admin":
            # return render(request, 'account/dashboard.html')
            return redirect('dashboard')

        elif user.role == "Referral Partner":
            # return render(request, 'account/base.html')
            return redirect('base')
        # return render(request, "account/add_leads.html")
    return render(request, 'account/add_leads.html')
 

def create_mem(request):

    if request.method == 'POST':
        
        fname = request.POST['name']
        Email = request.POST['email']
        phone = request.POST['phone']
        alt_phone = request.POST['alt_phone']
        designation = request.POST['designation']
        address = request.POST['address']
        role = request.POST['role']
        mapped_to = request.POST['mapped_to']
        mapped_to_nm = request.POST['mapped_to_nm']
        by_online = "no"

        if CustomUser.objects.filter(email=Email).exists():
            messages.info(request, 'Email Taken')
            return redirect('create_mem')
        else:
            password = BaseUserManager().make_random_password(10)
            user = CustomUser.objects.create_user(username=Email, password=password, email=Email, first_name=fname, phone=phone, alt_phone=alt_phone, designation=designation, address=address, role = role, mapped_to = mapped_to, mapped_to_name = mapped_to_nm, by_online = by_online)
            user.save()


            ini = ""
            if user.designation == "Salaried":
                ini += "SAL"
            elif user.designation == "Self Employed":
                ini += "SE"
            elif user.designation == "Freelancer":
                ini += "FL"
            elif user.designation == "Student":
                ini += "ST"
            elif user.designation == "Home Maker":
                ini += "HM"
            elif user.designation == "DSA":
                ini += "DSA"
            elif user.designation == "Insurance Agent":
                ini += "IA"
            elif user.designation == "Chartered Accountant":
                ini += "CA"
            elif user.designation == "Tax Consultants":
                ini += "TC"
            elif user.designation == "Banker":
                ini += "BNK"
            elif user.designation == "Company Secretary":
                ini += "CS"
            elif user.designation == "Real Estate Agent":
                ini += "REA"
            elif user.designation == "Builder":
                ini += "BLD"
            else:
                ini+="O"

            if user.role == "Referral Partner":
                ini += "RP"

            elif user.role == "Branch User":
                ini += "BU"

            elif user.role == "Business Associates":
                ini += "BA"
            
            elif user.role == "Business Partner":
                ini += "BP"

            elif user.role == "Coordinator":
                ini += "CO"

            elif user.role == "Creative Finserver Center":
                ini += "CFC"

            elif user.role == "Development Partner":
                ini += "DP"

            elif user.role == "Doc boy":
                ini += "DB"
            
            elif user.role == "Execution Partner":
                ini += "EP"

            elif user.role == "Execution team internal":
                ini += "ETI"

            elif user.role == "Field executive":
                ini += "FE"
            
            elif user.role == "Referral Agent":
                ini += "RA"

            elif user.role == "Relationship manager":
                ini += "RM"

            elif user.role == "Secured Vertical Head":
                ini += "SVH"
            
            elif user.role == "Sr. Development Partner":
                ini += "SDP"

            elif user.role == "Team Manager":
                ini += "TM"
            
            elif user.role == "Tele Sales":
                ini += "TS"

            elif user.role == "Users":
                ini += "Us"
    
            elif user.role == "Vertical Head":
                ini += "VH"
                 


            num = '{:04d}'.format(user.id)
            newusername = ini+num
            user.username = newusername
            user.save()


            # if user.role == "Referral Partner":
            #     ini = "ORP"
            #     num = '{:03d}'.format(user.id)
            #     newusername = ini+num
            #     user.username = newusername
            #     user.save()

            email_body = 'Hi ' + user.first_name+' \n Your username: '+ user.username+ '\n Your Password: '+ password
            email = EmailMessage(
                'Account Activated',
                email_body,
                '',
                [user.email],
            )
            email.send(fail_silently=False)
            messages.success(request, 'Account Created successfully')
            if request.user.role == "Admin":
            # return render(request, 'account/dashboard.html')
                return redirect('dashboard')

            elif request.user.role == "Referral Partner":
            # return render(request, 'account/base.html')
                return redirect('base')
            
    return render(request, 'account/create_mem.html')

def dashboard(request):
    return render(request, 'account/dashboard.html')

def base(request):
    return render(request, 'account/base.html')

def list_leads(request):
    if request.user.role == "Admin":
        ll = Leads.objects.all()
    elif request.user.role == "Referral Partner":  
        ll = Leads.objects.filter(added_by=str(request.user.id))
    ids = []
    for i in ll:
        ids.append(i.lead_id)
    
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    listleads = Leads.objects.filter(lead_id__in=ids).order_by(preserved)   
    # return render(request, 'music/songs.html',  {'song': song})
    return render(request, 'account/list_leads.html', {'listleads': listleads})

def terms(request):
    try:
        return FileResponse(open('terms.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()
