from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Mission, Target
from .serializers import (
    MissionSerializer, 
    TargetUpdateSerializer, 
    MissionAssignSerializer
)

class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def destroy(self, request, *args, **kwargs):
        mission = self.get_object()
        if mission.cat is not None:
            return Response(
                {"detail": "Cannot delete a mission that is assigned to a cat."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['patch'])
    def assign_cat(self, request, pk=None):
        mission = self.get_object()
        serializer = MissionAssignSerializer(data=request.data)
        
        if serializer.is_valid():
            mission.cat_id = serializer.validated_data['cat_id']
            mission.save()
            return Response(MissionSerializer(mission).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], url_path='targets/(?P<target_id>[^/.]+)')
    def update_target(self, request, pk=None, target_id=None):
        try:
            target = Target.objects.get(id=target_id, mission_id=pk)
        except Target.DoesNotExist:
            return Response(
                {"detail": "Target not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = TargetUpdateSerializer(target, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            
            mission = target.mission
            if all(t.is_complete for t in mission.targets.all()):
                mission.is_complete = True
                mission.save()
            
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)