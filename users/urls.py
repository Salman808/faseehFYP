from django.urls import path, include
from .views import *
from . import views
from django.views.generic.base import TemplateView

app_name = "users"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_job_posting, name="index_job_posting"),
    path('users/', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup'),
    path('company_dashboard', views.company_dashboard, name='company_dashboard'),
    path('Edit_Company_Profile', views.Edit_Company_Profile, name='Edit_Company_Profile'),
    # path('form_validation', views.form_validation, name='form_validation'),
    path('post_a_job', views.post_a_job, name='post_a_job'),
    path('List_all_jobs', views.List_all_jobs, name='List_all_jobs'),
    path('application/<int:id>/<str:status>',views.ApplicationStatusChange, name='set_application_status'),

    path('view_latest_jobs', views.view_latest_jobs, name='view_latest_jobs'),

# list Jobs at user End
    path('list_all_job_userEnd', views.list_all_job_userEnd, name='view_all_jobs'),
    path('user_single_job_detail/<int:id>', views.user_single_job_detail, name='user_single_job_detail'),
    # path('user_list_single_job/<int:id>', views.single_job_detail, name='view_single_job'),

    path('latest_jobs', views.latest_jobs, name='latest_jobs'),
    path('edit_a_job/<int:id>', views.edit, name='edit_a_job'),
    path('delete/<int:id>', views.destroy, name='delete_a_job'),
    # path('dashboard', TemplateView.as_view(template_name='Dashboard.html'), name='dashboard'),
    # path('cv_design', views.cv_design, name="cv_design"),
    path('blank', views.blank, name="blank"),
    path('company_registration_form', views.company_registration_form, name="company_registration_form"),
    path('login_form', views.company_login_form, name="login_form"),
    # job_posting URLS
    path('dashboard_job_posting', views.dashboard_job_posting, name='dashboard_job_posting'),

    path('applied_jobs', views.applied_jobs, name='applied_jobs'),

    path('profile/<int:id>', views.profile, name='profile'),
    # path('resume_page_job_posting', views.resume_page_job_posting, name='resume_page_job_posting'),
    # path('sample_page_job_posting', views.sample_page_job_posting, name='sample_page_job_posting'),
    path('upload_cv_job_posting', views.upload_cv_job_posting, name='upload_cv_job_posting'),
    path('cv_builder_tool_job_posting', views.cv_builder_tool_job_posting, name='cv_builder_tool_job_posting'),
    # path('cv_design_job_posting', views.cv_design_job_posting, name='cv_design_job_posting'),
    # path('register_job_posting', views.register_job_posting, name='register_job_posting'),

    path('about_us_job_posting', views.about_us_job_posting, name='about_us_job_posting'),
    path('contact_job_posting', views.contact_job_posting, name='contact_job_posting'),
    # File upload urls
    path('file', model_form_upload, name='file_upload'),
    path('model_form_upload', views.model_form_upload, name='model_form_upload'),
    path('basic-upload', BasicUploadView.as_view(), name='basic_upload'),
    path('progress-bar-upload', ProgressBarUploadView.as_view(), name='progress_bar_upload'),
    path('drag-and-drop-upload', DragAndDropUploadView.as_view(), name='drag_and_drop_upload'),
]

# urlpatterns = [

# Job_posting URLS
# path('users/', include('users.urls')),
# path('admin/', admin.site.urls),
# path('register_page', views.register_page, name='register_page'),
# # path('job_listings', views.job_listings, name='job_listings'),
# # path('edit/<int:id>', views.edit),
# # path('edit', views.edit, name='edit'),
# path('users/', include('users.urls')),
# ]