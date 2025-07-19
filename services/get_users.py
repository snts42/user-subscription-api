from services.data_store import user_store

def get_users(credit_card_filter=None):
    if credit_card_filter == "Yes":
        return [u for u in user_store if u.get('credit_card')]
    elif credit_card_filter == "No":
        return [u for u in user_store if not u.get('credit_card')]
    return user_store