# myapp/serializers.py
from rest_framework import serializers

class CommandSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    response = serializers.CharField(max_length=200)

    def validate_name(self, value):
        if not value.isidentifier():
            raise serializers.ValidationError("命令名稱必須是有效的 Python 標識符")
        return value

class BotConfigSerializer(serializers.Serializer):
    prefix = serializers.CharField(max_length=5, default='!')
    commands = CommandSerializer(many=True)

    def validate_commands(self, value):
        command_names = {cmd['name'] for cmd in value}
        if len(command_names) != len(value):
            raise serializers.ValidationError("命令名稱不能重複")
        return value