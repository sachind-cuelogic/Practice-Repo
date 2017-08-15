from private_message_app.models import Message
from django.template.loader import get_template

from django.conf import settings
from django.template import Context
import pdfkit

def get_dummy_agent():
    dummy_user = User.objects.get(email='noreply@tatamotors.com')
    return dummy_user

###############################################################################
# Function will generate chat text to export
###############################################################################
def export_ticket_chat(ticket_messages, ticket_data, chat_type):
    """
    This function saves all the private chat of a ticket
    into a text file with name as its id.
    """
    filename  = str(ticket_data['id'])
    file_path = settings.BASE_DIR + "/private_message_app/private-message/" + chat_type + filename + '.pdf'

    template  = get_template("chat_transcript.html")

    html      = template.render(Context(
        {
         'description': ticket_data['description'],
         'ticket_messages': ticket_messages,
         'incident_creator': ticket_data['reported_by']
         }
    ))
    pdfkit.from_string(html, file_path)

    return True
    