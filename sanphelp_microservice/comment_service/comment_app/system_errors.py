from comment_app import error_conf


def check_for_public_message_error(request):
    '''
    This for Handling errors of Ticket
    '''
    comment_data = request.data

    if not (comment_data.get('comment_text') or comment_data.get('attachment')):
        return error_conf.COMMENT_WITH_NO_ATTACHMENT_DISCRIPTION

    """
    check ticket status closed or not
    if closed return error message.
    """
    # if ticket_obj['ticket_status'] == 'Closed':
    #     return error_conf.MESSAGE_ON_TICKET_CLOSED

    return False
