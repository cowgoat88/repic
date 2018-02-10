from .models import Submission, SubredditsList
from rest_framework import viewsets
from django.http import HttpResponse
from .serializers import SubmissionSerializer, SubredditsListSerializer

    
class SubmissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows view of praw output
    """
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    
class SubredditsListViewSet(viewsets.ModelViewSet):
    """
    API endpoint to get subreddits list
    """
    queryset = SubredditsList.objects.all()
    serializer_class = SubredditsListSerializer

def subredditsList(request):
    """
    View the subreddits list in the db set it if it's empty
    """
    subs = SubredditsList.objects.all()
    for sub in subs:
        print(sub.subreddit)
    return HttpResponse()
    
        
        
