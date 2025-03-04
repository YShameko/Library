from django.shortcuts import render

from book.models import Borrowed


def send_reminders_to_users(request, reminders_list):
    msg_sent = []
    for each in reminders_list:
        record = Borrowed.objects.get(pk=each)
        msg_sent.append(record)
    return msg_sent
