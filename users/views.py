import os
import time
from django.conf import settings
from django.db.models import FilteredRelation, Q
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView
from .models import *

from django.shortcuts import render, redirect
from  .models import Job_Post

from .forms import ApplicantCreationForm, ApplicantChangeForm, DocumentForm, CompanyForm, CompanyCreationForm
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .Language_Processing.resumeParser import Parse
from django.views import View

from django.contrib.auth.decorators import login_required
from django.contrib import messages


class CompanyDashboard(View):

    def get(self,request):
        try:
            conmany_detail = company_profile.objects.get(company_id=request.user)
            jobs_counter = Job_Post.objects.filter(posted_by__company_id=request.user)
            applications= AppliedJobs.objects.filter(job__posted_by__company=request.user)
            return render(request, "layout-semi-dark.html", {'conmany_detail': conmany_detail,'jobs_counter':len(jobs_counter),'application_counter':len((applications))})
        except:
            return redirect('users:logout')


# def form_validation(request):
#     return render(request, 'form_validation.html')


class JobPostView(View):
    def post(self, request):
        if request.POST:
            a = Job_Post(job_designation=request.POST.get('job_designation'),posted_by=company_profile.objects.get(company=request.user),Job_title=request.POST.get('Job_title'),Job_Description=request.POST.get('Job_Description'),qualification_required=request.POST.get('qualification_required'),positions=request.POST.get('positions'),experience_required=request.POST.get('experience_required'), City=request.POST.get('City'),Contact_Number=request.POST.get('Contact_Number'), Country=request.POST.get('Country'), Region=request.POST.get('Region'),gender_preference=request.POST.get('gender_preference'),job_nature=request.POST.get('job_nature'))
            a.save()
            for i in request.POST.getlist('skills'):
                Job_Skill(job=a,title=i).save()
            return redirect('users:List_all_jobs')
    def get(self,request):
        return render(request, 'post_a_job.html')


class CompanyProfileView(View):

    def post(self,request):
        a = company_profile.objects.get(company=request.user)

        if request.method == 'POST' and request.POST:
            form = CompanyForm(instance=a,data=request.POST, files=request.FILES)
            if form.is_valid():
                a = form.save()
            return redirect('users:Edit_Company_Profile')

    def get(self, request):
        a = company_profile.objects.get(company=request.user)
        return render(request, 'Edit_Company_Profile.html',{'company_profile':a})


class JobEditView(View):

    def post(self,request, *args, **kwargs):
        id = kwargs.get('id')
        a = Job_Post.objects.get(pk=id)
        a.job_designation=request.POST.get('job_designation')
        a.Job_title=request.POST.get('Job_title')
        a.Job_Description=request.POST.get('Job_Description')
        a.skills_required=request.POST.get('skills_required')
        a.qualification_required=request.POST.get('qualification_required')

        a.positions=request.POST.get('positions')
        a.experience_required=request.POST.get('experience_required')
        a.City=request.POST.get('city')
        a.Contact_Number=request.POST.get('Contact_Number')
        a.Country=request.POST.get('Country')
        a.Region=request.POST.get('Region')
        a.job_nature=request.POST.get('job_nature')
        a.gender_preference=request.POST.get('gender_preference')
        a.save()
        return redirect('users:List_all_jobs')

    def get(self,request,*args,**kwargs):
        id = kwargs.get('id')
        Job_Detail = Job_Post.objects.get(pk=id)
        return render(request,'edit_a_job.html', {'Job_Detail':Job_Detail})


class JobListCompanyView(View):

    def get(self,request):
        if not request.user.is_company:
            return redirect('users:view_all_jobs')
        Job_Detail = Job_Post.objects.filter(Q(status=True) and Q(posted_by__company=request.user)).order_by('-posted_at')
        Application=AppliedJobs.objects.filter(~Q(status='RJ'),Q(job__posted_by__company=request.user))
        skills = Job_Skill.objects.filter(job_id__in=Job_Detail)
        parsed_resumes = [{'data':Parse(files=[i.resume.file.path]).information[-1],'application':i.resume.id} for i in Application]

        return render(request, "category1.html", {'Job_Detail': Job_Detail,'Application':Application, 'skills':skills,'parsed_resume':parsed_resumes})


