from django.conf import settings
from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count, Max, Min, Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (CreateView, FormView, RedirectView,
                                  TemplateView, UpdateView)

from accounts.forms import (ChangeEmailForm, ChangePasswordForm,
                            EditProfileForm, ResetPasswordConfirmForm,
                            UserFormRegistration, UserLoginForm)
from accounts.services.email import SendingEmail
from accounts.utils.token_generators import (EmailChangeTokenGenerator,
                                             TokenRegisterGenerator)
from problems.models import Solutions, Tasks

# Create your views here.


class UserLogin(LoginView):
    template_name = "login/login.html"
    form_class = UserLoginForm

    def get_success_url(self):
        return reverse_lazy("index")

    def form_valid(self, form):
        if form.is_valid():
            user = form.cleaned_data.get("user")
            password = form.cleaned_data["password"]

            if user.check_password(password):
                login(self.request, user)
                return super().form_valid(form)
            else:
                return self.form_invalid(form)


class UserLogout(LogoutView):
    next_page = reverse_lazy("accounts:login")


class UserActivation(RedirectView):
    url = reverse_lazy("accounts:profile")

    def get(self, request, pk, token, *args, **kwargs):
        try:
            current_user = get_user_model().objects.get(pk=pk)
        except (get_user_model().DoesNotExist, TypeError, ValueError):
            return HttpResponse("Invalid activation link.(Error)")
        if current_user and TokenRegisterGenerator().check_token(user=current_user, token=token):
            current_user.is_active = True
            current_user.save()

            login(request, current_user)

            return redirect(reverse_lazy("accounts:profile", kwargs={"pk": current_user.pk}))
        else:
            return HttpResponse("Invalid activation link.(without Error)")


class UserRegistration(CreateView):
    form_class = UserFormRegistration
    template_name = "login/registration.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.is_active = False
            self.object.save()
            send_email = SendingEmail()
            message = send_email.create_message(
                self.request,
                template_name="activate_account.html",
                user=self.object,
                token=TokenRegisterGenerator().make_token(self.object),
            )
            send_email.send_email(
                subject=settings.EMAIL_REGISTRATION_SUBJECT,
                message=message,
                cc=[
                    settings.EMAIL_HOST_USER,
                ],
                to=(self.object.email,),
            )
        return super().form_valid(form)


class Profile(TemplateView):
    template_name = "profile/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        solutions = Solutions.objects.filter(user_id=kwargs.get("pk")).select_related("task")
        new_context = {
            "solutions_user": solutions,
            "easy": solutions.filter(task__difficulty=0, status=1),
            "mid": solutions.filter(task__difficulty=1, status=1),
            "hard": solutions.filter(task__difficulty=2, status=1),
        }
        all_count_context = {
            "problems_count": Tasks.objects.count(),
            "easy_count_pr": Tasks.objects.filter(difficulty=0).count(),
            "mid_count_pr": Tasks.objects.filter(difficulty=1).count(),
            "hard_count_pr": Tasks.objects.filter(difficulty=2).count(),
        }

        time_memory = {
            "max_time": solutions.aggregate(max_time=Max("time"))["max_time"],
            "min_time": solutions.aggregate(min_time=Min("time"))["min_time"],
            "max_memory": solutions.aggregate(max_memory=Max("memory"))["max_memory"],
            "min_memory": solutions.aggregate(min_memory=Min("memory"))["min_memory"],
        }

        languages = {"count_aggregate_language": Solutions.objects.filter(user_id=kwargs.get("pk")).values("language__language").annotate(count=Count("language"))}

        context.update(new_context)
        context.update(all_count_context)
        context.update(time_memory)
        context.update(languages)

        context["user"] = get_user_model().objects.get(id=kwargs.get("pk"))

        return context


class EditProfile(UpdateView):
    template_name = "profile/edit_profile.html"
    model = get_user_model()
    form_class = EditProfileForm

    def get_success_url(self):
        return reverse_lazy("accounts:profile", kwargs={"pk": self.request.user.pk})

    def form_valid(self, form):
        form.instance.photo = self.request.FILES.get("file")
        return super().form_valid(form)


