import uuid

from private_message_app import error_conf

def check_for_private_message_error(request):
    """
    Error Handling For Private Message API 
    Check whether the message is empty or not
    """    
    data   = request.data
    user = uuid.UUID(data.get('user_id'))

    if user:    
	
	    if not data.get('message_text') or data.get('attachment'):
	        return error_conf.CANNOT_POST_EMPTY_MESSAGE

	    if not data.get('ticket'):
	    	return error_conf.TICKET_NOT_PROVIDED

	    if not data.get('receiver'):
	    	return error_conf.RECEIVER_NOT_PROVIDED
    else:
    	return error_conf.USER_NOT_AUTHENTICATED    	
