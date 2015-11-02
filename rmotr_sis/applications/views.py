import sys
from datetime import datetime

import stripe
from django.views.generic import View, FormView, TemplateView
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.conf import settings

from rmotr_sis.utils import send_template_mail
from applications.forms import (ApplicationFormStep1,
                                ApplicationFormStep2,
                                ApplicationFormStep3,
                                ApplicationFormStep4,
                                ApplicationFormStep5,
                                ApplicationFormStep6,
                                ApplicationFormStep7)
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

        # if available, save the "utm_source" query param
        application.utm_source = self.request.GET.get('utm_source', '')

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
                           context={
                               'next_step_url': next_step_url,
                               'first_name': form.cleaned_data['first_name']})

        return render(
            self.request,
            'applications/application_step_1_confirmation.html',
            context={
                'application': application
            })


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


class ApplicationStep3View(FormView):
    form_class = ApplicationFormStep3
    template_name = 'applications/application_step_3.html'

    def get_context_data(self, **kwargs):
        kwargs.setdefault('application', self.application)
        return super(ApplicationStep3View, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):

        self.application = get_object_or_404(
            Application, id=self.kwargs['uuid'])

        if self.application.status != 2:
            # the user is trying to access an invalid step
            raise Http404

        return super(ApplicationStep3View, self).dispatch(
            request, *args, **kwargs)

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

        context = {
            'scholarship_url': reverse(
                'applications:application-4',
                args=(str(self.kwargs['uuid']),)),
            'application': app
        }
        return render(
            self.request,
            'applications/application_step_3_confirmation.html',
            context=context
        )


