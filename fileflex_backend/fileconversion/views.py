from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Conversion, SubscriptionPlan, FAQ
from supabase import create_client, Client
from django.conf import settings
import uuid

supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    file = request.FILES.get('file')
    if not file:
        return JsonResponse({'error': 'No file provided'}, status=400)
    
    file_name = f"{uuid.uuid4()}-{file.name}"
    
    try:
        res = supabase.storage.from_(settings.SUPABASE_BUCKET).upload(file_name, file)
        
        if 'error' in res:
            return JsonResponse({'error': 'File upload failed'}, status=500)
        
        file_url = supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(file_name)
        
        conversion = Conversion.objects.create(
            user=request.user,
            file_name=file.name,
            input_format=file.name.split('.')[-1],
            input_file_url=file_url
        )
        
        return JsonResponse({'file_url': file_url, 'conversion_id': conversion.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_history(request):
    conversions = Conversion.objects.filter(user=request.user).order_by('-created_at')
    history = [{'id': c.id, 'file_name': c.file_name, 'input_format': c.input_format, 'output_format': c.output_format, 'download_url': c.output_file_url} for c in conversions]
    return JsonResponse({'history': history})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def convert_file(request):
    # Implement file conversion logic here
    # Update the Conversion object with output_format and output_file_url
    pass

@api_view(['GET'])
def subscription_plans(request):
    plans = SubscriptionPlan.objects.all()
    plan_data = [{'id': p.id, 'name': p.name, 'price': str(p.price), 'features': p.features} for p in plans]
    return JsonResponse({'plans': plan_data})

@api_view(['GET'])
def faq(request):
    faqs = FAQ.objects.all()
    faq_data = [{'id': f.id, 'question': f.question, 'answer': f.answer} for f in faqs]
    return JsonResponse({'faqs': faq_data})

@api_view(['POST'])
def contact(request):
    # Implement contact form submission logic
    pass

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def download_file(request, file_id):
    try:
        conversion = Conversion.objects.get(id=file_id, user=request.user)
        return JsonResponse({'download_url': conversion.output_file_url})
    except Conversion.DoesNotExist:
        return JsonResponse({'error': 'File not found'}, status=404)
