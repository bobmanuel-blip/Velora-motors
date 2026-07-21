from django import forms

from .models import Vehicle, VehicleImage


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        exclude = ["dealer", "view_count", "created_at", "updated_at"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
            "interior_features": forms.Textarea(attrs={"rows": 2}),
            "exterior_features": forms.Textarea(attrs={"rows": 2}),
            "safety_features": forms.Textarea(attrs={"rows": 2}),
            "technology_features": forms.Textarea(attrs={"rows": 2}),
        }


class VehicleImageForm(forms.ModelForm):
    class Meta:
        model = VehicleImage
        fields = ["image", "is_primary", "caption"]


VehicleImageFormSet = forms.modelformset_factory(
    VehicleImage, form=VehicleImageForm, extra=5, can_delete=True
)
