from django.views.generic import FormView, TemplateView
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render

from rmotr_sis.utils import send_template_mail
from scholarships.forms import (ScholarshipApplicationFormStep1,
                                ScholarshipApplicationFormStep2,
                                ScholarshipApplicationFormStep3)
from scholarships.models import ScholarshipApplication
from scholarships.forms import SKILLS_ASSESSMENT
from courses.models import Batch


class ScholarshipApplicationStep1View(FormView):
    form_class = ScholarshipApplicationFormStep1
    template_name = 'scholarships/application_step_1.html'
    success_url = '/scholarships/step1-success'

    def form_valid(self, form):

        # save model
        application = form.save()

        # assign application object to current batch
        batch = Batch.objects.get(accepting_applications=True)
        application.batch = batch
        application.save()

        next_step_url = reverse('scholarships:application-2',
                                args=(str(application.id),))

        # send confirmation email
        email = form.cleaned_data['email']
        subject = 'Thank you for applying to the rmotr.com scholarships program'
        send_template_mail(subject, 'scholarship-application.html',
                           recipient_list=[email],
                           context={'next_step_url': next_step_url})

        return HttpResponseRedirect(self.get_success_url())


class ScholarshipApplicationStep1ViewSuccess(TemplateView):

    template_name = 'scholarships/application_step_1_confirmation.html'


class ScholarshipApplicationStep2View(FormView):
    form_class = ScholarshipApplicationFormStep2
    template_name = 'scholarships/application_step_2.html'
    success_url = '/scholarships/step2-success'

    def dispatch(self, request, *args, **kwargs):

        # if the user access this view, it means that the email was validated
        try:
            app = ScholarshipApplication.objects.get(id=self.kwargs['uuid'], status='1')
        except (ValueError, ScholarshipApplication.DoesNotExist):
            raise Http404
        app.email_validated = True
        app.save()

        return super(ScholarshipApplicationStep2View, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        app = ScholarshipApplication.objects.get(id=self.kwargs['uuid'])

        app.gender = form.cleaned_data['gender']
        app.timezone = form.cleaned_data['timezone']
        app.birth_date = form.cleaned_data['birth_date']
        app.objective = form.cleaned_data['objective']
        app.experience = form.cleaned_data['experience']
        app.availability = form.cleaned_data['availability']
        app.occupation = form.cleaned_data['occupation']
        for instance in form.cleaned_data['course_instances']:
            app.course_instances.add(instance)

        # mark application as step2 completed
        app.status = '2'

        app.save()

        next_step_url = reverse('scholarships:application-3',
                                args=(str(app.id),))
        return render(self.request,
                      'scholarships/application_step_2_confirmation.html',
                      {'next_step_url': next_step_url})


class ScholarshipApplicationStep2ViewSuccess(TemplateView):

    template_name = 'scholarships/application_step_2_confirmation.html'


class ScholarshipApplicationStep3View(FormView):
    form_class = ScholarshipApplicationFormStep3
    template_name = 'scholarships/application_step_3.html'
    success_url = '/scholarships/step3-success'

    def dispatch(self, request, *args, **kwargs):

        # check that the user didn't complete this step in the past
        try:
            ScholarshipApplication.objects.get(id=self.kwargs['uuid'], status='2')
        except (ValueError, ScholarshipApplication.DoesNotExist):
            raise Http404

        return super(ScholarshipApplicationStep3View, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        app = ScholarshipApplication.objects.get(id=self.kwargs['uuid'])

        correct_count = 0
        for index, question in enumerate(SKILLS_ASSESSMENT):
            if question['correct'] == form.cleaned_data['q{}'.format(index)]:
                correct_count += 1

        app.skills_assessment_questions = SKILLS_ASSESSMENT
        app.skills_assessment_answers = form.cleaned_data
        app.skills_assessment_correct_count = correct_count

        # mark application as step3 completed
        app.status = '3'

        app.save()

        return HttpResponseRedirect(self.get_success_url())


class ScholarshipApplicationStep3ViewSuccess(TemplateView):

    template_name = 'scholarships/application_step_3_confirmation.html'
