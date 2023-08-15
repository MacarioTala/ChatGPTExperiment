from django.db import models
import openai
import os

# Create your models here.
class Opportunity(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    def __str__(self):
        return self.name
        
    def rewrite_me(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        prompt="Rewrite the following to make it more organized and attractive to volunteers: "+self.description

        messagelist=[{'role':'user','content':prompt}]

        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messagelist
            )
        
            if 'choices' in completion and len(completion['choices']) > 0 and 'message' in completion['choices'][0]:
            # Get the reply from the API response
                
                reply = completion['choices'][0]['message']['content']
            
            else:
                print("Unexpected response format:", completion)
        except Exception as e:
            print("Error occurred:", e)
        
        return reply