from django.db import models
from django.contrib.auth import get_user_model

# Get the user model
User = get_user_model()  # Use get_user_model() to support custom user models

class Community(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to User model
    box = models.TextField(max_length=500)  # TextField for community box

    def __str__(self):
        return self.name.username  # Optional: return a string representation
