from App import models

def get_header():
    header = {
            'Authorization': models.Token.objects.all()[0].bearer,
            'Accept': 'application/json'
        }
    return header