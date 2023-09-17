from django.forms.models import BaseInlineFormSet


class IngredientForm(BaseInlineFormSet):
    def _construct_form(self, i, **kwargs):
        form = super(IngredientForm, self)._construct_form(i, **kwargs)
        if i < 1:
            form.empty_permitted = False
        return form
