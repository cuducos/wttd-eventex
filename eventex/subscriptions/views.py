from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm


def subscribe(request):

    if request.method == 'POST':

        # validate form data
        form = SubscriptionForm(request.POST)
        if form.is_valid():

            # create email body
            body = render_to_string('subscriptions/subscription_email.txt',
                                    form.cleaned_data)

            # send email
            sender = 'contato@eventex.com.br'
            mail.send_mail('Confirmação de Inscrição', body, sender,
                           [sender, form.cleaned_data['email']])

            # show success message
            messages.success(request, 'Inscrição realizada com sucesso!')
            return HttpResponseRedirect('/inscricao/')

        # show errors
        else:
            return render(request, 'subscriptions/subscription_form.html',
                          {'form': form})

    # render new form
    return render(request, 'subscriptions/subscription_form.html',
                  {'form': SubscriptionForm()})
