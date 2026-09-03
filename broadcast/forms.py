from django import forms

from .models import Program, ProgramCategory


class ProgramCategoryForm(forms.ModelForm):
    class Meta:
        model = ProgramCategory
        fields = "__all__"

    def clean_name(self):
        name = (self.cleaned_data.get("name") or "").strip()
        queryset = ProgramCategory.objects.filter(name=name)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise forms.ValidationError("节目名称已存在，请更换名称后再保存。")
        return name


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = "__all__"

    def clean_title(self):
        return (self.cleaned_data.get("title") or "").strip()

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        category = cleaned_data.get("category")

        if title and category:
            queryset = Program.objects.filter(category=category, title=title)
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise forms.ValidationError("该节目类别下已经存在同名节目，请更换节目标题后再保存。")

        return cleaned_data