class ApplicationStatusChange(View):
    def get(self,request, *args, **kwargs):
        status = kwargs.get('status')
        id = kwargs.get('id')
        application = AppliedJobs.objects.get(pk=id)
        if status:
            application.status = status
            application.save()

        return redirect('users:List_all_jobs')


class ProfileUserView(View):

    def get(self,request,*args,**kwargs):
        id = kwargs.get('id')
        data = Applicant.objects.get(pk=id)
        return render(request, 'profile.html', {'Applicant':data})


class JobListUserView(View):

    def get(self,request):
        Job_Detail = Job_Post.objects.all().filter(status=True)
        return render(request, "all_jobs_userEnd.html", {'Job_Detail': Job_Detail})


class JobDetailUserView(View):
    def get(self,request, *args, **kwargs):
        id = kwargs.get('id')

        Job_Detail = Job_Post.objects.get(pk=id)
        try:
            status= AppliedJobs.objects.get(job=Job_Detail,applicant=request.user)
        except AppliedJobs.DoesNotExist:
            status = None
        return render(request, "single_job_detail.html", {'Job_Detail': Job_Detail, 'status': status})

    def post(self,request, *args, **kwargs):
        id = kwargs.get('id')

        Job_Detail = Job_Post.objects.get(pk=id)
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            a = form.save()
            AppliedJobs(applicant=request.user, resume=a,job=Job_Post.objects.get(pk=id)).save()
            messages.add_message(request, messages.SUCCESS, 'User successfully Applied.')
            return redirect('users:applied_jobs')
        else:
            messages.add_message(request, messages.SUCCESS, 'Error! Your applicat...')
            return render(request, "single_job_detail.html", {'Job_Detail': Job_Detail, 'errors':form.errors})


class JobDeleteView(DeleteView):
    success_url = None
    Job_Detail = Job_Post.objects.all()

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return render(request, "category1.html", {'Job_Detail': self.Job_Detail})


@login_required
def edit_a_job(request,id):
    return render(request, 'edit_a_job.html')


class SignUpView(View):

    def post(self,request):
        form = ApplicantCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login_form')

    def get(self,request):
        form = ApplicantChangeForm()
        return render(request, 'register_1.html', {'form': form})


class CompanyRegisterView(View):

    def get(self,request):
        form = CompanyCreationForm()
        return render(request, 'registration/company_registration_form.html', {'form': form})

    def post(self,request):
        form2 = CompanyCreationForm(request.POST)
        if form2.is_valid():
            user = form2.save()
            company = company_profile(company_address=request.POST.get('company_address'), company=user,company_contact=request.POST.get('company_contact'))
            company.save()
            return redirect('users:login_form')
        return render(request, 'registration/company_registration_form.html', {'form': form2})



def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, request.user)
        if form.is_valid():
            your_media_root = settings.MEDIA_ROOT
            file = form.cleaned_data.get('document').name
            form.save()
            path = os.path.join(your_media_root,'documents',file)
            #file_path = path + '\\' + file
            data = Parse(files=[path])
            print(data)
            return render(request,'upload_file.html', {'mydata':data.information[0]})
    else:
        form = DocumentForm()
    return render(request, 'upload_file.html', {
        'form': form
    })


class BasicUploadView(View):
    def get(self, request):
        photos_list = Document.objects.all()
        return render(self.request, 'basic_upload/index.html', {'photos': photos_list})

    def post(self, request):
        data = dict(self.request.POST)
        data['uploaded_by'] = self.request.user
        form = DocumentForm(data, self.request.FILES, request.user)
        if form.is_valid():
            your_media_root = settings.MEDIA_ROOT
            file = form.cleaned_data.get('file').name
            photo = form.save()
            path = os.path.join(photo.file.file.name)
            # file_path = path + '\\' + file
            data = Parse(files=[path])
            print(data)
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class ProgressBarUploadView(View):
    def get(self, request):
        photos_list = Document.objects.all()
        return render(self.request, 'progress_bar_upload/index.html', {'photos': photos_list})

    def post(self, request):
        time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = DocumentForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class DragAndDropUploadView(View):
    def get(self, request):
        photos_list = Document.objects.all()
        return render(self.request, 'drag_and_drop_upload/index.html', {'photos': photos_list})

    def post(self, request):
        form = DocumentForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