class ChangePassword(UpdateView):
    template_name = "profile/passwords/change_password.html"
    form_class = ChangePasswordForm
    model = get_user_model()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            user = self.request.user
            user.set_password(form.cleaned_data["new_password"])
            user.save()

            update_session_auth_hash(self.request, user)

            return redirect(reverse_lazy("accounts:profile", kwargs={"pk": user.pk}))


class ChangeEmail(FormView):
    template_name = "profile/change_email.html"
    form_class = ChangeEmailForm
    model = get_user_model()

    def get_success_url(self):
        return reverse_lazy("accounts:profile", kwargs={"pk": self.request.user.pk})

    def form_valid(self, form):
        if form.is_valid():
            user = self.request.user
            new_email = form.cleaned_data["new_email"]
            send_email = SendingEmail()
            message = send_email.create_message(
                self.request,
                template_name="confirm_email_change_email.html",
                user=user,
                token=EmailChangeTokenGenerator().make_token(user),
                new_email=new_email,
            )

            send_email.send_email(
                subject=settings.EMAIL_REGISTRATION_SUBJECT,
                message=message,
                to=(new_email,),
                cc=[
                    settings.EMAIL_HOST_USER,
                ],
            )
            self.request.session[f"new_email_{user.pk}"] = new_email

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class ChangeEmailActivation(UpdateView):
    def get(self, request, pk, token, *args, **kw):
        try:
            user = get_user_model().objects.get(pk=pk)
        except (get_user_model().DoesNotExist, TypeError, ValueError):
            return HttpResponse("Invalid activation link.(Error)")
        if user and EmailChangeTokenGenerator().check_token(user=user, token=token):
            email = self.request.GET.get("email")
            try:
                session_email = request.session.pop(f"new_email_{user.pk}")
            except KeyError:
                return HttpResponse("Invalid activation link. Email is not valid. Try changing it again.")
            if session_email == email:
                user.email = email
                user.save()
                return redirect(reverse_lazy("accounts:profile", kwargs={"pk": user.pk}))
            else:
                return HttpResponse("Invalid activation link. Email is not valid. Try changing it again.")
        else:
            return HttpResponse("Invalid activation link.(without Error)")


class ResetPassword(View):
    """because through ccbv the uid is used in PasswordResetView and there is heavy logic, it’s better to rewrite it yourself"""

    template_name = "profile/passwords/reset_password.html"
    success_url = reverse_lazy("index")

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")

        try:
            user = get_user_model().objects.get(Q(email=email) | Q(username=email))
        except get_user_model().DoesNotExist:
            return redirect(self.success_url)

        send_email = SendingEmail()
        message = send_email.create_message(
            request,
            template_name="profile/passwords/password_reset_confirm.html",
            user=user,
            token=PasswordResetTokenGenerator().make_token(user),
        )

        send_email.send_email(
            subject=settings.EMAIL_SUBJECT_RESET_PASSWORD,
            message=message,
            to=(user.email,),
        )
        return redirect(self.success_url)


class ResetPasswordConfirm(View):
    success_url = reverse_lazy("accounts:password_reset_complete")
    template_name = "profile/passwords/password_reset_confirm_new.html"
    form_class = ResetPasswordConfirmForm

    def get(self, request, pk, token, *args, **kwargs):
        return render(
            request,
            "profile/passwords/password_reset_confirm_new.html",
            context={"pk": pk, "token": token, "form": self.get_form(request)},
        )

    def post(self, request, pk, token, *args, **kwargs):
        form = self.get_form(request)
        try:
            user = get_user_model().objects.get(pk=pk)
        except get_user_model().DoesNotExist:
            return HttpResponse("Invalid link (user)")
        if form.is_valid():
            new_password = form.cleaned_data.get("new_password2")
            if user and PasswordResetTokenGenerator().check_token(user=user, token=token):
                user.set_password(new_password)
                user.save()
                return redirect(reverse_lazy("accounts:login"))
            else:
                return HttpResponse("Invalid link(token)")
        else:
            return HttpResponse("Invalid link (form)")

    def get_form(self, request):
        return self.form_class(request.POST)
