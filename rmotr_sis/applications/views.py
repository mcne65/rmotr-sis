from django.views.generic import FormView, TemplateView
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404

from rmotr_sis.utils import send_template_mail
from applications.forms import (ApplicationFormStep1,
                                ApplicationFormStep2,
                                ApplicationFormStep3)
from applications.models import Application
from applications.forms import SKILLS_ASSESSMENT
from courses.models import Batch


class ApplicationStep1View(FormView):
    form_class = ApplicationFormStep1
    template_name = 'applications/application_step_1.html'
    success_url = '/applications/step1-success'

    def form_valid(self, form):

        # save model
        application = form.save()

        # assign application object to current batch
        batch = Batch.objects.get(accepting_applications=True)
        application.batch = batch
        application.save()

        next_step_url = reverse('applications:application-2',
                                args=(str(application.id),))

        # send confirmation email
        email = form.cleaned_data['email']
        subject = 'Thank you for applying to the rmotr.com applications program'
        send_template_mail(subject, 'application-email-confirm.html',
                           recipient_list=[email],
                           context={'next_step_url': next_step_url,
                                    'first_name': form.cleaned_data['first_name']})

        return HttpResponseRedirect(self.get_success_url())


class ApplicationStep1ViewSuccess(TemplateView):

    template_name = 'applications/application_step_1_confirmation.html'


class ApplicationStep2View(FormView):
    form_class = ApplicationFormStep2
    template_name = 'applications/application_step_2.html'
    success_url = '/applications/step2-success'

    def dispatch(self, request, *args, **kwargs):

        try:
            app = get_object_or_404(Application, id=self.kwargs['uuid'])
        except ValueError:
            raise Http404

        if app.status == 2:
            # user already completed step2, redirect to step3
            url = reverse('applications:application-3', args=(str(app.id),))
            return HttpResponseRedirect(url)
        elif app.status == 3:
            # user already completed all steps, show application confirmation
            return render(self.request,
                          'applications/application_step_3_confirmation.html')

        # if the user access this view, it means that the email was validated
        app.email_validated = True

        app.save()

        return super(ApplicationStep2View, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        try:
            app = get_object_or_404(Application, id=self.kwargs['uuid'])
        except ValueError:
            raise Http404

        app.gender = form.cleaned_data['gender']
        app.timezone = form.cleaned_data['timezone']
        app.birth_date = form.cleaned_data['birth_date']
        app.objective = form.cleaned_data['objective']
        app.experience = form.cleaned_data['experience']
        app.availability = form.cleaned_data['availability']
        app.occupation = form.cleaned_data['occupation']
        for instance in form.cleaned_data['course_instances']:
            app.course_instances.add(instance)
        for referral in form.cleaned_data['referrals']:
            app.referrals.add(referral)

        # mark application as step2 completed
        app.status = 2

        app.save()

        step3_url = reverse('applications:application-3',
                            args=(str(app.id),))
        return HttpResponseRedirect(step3_url)


class ApplicationStep2ViewSuccess(TemplateView):

    template_name = 'applications/application_step_2_confirmation.html'


class ApplicationStep3View(FormView):
    form_class = ApplicationFormStep3
    template_name = 'applications/application_step_3.html'
    success_url = '/applications/step3-success'

    def dispatch(self, request, *args, **kwargs):

        app = get_object_or_404(Application, id=self.kwargs['uuid'])

        if app.status == 1:
            # user didn't complete step2 yet, redirect back to step2
            url = reverse('applications:application-2', args=(str(app.id),))
            return HttpResponseRedirect(url)
        elif app.status == 3:
            # user already completed this step, show application confirmation
            return render(self.request,
                          'applications/application_step_3_confirmation.html')

        return super(ApplicationStep3View, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        app = Application.objects.get(id=self.kwargs['uuid'])

        correct_count = 0
        for index, question in enumerate(SKILLS_ASSESSMENT):
            if question['correct'] == form.cleaned_data['q{}'.format(index)]:
                correct_count += 1

        app.skills_assessment_questions = SKILLS_ASSESSMENT
        app.skills_assessment_answers = form.cleaned_data
        app.skills_assessment_correct_count = correct_count

        # mark application as step3 completed
        app.status = 3

        app.save()

        return HttpResponseRedirect(self.get_success_url())


class ApplicationStep3ViewSuccess(TemplateView):

    template_name = 'applications/application_step_3_confirmation.html'
