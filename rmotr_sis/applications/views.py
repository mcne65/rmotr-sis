from django.views.generic import FormView, TemplateView
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.conf import settings

from rmotr_sis.utils import send_template_mail
from applications.forms import (ApplicationFormStep1,
                                ApplicationFormStep2,
                                ApplicationFormStep3,
                                ApplicationFormStep4)
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
        subject = 'Thank you for applying to rmotr.com courses'
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

    def dispatch(self, request, *args, **kwargs):

        try:
            app = get_object_or_404(Application, id=self.kwargs['uuid'])
        except ValueError:
            raise Http404

        if app.status != 1:
            # the user is trying to access an invalid step
            raise Http404

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
        app.referrals_other = form.cleaned_data['referrals_other']

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
    #success_url = '/applications/step3-success'

    def dispatch(self, request, *args, **kwargs):

        app = get_object_or_404(Application, id=self.kwargs['uuid'])

        if app.status != 2:
            # the user is trying to access an invalid step
            raise Http404

        return super(ApplicationStep3View, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('applications:application-3-success',
                       args=(str(self.kwargs['uuid']),))

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

        # notify admins
        subject = '{} {} has completed the application form'.format(
            app.first_name.title(), app.last_name.title())
        application_url = reverse('admin:applications_application_change',
                                  args=(str(app.id),))
        send_template_mail(subject, 'application-admin-notify.html',
                           recipient_list=[a[1] for a in settings.ADMINS],
                           context={'application_url': application_url,
                                    'application': app})

        return HttpResponseRedirect(self.get_success_url())


class ApplicationStep3ViewSuccess(TemplateView):

    template_name = 'applications/application_step_3_confirmation.html'

    def get_context_data(self, **kwargs):
        return {'scholarship_url': reverse('applications:application-4',
                                           args=(str(self.kwargs['uuid']),))}


class ApplicationStep4View(FormView):
    form_class = ApplicationFormStep4
    template_name = 'applications/application_step_4.html'
    success_url = '/applications/step4-success'

    def dispatch(self, request, *args, **kwargs):

        try:
            app = get_object_or_404(Application, id=self.kwargs['uuid'])
        except ValueError:
            raise Http404

        if app.status != 3:
            # the user is trying to access an invalid step
            raise Http404

        # if the user access this view, it means that he need a scholarship
        app.need_scholarship = True

        app.save()

        return super(ApplicationStep4View, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('applications:application-4-success',
                       args=(str(self.kwargs['uuid']),))

    def form_valid(self, form):
        app = Application.objects.get(id=self.kwargs['uuid'])
        for i in range(6):
            q_name = 'scholarship_q{}'.format(i + 1)
            setattr(app, q_name, form.cleaned_data[q_name])

        # mark application as step4 completed
        app.status = 4

        app.save()
        return HttpResponseRedirect(self.get_success_url())


class ApplicationStep4ViewSuccess(TemplateView):

    template_name = 'applications/application_step_4_confirmation.html'