#   company views

class IndexView(View):
    def get(self,request):
        return render(request, 'index_job.html')

# def form_validation(request):
#         return render(request, 'form_validation.html')


def cv_design(request):
    user = request.user
    return render(request, 'cv_design.html')

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class UserResumeView(View):
    def get(self,request):
        if request.user.is_company:
            return Http404
        a = Resume.objects.get(applicantID=request.user)
        applicant = Applicant.objects.all()
        educations = Resume_Education.objects.filter(resumeID=a)
        skills = Resume_Skills.objects.filter(resumeID=a)
        Activities = Resume_Activities.objects.filter(resumeID=a)
        if request.GET.get('pdf'):
            pdf = render_to_pdf('pdf/cv_pdf.html', {'user':request.user, 'educations':educations,'resume':a,'skills':skills,'Activities':Activities ,'applicant':applicant})
            return HttpResponse(pdf, content_type='application/pdf')
        return render(request,'blank.html', {'user':request.user, 'educations':educations,'resume':a,'skills':skills,'pdf':True})


class LoginView(View):
    def get(self,request):
        return render(request, 'registration/login.html')


class DashBoardUserView(View):
    def get(self,request):
        if request.user.is_company:
            return redirect('users:company_dashboard')
        allSkills = Resume_Skills.objects.filter(resumeID__applicantID=request.user).values('skill_names')
        allSkills = [i.get('skill_names') for i in allSkills]
        jobs= set([i for i in Job_Post.objects.filter(status=True, job_skill__title__in=allSkills, City=request.user.place).order_by('-posted_at')])
        return render(request,'testing.html',{'jobs':jobs,})


class LatestJobsView(View):

    def get(self,request):
        jobs= Job_Post.objects.filter(status=True,City=request.user.place).order_by('-posted_at')
        return render(request,'view_latest_job.html',{'jobs':jobs,})


class AppliedJobsView(View):
    def get(self,request):
        if request.user.is_company:
            raise Http404
        jobs= Job_Post.objects.filter(appliedjobs__applicant=request.user)
        return render(request,'applied_jobs.html',{'jobs':jobs,})


class AboutUSJobView(View):

    def get(self,request):
        return render(request,'about_us_job_posting.html')


class ContactJobView(View):

    def get(self,request):
        return render(request,'contact_job_posting.html')


def upload_cv_job_posting(request):
    return render(request,'upload_cv_job_posting.html')


class ResumeBuilderView(View):
    def get(self,request):
        try:
            a= Resume.objects.get(applicantID=request.user)
            b= Resume_Education.objects.filter(resumeID=a)
            c= Resume_Skills.objects.filter(resumeID=a)
            d= Resume_Activities.objects.filter(resumeID=a)
        except Resume.DoesNotExist:
            a = None
            b = None
            c = None
            d = None
        return render(request, 'cv_builder_tool_job_posting.html',
                      {'ResumeDetail': a, 'edu': b, 'skills': c, 'activities': d,'request':request})

    def post(self,request):
        try:
            usr = request.user
            usr.place = request.POST.get('place')
            usr.country = request.POST.get('country')
            usr.save()
            a = Resume.objects.get(applicantID=request.user)
            a.resume_summary = request.POST.get('summary')
            Resume_Skills.objects.filter(resumeID=a).delete()
            Resume_Education.objects.filter(resumeID=a).delete()
            for i in request.POST.getlist('skills'):
                if i:
                    Resume_Skills(resumeID=a,skill_names=i).save()
            for i in request.POST.getlist('education'):
                if i:
                    Resume_Education(resumeID=a,name=i).save()

        except Resume.DoesNotExist:
            a = Resume(resume_summary=request.POST.get('summary'), applicantID=request.user,
                       address=request.POST.get('address'))
            a.save()
            for i in request.POST.getlist('skills'):
                Resume_Skills(resumeID=a,skill_names=i).save()
            for i in request.POST.getlist('education'):
                Resume_Education(resumeID=a,name=i).save()
        return redirect('users:cv_builder_tool_job_posting')



# def cv_design_job_posting(request):
#         resume_detail = Resume.objects.all()
#         return render(request, "cv_design_job_posting.html", {'resume_detail': resume_detail})