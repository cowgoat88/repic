from rest_framework import serializers
from .models import Submission, SubredditsList

class SubmissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Submission
        fields = ('id', 'title', 'score', 'url', 'mp4', 'nsfw', 'sitetag', 'created')
        
class SubredditsListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubredditsList
        fields = ('id', 'subreddit', 'nsfw')