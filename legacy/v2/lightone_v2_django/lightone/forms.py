from django import forms
from .models import MemberSession

class SessionRecordForm(forms.ModelForm):
    class Meta:
        model = MemberSession
        fields = ['member_name', 'goal', 'discomfort_area', 'form_accuracy', 'rep_score', 'rest_score', 'pain_response', 'rpe', 'qc_status', 'qc_score', 'memo']
        widgets = {
            'member_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '회원 이름'}),
            'goal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '오늘의 목표'}),
            'discomfort_area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '불편감 부위 (선택)'}),
            'form_accuracy': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10', 'step': '1'}),
            'rep_score': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100', 'step': '1'}),
            'rest_score': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100', 'step': '1'}),
            'qc_status': forms.Select(attrs={'class': 'form-control'}),
            'qc_score': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100', 'step': '1'}),
            'posture_score': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100', 'step': '1'}),
            'lifestyle_score': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100', 'step': '1'}),
            'function_training_score': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100', 'step': '1'}),
            'pain_response': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10', 'step': '1'}),
            'qc_status': forms.Select(attrs={'class': 'form-control'}),
            'qc_score': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100', 'step': '1'}),
            'rpe': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10', 'step': '1'}),
            'memo': forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': '트레이너 메모'}),
        }
