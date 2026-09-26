from django import forms

from .models import BroadcastCard, Program, ProgramCategory, SystemConfig


class SystemConfigForm(forms.ModelForm):
    class Meta:
        model = SystemConfig
        fields = "__all__"

    def clean_first_week_start_date(self):
        value = self.cleaned_data["first_week_start_date"]
        if value.weekday() != 0:
            raise forms.ValidationError("第一周起始日期必须是星期一。")
        return value


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

    def clean(self):
        cleaned_data = super().clean()
        alternate = cleaned_data.get("alternate_with")
        if alternate and alternate == self.instance:
            self.add_error("alternate_with", "轮替节目不能选择自身。")
        return cleaned_data


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
                raise forms.ValidationError(
                    "该节目类别下已经存在同名节目，请更换节目标题后再保存。"
                )

        return cleaned_data


class BroadcastCardForm(forms.ModelForm):
    class Meta:
        model = BroadcastCard
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        card_type = cleaned_data.get("card_type")
        category = cleaned_data.get("category")
        link_url = cleaned_data.get("link_url")

        if (
            card_type
            in (
                BroadcastCard.TYPE_LATEST_PROGRAM,
                BroadcastCard.TYPE_PROGRAM_LIST,
            )
            and not category
        ):
            self.add_error("category", "这种卡片必须选择节目类别。")

        if card_type == BroadcastCard.TYPE_DIRECT_LINK and not link_url:
            self.add_error("link_url", "外部链接卡片必须填写链接地址。")

        return cleaned_data
