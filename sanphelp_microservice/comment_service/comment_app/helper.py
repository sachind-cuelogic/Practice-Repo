import pdfkit
from django.conf import settings
from django.template import Context
from django.template.loader import get_template



###############################################################################
# Function will generate chat text to export
###############################################################################
def export_ticket_chat(ticket_messages,ticket_obj,ticket_id, chat_type):
    """
    This function saves all the private chat of a ticket
    into a text file with name as its id.
    """
    filename = str(ticket_obj['id'])
    file_path = settings.BASE_DIR + "/comment_app/public-message/" + chat_type + filename + '.pdf'
    template = get_template("chat_transcript.html")
    html = template.render(Context(
        {'incident_id': ticket_id,
         'description': ticket_obj['description'],
         'ticket_messages': ticket_messages,
         'incident_creator': ticket_obj['reported_by']
         }
    ))
    
    pdfkit.from_string(html, file_path)
    
    return True
