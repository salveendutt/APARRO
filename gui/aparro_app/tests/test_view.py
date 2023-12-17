from django.test import TestCase, RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from aparro_app.views import take_order
from pydub import AudioSegment
import os 
import io
class TakeOrderViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_take_order_view(self):
        audio_path = os.path.join(os.path.dirname(__file__), "order.wav")
        with open(audio_path, 'rb') as f:
            audio_data = f.read()
        audio_buffer = io.BytesIO(audio_data)

        # Create a request object with the POST data
        url = reverse('take_order')  # assuming 'take_order' is the name of the URL pattern
        request = self.factory.post(url, {'audio_data': audio_buffer})

        # Call the view function
        response = take_order(request)

        # Check if the response is a JSON response
        self.assertEqual(response.status_code, 200)

        response_data = response.content.decode('utf-8')
        self.assertIn('Your order is: 1 Big Mac, 1 Coke', response_data)