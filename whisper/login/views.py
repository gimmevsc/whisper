from django.http import JsonResponse
from register.models import User
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def loginUser(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            data = json.loads(request.body.decode('utf-8'))
            username_or_email = data.get('username')
            password = data.get('password')

            if '@' in str(username_or_email):
                try:
                    user = User.objects.get(email_address=username_or_email)
                    username = user.username
                except User.DoesNotExist:
                    user = None
            else:
                username = username_or_email
                        
            # Custom authentication logic
            user = User.objects.filter(username=username, password=password).first()
            if user is not None:
                # Login successful
                return JsonResponse({'message': 'Login successful'}, status=200)
            else:
                # Invalid credentials
                return JsonResponse({'message': 'Invalid username or password'}, status=400)
        except json.JSONDecodeError:
            # Invalid JSON data
            return JsonResponse({'message': 'Invalid JSON data in request body'}, status=400)
        except Exception as e:
            # Other error
            return JsonResponse({'message': 'An error occurred'}, status=500)
    else:
        # Method not allowed
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)