class ApplicationStep4View(FormView):
    form_class = ApplicationFormStep4
    template_name = 'applications/application_step_4.html'
    success_url = '/applications/step4-success'

    def get_context_data(self, **kwargs):
        kwargs.setdefault('application', self.application)
        return super(ApplicationStep4View, self).get_context_data(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        try:
            self.application = get_object_or_404(Application, id=self.kwargs['uuid'])
        except ValueError:
            raise Http404

        if self.application.status != 3:
            # the user is trying to access an invalid step
            raise Http404

        # if the user access this view, it means that he need a scholarship
        self.application.need_scholarship = True
        self.application.save()

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


        # send email with first scholarship assignment
        subject = 'Scholarship application assignment 1'
        solution_url = reverse('applications:application-5',
                               args=(str(app.id),))
        send_template_mail(subject, 'application-scholarship-assignment-1.html',
                           recipient_list=[app.email],
                           context={'solution_url': solution_url,
                                    'scholarship_assignment_url': settings.SCHOLARSHIP_ASSIGNMENTS['assignment_1'],
                                    'application': app})
        app.scholarship_a1_email_sent = datetime.now()

        app.save()
        return render(self.request, 'applications/application_step_4_confirmation.html')


class BaseApplicationScholarshipAssignmentView(FormView):

    def get_form_class(self):
        return getattr(sys.modules[__name__],
                       'ApplicationFormStep{}'.format(self.current_status))

    def get_template_names(self):
        return ['applications/application_step_{}.html'.format(self.current_status)]

    def dispatch(self, request, *args, **kwargs):

        try:
            app = get_object_or_404(Application, id=self.kwargs['uuid'])
        except ValueError:
            raise Http404

        if app.status != self.current_status - 1:
            # the user is trying to access an invalid step
            raise Http404

        return super(BaseApplicationScholarshipAssignmentView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        value = settings.SCHOLARSHIP_ASSIGNMENTS['assignment_{}'.format(self.assignment_number)]
        kwargs['scholarship_assignment_url'] = value
        return kwargs

    def get_success_url(self):
        return reverse('applications:application-{}-success'.format(self.current_status),
                       args=(str(self.kwargs['uuid']),))

    def form_valid(self, form):
        app = Application.objects.get(id=self.kwargs['uuid'])
        field = 'scholarship_a{}_solution'.format(self.assignment_number)
        solution = form.cleaned_data['scholarship_a{}_solution'.format(self.assignment_number)]
        setattr(app, field, solution)

        # mark application as step5 completed
        app.status = self.current_status

        # send email with the next scholarship assignment
        if not hasattr(self, 'last_assignment') or not self.last_assignment:
            subject = 'Scholarship application assignment {}'.format(self.assignment_number + 1)
            solution_url = reverse(
                'applications:application-{}'.format(self.current_status + 1),
                args=(str(app.id),)
            )
            email_template = 'application-scholarship-assignment-{}.html'.format(self.assignment_number + 1)
            send_template_mail(
                subject,
                email_template,
                recipient_list=[app.email],
                context={
                    'solution_url': solution_url,
                    'scholarship_assignment_url': settings.SCHOLARSHIP_ASSIGNMENTS['assignment_{}'.format(self.assignment_number + 1)],
                    'application': app
                }
            )
            field = 'scholarship_a{}_email_sent'.format(self.assignment_number + 1)
            setattr(app, field, datetime.now())

        app.save()
        template = 'applications/application_step_{}_confirmation.html'.format(self.current_status)
        return render(self.request, template)


class ApplicationStep5View(BaseApplicationScholarshipAssignmentView):
    current_status = 5
    assignment_number = 1


class ApplicationStep6View(BaseApplicationScholarshipAssignmentView):
    current_status = 6
    assignment_number = 2


class ApplicationStep7View(BaseApplicationScholarshipAssignmentView):
    current_status = 7
    assignment_number = 3
    last_assignment = True


class ConfirmationStepView(TemplateView):
    BASE_TEMPLATE_NAME = 'applications/application_step_{step}_confirmation.html'

    def get(self, request, step, *args, **kwargs):
        self.template_name = self.BASE_TEMPLATE_NAME.format(step=step)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class ApplicationCheckoutView(View):

    def get(self, *args, **kwargs):
        application = get_object_or_404(Application, id=kwargs['uuid'])

        # don't accept payments if student was not selected or payment was
        # already registered
        if not application.selected or application.charge_id:
            raise Http404

        context = {
            'app': application,
            'public_key': settings.STRIPE['public_key'],
            'amount_cents': settings.COURSE_PRICE,
            'amount_dollars': int(settings.COURSE_PRICE) / 100
        }
        return render(self.request, 'applications/application_checkout.html',
                      context=context)

    def post(self, *args, **kwargs):
        stripe.api_key = settings.STRIPE['secret_key']
        application = get_object_or_404(Application, id=kwargs['uuid'])
        try:
            charge = stripe.Charge.create(
                amount=settings.COURSE_PRICE,  # amount in cents
                currency="usd",
                source=self.request.POST['stripeToken'],
                description="Remote Python Course",
                metadata={'application_id': kwargs['uuid'],
                          'email': application.email,
                          'batch': application.batch.number})
        except stripe.error.CardError as e:
            # The card has been declined
            context = {
                'app': application,
                'public_key': settings.STRIPE['public_key'],
                'amount_cents': settings.COURSE_PRICE,
                'amount_dollars': int(settings.COURSE_PRICE) / 100,
                'error': e
            }
            return render(self.request, 'applications/application_checkout.html',
                          context=context)
        else:
            # save payment details
            application.charge_id = charge['id']
            application.charge_details = charge
            application.save()

            # notify admins
            subject = '{} {} has just performed a checkout'.format(
                application.first_name.title(), application.last_name.title())
            application_url = reverse('admin:applications_application_change',
                                      args=(str(application.id),))
            context = {
                'application_url': application_url,
                'amount_dollars': int(settings.COURSE_PRICE) / 100,
                'application': application
            }
            send_template_mail(subject, 'application-checkout-notify.html',
                               recipient_list=[a[1] for a in settings.ADMINS],
                               context=context)

            return render(self.request, 'applications/application_checkout_success.html',
                          context={'app': application})
