# app/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import numpy as np
from PIL import Image
import tensorflow as tf
from io import BytesIO
import json
import openai 
from django.contrib.auth.decorators import login_required

from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib import messages
from django.shortcuts import get_object_or_404


# Load the model from the .h5 file
MODEL = tf.keras.models.load_model("app/templates/skin.keras")


# Define the class names
CLASS_NAMES = [
    "BA-cellulitis",
    "BA-impetigo",
    "FU-athletes-foot",
    "FU-nail-fungus",
    "FU-ringworm",
    "PA-cutaneous-larva-migrans",
    "VI-chickenpox",
    "VI-shingles"
]

def read_file_as_image(file) -> np.ndarray:
    """
    Read and preprocess the image file for model prediction.
    """
    image = Image.open(BytesIO(file.read()))
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize((256, 256))
    image_array = np.array(image) / 255.0  # Normalize the image
    return image_array

@csrf_exempt  # Exempt the view from CSRF verification for simplicity
def predict_image(request):
    """
    Handle the image upload and prediction.
    """
    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']  # Get the uploaded file
        try:
            # Read and preprocess the file
            image = read_file_as_image(file)
            # Prepare the image for model prediction
            img_batch = np.expand_dims(image, axis=0)  # Add batch dimension

            # Perform prediction
            predictions = MODEL.predict(img_batch)

            # Determine the predicted class and confidence
            predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
            confidence = np.max(predictions[0])*100

            # Return prediction results as JSON response
            return JsonResponse({
                "filename": file.name,
                "class": predicted_class,
                "confidence": float(confidence)
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method or no file provided."}, status=400)
@login_required
def upload_page(request):
    """
    Render the upload page and handle prediction results.
    """
    result = None
    if request.method == 'POST':
        response = predict_image(request)
        if response.status_code == 200:
            result = response.content.decode('utf-8')  # Decode the JSON response
            result = json.loads(result)  # Parse the JSON string to a dictionary
    
    return render(request, 'upload_and_predict.html', {'result': result})

from .models import Community
from .form import CommunityForm

@login_required
def CommunityView(request):
    if request.method == 'POST':
        form = CommunityForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)  # Create the instance but don't save yet
            community.name = request.user  # Assign the current user as the owner of the community
            community.save()  # Save the community instance
            return redirect('community')  # Redirect to the same community page after saving
    else:
        form = CommunityForm()  # Create an empty form

    # Retrieve all communities for display
    communities = Community.objects.all()

    return render(request, "community.html", {
        'form': form,
        'communities': communities
    })


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Define the tomato disease data directly in the views.py file
skin_disease_data = {
    
  "BA-cellulitis": {
    "scientific_name": "Cellulitis",
    "cause": "Bacterial infection, commonly caused by Staphylococcus aureus or Streptococcus species",
    "solution": {
      "medicine": ["Penicillin", "Amoxicillin", "Cephalexin", "Clindamycin"],
      "remedy": {
        "what_to_eat": ["Vitamin C-rich foods (oranges, strawberries)", "Zinc-rich foods (nuts, seeds)", "Garlic (antimicrobial)"],
        "what_not_to_eat": ["Processed foods", "Sugary foods", "Refined carbohydrates"]
      }
    }
  },
  "BA-impetigo": {
    "scientific_name": "Impetigo",
    "cause": "Bacterial infection, often caused by Staphylococcus aureus or Streptococcus pyogenes",
    "solution": {
      "medicine": ["Topical mupirocin ointment", "Oral antibiotics like Amoxicillin or Cephalexin"],
      "remedy": {
        "what_to_eat": ["Probiotic-rich foods (yogurt, kefir)", "Immune-boosting fruits (kiwi, citrus)", "Leafy greens (spinach)"],
        "what_not_to_eat": ["Processed sugars", "Greasy fast foods", "Alcohol"]
      }
    }
  },
  "FU-athletes-foot": {
    "scientific_name": "Tinea pedis",
    "cause": "Fungal infection caused by dermatophytes, typically Trichophyton species",
    "solution": {
      "medicine": ["Topical antifungals like Terbinafine, Clotrimazole", "Oral antifungals in severe cases"],
      "remedy": {
        "what_to_eat": ["Probiotics (yogurt, kimchi)", "Garlic (antifungal properties)", "Omega-3 rich foods (fish, flaxseeds)"],
        "what_not_to_eat": ["Refined carbs", "Sugary foods", "Alcohol"]
      }
    }
  },
  "FU-nail-fungus": {
    "scientific_name": "Onychomycosis",
    "cause": "Fungal infection, often caused by dermatophytes like Trichophyton rubrum",
    "solution": {
      "medicine": ["Topical antifungals like Ciclopirox", "Oral antifungals like Terbinafine, Itraconazole"],
      "remedy": {
        "what_to_eat": ["Probiotic foods (yogurt, kefir)", "Anti-inflammatory foods (turmeric, ginger)", "Vitamin E-rich foods (almonds, spinach)"],
        "what_not_to_eat": ["Refined sugars", "Processed foods", "Alcohol"]
      }
    }
  },
  "FU-ringworm": {
    "scientific_name": "Tinea corporis",
    "cause": "Fungal infection caused by dermatophytes like Trichophyton or Microsporum species",
    "solution": {
      "medicine": ["Topical antifungals like Clotrimazole, Miconazole", "Oral antifungals in severe cases"],
      "remedy": {
        "what_to_eat": ["Probiotic-rich foods", "Garlic (natural antifungal)", "Vitamin C-rich fruits (oranges, berries)"],
        "what_not_to_eat": ["Sugary foods", "Alcohol", "Refined carbohydrates"]
      }
    }
  },
  "PA-cutaneous-larva-migrans": {
    "scientific_name": "Cutaneous larva migrans",
    "cause": "Parasitic infection, usually caused by hookworm larvae from the Ancylostoma species",
    "solution": {
      "medicine": ["Albendazole", "Ivermectin"],
      "remedy": {
        "what_to_eat": ["Iron-rich foods (leafy greens, lentils)", "Vitamin C-rich foods to improve iron absorption", "Immune-boosting foods (garlic, ginger)"],
        "what_not_to_eat": ["Sugary foods", "Processed foods", "Excess red meat"]
      }
    }
  },
  "VI-chickenpox": {
    "scientific_name": "Varicella",
    "cause": "Viral infection caused by the varicella-zoster virus (VZV)",
    "solution": {
      "medicine": ["Antihistamines for itching", "Antiviral medications like Acyclovir in severe cases"],
      "remedy": {
        "what_to_eat": ["Vitamin C-rich foods (citrus fruits, berries)", "Zinc-rich foods (nuts, seeds)", "Hydrating fluids (broths, coconut water)"],
        "what_not_to_eat": ["Spicy foods", "Salty foods", "Caffeinated beverages"]
      }
    }
  },
  "VI-shingles": {
    "scientific_name": "Herpes zoster",
    "cause": "Reactivation of the varicella-zoster virus (VZV) in individuals who had chickenpox",
    "solution": {
      "medicine": ["Antiviral medications like Acyclovir, Valacyclovir", "Pain relievers like Ibuprofen, Acetaminophen"],
      "remedy": {
        "what_to_eat": ["Vitamin C-rich foods (kiwi, bell peppers)", "Vitamin B12-rich foods (fish, eggs)", "Probiotic foods (yogurt, sauerkraut)"],
        "what_not_to_eat": ["Sugary foods", "Processed foods", "Excess caffeine"]
      }
    }
  }
}




@csrf_exempt
def SolutionView(request):
    # Get the disease name from the GET request
    disease_name = request.GET.get('disease_name', None)

    # Check if disease name is provided
    if not disease_name:
        return JsonResponse({'error': 'Please provide a disease name'}, status=400)

  # Do not normalize; use the disease name as is
    disease_info = skin_disease_data.get(disease_name, None)


    # Check if the disease information was found
    if not disease_info:
        return JsonResponse({'error': 'Disease not found'}, status=404)

    # Return the disease information as a JSON object
    context = {
    'disease_name': disease_name,
    'scientific_name': disease_info['scientific_name'],
    'cause': disease_info['cause'],
    'solution': {
        'medicine': disease_info['solution']['medicine'],
        'remedy': {
            'what_to_eat': disease_info['solution']['remedy']['what_to_eat'],
            'what_not_to_eat': disease_info['solution']['remedy']['what_not_to_eat']
        }
    }
}


    # Render the solution.html template with the context data
    return render(request, 'solution.html', context)


# Create your views here.



def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')  # Redirect to the login page after successful signup
    else:
        form = UserCreationForm()  # Create a blank form for GET requests

    return render(request, 'signup.html', {'form': form})  # Pass the f
        
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log the user in
            next_url = request.GET.get('next')  # Get the next URL from the query parameters
            if next_url:  # If there is a next URL, redirect there
                return redirect(next_url)
              
              
            return redirect('upload_page')  # Default redirect to  if no next URL
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
        
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request,"Logout Successfully")
    return redirect('login')
def remove(request, id):
  
    community = get_object_or_404(Community, id=id) 
    community.delete()  # Delete the community
   
    return redirect("community") 