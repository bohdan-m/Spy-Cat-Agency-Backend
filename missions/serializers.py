# missions/serializers.py
from rest_framework import serializers
from .models import Mission, Target
from cats.models import SpyCat

class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['id', 'name', 'country', 'notes', 'is_complete', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)
    cat_name = serializers.CharField(source='cat.name', read_only=True)

    class Meta:
        model = Mission
        fields = ['id', 'cat', 'cat_name', 'is_complete', 'targets', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_targets(self, value):
        if len(value) < 1 or len(value) > 3:
            raise serializers.ValidationError("Mission must have between 1 and 3 targets.")
        return value

    def validate_cat(self, value):
        if value and Mission.objects.filter(cat=value, is_complete=False).exists():
            raise serializers.ValidationError("This cat is already assigned to an active mission.")
        return value

    def create(self, validated_data):
        targets_data = validated_data.pop('targets')
        mission = Mission.objects.create(**validated_data)
        
        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        
        return mission


class TargetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['notes', 'is_complete']

    def validate(self, data):
        target = self.instance
        
        if target.is_complete or target.mission.is_complete:
            if 'notes' in data and data['notes'] != target.notes:
                raise serializers.ValidationError("Cannot update notes for a completed target or mission.")
        
        return data


class MissionAssignSerializer(serializers.Serializer):
    cat_id = serializers.IntegerField()

    def validate_cat_id(self, value):
        try:
            cat = SpyCat.objects.get(id=value)
        except SpyCat.DoesNotExist:
            raise serializers.ValidationError("Cat not found.")
        
        if Mission.objects.filter(cat=cat, is_complete=False).exists():
            raise serializers.ValidationError("This cat is already assigned to an active mission.")
        
        return value